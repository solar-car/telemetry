import os.path

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random


class AuthenticationManager:
    def __init__(self, state_handler):
        self.private_key_path = "Data/auth"
        self.public_key_path = "Data.public.key"

        self.state_handler = state_handler

    def check_for_existing_keys(self):
        if os.path.exists(self.private_key_path):
            return True
        else:
            return False

    def create_rsa_key_pair(self, passphrase):
        key = RSA.generate(2048)
        with open(self.private_key_path, "wb") as file:
            file.write(key.export_key("DER", passphrase=passphrase))

        with open(self.public_key_path, "wb") as file:
            file.write(key.publickey().export_key())

    def aes_encrypt_data(self, data, passphrase):
        salt = Random.get_random_bytes(16)
        nonce = Random.get_random_bytes(16)

        key = PBKDF2(passphrase, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)  # Using GCM authentication mode
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())

        with open("Data/aes", "wb") as file:
            file.write(salt)
            file.write(nonce)
            file.write(tag)
            file.write(ciphertext)

    def aes_decrypt_data(self, passphrase):
        with open("Data/aes", "rb") as file:
            line = file.read()

            # The salt, nonce, and tag are each 16 bytes long
            salt = line[0:16]
            nonce = line[16:32]
            tag = line[32:48]

            ciphertext = line[48:]
            key = PBKDF2(passphrase, salt)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        return plaintext


class ServerKeyManager:
    def __init__(self):
        pass