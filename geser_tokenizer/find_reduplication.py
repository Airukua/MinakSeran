import re
from typing import List

def extract_reduplications(text: str) -> List[str]:
    """
    Extracts reduplicated words (e.g., 'abi-abis', 'ancang-ancang') from the input text.

    A reduplicated word is defined here as two identical word-like parts
    joined by a hyphen. Each part must consist of alphanumeric characters
    or underscores.

    Args:
        text (str): The input string to search for reduplicated words.

    Returns:
        List[str]: A list of the matched reduplicated words.
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")

    # Updated pattern: (\w+) captures a word part, and \1 ensures the second part is identical.
    pattern = r'(\b\w+)-\1\b'
    # \b is a word boundary, ensuring we match whole words and not parts of larger words.
    return re.findall(pattern, text)