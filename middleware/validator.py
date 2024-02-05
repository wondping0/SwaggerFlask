import re

def is_strong_password(password):
    """
    Check if a password is strong according to the following criteria:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character (e.g., !@#$%^&*)

    :param password: The password to be checked
    :return: True if the password is strong, False otherwise
    """
    # Check length
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check for at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # Check for at least one special character
    special_characters = r"[@#$%^&*()_+{}\[\]:;<>,.?/~`'\"!-]"
    if not re.search(special_characters, password):
        return False

    # If all checks pass, the password is strong
    return True

def is_valid_email(email):
    """
    Check if an email address is valid according to a basic pattern.

    :param email: The email address to be checked
    :return: True if the email is valid, False otherwise
    """
    # Basic email pattern validation using a regular expression
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_pattern, email):
        return True
    else:
        return False

