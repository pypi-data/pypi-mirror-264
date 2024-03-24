from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20_Poly1305
import base64

def generate_key(password, salt):
    """
    Generates a key using the Argon2 key derivation function.

    Args:
        password (bytes): The password.
        salt (bytes): The salt.

    Returns:
        bytes: The generated key.
    """
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
    return key

def nonce_encrypt(message, password):
    """
    Encrypts the message using a salt and password.

    Args:
        message (str): The message to be encrypted.
        password (str): The password.

    Returns:
        tuple: A tuple containing the salt, nonce, and ciphertext.
    """
    salt = get_random_bytes(16)
    key = generate_key(password.encode(), salt)
    nonce = get_random_bytes(12)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(salt).decode('utf-8'), base64.b64encode(nonce).decode('utf-8'), base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(tag).decode('utf-8')

def nonce_decrypt(salt, nonce, ciphertext, tag, password):
    """
    Decrypts the ciphertext using the salt, nonce, and password.

    Args:
        salt (str): The base64-encoded salt.
        nonce (str): The base64-encoded nonce.
        ciphertext (str): The base64-encoded ciphertext.
        tag (str): The base64-encoded tag.
        password (str): The password.

    Returns:
        str: The decrypted message.
    """
    salt = base64.b64decode(salt)
    nonce = base64.b64decode(nonce)
    ciphertext = base64.b64decode(ciphertext)
    tag = base64.b64decode(tag)
    key = generate_key(password.encode(), salt)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    try:
        decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_message.decode()
    except ValueError:
        return "Decryption failed"

# Example usage:
'''
message = "Hello, World!"
password = "MySecretPassword"

salt, nonce, ciphertext, tag = nonce_encrypt(message, password)
print("Salt:", salt)
print("Nonce:", nonce)
print("Ciphertext:", ciphertext)
print("Tag:", tag)

decrypted_message = nonce_decrypt(salt, nonce, ciphertext, tag, password)
print("Decrypted message:", decrypted_message)
'''