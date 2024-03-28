from nyu_caesar_crypt_mar24 import caesar_crypt as caesar

def main():
    print("Welcome to the Caesar Cipher Tool!")

    # Ask the user what they want to do
    mode = input("Do you want to (e)ncrypt, (d)ecrypt, or (b)rute-force a message? ").lower()
    if mode.startswith('e'):
        operation = "encrypt"
    elif mode.startswith('d'):
        operation = "decrypt"
    elif mode.startswith('b'):
        operation = "brute-force"
    else:
        print("Invalid option selected. Exiting.")
        return

    text = input(f"Enter the text to {operation}: ")

    if operation in ["encrypt", "decrypt"]:
        # User input for the shift amount with error handling for encrypt/decrypt
        while True:
            shift_input = input("Enter the shift amount (a number): ")
            try:
                shift = int(shift_input)
                break
            except ValueError:
                print("Please enter a valid number for the shift amount.")

        if operation == "encrypt":
            result_text = caesar.caesar_encrypt(text, shift)
        else:  # operation == "decrypt"
            result_text = caesar.caesar_decrypt(text, shift)

        # Display the result
        print(f"Result ({operation}ed text): {result_text}")

    elif operation == "brute-force":
        # Brute-force operation, assuming brute_force_decrypt function is implemented in caesar_crypt
        print("Attempting to brute-force the encrypted message...")
        possible_decryptions = caesar.brute_force_decrypt(text)
        for shift, decryption in possible_decryptions.items():
            print(f"Shift {shift}: {decryption}")

if __name__ == "__main__":
    main()
