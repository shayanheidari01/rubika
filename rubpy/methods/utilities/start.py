from ... import exceptions
from ...crypto import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import asyncio
import rubpy


class Start:
    async def start(self: "rubpy.Client", phone_number: str = None):
        if self.display_welcome:
            for char in rubpy.__welcome__:
                print(char, sep='', end='', flush=True)
                await asyncio.sleep(0.01)

        if not hasattr(self, 'connection'):
            await self.connect()

        try:
            self.decode_auth = Crypto.decode_auth(self.auth) if self.auth is not None else None
            self.import_key = pkcs1_15.new(RSA.import_key(self.private_key.encode())) if self.private_key is not None else None
            result = await self.get_me()
            self.guid = result.user.user_guid
            self.logger.info('user', extra={'guid': result})

        except exceptions.NotRegistered:
            self.logger.debug('user not registered!')
            if phone_number is None:
                phone_number = input('Phone Number: ')
                is_phone_number_true = True
                while is_phone_number_true:
                    if input(f'Is the {phone_number} correct[y or n] > ').lower() == 'y':
                        is_phone_number_true = False
                    else:
                        phone_number = input('Phone Number: ')

            if phone_number.startswith('0'):
                phone_number = '98{}'.format(phone_number[1:])
            elif phone_number.startswith('+98'):
                phone_number = phone_number[1:]
            elif phone_number.startswith('0098'):
                phone_number = phone_number[2:]

            result = await self.send_code(phone_number=phone_number)

            if result.status == 'SendPassKey':
                while True:
                    pass_key = input(f'Password [{result.hint_pass_key}] > ')
                    result = await self.send_code(phone_number=phone_number, pass_key=pass_key)

                    if result.status == 'OK':
                        break

            public_key, self.private_key = Crypto.create_keys()
            while True:
                phone_code = input('Code: ')

                result = await self.sign_in(
                    phone_code=phone_code,
                    phone_number=phone_number,
                    phone_code_hash=result.phone_code_hash,
                    public_key=public_key)

                if result.status == 'OK':
                    result.auth = Crypto.decrypt_RSA_OAEP(self.private_key, result.auth)
                    self.key = Crypto.passphrase(result.auth)
                    self.auth = result.auth
                    self.decode_auth = Crypto.decode_auth(self.auth)
                    self.import_key = pkcs1_15.new(RSA.import_key(self.private_key.encode())) if self.private_key is not None else None
                    self.session.insert(
                        auth=self.auth,
                        guid=result.user.user_guid,
                        user_agent=self.user_agent,
                        phone_number=result.user.phone,
                        private_key=self.private_key)

                    await self.register_device()
                    break

        return self