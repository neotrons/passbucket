import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCrypt(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        if raw != '' and raw is not None:
            raw = self._pad(raw)
            iv = Random.new().read(AES.block_size)
            crypt = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + crypt.encrypt(raw.encode())).decode("ascii")
        else:
            return ''

    def decrypt(self, enc):
        if enc != '' and enc is not None:
            enc = base64.b64decode(enc.encode("ascii"))
            iv = enc[:AES.block_size]
            crypt = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(crypt.decrypt(enc[AES.block_size:])).decode('utf-8')
        return ''

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
