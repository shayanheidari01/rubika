import threading
import asyncio
import aiohttp
import aiofiles
import inspect
import rubpy
import os
import uuid
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
        'origin': 'https://web.rubika.ir',
        'referer': 'https://web.rubika.ir/',
        'content-type': 'application/json',
        'connection': 'keep-alive'
    }

    def __init__(self, client: "rubpy.Client") -> None:
        """
        مقداردهی اولیه کلاس Network.

        پارامترها:
        - client: نمونه‌ای از rubpy.Client.
        """
        self.client = client
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
        بستن ClientSession از aiohttp.
        """
        if self.session and not self.session.closed:
            await self.session.close()

    async def get_dcs(self, max_retries: int = 3, backoff: float = 1.0) -> bool:
        """
        دریافت URLهای API و WebSocket با مکانیزم بازآزمایی.

        خروجی:
        True در صورت موفقیت.
        """
        for attempt in range(max_retries):
            try:
                async with self.session.get('https://getdcmess.iranlms.ir/', proxy=self.client.proxy) as response:
                    response.raise_for_status()
                    data = (await response.json()).get('data')
                    self.api_url = f"{data['API'][data['default_api']]}/"
                    self.wss_url = data['socket'][data['default_socket']]
                    return True
            except Exception as e:
                self.logger.warning(f"خطا در دریافت Data Centers، تلاش {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff * (2 ** attempt))
        raise exceptions.NetworkError("دریافت Data Centers ناموفق بود")

    async def request(self, url: str, data: dict, max_retries: int = 3, backoff: float = 1.0) -> dict:
        """
        ارسال درخواست HTTP POST با بازآزمایی.

        پارامترها:
        - url: آدرس endpoint API.
        - data: داده‌های ارسالی.
        - max_retries: حداکثر تعداد تلاش‌ها.
        - backoff: تأخیر پایه برای بازآزمایی.

        خروجی:
        پاسخ JSON-decoded.
        """
        for attempt in range(max_retries):
            try:
                async with self.session.post(url, json=data, proxy=self.client.proxy) as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception as e:
                self.logger.warning(f"خطا در درخواست، تلاش {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff * (2 ** attempt))
        raise exceptions.NetworkError(f"درخواست به {url} پس از {max_retries} تلاش ناموفق بود")

    async def send(self, **kwargs) -> dict:
        """
        ارسال درخواست به API روبیکا.

        پارامترها:
        - kwargs: پارامترهای درخواست.

        خروجی:
        پاسخ JSON-decoded.
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
            return await self.request(url, data)

        elif api_version == '0':
            data.update({'auth': auth, 'client': client, 'data': input_data, 'method': method})
        elif api_version == '4':
            data.update({'client': client, 'method': method})
        elif api_version == 'bot':
            return await self.request(f"{self.bot_api_url}{method}", input_data)

        return await self.request(url, data)

    async def handle_update(self, name: str, update: dict) -> None:
        """
        مدیریت آپدیت‌ها برای handlerهای ثبت‌شده.
        """
        for func, handler in self.client.handlers.items():
            try:
                if isinstance(handler, type):
                    handler = handler()

                if handler.__name__ != capitalize(name):
                    continue

                if not await handler(update=update):
                    continue

                update_obj = Update(handler.original_update)
                if not inspect.iscoroutinefunction(func):
                    threading.Thread(target=func, args=(update_obj,)).start()
                else:
                    asyncio.create_task(func(update_obj))
            except exceptions.StopHandler:
                break
            except Exception as e:
                self.logger.error(f"خطا در handler برای {name}: {e}", extra={'data': update}, exc_info=True)

    async def get_updates(self) -> None:
        """
        دریافت آپدیت‌ها از WebSocket روبیکا با منطق اتصال مجدد.
        """
        asyncio.create_task(self.keep_socket())
        while True:
            try:
                async with self.session.ws_connect(self.wss_url, proxy=self.client.proxy, receive_timeout=5) as ws:
                    self.ws = ws
                    await ws.send_json({'method': 'handShake', 'auth': self.client.auth, 'api_version': '6', 'data': ''})
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            asyncio.create_task(self.handle_text_message(msg.json()))
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            break
            except (aiohttp.ServerTimeoutError, TimeoutError, aiohttp.ClientError) as e:
                self.logger.warning(f"اتصال WebSocket قطع شد: {e}. تلاش برای اتصال مجدد...")
                await asyncio.sleep(5)

    async def keep_socket(self) -> None:
        """
        حفظ اتصال WebSocket با ارسال پینگ‌های دوره‌ای.
        """
        while True:
            try:
                await asyncio.sleep(10)
                if self.ws and not self.ws.closed:
                    await self.ws.send_json({})
                    await self.client.get_chats_updates()
            except Exception as e:
                self.logger.warning(f"خطا در حفظ اتصال WebSocket: {e}")
                continue

    async def handle_text_message(self, msg_data: dict) -> None:
        """
        مدیریت پیام‌های متنی دریافت‌شده از WebSocket.

        پارامترها:
        - msg_data: داده JSON تجزیه‌شده.
        """
        if not (data_enc := msg_data.get('data_enc')):
            self.logger.debug("کلید data_enc یافت نشد", extra={'data': msg_data})
            return

        try:
            decrypted_data = Crypto.decrypt(data_enc, key=self.client.key)
            user_guid = decrypted_data.pop('user_guid')
            tasks = [
                self.handle_update(name, {**update, 'client': self.client, 'user_guid': user_guid})
                for name, package in decrypted_data.items()
                if isinstance(package, list)
                for update in package
            ]
            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(f"خطا در مدیریت WebSocket: {e}", extra={'data': msg_data}, exc_info=True)

    async def upload_file(self, file, mime: str = None, file_name: str = None, chunk: int = 1048576,
                         callback=None, max_retries: int = 3, backoff: float = 1.0) -> Update:
        """
        آپلود فایل به روبیکا با منطق بازآزمایی.

        پارامترها:
        - file: مسیر فایل یا بایت‌ها.
        - mime: نوع MIME فایل.
        - file_name: نام فایل.
        - chunk: اندازه قطعه برای آپلود.
        - callback: callback برای پیشرفت.
        - max_retries: حداکثر تعداد تلاش‌ها.
        - backoff: تأخیر پایه برای بازآزمایی.

        خروجی:
        شیء Update با متادیتای فایل.
        """
        if isinstance(file, str):
            if not os.path.exists(file):
                raise ValueError('فایل در مسیر مشخص‌شده یافت نشد')
            file_name = file_name or os.path.basename(file)
            file_size = os.path.getsize(file)
        elif isinstance(file, bytes):
            if not file_name:
                raise ValueError('نام فایل مشخص نشده است')
            file_size = len(file)
        else:
            raise TypeError('فایل باید مسیر یا بایت باشد')

        mime = mime or file_name.split('.')[-1]

        result = await self.client.request_send_file(file_name, file_size, mime)
        file_id, dc_id, upload_url, access_hash_send = result.id, result.dc_id, result.upload_url, result.access_hash_send
        total_parts = (file_size + chunk - 1) // chunk

        async def upload_chunk(data, part_number):
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
                    self.logger.warning(f"خطا در آپلود قطعه {part_number}، تلاش {attempt + 1}/{max_retries}: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(backoff * (2 ** attempt))
                    else:
                        raise

        index = 0
        if isinstance(file, str):
            async with aiofiles.open(file, 'rb') as f:
                while index < total_parts:
                    await f.seek(index * chunk)
                    data = await f.read(chunk)
                    result = await upload_chunk(data, index + 1)
                    if result.get('status') == 'ERROR_TRY_AGAIN':
                        result = await self.client.request_send_file(file_name, file_size, mime)
                        file_id, dc_id, upload_url, access_hash_send = result.id, result.dc_id, result.upload_url, result.access_hash_send
                        index = 0
                        continue
                    if callable(callback):
                        try:
                            if inspect.iscoroutinefunction(callback):
                                await callback(file_size, (index + 1) * chunk)
                            else:
                                callback(file_size, (index + 1) * chunk)
                        except exceptions.CancelledError:
                            return None
                        except Exception as e:
                            self.logger.error(f"خطا در callback: {e}")
                    index += 1
        else:
            while index < total_parts:
                data = file[index * chunk:(index + 1) * chunk]
                result = await upload_chunk(data, index + 1)
                if result.get('status') == 'ERROR_TRY_AGAIN':
                    result = await self.client.request_send_file(file_name, file_size, mime)
                    file_id, dc_id, upload_url, access_hash_send = result.id, result.dc_id, result.upload_url, result.access_hash_send
                    index = 0
                    continue
                if callable(callback):
                    try:
                        if inspect.iscoroutinefunction(callback):
                            await callback(file_size, (index + 1) * chunk)
                        else:
                            callback(file_size, (index + 1) * chunk)
                    except exceptions.CancelledError:
                        return None
                    except Exception as e:
                        self.logger.error(f"خطا در callback: {e}")
                index += 1

        if result['status'] == 'OK' and result['status_det'] == 'OK':
            return Update({
                'mime': mime,
                'size': file_size,
                'dc_id': dc_id,
                'file_id': file_id,
                'file_name': file_name,
                'access_hash_rec': result['data']['access_hash_rec']
            })
        raise exceptions(result['status_det'])(result)

    async def download(self, dc_id: int, file_id: int, access_hash: str, size: int, chunk: int = 131072,
                      callback=None, gather: bool = False, save_as: str = None, max_retries: int = 3, backoff: float = 1.0) -> bytes:
        """
        دانلود فایل از روبیکا.

        پارامترها:
        - dc_id: شناسه مرکز داده.
        - file_id: شناسه فایل.
        - access_hash: هش دسترسی فایل.
        - size: اندازه کل فایل.
        - chunk: اندازه قطعه برای دانلود.
        - callback: callback برای پیشرفت.
        - gather: استفاده از asyncio.gather برای دانلود همزمان.
        - save_as: مسیر ذخیره فایل (در صورت مشخص بودن).
        - max_retries: حداکثر تعداد تلاش‌ها.
        - backoff: تأخیر پایه برای بازآزمایی.

        خروجی:
        محتوای فایل دانلودشده (بایت) یا مسیر فایل ذخیره‌شده.
        """
        headers = {
            'auth': self.client.auth,
            'access-hash-rec': access_hash,
            'file-id': str(file_id),
            'user-agent': self.client.user_agent
        }
        base_url = f'https://messenger{dc_id}.iranlms.ir'

        async def fetch_chunk(session, start_index, last_index):
            chunk_headers = headers.copy()
            chunk_headers.update({'start-index': str(start_index), 'last-index': str(last_index)})
            for attempt in range(max_retries):
                try:
                    async with session.post('/GetFile.ashx', headers=chunk_headers, proxy=self.client.proxy) as response:
                        if response.status != 200:
                            self.logger.warning(f"دانلود ناموفق با وضعیت {response.status}")
                            return b''
                        return await response.read()
                except Exception as e:
                    self.logger.warning(f"خطا در دانلود قطعه {start_index}-{last_index}، تلاش {attempt + 1}/{max_retries}: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(backoff * (2 ** attempt))
                    else:
                        return b''

        async with aiohttp.ClientSession(base_url=base_url, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            if save_as:
                async with aiofiles.open(save_as, 'wb') as f:
                    start_index = 0
                    while start_index < size:
                        last_index = min(start_index + chunk, size) - 1
                        data = await fetch_chunk(session, start_index, last_index)
                        if not data:
                            break
                        await f.write(data)
                        start_index = last_index + 1
                        if callable(callback):
                            try:
                                if inspect.iscoroutinefunction(callback):
                                    await callback(size, start_index)
                                else:
                                    callback(size, start_index)
                            except Exception as e:
                                self.logger.error(f"خطا در callback: {e}")
                return save_as
            else:
                if gather:
                    tasks = [fetch_chunk(session, start, min(start + chunk, size) - 1) for start in range(0, size, chunk)]
                    chunks = await asyncio.gather(*tasks)
                    result = b''.join(filter(None, chunks))
                    if callable(callback):
                        try:
                            if inspect.iscoroutinefunction(callback):
                                await callback(size, len(result))
                            else:
                                callback(size, len(result))
                        except Exception as e:
                            self.logger.error(f"خطا در callback: {e}")
                    return result
                else:
                    result = b''
                    start_index = 0
                    while start_index < size:
                        last_index = min(start_index + chunk, size) - 1
                        data = await fetch_chunk(session, start_index, last_index)
                        if not data:
                            break
                        result += data
                        start_index = last_index + 1
                        if callable(callback):
                            try:
                                if inspect.iscoroutinefunction(callback):
                                    await callback(size, len(result))
                                else:
                                    callback(size, len(result))
                            except Exception as e:
                                self.logger.error(f"خطا در callback: {e}")
                    return result