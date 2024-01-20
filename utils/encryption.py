from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode


def derive_key(password, salt:bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # Adjust the number of iterations based on your security requirements
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt(data:str, password:str) -> str:
    salt:bytes = get_random_bytes(16)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv=get_random_bytes(16))
    ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    bts: bytes = salt + cipher.iv + ciphertext
    return bts.hex()

def decrypt(ciphertext:str, password:str):
    data = bytes.fromhex(ciphertext)
    salt = data[:16]
    iv = data[16:32]
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(data[32:]), AES.block_size).decode('utf-8')