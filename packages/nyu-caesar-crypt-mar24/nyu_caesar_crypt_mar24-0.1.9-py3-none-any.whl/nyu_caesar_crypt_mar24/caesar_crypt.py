def caesar_encrypt(text, shift):
    """
    Encrypts a given text using the Caesar cipher, extended to include numbers.

    :param text: The input string to encrypt.
    :param shift: The number of positions to shift each character.
    :return: The encrypted string.
    """
    encrypted_text = ""
    
    for char in text:
        if char.isupper():
            encrypted_char = chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            encrypted_char = chr((ord(char) + shift - 97) % 26 + 97)
        elif char.isdigit():
            encrypted_char = chr((ord(char) + shift - 48) % 10 + 48)
        else:
            encrypted_char = char
        encrypted_text += encrypted_char

    return encrypted_text

def caesar_decrypt(text, shift):
    """
    Decrypts a given text using the Caesar cipher, extended to include numbers.

    This function decrypts by applying the inverse of the encryption shift. 
    Given the cyclical nature of the cipher, decrypting is equivalent to encrypting
    with a shift of -shift.

    :param text: The input string to decrypt.
    :param shift: The number of positions the characters were shifted to encrypt.
    :return: The decrypted string.
    """
        
    return caesar_encrypt(text, -shift)


def brute_force_decrypt(encrypted_text):
    """
    Attempts to decrypt an encrypted message by trying all possible shifts.

    :param encrypted_text: The encrypted message to decrypt.
    :return: A dictionary of all possible shifts and their corresponding decrypted messages.
    """
    possible_messages = {}
    for shift in range(26):
        decrypted_text = caesar_decrypt(encrypted_text, shift)
        possible_messages[shift] = decrypted_text
    return possible_messages


def verify_encryption_decryption(original_text, decrypted_text):
    """
    Verifies that the original plaintext matches the decrypted text,
    indicating the encryption and decryption processes are inverses of each other.

    :param original_text: The original plaintext before encryption.
    :param decrypted_text: The text after being encrypted and then decrypted.
    :return: True if the original and decrypted texts match, False otherwise.
    """
    return original_text == decrypted_text
