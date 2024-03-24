import sys
import os

# Add the parent directory of MonoCipher to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can perform relative imports
from MonoCipher.SimpleEncryption import shift_encrypt, shift_decrypt
from MonoCipher.ByteEncryption import byte_encrypt, byte_decrypt
from MonoCipher.SaltEncryption import salt_encrypt, salt_decrypt

def test_shift_cipher():
    message = "Hello, World!"
    shift = 3

    # Test shift encryption and decryption
    encrypted_message = shift_encrypt(message, shift)
    decrypted_message = shift_decrypt(encrypted_message, shift)
    assert decrypted_message == message, "Shift encryption/decryption failed"
    print("Shift cipher test passed.")

def test_byte_cipher():
    message = "Hello, World!"
    password = "MySecretPassword"

    # Test byte encryption and decryption
    iv, ciphertext = byte_encrypt(message, password)
    decrypted_message = byte_decrypt(iv, ciphertext, password)
    assert decrypted_message == message, "Byte encryption/decryption failed"
    print("Byte cipher test passed.")

def test_salt_cipher():
    message = "Hello, World!"
    password = "MySecretPassword"

    # Test salt encryption and decryption
    salt, iv, ciphertext = salt_encrypt(message, password)
    decrypted_message = salt_decrypt(salt, iv, ciphertext, password)
    assert decrypted_message == message, "Salt encryption/decryption failed"
    print("Salt cipher test passed.")


if __name__ == "__main__":
    test_shift_cipher()
    test_byte_cipher()
    test_salt_cipher()