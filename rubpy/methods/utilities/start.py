from ... import exceptions
from ...crypto import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import rubpy
import re

def convert_farsi_digits(text):
    return text.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))

def normalize_phone_number(phone: str) -> str:
    phone = convert_farsi_digits(phone)
    phone = phone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    # پترن کامل: تشخیص شماره داخلی و بین‌المللی (تا ۱۵ رقم طبق استاندارد ITU-T E.164)
    pattern = re.compile(r"^(?:\+|00)?(\d{7,15})$")

    match = pattern.match(phone)
    if match:
        return match.group(1) if phone.startswith("00") else f"{match.group(1)}"
    return None

class Start:
    async def start(self: "rubpy.Client", phone_number: str = None):
        """
        Start the RubPy client, handling user registration if necessary.

        Args:
        - phone_number (str): The phone number to use for starting the client.

        Returns:
        - The initialized client.
        """
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

            phone_number = normalize_phone_number(phone_number)
            phone_number = f'98{phone_number[1:]}' if phone_number.startswith('0') else phone_number
            result = await self.send_code(phone_number=phone_number, send_type='SMS')

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

                    await self.register_device(device_model=self.name)
                    break

        return self