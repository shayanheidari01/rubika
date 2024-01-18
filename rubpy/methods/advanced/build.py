from ...crypto import Crypto
from ... import exceptions
from ...types import Results
from typing import Union
import rubpy

class Builder:
    async def builder(
            self: "rubpy.Client",
            name: str,
            tmp_session: bool = False,
            encrypt: bool = True,
            dict: bool = False,
            input: dict = None,
    ) -> Union[Results, dict]:
        if not self.connection.api_url:
            await self.connection.get_dcs()

        if self.auth is None:
            self.auth = Crypto.secret(length=32)
            # self._client._logger.info(
            #     'create auth secret', extra={'data': self._client._auth})

        if self.key is None:
            self.key = Crypto.passphrase(self.auth)
            # self._client._logger.info(
            #     'create key passphrase', extra={'data': self._client._key})

        result = await self.connection.send(method=name,
                                            tmp_session=tmp_session,
                                            encrypt=encrypt,
                                            input=input)
        data_enc = result.get('data_enc')
        if data_enc:
            result = Crypto.decrypt(data_enc,
                                key=self.key)

        status = result['status']
        status_det = result['status_det']

        if status == 'OK' and status_det == 'OK':
            if dict:
                return result.get('data')

            result['data']['_client'] = self
            return Results(result['data'])

        raise exceptions(status_det)(result, request=None)