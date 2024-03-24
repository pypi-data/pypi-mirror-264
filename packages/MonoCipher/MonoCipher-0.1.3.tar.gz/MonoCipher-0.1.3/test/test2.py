import sys
import os

# Add the parent directory of MonoCipher to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can perform relative imports
from MonoCipher.HmacEncryption import hmac_encrypt, hmac_decrypt
from MonoCipher.NonceEncryption import nonce_encrypt, nonce_decrypt
from MonoCipher.MacEncryption import MacEncryption

def test_hmac_cipher():
    message = "Hello, World!"
    password = "MySecretPassword"

    # Test HMAC encryption and decryption
    salt, iv, ciphertext, hmac_digest = hmac_encrypt(message, password)
    decrypted_message = hmac_decrypt(salt, iv, ciphertext, hmac_digest, password)
    assert decrypted_message == message, "HMAC encryption/decryption failed"
    print("HMAC cipher test passed.")

def test_nonce_cipher():
    message = "Hello, World!"
    password = "MySecretPassword"

    # Test nonce encryption and decryption
    salt, nonce, ciphertext, tag = nonce_encrypt(message, password)
    decrypted_message = nonce_decrypt(salt, nonce, ciphertext, tag, password)
    assert decrypted_message == message, "Nonce encryption/decryption failed"
    print("Nonce cipher test passed.")

def test_mac_cipher():
    # Initialize MacEncryption instance with a password
    password = "MySecretPassword"
    mac_encryption = MacEncryption(password)

    # Test MAC encryption and decryption
    message = "Hello, World!"
    salt, nonce, ciphertext, tag = mac_encryption.mac_encrypt(message)
    decrypted_message = mac_encryption.mac_decrypt(salt, nonce, ciphertext, tag)
    
    assert decrypted_message == message, "MAC encryption/decryption failed"
    print("MAC cipher test passed.")

if __name__ == "__main__":
    test_hmac_cipher()
    test_nonce_cipher()
    test_mac_cipher()
