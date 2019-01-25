from Crypto.PublicKey import RSA
from Crypto.Cipher import AES


class AuthenticationManager:
    def __init__(self):
        self.auth_file_path = "Data/auth"

    def load_private_key(self, password):
        with open(self.auth_file_path) as auth_file:
            file_data = auth_file.read()


    def create_key_pair(self):
        pass


class ServerKeyManager:
    def __init__(self):
        pass