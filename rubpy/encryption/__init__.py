from Crypto.Cipher.AES import new
from Crypto.Util.Padding import unpad, pad
from pybase64 import b64decode, b64encode


class Encryption(object):
    def __init__(self, auth):
        if len(auth) != 32 and not auth.isalpha():
            raise ValueError('Your AUTH ID is incorrect, please check and try again.')
        self.key = bytearray(self.secret(auth), 'utf-8')
        self.iv = bytearray.fromhex('0' * 32)

    def secret(self, e):
        return ''.join(chr(((ord(cha) - 97 + 9) % 26) + 97) for cha in e[16:24] + e[0:8] + e[24:32] + e[8:16])

    def encrypt(self, text):
        return b64encode(new(self.key, 2, self.iv).encrypt(pad(text.encode(), 16))).decode()

    def decrypt(self, text):
        return unpad(new(self.key, 2, self.iv).decrypt(b64decode(text.encode())), 16).decode()