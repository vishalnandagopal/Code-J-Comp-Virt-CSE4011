from datetime import date, datetime
from os import getenv, path, listdir, makedirs

import rsa
from cryptography.fernet import Fernet


class CommonEncryption:
    def encrypt(self):
        ...

    def decrypt(self):
        ...

    def encrypt_int(self, num: int):
        return self.encrypt(str(num))

    def decrypt_int(self, message: str):
        return int(self.decrypt(message))

    def encrypt_date(self, date_message: date):
        return self.encrypt(str(date))

    def decrypt_date(self, date_encrypted: str):
        print(self.decrypt(date_encrypted))
        return datetime.strptime(self.decrypt(date_encrypted), "%Y-%m-%d")


class Assymetric(CommonEncryption):
    def __init__(self):
        self.publicKey, self.privateKey = rsa.newkeys(512)

    def encrypt(self, message: str):
        return rsa.encrypt(str(message).encode(), self.publicKey)

    def decrypt(self, message: str):
        return rsa.decrypt(message, self.privateKey).decode()


class Symmetric(CommonEncryption):
    def __init__(self):
        self.key = Symmetric.get_key()
        print("Key is " + str(self.key))
        self.fernet = Fernet(self.key)

    def get_key():
        try:
            if "password.log" in listdir(path.dirname(__file__) + "/log"):
                with open("./log/password.log", "rb") as f:
                    key = f.read()
                    return key
        except FileNotFoundError:
            print(
                "Log file or log folder doesn't seem to exist so will be creating a new key"
            )

        key = Fernet.generate_key()

        password_log_file_name = path.dirname(__file__) + "/log/password.log"
    
        makedirs(path.dirname(password_log_file_name), exist_ok=True)

        with open(password_log_file_name, "w+") as f:
            f.write(str(key).strip("b").strip("'"))

        return key

    def encrypt(self, message: str):
        return self.fernet.encrypt(str(message).encode())

    def decrypt(self, encrypted_message: str):
        return self.fernet.decrypt(encrypted_message).decode()


def get_encryptor():
    if getenv("LIBRARY") not in ("rsa", "cryptography"):
        enc_class = Symmetric()
    elif getenv("LIBRARY") == "cryptography":
        enc_class = Symmetric()
    else:
        enc_class = Assymetric()
    return enc_class


if __name__ == "__main__":
    """
    TESTS
    """
    from random import randint

    encryptor = get_encryptor()
    test = "vishal"
    if test == encryptor.decrypt(encryptor.encrypt(test)):
        print(True)

    random_int = randint(1, 2314124)
    if random_int == encryptor.decrypt_int(encryptor.encrypt_int(random_int)):
        print(True)
