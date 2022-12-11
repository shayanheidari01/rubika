from Crypto.Util.Padding import pad, unpad
from pybase64 import b64encode, b64decode
from Crypto.Cipher.AES import new


__all__ = ('Crypto')


class Crypto:
    __slots__ = ('key', 'iv',)

    def __init__(self, key):
        if len(key) != 32 and not key.isalpha():
            raise ValueError('Your AUTH is incorrect, please check and try again')
        else:
            self.key = bytearray(self.secret(key), 'UTF-8')
            self.iv = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def secret(self, key):
        return ''.join(chr(((ord(cha) - 97 + 9) % 26) + 97) for cha in key[16:24] + key[0:8] + key[24:32] + key[8:16])

    def decrypt(self, text):
        return unpad(
            new(
                self.key, 2, self.iv
                ).decrypt(
                    b64decode(text.encode('UTF-8')
                )),
                16
            ).decode('UTF-8')

    def encrypt(self, text):
        return b64encode(new(self.key, 2, self.iv).encrypt(pad(text.encode('UTF-8'), 16))).decode('UTF-8')