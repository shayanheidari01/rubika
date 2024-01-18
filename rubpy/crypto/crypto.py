import re
import json
import base64
import string
import secrets
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from string import ascii_lowercase, ascii_uppercase

class Crypto:
    AES_IV = b'\x00' * 16

    @staticmethod
    def decode_auth(auth: str) -> str:
        """
        Decode an auth string by applying character substitutions.

        Args:
            auth (str): The input auth string.

        Returns:
            str: The decoded auth string.
        """
        result_list, digits = [], '0123456789'
        translation_table_lower = str.maketrans(
            ascii_lowercase,
            ''.join([chr(((32 - (ord(c) - 97)) % 26) + 97) for c in ascii_lowercase])
        )
        translation_table_upper = str.maketrans(
            ascii_uppercase,
            ''.join([chr(((29 - (ord(c) - 65)) % 26) + 65) for c in ascii_uppercase])
        )

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
        """
        Generate a passphrase from an auth string.

        Args:
            auth (str): The input auth string.

        Returns:
            str: The generated passphrase.
        """
        if len(auth) != 32:
            raise ValueError('auth length should be 32 digits')

        result_list = []
        chunks = re.findall(r'\S{8}', auth)
        for character in (chunks[2] + chunks[0] + chunks[3] + chunks[1]):
            result_list.append(chr(((ord(character) - 97 + 9) % 26) + 97))
        return ''.join(result_list)

    @classmethod
    def secret(cls, length):
        """
        Generate a random secret of the given length.

        Args:
            length (int): Length of the secret.

        Returns:
            str: The generated secret.
        """
        return ''.join(secrets.choice(string.ascii_lowercase)
                       for _ in range(length))

    @classmethod
    def decrypt(cls, data, key):
        """
        Decrypt data using AES encryption.

        Args:
            data (str): The encrypted data.
            key (str): The encryption key.

        Returns:
            dict: The decrypted data as a dictionary.
        """
        aes = AES.new(key.encode(), AES.MODE_CBC, cls.AES_IV)
        dec = aes.decrypt(base64.urlsafe_b64decode(data.encode('UTF-8')))
        return json.loads(unpad(dec, AES.block_size).decode('UTF-8'))

    @classmethod
    def encrypt(cls, data: str, key: str):
        """
        Encrypt data using AES encryption.

        Args:
            data (str or dict): The data to be encrypted.
            key (str): The encryption key.

        Returns:
            str: The encrypted data as a string.
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        raw = pad(data.encode('UTF-8'), AES.block_size)
        aes = AES.new(key.encode(), AES.MODE_CBC, cls.AES_IV)
        return base64.b64encode(aes.encrypt(raw)).decode('UTF-8')

    @staticmethod
    def sign(pkcs1_15: "pkcs1_15.new", data: str) -> str:
        """
        Sign data using an RSA private key.

        Args:
            private_key (str): The RSA private key.
            data (str): The data to be signed.

        Returns:
            str: The base64-encoded signature.
        """
        #key = RSA.import_key(private_key.encode('utf-8'))
        signature = pkcs1_15.sign(SHA256.new(data.encode('utf-8')))
        return base64.b64encode(signature).decode('utf-8')

    @staticmethod
    def create_keys() -> tuple:
        """
        Generate RSA public and private keys.

        Returns:
            tuple: A tuple containing the base64-encoded public key and the private key.
        """
        keys = RSA.generate(1024)
        public_key = Crypto.decode_auth(base64.b64encode(keys.publickey().export_key()).decode('utf-8'))
        private_key = keys.export_key().decode('utf-8')
        return public_key, private_key

    @staticmethod
    def decrypt_RSA_OAEP(private_key: str, data: str):
        """
        Decrypt data using RSA OAEP encryption.

        Args:
            private_key (str): The RSA private key.
            data (str): The encrypted data.

        Returns:
            str: The decrypted data as a string.
        """
        key = RSA.import_key(private_key.encode('utf-8'))
        return PKCS1_OAEP.new(key).decrypt(base64.b64decode(data)).decode('utf-8')