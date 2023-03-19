import string
import random
import secrets
import webbrowser
import os
import json
from cryptography.fernet import Fernet

def get_character_set():
    char_set = ""
    while not char_set:
        user_input = input("Would you like letters, numbers, special characters, or a combination of them? (letters/numbers/special/combination): ").lower()
        if user_input == "letters":
            char_set = string.ascii_letters
        elif user_input == "numbers":
            char_set = string.digits
        elif user_input == "special":
            char_set = string.punctuation
        elif user_input == "combination":
            char_set = string.ascii_letters + string.digits + string.punctuation
        else:
            print("Invalid input. Please try again.")
    return char_set

def get_password_length():
    while True:
        try:
            length = int(input("Choose the length of your password (between 3 and 20 characters): "))
            if 3 <= length <= 20:
                return length
            else:
                print("Invalid input. Please choose a number between 3 and 20.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_randomness_level():
    while True:
        level = input("How random would you like the password to be? (less_random/mix/more_random): ").lower()
        if level in ["less_random", "mix", "more_random"]:
            return level
        else:
            print("Invalid input. Please try again.")

def generate_password(char_set, length, randomness_level):
    if randomness_level == "less_random":
        return "".join(random.choices(char_set, k=length))
    elif randomness_level == "mix":
        return "".join(random.sample(char_set, k=length) if len(char_set) >= length else random.choices(char_set, k=length))
    else:  # more_random
        return "".join(secrets.choice(char_set) for _ in range(length))

def password_strength_indicator(password):
    # Implement a simple password strength indicator (you can improve this further)
    if len(password) >= 10 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password) and any(c in string.punctuation for c in password):
        return "Strong"
    else:
        return "Weak"

def encrypt_password(password, master_password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password, key

def save_password(encrypted_password, key, filename):
    with open(filename, "wb") as f:
        f.write(key + b"\n" + encrypted_password)

def load_password(filename, master_password):
    with open(filename, "rb") as f:
        key, encrypted_password = f.read().split(b"\n")
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_password

def save_preset(preset, filename):
    with open(filename, "w") as f:
        json.dump(preset, f)

def load_preset(filename):
    with open(filename, "r") as f:
        preset = json.load(f)
    return preset

def main():
    char_set = get_character_set()
    length = get_password_length()
    randomness_level = get_randomness_level()
    password = generate_password(char_set, length, randomness_level)
    strength = password_strength_indicator(password)
    print(f"Generated password: {password}")
    print(f"Password strength: {strength}")

    # Open the password in the default browser
    with open("password.html", "w") as f:
        f.write(f"<html><body><h1>Generated Password:</h1><h2>{password}</h2></body></html>")
    webbrowser.open("password.html")

    # Save and load encrypted password example
    master_password = input("Please enter a master password to encrypt and save the generated password: ")
    encrypted_password, key = encrypt_password(password, master_password)
    save_password(encrypted_password, key, "encrypted_password.txt")
    print("Encrypted password saved.")

    loaded_password = load_password("encrypted_password.txt", master_password)
    print(f"Loaded password: {loaded_password}")

    # Save and load password generation preset example
    preset = {
        "char_set": char_set,
        "length": length,
        "randomness_level": randomness_level,
    }
    save_preset(preset, "preset.json")
    print("Preset saved.")

    loaded_preset = load_preset("preset.json")
    print(f"Loaded preset: {loaded_preset}")

if __name__ == "__main__":
    main()
