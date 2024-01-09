import asyncio
import aiohttp
import rubpy
import aiofiles
import os
from .crypto import Crypto
from . import exceptions
from .types import Results

def capitalize(text: str):
    return ''.join([c.title() for c in text.split('_')])

class Network:
    HEADERS = {'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/102.0.0.0 Safari/537.36'),
            	'origin': 'https://web.rubika.ir',
            	'referer': 'https://web.rubika.ir/'}

    def __init__(self, client: "rubpy.Client") -> None:
        self.client = client
        self.session = aiohttp.ClientSession(
            headers=self.HEADERS,
            timeout=aiohttp.ClientTimeout(client.timeout),
        )

        if client.bot_token is not None:
            self.bot_api_url = f'https://messengerg2b1.iranlms.ir/v3/{client.bot_token}/'

        self.api_url = None
        self.wss_url = None

    async def close(self):
        await self.session.close()

    async def get_dcs(self):
        try_count = 0

        while True:
            try:
                async with self.session.get('https://getdcmess.iranlms.ir/', verify_ssl=False) as response:
                    if not response.ok:
                        continue

                    response = (await response.json()).get('data')

                self.api_url = response.get('API').get(response.get('default_api'))
                self.wss_url = response.get('socket').get(response.get('default_socket'))
                return True

            except aiohttp.ServerTimeoutError:
                try_count += 1
                print(f'Server timeout error ({try_count})')
                await asyncio.sleep(try_count)
                continue

            except aiohttp.ClientConnectionError:
                try_count += 1
                print(f'Client connection error ({try_count})')
                await asyncio.sleep(try_count)
                continue

    async def request(self, url: str, data: dict):
        for _ in range(3):
            try:
                async with self.session.request(method='POST', url=url, json=data, verify_ssl=False) as response:
                    if response.ok:
                        return await response.json()

            except aiohttp.ServerTimeoutError:
                print('Rubika server timeout error, try again ({})'.format(_))

    async def send(self, **kwargs):
        api_version: str = str(kwargs.get('api_version', self.client.API_VERSION))
        auth: str = kwargs.get('auth', self.client.auth)
        client: dict = kwargs.get('client', self.client.DEFAULT_PLATFORM)
        input: dict = kwargs.get('input', {})
        method: str = kwargs.get('method', 'getUserInfo')
        encrypt: bool = kwargs.get('encrypt', True)
        tmp_session: bool = kwargs.get('tmp_session', False)
        url: str = kwargs.get('url', self.api_url)

        data = dict(
            api_version=api_version,
        )

        data['tmp_session' if tmp_session is True else 'auth'] = auth if tmp_session is True else Crypto.decode_auth(auth)

        if api_version == '6':
            data_enc = dict(
                client=client,
                method=method,
                input=input,
            )

            if encrypt is True:
                data['data_enc'] = Crypto.encrypt(data_enc, key=self.client.key)

            if tmp_session is False:
                data['sign'] = Crypto.sign(self.client.private_key, data['data_enc'])

        elif api_version == '0':
            data['auth'] = auth
            data['client'] = client
            data['data'] = input
            data['method'] = method

        elif api_version == '4':
            data['client'] = client
            data['method'] = method

        elif api_version == 'bot':
            return await self.request(
                url=self.bot_api_url + method,
                data=input,
            )

        return await self.request(url, data=data)

    async def update_handler(self, update: dict):
        data_enc: str = update.get('data_enc')

        if data_enc:
            result = Crypto.decrypt(data_enc, key=self.client.key)
            user_guid = result.pop('user_guid')

            for name, package in result.items():
                if not isinstance(package, list):
                    continue

                for update in package:
                    update['client'] = self.client
                    update['user_guid'] = user_guid

                for func, handler in self.client.handlers.items():
                    try:
                        # if handler is empty filters
                        if isinstance(handler, type):
                            handler = handler()

                        if handler.__name__ != capitalize(name):
                            continue

                        # analyze handlers
                        if not await handler(update=update):
                            continue

                        asyncio.create_task(func(handler))

                    except exceptions.StopHandler:
                        #print(error.message)
                        break

                    except Exception:
                        pass
                        # self._client._logger.error(
                        #     'handler raised an exception', extra={'data': update}, exc_info=True)

    async def get_updates(self):
        try_count = 0

        while True:
            try:
                async with self.session.ws_connect(self.wss_url, verify_ssl=False) as wss:
                    self.ws_connect = wss
                    await self.send_json_to_ws()
                    asyncio.create_task(self.send_json_to_ws(data=True))

                    if try_count != 0:
                        print('The connection was re-established.')
                        try_count = 0

                    async for message in wss:
                        if message.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                            await self.send_json_to_ws()

                        message = message.json()
                        await self.update_handler(message)

            except aiohttp.ClientConnectionError:
                try_count += 1
                print(f'Client connection error ({try_count})')
                await asyncio.sleep(try_count)

            except ConnectionResetError:
                try_count += 1
                print(f'Connection reset error ({try_count})')
                await asyncio.sleep(try_count)

    async def send_json_to_ws(self, data=False):
        if data:
            while True:
                #try:
                await asyncio.sleep(10)
                await self.ws_connect.send_json('{}')

        return await self.ws_connect.send_json(
            {
                'method': 'handShake',
                'auth': self.client.auth,
                'api_version': '5',
                'data': '',
            })
    
    async def upload_file(self, file, mime: str = None, file_name: str = None, chunk: int = 1048576 * 2,
                          callback=None, *args, **kwargs):
        if isinstance(file, str):
            if not os.path.exists(file):
                raise ValueError('file not found in the given path')

            if file_name is None:
                file_name = os.path.basename(file)

            async with aiofiles.open(file, 'rb') as file:
                file = await file.read()

        elif not isinstance(file, bytes):
            raise TypeError('file arg value must be file path or bytes')

        if file_name is None:
            raise ValueError('the file_name is not set')

        if mime is None:
            mime = file_name.split('.')[-1]

        result = await self.client.request_send_file(file_name, len(file), mime)

        id = result.id
        index = 0
        dc_id = result.dc_id
        total = int(len(file) / chunk + 1)
        upload_url = result.upload_url
        access_hash_send = result.access_hash_send

        while index < total:
            data = file[index * chunk: index * chunk + chunk]
            try:
                result = await self.session.post(
                        upload_url,
                        headers={
                            'auth': self.client.auth,
                            'file-id': id,
                            'total-part': str(total),
                            'part-number': str(index + 1),
                            'chunk-size': str(len(data)),
                            'access-hash-send': access_hash_send
                        },
                        data=data
                    )
                result = await result.json()
                
                if result.get('status') != 'OK':
                    raise exceptions.UploadError(result.get('status'),
                                                 result.get('status_det'),
                                                 dev_message=result.get('dev_message'))

                if callable(callback):
                        try:
                            await callback(len(file), index * chunk)

                        except exceptions.CancelledError:
                            return None

                        except Exception:
                            pass

                index += 1

            except Exception:
                   pass

        status = result['status']
        status_det = result['status_det']

        if status == 'OK' and status_det == 'OK':
            result = {
                'mime': mime,
                'size': len(file),
                'dc_id': dc_id,
                'file_id': id,
                'file_name': file_name,
                'access_hash_rec': result['data']['access_hash_rec']
            }

            return Results(result)

        #self._client._logger.debug('upload failed', extra={'data': result})
        raise exceptions(status_det)(result, request=result)
    
    async def download(self, dc_id: int, file_id: int, access_hash: str, size: int, chunk=131072, callback=None):
        url = f'https://messenger{dc_id}.iranlms.ir/GetFile.ashx'
        start_index = 0
        result = b''

        headers = {
            'auth': self.client.auth,
            'access-hash-rec': access_hash,
            'file-id': str(file_id),
            'user-agent': self.client.user_agent
        }

        async with aiohttp.ClientSession() as session:
            while True:
                last_index = start_index + chunk - 1 if start_index + chunk < size else size - 1

                headers['start-index'] = str(start_index)
                headers['last-index'] = str(last_index)

                response = await session.post(url, headers=headers)
                if response.ok:
                    data = await response.read()
                    if data:
                        result += data
                        if callback:
                            await callback(size, len(result))

                # Check for the end of the file
                if len(result) >= size:
                    break

                # Update the start_index value to fetch the next part of the file
                start_index = last_index + 1

        return result
