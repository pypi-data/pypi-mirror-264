import pytest
from src.nyu_caesar_crypt_mar24.caesar_crypt import caesar_encrypt, caesar_decrypt, brute_force_decrypt, verify_encryption_decryption

def test_caesar_encrypt():
    # Test cases: encrypt function
    print("Testing caesar_encrypt function...")
    # Test, error message (if failure)
    assert caesar_encrypt("hello", 3) == "khoor", "Test case failed: caesar_encrypt('hello', 3)"
    assert caesar_encrypt("abcXYZ", 5) == "fghCDE", "Test case failed: caesar_encrypt('abcXYZ', 5)"
    assert caesar_encrypt("123", 3) == "456", "Test case failed: caesar_encrypt('123', 3)"
    assert caesar_encrypt("$%Hello, World!", 18) == "$%Zwddg, Ogjdv!", "Test case failed: caesar_encrypt('$%Hello, World!', 18)"
    print("All caesar_encrypt tests passed.")

def test_caesar_decrypt():
    # Test cases: decrypt function
    print("Testing caesar_decrypt function...")
    assert caesar_decrypt("khoor", 3) == "hello", "Test case failed: caesar_decrypt('khoor', 3)"
    assert caesar_decrypt("fghCDE", 5) == "abcXYZ", "Test case failed: caesar_decrypt('fghCDE', 5)"
    assert caesar_decrypt("456", 3) == "123", "Test case failed: caesar_decrypt('456', 3)"
    assert caesar_decrypt("$%Zwddg, Ogjdv!", 18) == "$%Hello, World!", "Test case failed: caesar_decrypt('$%Zwddg, Ogjdv!', 18)"
    print("All caesar_decrypt tests passed.")

def test_brute_force_decrypt():
    # Test cases: brute force decryption
    print("Testing brute_force_decrypt function...")
    encrypted_text = caesar_encrypt("hello", 3)
    decrypted_messages = brute_force_decrypt(encrypted_text)
    assert "hello" in decrypted_messages.values(), "Test case failed: brute_force_decrypt('hello', 3)"
    print("All brute_force_decrypt tests passed.")

def test_verify_crypt():
    # Test cases: crypt verification
    print("Testing verify_crypt function...")
    encrypted_text = caesar_encrypt("hello", 3)
    decrypted_text = caesar_decrypt(encrypted_text, 3)
    assert verify_encryption_decryption("hello", decrypted_text) is True, "Test case failed: verify_encryption_decryption('hello', decrypted_text)"
    assert verify_encryption_decryption("hello", "world") is False, "Test case failed: verify_encryption_decryption('hello', 'world')"
    print("All verify_crypt tests passed.")


# Main for testing
if __name__ == "__main__":
    test_caesar_encrypt()
    test_caesar_decrypt()
    test_brute_force_decrypt()
    test_verify_crypt()
