import os
import sys
from cryptography.fernet import Fernet

def load_key_and_encrypted_password(filename):
    with open(filename, "rb") as file:
        key, encrypted_password = file.read().split(b"\n")
    return key, encrypted_password

def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

def main():
    encrypted_passwords_file = "encrypted_password.txt"

    if not os.path.exists(encrypted_passwords_file):
        print("Cannot find encrypted passwords file.")
        sys.exit(1)

    key, encrypted_password = load_key_and_encrypted_password(encrypted_passwords_file)
    decrypted_password = decrypt_password(encrypted_password, key)
    print(f"Decrypted password: {decrypted_password}")

if __name__ == "__main__":
    main()