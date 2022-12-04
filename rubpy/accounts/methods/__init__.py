from ..connections import Connections
from ...crypto import Crypto
from json import dumps, loads
from ...exceptions import (
    NotRegistered,
    InvaildAuth,
    InvalidInput,
    TooRequests,
    Repeated,
)



Web = {
        'app_name': 'Main',
        'app_version': '4.1.7',
        'platform': 'Web',
        'package': 'web.rubika.ir',
        'lang_code': 'fa'
}
Android = {
        'app_name': 'Main',
        'app_version': '3.0.7',
        'platform': 'Android',
        'package': 'ir.resaneh1.iptv',
        'lang_code': 'fa'
}


class MethodsMaker:
    __slots__ = (
        '__auth__',
        'cns',
        '__crypto__',
        '__uploader__',
    )
    def __init__(self, auth):
        self.__auth__ = auth
        self.cns = Connections(auth)
        self.__uploader__ = self.cns.uploadFile
        self.__crypto__ = Crypto(auth)

    async def request(self, method, data, method_type=5, custom_client=False):
        if method_type == 5:
            data = {
                'api_version': '5',
                'auth': self.__auth__,
                'data_enc': self.__crypto__.encode(dumps({
                    'method': method,
                    'input': data,
                    'client': Web if custom_client == False else Android
                })
            )}
            response = await self.cns.POST(data=data)
            response = loads(self.__crypto__.decode(response.get('data_enc')))
            status = response.get('status')
            if status == 'OK':
                return response.get('data')
            elif status == 'ERROR_GENERIC' or status == 'ERROR_ACTION':
                status_det = response.get('status_det')
                if status_det == 'NOT_REGISTERED':
                    raise NotRegistered('Your AUTH is incorrect')
                elif status_det == 'INVALID_INPUT':
                    raise InvalidInput('The data sent to the server is wrong')
                elif status_det == 'INVALID_AUTH':
                    raise InvaildAuth('An error was received from the server side, probably the data sent is wrong or your AUTH is invalid')
                elif status_det == 'TOO_REQUESTS':
                    raise TooRequests('Unfortunately, your account has been limited')
                else:
                    raise RuntimeWarning(response)

        elif method_type == 4:
            data = {
                'api_version': '4',
                'auth': self.__auth__,
                'client': Android,
                'method': method,
                'data_enc': self.__crypto__.encode(
                    dumps(data)
                )
            }
            response = await self.cns.POST(
                data=data,
            )
            status = response.get('status')
            if status == 'OK':
                return loads(self.__crypto__.decode(response.get('data_enc'))).get('data')
            elif status == 'ERROR_GENERIC' or status == 'ERROR_ACTION':
                status_det = response.get('status_det')
                if status_det == 'NOT_REGISTERED':
                    raise NotRegistered('Your AUTH is incorrect')
                elif status_det == 'INVALID_INPUT':
                    raise InvalidInput('The data sent to the server is wrong')
                elif status_det == 'INVALID_AUTH':
                    raise InvaildAuth('An error was received from the server side, probably the data sent is wrong or your AUTH is invalid')
                elif status_det == 'TOO_REQUESTS':
                    raise TooRequests('Unfortunately, your account has been limited')
                else:
                    raise RuntimeWarning(response)
