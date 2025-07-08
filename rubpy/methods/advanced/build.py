from ...crypto import Crypto
from ... import exceptions
from ...types import Update
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
    ) -> Union[Update, dict]:
        """
        Build and send a request to the Rubika API.

        Args:
            - name (str): The API method name.
            - tmp_session (bool, optional): Whether to use a temporary session. Defaults to False.
            - encrypt (bool, optional): Whether to encrypt the data. Defaults to True.
            - dict (bool, optional): Return the result as a dictionary. Defaults to False.
            - input (dict, optional): The input data for the API method. Defaults to None.

        Returns:
            - Union[rubpy.types.Update, dict]: Result of the API call.
        """
        if not self.connection.api_url:
            await self.connection.get_dcs()

        if self.auth is None:
            self.auth = Crypto.secret(length=32)
            self.logger.info(
                'create auth secret', extra={'data': self.auth})

        if self.key is None:
            self.key = Crypto.passphrase(self.auth)
            self.logger.info(
                'create key passphrase', extra={'data': self.key})

        result = await self.connection.send(method=name,
                                            tmp_session=tmp_session,
                                            encrypt=encrypt,
                                            input=input or {})
        if result is not None:
            data_enc = result.get('data_enc')
            if data_enc is not None:
                result = Crypto.decrypt(data_enc,
                                        key=self.key)

            status = result['status']
            status_det = result['status_det']

            if status == 'OK' and status_det == 'OK':
                if dict:
                    return result.get('data')

                result['data']['_client'] = self
                return Update(result['data'])

            raise exceptions(status_det)(result, request=None)