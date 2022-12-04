from urllib3 import PoolManager
from websockets import connect, ConnectionClosed
from random import randint, choice
from json import dumps, loads
from time import time
from ...crypto import Crypto


__all__ = ('Connections', 'WebSocket')


class Connections:
    __slots__ = ('__manager__', '__auth__')

    def __init__(self, auth):
        self.__manager__ = PoolManager(headers={'Content-Type':'application/json'})
        self.__auth__ = auth

    async def GET(self, url, headers=None, download=False):
        async def runner():
            if download:
                while True:
                    response = self.__manager__.request('GET', url, headers=headers)
                    status = response.status
                    if status == 200:
                        return response.data
                    elif status == 502:
                        continue
                    else:
                        data = response.data.decode('UTF-8')
                        raise Exception(f'An error received from rubika server(download servers):\n\tError: {data or {}}\n\tstatus code: {status}')
            else:
                return loads(self.__manager__.request('GET', url, headers=headers).data.decode('UTF-8'))
        return await runner()

    async def getdcmess(self, ws=False,):
        url = 'https://getdcmess.iranlms.ir/'
        if ws:
            response = await self.GET(url=url)
            return response.get('data').get('socket').values()
        else:
            response = await self.GET(url=url)
            return response.get('data').get('API').values()

    async def POST(self, data):
        data = dumps(data)
        while True:
            response = self.__manager__.request('POST', url=f'https://messengerg2c{randint(1,2)}.iranlms.ir/', body=data.encode('UTF-8'))
            status = response.status
            if status == 200:
                return loads(response.data.decode('UTF-8'))
            elif status == 502:
                continue
            else:
                raise Exception('response status: {}\nresponse body: {}'.format(status, response.data.decode('UTF-8') or {}))

    async def uploadData(self, url, data, headers):
        while True:
            response = self.__manager__.request('POST', url=url, body=data, headers=headers)
            status = response.status
            if status == 200:
                return loads(response.data.decode('UTF-8'))
            elif status == 502:
                continue
            else:
                raise Exception('response status: {}\nresponse body: {}'.format(status, response.data.decode('UTF-8') or {}))

    async def uploadFile(self, upload_url, access_hash_send, file_id, file_bytes):
        size = str(len(file_bytes))
        headers = {
            'auth': self.__auth__,
            'chunk-size': size,
            'part-number': '1',
            'total-part': '1',
            'file-id': str(file_id),
            'access-hash-send': access_hash_send,
            'content-type': 'application/octet-stream',
        }

        if int(size) <= 131072:
            response = await self.uploadData(upload_url, file_bytes, headers)
            return response.get('data').get('access_hash_rec')

        else:
            size = int(size)
            total_part = size // 131072 + 1
            for part_number in range(1, total_part + 1):
                bsb = (part_number - 1) * 131072 # base set  file bytes
                headers["chunk-size"], headers["part-number"], headers["total-part"] = "131072" if part_number != total_part else str(len(file_bytes[bsb:])), str(part_number), str(total_part)
                if part_number != total_part:
                    data = file_bytes[bsb:bsb + 131072]
                    response = await self.uploadData(upload_url, data, headers)
                    assert response.get('data') == None
                else:
                    data = file_bytes[bsb:]
                    response = await self.uploadData(upload_url, data, headers)
                    return response.get('data').get('access_hash_rec')


class WebSocket:

    __slots__ = (
        '__auth__',
        '__crypto__',
        'getdcmess',
        'data',
    )

    def __init__(self, auth,):
        self.__auth__ = auth
        self.__crypto__ = Crypto(auth,)
        self.getdcmess = Connections(auth).getdcmess
        self.data = {
            'api_version': '5',
            'auth': auth,
            'method': 'handShake'
        }
        del auth

    async def handSnake(self,):
        wss = choice(list(await self.getdcmess(ws=True,),),)
        async for websocket in connect(wss,):
            try:
                await websocket.send(dumps(self.data,),)
                while True:
                    data = await websocket.recv()
                    if data != '{"status":"OK","status_det":"OK"}':
                        yield loads(data,)
                    else: continue
            except ConnectionClosed: continue

    async def updatesHandler(self, chat_updates=False, message_updates=True, show_notifications=False):
        async for message in self.handSnake():
            if message.get('type') == 'messenger':
                data = loads(self.__crypto__.decode(message.get('data_enc')))
                if message_updates and chat_updates and show_notifications:
                    yield message
                elif message_updates:
                    if 'message_updates' in data:
                        for i in data.get('message_updates'):
                            yield i
                elif chat_updates:
                    if 'chat_updates' in data:
                        for i in data.get('chat_updates'):
                            yield i
                elif show_notifications:
                    if 'show_notifications' in data:
                        for i in data.get('show_notifications'):
                            yield i