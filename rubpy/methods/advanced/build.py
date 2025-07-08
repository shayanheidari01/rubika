from ...crypto import Crypto
from ... import exceptions
from ...types import Updates
from typing import Union
import rubpy

class Builder:
    async def builder(
        self: "rubpy.Client",
        name: str,
        tmp_session: bool = False,
        encrypt: bool = True,
        dict: bool = False,
        input: dict = None, *args, **kwargs,
    ) -> Union[Updates, dict]:
        """
        Build and send a request to the Rubika API.

        Args:
            name (str): The API method name.
            tmp_session (bool, optional): Whether to use a temporary session. Defaults to False.
            encrypt (bool, optional): Whether to encrypt the data. Defaults to True.
            dict_output (bool, optional): Return the result as a dictionary. Defaults to False.
            input_data (dict, optional): The input data for the API method. Defaults to None.

        Returns:
            Union[Results, dict]: Result of the API call.
        """
        # Ensure the API URL is set
        if not self.connection.api_url:
            await self.connection.get_dcs()

        # Generate authentication secret if not available
        if self.auth is None:
            self.auth = Crypto.secret(length=32)

        # Generate key passphrase if not available
        if self.key is None:
            self.key = Crypto.passphrase(self.auth)

        # Send the request to the Rubika API
        result = await self.connection.send(
            method=name,
            tmp_session=tmp_session,
            encrypt=encrypt,
            input=input
        )

        if result:
            # Decrypt data if encryption is used
            data_enc = result.get('data_enc')
            if data_enc:
                result = Crypto.decrypt(data_enc, key=self.key)

            # Extract status details
            status = result['status']
            status_det = result['status_det']

            if status == 'OK':
                if dict:
                    return result.get('data')

                # Attach the RubPy client instance to the result data
                result['data']['client'] = self
                return Updates(result['data'])

            # Raise an exception based on the status details
            raise exceptions(status_det)(result, request=None)
