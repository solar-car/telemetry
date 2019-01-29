from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random


class AuthenticationManager:
    def __init__(self):
        self.auth_file_path = "Data/auth"

    def create_key_pair(self, password):
        pass

    @staticmethod
    def encrypt_private_key(private_key, passphrase):
        salt = Random.get_random_bytes(16)
        nonce = Random.get_random_bytes(16)

        key = PBKDF2(passphrase, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(private_key.encode())

        with open("Data/auth", "wb") as file:
            file.write(salt)
            file.write(nonce)
            file.write(tag)
            file.write(ciphertext)

    @staticmethod
    def decrypt_private_key(passphrase):
        with open("Data/auth", "rb") as file:
            line = file.read()

            # The salt, nonce, and tag are each 16 bytes long
            salt = line[0:16]
            nonce = line[16:32]
            tag = line[32:48]

            ciphertext = line[48:]
            key = PBKDF2(passphrase, salt)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            private_key = cipher.decrypt_and_verify(ciphertext, tag)

        return private_key


class ServerKeyManager:
    def __init__(self):
        pass
