import re
import json
import base64
import string
import secrets
from json import JSONDecoder
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from string import ascii_lowercase, ascii_uppercase

class Crypto(object):
    AES_IV = b'\x00' * 16

    def decode_auth(auth: str) -> str:
        result_list, digits = [], '0123456789'
        translation_table_lower = str.maketrans(ascii_lowercase, ''.join([chr(((32 - (ord(c) - 97)) % 26) + 97) for c in ascii_lowercase]))
        translation_table_upper = str.maketrans(ascii_uppercase, ''.join([chr(((29 - (ord(c) - 65)) % 26) + 65) for c in ascii_uppercase]))

        for char in auth:
            if char in ascii_lowercase:
                result_list.append(char.translate(translation_table_lower))
            elif char in ascii_uppercase:
                result_list.append(char.translate(translation_table_upper))
            elif char in digits:
                result_list.append(chr(((13 - (ord(char) - 48)) % 10) + 48))
            else:
                result_list.append(char)

        return ''.join(result_list)

    @classmethod
    def passphrase(cls, auth):
        if len(auth) != 32:
            raise ValueError('auth length should be 32 digits')

        result_list = []
        chunks = re.findall(r'\S{8}', auth)
        for character in (chunks[2] + chunks[0] + chunks[3] + chunks[1]):
            result_list.append(chr(((ord(character) - 97 + 9) % 26) + 97))
        return ''.join(result_list)

    @classmethod
    def secret(cls, length):
        return ''.join(secrets.choice(string.ascii_lowercase)
                       for _ in range(length))

    @classmethod
    def decrypt(cls, data, key):
        decoder = JSONDecoder()
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, cls.AES_IV)
        decoded_data = base64.b64decode(data)
        result, _ = decoder.raw_decode(cipher.decrypt(decoded_data).decode('utf-8'))
        return result

    @classmethod
    def encrypt(cls, data, key):
        if not isinstance(data, str):
            data = json.dumps(data, default=lambda x: str(x))
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, cls.AES_IV)
        length = 16 - (len(data) % 16)
        data += chr(length) * length
        return (
            base64.b64encode(cipher.encrypt(data.encode('utf-8')))
            .decode('utf-8')
        )

    def sign(private_key: str, data: str) -> str:
        key = RSA.import_key(private_key.encode('utf-8'))
        signature = pkcs1_15.new(key).sign(
            SHA256.new(data.encode('utf-8')))
        return base64.b64encode(signature).decode('utf-8')

    def create_keys() -> tuple:
        keys = RSA.generate(1024)
        public_key = Crypto.decode_auth(base64.b64encode(keys.publickey().export_key()).decode('utf-8'))
        private_key = keys.export_key().decode('utf-8')
        return public_key, private_key
    
    def decrypt_RSA_OAEP(private_key: str, data: str):
        key = RSA.import_key(private_key.encode('utf-8'))
        return PKCS1_OAEP.new(key).decrypt(base64.b64decode(data)).decode('utf-8')