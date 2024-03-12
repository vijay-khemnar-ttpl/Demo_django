import random
import string


def make_random_password(length=12):
    SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}|;:'<>,.?/"

    """Generates a random password that meets the following conditions:
    * Minimum 8 characters long
    * At least one lowercase character
    * At least one uppercase character
    * At least one number
    * At least one special character from the following set: !@#$%^&*()-_=+[]{}|;:'<>,.?/

    Args:
        length: The length of the password to generate.

    Returns:
        A random password string.
    """

    characters = string.ascii_letters + string.digits + SPECIAL_CHARACTERS
    password = ""
    while len(password) < length or not any(c in SPECIAL_CHARACTERS for c in password):
        character = random.choice(characters)
        password += character

    if not any(c.islower() for c in password):
        password += random.choice(string.ascii_lowercase)
    if not any(c.isupper() for c in password):
        password += random.choice(string.ascii_uppercase)
    if not any(c.isdigit() for c in password):
        password += random.choice(string.digits)

    return password
