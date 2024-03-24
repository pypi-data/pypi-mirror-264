from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import base64

class MacEncryption:
    def __init__(self, password):
        self.password = password
        self.salt = get_random_bytes(16)
        self.master_key = self.derive_master_key()

    def derive_master_key(self):
        return scrypt(self.password.encode(), self.salt, key_len=32, N=2**20, r=8, p=1)

    def generate_nonce(self):
        return get_random_bytes(12)

    def mac_encrypt(self, message):
        nonce = self.generate_nonce()
        cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)

        ciphertext, tag = cipher.encrypt_and_digest(message.encode())

        return base64.b64encode(self.salt).decode('utf-8'), base64.b64encode(nonce).decode('utf-8'), \
               base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(tag).decode('utf-8')

    def mac_decrypt(self, salt, nonce, ciphertext, tag):
        salt = base64.b64decode(salt)
        nonce = base64.b64decode(nonce)
        ciphertext = base64.b64decode(ciphertext)
        tag = base64.b64decode(tag)

        cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)

        try:
            decrypted_message = cipher.decrypt_and_verify(ciphertext, tag).decode()
            return decrypted_message
        except ValueError:
            return "Decryption failed: MAC check failed"

# Example usage:
'''
password = "MySecretPassword"
message = "Hello, World!"

strong_tag_encryption = TagEncryption(password)

# Encryption
salt, nonce, ciphertext, tag = strong_tag_encryption.encrypt(message)
print("Salt:", salt)
print("Nonce:", nonce)
print("Ciphertext:", ciphertext)
print("Tag:", tag)

# Decryption
decrypted_message = strong_tag_encryption.decrypt(salt, nonce, ciphertext, tag)
print("Decrypted message:", decrypted_message)
'''