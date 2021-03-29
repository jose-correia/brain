from jeec_brain.apps.auth.services.encoding_service import PKCS7Encoder
import base64
from Crypto import Random
from Crypto.Cipher import AES
import logging

logger = logging.getLogger(__name__)

class EncryptTokenService(object):

    @classmethod
    def __init__(self, plaintext):
        self.plaintext = plaintext

    def call(self):
        master_key = b'12345678901234561234567890123456'         
        encoder = PKCS7Encoder()
        raw = encoder.encode(self.plaintext)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new( master_key, AES.MODE_CBC, iv )
        encrypted_text = base64.b64encode(iv + cipher.encrypt(str.encode(raw))) 

        return str(encrypted_text, 'utf-8').replace('+','_')