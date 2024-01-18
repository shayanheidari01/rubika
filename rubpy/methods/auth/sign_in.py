import rubpy


class SignIn:
    async def sign_in(self: "rubpy.Client",
                     phone_code: str,
                     phone_number: str,
                     phone_code_hash: str,
                     public_key: str,
    ):
        return await self.builder(name='signIn',
                                 input={
                                     'phone_code': phone_code,
                                     'phone_number': phone_number,
                                     'phone_code_hash': phone_code_hash,
                                     'public_key': public_key,
                                 },
                                 tmp_session=True,)