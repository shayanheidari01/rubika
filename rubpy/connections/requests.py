from ujson import loads, dumps
from urllib.request import urlopen
from random import choice
from ..encryption import Encryption
from ..exceptions import NotRegistered, InvalidInput, InvaildAuth, TooRequests
from httpx import AsyncClient
from urllib3 import PoolManager


class Requests(object):
    def __init__(self, auth):
        self.auth = auth
        self.web = {'app_name': 'Main', 'app_version': '4.1.7', 'platform': 'Web', 'package': 'web.rubika.ir', 'lang_code': 'fa' }
        self.android = {'app_name': 'Main', 'app_version': '3.0.7', 'platform': 'Android', 'package': 'ir.resaneh1.iptv', 'lang_code': 'fa' }
        self.__address = list(loads(urlopen('https://getdcmess.iranlms.ir/').read().decode('utf-8')).get('data').get('API').values())
        self.enc = Encryption(auth)
        self.async_client = AsyncClient()
        self.__manager = PoolManager()

    async def post(self, url, json=None, is_upload=False, headers=None, data=None):
        if is_upload:
            response = self.__manager.request('POST', url, body=data, headers=headers)
            if response.status == 200:
                return loads(response.data.decode('utf-8'))
            else: return False
        else:
            response = await self.async_client.request('POST', url, json=json)
            if response.status_code == 200:
                return response.json()
            else: return False

    async def uploadFile(self, url, access_hash_send, file_id, byte):
        file_size = len(byte)
        if file_size <= 131072:
            header = {
				'access-hash-send': access_hash_send,
				'file-id': str(file_id),
				'part-number': '1',
				'total-part': '1',
				'chunk-size': str(file_size),
				'auth': self.auth
			}
            for i in range(5):
                try:
                    response = await self.post(url, data=byte, headers=header, is_upload=True)
                    if response: return response.get('data').get('access_hash_rec')
                    else: continue
                except ConnectionError: continue
        else:
            total_part = round(len(byte) / 131072 + 1)
            header = {
				'access-hash-send': access_hash_send,
				'file-id': (file_id),
				'part-number': '1',
				'total-part': total_part,
				'chunk-size': '131072',
				'auth': self.auth
			}
            for part_number in range(1, total_part + 1):
                if part_number != total_part:
                    bytes_counter = part_number - 1
                    bytes_counter = bytes_counter * 131072
                    for i in range(5):
                        try:
                            header['part-number'] = part_number
                            response = await self.post(url, data=byte[bytes_counter:bytes_counter + 131072], headers=header, is_upload=True)
                            if response:
                                break
                            else:
                                continue
                        except ConnectionError:
                            continue
                else:
                    bytes_counter = part_number - 1
                    bytes_counter = bytes_counter * 131072
                    for i in range(5):
                        try:
                            header['part-number'] = total_part
                            header['chunk-size'] = str(len(byte[bytes_counter:]))
                            response = await self.post(url, data=byte[bytes_counter:], headers=header, is_upload=True)
                            if response:
                                return response.get('data').get('access_hash_rec')
                            else:
                                continue
                        except ConnectionError:
                            continue

    async def send(self, method, data, method_type=None, custum_client=False):
        if method_type == None:
            data = {'api_version': '4', 'auth': self.auth, 'client': self.android, 'method': method, 'data_enc': self.enc.encrypt(dumps(data))}
            while True:
                try:
                    response = await self.post(self.getDC(), json=data)
                    if response:
                        if response.get('status') == 'ERROR_GENERIC' or response.get('status') == 'ERROR_ACTION':
                            if response.get('status_det') == 'NOT_REGISTERED':
                                raise NotRegistered('Your AUTH is incorrect')
                            elif response.get('status_det') == 'INVALID_INPUT':
                                raise InvalidInput('The data sent to the server is wrong')
                            elif response.get('status_det') == 'INVALID_AUTH':
                                raise InvaildAuth('An error was received from the server side, probably the data sent is wrong or your AUTH is invalid')
                            elif response.get('status_det') == 'TOO_REQUESTS':
                                raise TooRequests('Unfortunately, your account has been limited')
                            else: raise RuntimeWarning(response)
                        elif response.get('status') == 'OK' and response.get('status_det') == 'OK':
                            return loads(self.enc.decrypt(response.get('data_enc')))
                    else: continue
                except ConnectionError: continue

        elif method_type == 5:
            data = {'api_version': '5', 'auth': self.auth, 'data_enc': self.enc.encrypt(dumps({'method': method, 'input': data, 'client': self.web if custum_client == False else self.android}))}
            while True:
                try:
                    response = await self.post(self.getDC(), json=data)
                    if response:
                        response = loads(self.enc.decrypt(response.get('data_enc')))
                        if response.get('status') == 'ERROR_GENERIC' or response.get('status') == 'ERROR_ACTION':
                            if response.get('status_det') == 'NOT_REGISTERED':
                                raise NotRegistered('Your AUTH is incorrect')
                            elif response.get('status_det') == 'INVALID_INPUT':
                                raise InvalidInput('The data sent to the server is wrong')
                            elif response.get('status_det') == 'INVALID_AUTH':
                                raise InvaildAuth('An error was received from the server side, probably the data sent is wrong or your AUTH is invalid')
                            elif response.get('status_det') == 'TOO_REQUESTS':
                                raise TooRequests('Unfortunately, your account has been limited')
                            else: raise RuntimeWarning(response)
                        else:
                            return response
                    else: continue
                except ConnectionError: continue

    def getDC(self): return choice(self.__address)