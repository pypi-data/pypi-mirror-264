import re

def validate_number(number):
    """
    Validate mobile phone number.

    Parameters:
    number (str): Mobile phone number to validate.

    Returns:
    bool: True if the number is valid, False otherwise.
    """
    # Regular expression for a valid mobile phone number
    pattern = re.compile(r'^(\+\d{1,3}[- ]?)?\d{10}$')

    # Check if the number matches the pattern
    if pattern.match(number):
        return True
    else:
        return False