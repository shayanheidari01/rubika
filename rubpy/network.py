import threading
import asyncio
from typing import Callable, Dict, Optional, Union
import aiohttp
import aiofiles
import inspect
import rubpy
import os
import logging
from .types import Update
from .crypto import Crypto
from . import exceptions

def capitalize(text: str) -> str:
    """
    تبدیل رشته snake_case به CamelCase.

    پارامترها:
    - text: رشته با فرمت snake_case.

    خروجی:
    رشته با فرمت CamelCase.
    """
    return ''.join(word.title() for word in text.split('_'))

class Network:
    HEADERS = {
        'origin': 'https://m.rubika.ir',
        'referer': 'https://m.rubika.ir/',
        'content-type': 'application/json',
        'connection': 'keep-alive'
    }

    def __init__(self, client: "rubpy.Client") -> None:
        """
        Network class initializition.

        Parameters:
        - client: Instance of rubpy.Client.
        """
        self.client = client
        self.max_retries = client.max_retries
        self.logger = logging.getLogger(__name__)
        self.headers = self.HEADERS.copy()
        self.headers['user-agent'] = client.user_agent

        if client.DEFAULT_PLATFORM['platform'] == 'Android':
            self.headers.pop('origin', None)
            self.headers.pop('referer', None)
            self.headers['user-agent'] = 'okhttp/3.12.1'
            client.DEFAULT_PLATFORM['package'] = 'app.rbmain.a'
            client.DEFAULT_PLATFORM['app_version'] = '3.8.2'

        connector = aiohttp.TCPConnector(verify_ssl=False, limit=100)
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=client.timeout)
        )

        self.bot_api_url = f'https://messengerg2b1.iranlms.ir/v3/{client.bot_token}/' if client.bot_token else None
        self.api_url = None
        self.wss_url = None
        self.ws = None

    async def close(self) -> None:
        """
        Close the aiphttp.ClientSession
        """
        if self.session and not self.session.closed:
            await self.session.close()

    async def get_dcs(self, max_retries: int = 3, backoff: float = 1.0) -> bool:
        """
        Retrieves API and WebSocket URLs with retry and exponential backoff.

        This method fetches the data center configuration from Rubika's endpoint,
        sets the API and WebSocket URLs on the client instance, and handles network
        or server errors with retry logic.

        Args:
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
            backoff (float, optional): Base delay in seconds for exponential backoff. Defaults to 1.0.

        Returns:
            bool: True if the data center configuration was successfully retrieved.

        Raises:
            NetworkError: If all retry attempts fail to fetch the data centers.
        """
        url = 'https://getdcmess.iranlms.ir/'
        for attempt in range(max_retries):
            try:
                async with self.session.get(url, proxy=self.client.proxy) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    data = json_data.get('data', {})
                    api_list = data.get('API', {})
                    socket_list = data.get('socket', {})

                    self.api_url = f"{api_list.get(data.get('default_api'))}/"
                    self.wss_url = socket_list.get(data.get('default_socket'))

                    if self.api_url and self.wss_url:
                        return True
                    else:
                        raise ValueError("Incomplete data received from server.")

            except Exception as e:
                self.logger.warning(f"Failed to retrieve Data Centers (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff * (2 ** attempt))

        raise exceptions.NetworkError("Failed to fetch Data Centers after multiple attempts.")

    async def request(
        self,
        url: str,
        data: Dict,
        max_retries: int = 3,
        backoff: float = 1.0
    ) -> Dict:
        """
        Sends an HTTP POST request with retry logic and exponential backoff.

        This method attempts to send a POST request to the specified URL using the
        provided JSON data. If the request fails due to network issues or server errors,
        it retries up to `max_retries` times with a growing delay.

        Args:
            url (str): The target API endpoint.
            data (dict): The JSON-serializable payload to send.
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
            backoff (float, optional): Base delay in seconds for exponential backoff. Defaults to 1.0.

        Returns:
            dict: The parsed JSON response from the server.

        Raises:
            NetworkError: If the request fails after all retry attempts.
        """
        for attempt in range(max_retries):
            try:
                async with self.session.post(url, json=data, proxy=self.client.proxy) as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception as e:
                self.logger.warning(
                    f"Request to {url} failed (attempt {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff * (2 ** attempt))

        raise exceptions.NetworkError(f"Request to {url} failed after {max_retries} attempts.")

    async def send(self, **kwargs) -> dict:
        """
        Send request to Rubika's API

        Parameters:
        - kwargs: Request parameters

        Returns:
        - JSON-decoded response.
        """
        api_version = str(kwargs.get('api_version', self.client.API_VERSION))
        auth = kwargs.get('auth', self.client.auth)
        client = kwargs.get('client', self.client.DEFAULT_PLATFORM)
        input_data = kwargs.get('input', {})
        method = kwargs.get('method', 'getUserInfo')
        encrypt = kwargs.get('encrypt', True)
        tmp_session = kwargs.get('tmp_session', False)
        url = kwargs.get('url', self.api_url)

        data = {'api_version': api_version}
        key = 'tmp_session' if tmp_session else 'auth'
        data[key] = auth if tmp_session else self.client.decode_auth

        if api_version == '6':
            data_enc = {'client': client, 'method': method, 'input': input_data}
            if encrypt:
                data['data_enc'] = Crypto.encrypt(data_enc, key=self.client.key)
                if not tmp_session:
                    data['sign'] = Crypto.sign(self.client.import_key, data['data_enc'])
            return await self.request(url, data, max_retries=self.max_retries)

        elif api_version == '0':
            data.update({'auth': auth, 'client': client, 'data': input_data, 'method': method})
        elif api_version == '4':
            data.update({'client': client, 'method': method})
        elif api_version == 'bot':
            return await self.request(f"{self.bot_api_url}{method}", input_data, max_retries=self.max_retries)

        return await self.request(url, data, max_retries=self.max_retries)

    async def handle_update(self, name: str, update: dict) -> None:
        """
        Dispatches incoming updates to the registered handlers.

        This method iterates over all registered client handlers and invokes the one
        whose name matches the incoming update type. Handlers can be coroutine functions
        or regular functions (executed in a background thread). If a handler raises
        `StopHandler`, it halts further processing of that update.

        Args:
            name (str): The name/type of the incoming update (e.g. "message", "chat").
            update (dict): The update payload received from the server.

        Returns:
            None

        Logs:
            - Errors during handler execution, including traceback.
        """
        for func, handler in self.client.handlers.items():
            try:
                if isinstance(handler, type):
                    handler = handler()

                if handler.__name__ != capitalize(name):
                    continue

                if not await handler(update=update):
                    continue

                update_obj = Update(update.copy())
                if not inspect.iscoroutinefunction(func):
                    threading.Thread(target=func, args=(update_obj,)).start()
                else:
                    asyncio.create_task(func(update_obj))
            except exceptions.StopHandler:
                break
            except Exception as e:
                self.logger.error(
                    f"Error in handler for '{name}': {e}",
                    extra={'data': update},
                    exc_info=True
                )
                #self.logger.error(f"خطا در handler برای {name}: {e}", extra={'data': update}, exc_info=True)

    async def get_updates(self) -> None:
        """
        Continuously listens for updates from Rubika's WebSocket API,
        maintaining connection with automatic reconnection logic.

        This coroutine establishes a persistent WebSocket connection to Rubika,
        performs handshake authentication, and listens for incoming messages.
        If the connection drops or times out, it waits briefly and reconnects.
        It also launches a background task to keep the socket alive.

        Returns:
            None

        Logs:
            - Warning on connection failures or errors during communication.
        """
        asyncio.create_task(self.keep_socket())

        while True:
            try:
                async with self.session.ws_connect(
                    self.wss_url,
                    proxy=self.client.proxy
                ) as ws:
                    self.ws = ws

                    # Send initial handshake
                    await ws.send_json({
                        'method': 'handShake',
                        'auth': self.client.auth,
                        'api_version': '6',
                        'data': ''
                    })

                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            asyncio.create_task(self.handle_text_message(msg.json()))
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            self.logger.warning("WebSocket closed or errored; reconnecting...")
                            break

            except (aiohttp.ServerTimeoutError, TimeoutError, aiohttp.ClientError) as e:
                self.logger.warning(f"WebSocket connection lost: {e}. Retrying in 3 seconds...")
                await asyncio.sleep(3)

    async def keep_socket(self) -> None:
        """
        Maintains the WebSocket connection by periodically sending pings
        and checking for chat updates.

        This coroutine runs indefinitely, sending an empty JSON object
        to the server every 10 seconds to keep the connection alive. If the
        WebSocket is closed or an exception occurs, it logs a warning and retries.

        Returns:
            None

        Logs:
            - Warning if the connection check or ping fails.
        """
        while True:
            try:
                await asyncio.sleep(10)

                if self.ws and not self.ws.closed:
                    await self.ws.send_json({})
                    await self.client.get_chats_updates()
                else:
                    self.logger.warning("WebSocket is not connected or already closed.")
            except Exception as e:
                self.logger.warning(f"Exception while keeping WebSocket alive: {e}", exc_info=True)

    async def handle_text_message(self, msg_data: Dict) -> None:
        """
        Handles incoming text messages received via WebSocket.

        This method decrypts the incoming `data_enc` field using the client's key,
        extracts updates, and dispatches them asynchronously to the appropriate handler(s).

        Args:
            msg_data (dict): Parsed JSON dictionary received from the WebSocket.

        Returns:
            None

        Logs:
            - Debug message if `data_enc` is missing.
            - Error message if decryption or handling fails.
        """
        data_enc = msg_data.get('data_enc')
        if not data_enc:
            self.logger.debug("Missing 'data_enc' key in message", extra={'data': msg_data})
            return

        try:
            decrypted_data = Crypto.decrypt(data_enc, key=self.client.key)
            user_guid = decrypted_data.pop('user_guid')

            tasks = [
                self.handle_update(name, {**update, 'client': self.client, 'user_guid': user_guid})
                for name, updates in decrypted_data.items()
                if isinstance(updates, list)
                for update in updates
            ]

            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error("Exception while handling WebSocket message",
                            extra={'data': msg_data},
                            exc_info=True)

    async def upload_file(
        self,
        file: Union[str, bytes],
        mime: Optional[str] = None,
        file_name: Optional[str] = None,
        chunk: int = 1048576,
        callback: Optional[Callable[[int, int], Union[None, asyncio.Future]]] = None,
        max_retries: int = 3,
        backoff: float = 1.0,
        *args, **kwargs
    ) -> Update:
        """
        Uploads a file to Rubika with chunked transfer and retry logic.

        Supports both file path and raw bytes input. Uploads in chunks and
        provides progress updates via optional callback. If the server requests
        reinitialization (e.g. due to expired upload credentials), it automatically
        resets and resumes the process.

        Args:
            file (str or bytes): File path or bytes to upload.
            mime (str, optional): MIME type of the file. Defaults to file extension.
            file_name (str, optional): Name of the file to assign. Required for bytes input.
            chunk (int, optional): Chunk size in bytes. Defaults to 1MB.
            callback (callable, optional): Function or coroutine for progress reporting.
                Called with (total_size, uploaded_bytes).
            max_retries (int, optional): Max retry attempts per chunk. Defaults to 3.
            backoff (float, optional): Initial delay (in seconds) for exponential retry backoff. Defaults to 1.0.

        Returns:
            Update: An object containing metadata about the uploaded file (dc_id, file_id, size, mime, etc.).

        Raises:
            ValueError: If file path is invalid or file_name is missing for bytes input.
            TypeError: If the file argument is neither str nor bytes.
            Exception: If the upload fails after retries.
        """
        if isinstance(file, str):
            if not os.path.exists(file):
                raise ValueError("File not found at the given path.")
            file_name = file_name or os.path.basename(file)
            file_size = os.path.getsize(file)
        elif isinstance(file, bytes):
            if not file_name:
                raise ValueError("file_name must be specified when uploading from bytes.")
            file_size = len(file)
        else:
            raise TypeError("file must be a file path (str) or raw bytes.")

        mime = mime or file_name.split('.')[-1]

        async def handle_callback(total: int, current: int):
            if not callable(callback):
                return
            try:
                if inspect.iscoroutinefunction(callback):
                    await callback(total, current)
                else:
                    callback(total, current)
            except exceptions.CancelledError:
                return None
            except Exception as e:
                self.logger.error(f"Callback error: {e}")

        async def upload_chunk(data: bytes, part_number: int) -> dict:
            for attempt in range(max_retries):
                try:
                    async with self.session.post(
                        url=upload_url,
                        headers={
                            'auth': self.client.auth,
                            'file-id': file_id,
                            'total-part': str(total_parts),
                            'part-number': str(part_number),
                            'chunk-size': str(len(data)),
                            'access-hash-send': access_hash_send
                        },
                        data=data,
                        proxy=self.client.proxy
                    ) as response:
                        return await response.json()
                except Exception as e:
                    self.logger.warning(
                        f"Error uploading chunk {part_number} (attempt {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(backoff * (2 ** attempt))
                    else:
                        raise

        # Initial request to get upload metadata
        result = await self.client.request_send_file(file_name, file_size, mime)
        file_id, dc_id, upload_url, access_hash_send = result.id, result.dc_id, result.upload_url, result.access_hash_send
        total_parts = (file_size + chunk - 1) // chunk

        index = 0
        while index < total_parts:
            if isinstance(file, str):
                async with aiofiles.open(file, 'rb') as f:
                    await f.seek(index * chunk)
                    data = await f.read(chunk)
            else:
                data = file[index * chunk:(index + 1) * chunk]

            upload_result = await upload_chunk(data, index + 1)

            if upload_result.get('status') == 'ERROR_TRY_AGAIN':
                self.logger.warning("Server requested reinitialization. Restarting upload.")
                result = await self.client.request_send_file(file_name, file_size, mime)
                file_id, dc_id, upload_url, access_hash_send = result.id, result.dc_id, result.upload_url, result.access_hash_send
                index = 0
                continue

            await handle_callback(file_size, min((index + 1) * chunk, file_size))
            index += 1

        if upload_result.get('status') == 'OK' and upload_result.get('status_det') == 'OK':
            return Update({
                'mime': mime,
                'size': file_size,
                'dc_id': dc_id,
                'file_id': file_id,
                'file_name': file_name,
                'access_hash_rec': upload_result['data']['access_hash_rec']
            })

        raise exceptions(upload_result.get('status_det'))(upload_result)

    async def download(
        self,
        dc_id: int,
        file_id: int,
        access_hash: str,
        size: int,
        chunk: int = 131072,
        callback: Optional[Callable[[int, int], Union[None, asyncio.Future]]] = None,
        gather: bool = False,
        save_as: Optional[str] = None,
        max_retries: int = 3,
        backoff: float = 1.0,
        *args, **kwargs
    ) -> Union[bytes, str]:
        """
        Download a file from Rubika using its file ID and access hash.

        This function supports downloading files either to memory (as bytes)
        or saving directly to disk. It also supports parallel downloading using
        asyncio.gather and provides retry logic with exponential backoff.

        Args:
            dc_id (int): Data center ID.
            file_id (int): Unique identifier of the file.
            access_hash (str): Access hash associated with the file.
            size (int): Total size of the file in bytes.
            chunk (int, optional): Size of each download chunk in bytes. Defaults to 131072 (128 KB).
            callback (callable, optional): A function or coroutine called with (total_size, downloaded_size)
                to report progress.
            gather (bool, optional): If True, downloads chunks in parallel using asyncio.gather. Defaults to False.
            save_as (str, optional): If specified, path to save the downloaded file. If None, returns file content.
            max_retries (int, optional): Maximum number of retry attempts for each chunk. Defaults to 3.
            backoff (float, optional): Base delay (in seconds) for exponential backoff. Defaults to 1.0.

        Returns:
            bytes or str: The downloaded file content as bytes (if `save_as` is None),
                        or the path to the saved file (if `save_as` is specified).

        Raises:
            None explicitly, but logs warnings and errors internally on failed retries or callback exceptions.
        """
        headers = {
            'auth': self.client.auth,
            'access-hash-rec': access_hash,
            'file-id': str(file_id),
            'user-agent': self.client.user_agent
        }
        base_url = f'https://messenger{dc_id}.iranlms.ir'

        async def fetch_chunk(session, start: int, end: int) -> bytes:
            chunk_headers = {**headers, 'start-index': str(start), 'last-index': str(end)}
            for attempt in range(max_retries):
                try:
                    async with session.post('/GetFile.ashx', headers=chunk_headers, proxy=self.client.proxy) as resp:
                        if resp.status == 200:
                            return await resp.read()
                        self.logger.warning(f"Download failed with status {resp.status}")
                except Exception as e:
                    self.logger.warning(f"Error downloading chunk {start}-{end} (Attempt {attempt+1}): {e}")
                await asyncio.sleep(backoff * (2 ** attempt))
            return b''

        async def handle_callback(total: int, current: int):
            if not callable(callback):
                return
            try:
                if inspect.iscoroutinefunction(callback):
                    await callback(total, current)
                else:
                    callback(total, current)
            except Exception as e:
                self.logger.error(f"Callback error: {e}")

        async with aiohttp.ClientSession(base_url=base_url, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            if save_as:
                async with aiofiles.open(save_as, 'wb') as f:
                    for start in range(0, size, chunk):
                        end = min(start + chunk, size) - 1
                        data = await fetch_chunk(session, start, end)
                        if not data:
                            break
                        await f.write(data)
                        await handle_callback(size, end + 1)
                return save_as

            elif gather:
                tasks = [
                    fetch_chunk(session, start, min(start + chunk, size) - 1)
                    for start in range(0, size, chunk)
                ]
                chunks = await asyncio.gather(*tasks)
                result = b''.join(filter(None, chunks))
                await handle_callback(size, len(result))
                return result

            else:
                result = bytearray()
                for start in range(0, size, chunk):
                    end = min(start + chunk, size) - 1
                    data = await fetch_chunk(session, start, end)
                    if not data:
                        break
                    result.extend(data)
                    await handle_callback(size, len(result))
                return bytes(result)