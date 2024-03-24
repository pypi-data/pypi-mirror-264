from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad
import base64

def generate_key(password, salt):
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
    return key

def generate_iv():
    return get_random_bytes(16)

def hmac_encrypt(message, password):
    salt = get_random_bytes(16)
    key = generate_key(password.encode(), salt)
    iv = generate_iv()

    # Pad the message before encryption
    padded_message = pad(message.encode(), AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_message)

    h = HMAC.new(key, digestmod=SHA256)
    h.update(ciphertext)
    hmac_digest = h.digest()

    return base64.b64encode(salt).decode('utf-8'), base64.b64encode(iv).decode('utf-8'), \
           base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(hmac_digest).decode('utf-8')

def hmac_decrypt(salt, iv, ciphertext, hmac_digest, password):
    salt = base64.b64decode(salt)
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)
    hmac_digest = base64.b64decode(hmac_digest)

    key = generate_key(password.encode(), salt)

    h = HMAC.new(key, digestmod=SHA256)
    h.update(ciphertext)
    if hmac_digest != h.digest():
        return "Authentication failed"

    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_message = cipher.decrypt(ciphertext)
        unpadded_message = unpad(decrypted_message, AES.block_size)
        return unpadded_message.decode()
    except Exception as e:
        return f"Decryption failed: {str(e)}"


# Example usage
'''
message = "Hello, World!"
password = "MySecretPassword"

# Encrypt the message
salt, iv, ciphertext, hmac_digest = hmac_encrypt(message, password)
print("Salt:", salt)
print("IV:", iv)
print("Ciphertext:", ciphertext)
print("HMAC Digest:", hmac_digest)

# Decrypt the message
decrypted_message = hmac_decrypt(salt, iv, ciphertext, hmac_digest, password)
print("Decrypted message:", decrypted_message)
'''