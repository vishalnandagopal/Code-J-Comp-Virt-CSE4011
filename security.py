from datetime import date, datetime
from os import getenv
from time import ctime

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
        return rsa.encrypt(message.encode(), self.publicKey)

    def decrypt(self, message: str):
        return rsa.decrypt(message, self.privateKey).decode()


class Symmetric(CommonEncryption):
    def __init__(self):
        self.key = Fernet.generate_key()
        with open("password.log", "a") as f:
            f.write(f"Password generated at {ctime()} is {self.key}\n")
        self.fernet = Fernet(self.key)

    def encrypt(self, message: str):
        return self.fernet.encrypt(message.encode())

    def decrypt(self, encrypted_message: str):
        return self.fernet.decrypt(encrypted_message).decode()


if getenv("LIBRARY") not in ("rsa", "cryptography"):
    enc_class = Symmetric()
elif getenv("LIBRARY") == "cryptography":
    enc_class = Symmetric()
else:
    enc_class = Assymetric()

if __name__ == "__main__":
    """
    TESTS
    """
    from datetime import date as d
    from random import randint

    test = "vishal"
    if test == enc_class.decrypt(enc_class.encrypt(test)):
        print(True)

    random_int = randint(1, 2314124)
    if random_int == enc_class.decrypt_int(enc_class.encrypt_int(random_int)):
        print(True)

    random_date = d.today()
    if random_date == enc_class.decrypt_date(enc_class.encrypt_date(random_date)):
        print(True)
