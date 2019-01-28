from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random


class AuthenticationManager:
    def __init__(self):
        self.auth_file_path = "Data/auth"

    def load_private_key(self, passphrase):
        with open(self.auth_file_path) as auth_file:
            file_data = auth_file.read()

    def create_key_pair(self, password):
        pass

    def encrypt_private_key(self, private_key, passphrase):
        salt = Random.get_random_bytes(16)
        nonce = Random.get_random_bytes(16)

        key = PBKDF2(passphrase, salt)
        print(key)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(private_key.encode())

        newline = b"\n"
        with open("Data/auth", "wb") as file:
            file.write(salt + newline)
            file.write(nonce + newline)
            file.write(ciphertext + newline)
            file.write(tag + newline)

    def decrypt_private_key(self, passphrase):
        with open("Data/auth", "rb") as file:
            data = [x[:-2] for x in file.readlines()]
            data = {"salt": data[0], "nonce": data[1], "ciphertext": data[2], "tag": data[3]}
            key = PBKDF2(passphrase, data["salt"])
            print(key)
            cipher = AES.new(key, AES.MODE_GCM, nonce=data["nonce"])
            plaintext = cipher.decrypt_and_verify(data["ciphertext"], data["tag"])
            print(plaintext)


class ServerKeyManager:
    def __init__(self):
        pass

a = AuthenticationManager()

password = "aaaaaaaaaaaaaaa"
key = "hello"

a.encrypt_private_key(key, password)
a.decrypt_private_key(password)