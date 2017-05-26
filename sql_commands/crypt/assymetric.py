from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random


class RSADriver:
    def __init__(self):
        pass

    @staticmethod
    def generate_keys(key_length=4096):
        random_generator = Random.new().read

        keys = RSA.generate(key_length, random_generator)
        return keys

    @staticmethod
    def get_public_key(keys, encoding="PEM"):
        if encoding not in ["PEM", "DER"]:
            print "Invalid encoding type"
            return 0

        return keys.publickey().exportKey(encoding)

    @staticmethod
    def get_private_key(keys, encoding="PEM"):
        if encoding not in ["PEM", "DER"]:
            print "Invalid encoding type"
            return 0

        return keys.exportKey(encoding)

    @staticmethod
    def encrypt_data(message, keys, random_param = None):
        return keys.publickey().encrypt(message, random_param)

    @staticmethod
    def decrypt_data(cipher_text, keys):
        return keys.decrypt(cipher_text)

    @staticmethod
    def sign_message(message, keys):
        hashed_message = SHA256.new(message).digest()
        signature = keys.sign(hashed_message, '')
        return signature

    @staticmethod
    def verify_message(message, signature, keys):
        hashed_message = SHA256.new(message).digest()
        return keys.publickey().verify(hashed_message, signature)