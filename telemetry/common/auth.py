import os.path

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random

# Reminder: I am not a cryptographer and can't guarantee any of these implementations are 100% secure. Their intended
# purpose is mostly to add an extra barrier to prevent random unauthorized connections to the server, and not to
# handle sensitive information. Also, keep in mind I mostly did this part for fun, not out of any real need.


class Authentication:
    # Convenience wrapper around the os.path.exists() function
    @staticmethod
    def check_for_existing_keys(path):
        if os.path.exists(path):
            return True
        else:
            return False

    # Generate an RSA public and private key pair using a passphrase
    @staticmethod
    def create_rsa_key_pair(path, passphrase):
        key = RSA.generate(2048)
        with open(path, "wb") as file:
            file.write(key.export_key("DER", passphrase=passphrase))  # "DER" parameter = save as bytes

        with open(path, "wb") as file:
            file.write(key.publickey().export_key())

    @staticmethod
    def aes_encrypt_data(path, data, passphrase):
        salt = Random.get_random_bytes(16)
        nonce = Random.get_random_bytes(16)

        # Convert the passphrase of arbitrary length into a 16-byte RSA key
        key = PBKDF2(passphrase, salt)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)  # Using GCM authentication mode
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())

        # Write the salt, nonce, tag, and ciphertext to provided file path as a single bytestring
        with open(path, "wb") as file:
            file.write(salt)
            file.write(nonce)
            file.write(tag)
            file.write(ciphertext)

    @staticmethod
    def aes_decrypt_data(path, passphrase):
        with open(path, "rb") as file:
            line = file.read()

            # The salt, nonce, and tag are each 16 bytes long
            salt = line[0:16]
            nonce = line[16:32]
            tag = line[32:48]
            # The rest of the bytestring is the actual encrypted data
            ciphertext = line[48:]

            key = PBKDF2(passphrase, salt)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        return plaintext

    @staticmethod
    def convert_to_salted_hash(passphrase):
        salt = Random.get_random_bytes(16)
        return salt, PBKDF2(passphrase, salt)


class Credentials:
    def __init__(self, salt, salted_hash):
        self.salt = salt
        self.salted_hash = salted_hash
