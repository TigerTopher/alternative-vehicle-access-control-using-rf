from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64decode
from base64 import b64encode

# AES have variants AES-128, AES-196, and AES-256
# These numbers stand for the bit length of the keys
# Note that all of these variants have its bit length that
# is divisible by 16. The block size is set to be 16.

# To encrypt the message, the length of the message must be a multiple of the length of the key.
# Note that this pads \r so that the  final length would be multiple of the block size
# Sample lambda code:
#   pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
#   unpad = lambda s: s[0:-ord(s[-1])]

# Note that the length of the ciphertext is equivalent to the length of the key


class AESDriver:
    def __init__(self):
        pass

    @staticmethod
    def base64encode(text):
        return b64encode(text)

    @staticmethod
    def base64decode(base64_text):
        return b64decode(base64_text)

    @staticmethod
    def pad(s, block_size=16):
        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)

    @staticmethod
    def unpad(s):
        return s[0:-ord(s[-1])]

    @staticmethod
    def generate_key(byte_length=16):
        return Random.new().read(byte_length)

    @staticmethod
    def encrypt_data(plaintext, key, byte_length, iv=""):
        mode = AES.MODE_CBC
        if iv == "":
            iv = byte_length * '\x00'

        encrypter = AES.new(key, mode, IV=iv)
        if len(plaintext) % 16 == 0:
            # return encrypter.encrypt(plaintext)
            return b64encode(encrypter.encrypt(plaintext))
            # return b64encode(iv + encrypter.encrypt(plaintext))
        return b64encode(encrypter.encrypt(AESDriver.pad(plaintext)))

        # return b64encode(iv + encrypter.encrypt(AESDriver.pad(plaintext)))
        # return encrypter.encrypt(AESDriver.pad(plaintext))

    @staticmethod
    def decrypt_data(ciphertext, key, byte_length, iv=""):
        mode = AES.MODE_CBC
        if iv == "":
            iv = byte_length * '\x00'

        enc = b64decode(ciphertext)
        # iv = enc[:16]

        decrypter = AES.new(key, mode, IV=iv)

        # if len(decrypter.decrypt(enc).decode('utf-8')) % 16 == 0:
        #     print "Padded: ", AESDriver.unpad(decrypter.decrypt(enc).decode('utf-8'))
        #     print AESDriver.unpad(decrypter.decrypt(enc).decode('utf-8')) == decrypter.decrypt(enc).decode('utf-8')
        # else:
        #     print "No padding", decrypter.decrypt(enc).decode('utf-8')

        # if len(plaintext) % 16 == 0:
        #     return AESDriver.unpad(decrypter.decrypt(enc).decode('utf-8'))
        # # return AESDriver.unpad(decrypter.decrypt(ciphertext))
        return decrypter.decrypt(enc).decode('utf-8')
