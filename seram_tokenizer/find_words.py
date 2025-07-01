# Part of this code inspired by https://github.com/OpenNMT/Tokenizer/blob/master/bindings/python/README.md
import os
from typing import List, Set
import pkg_resources

# Load the dictionary words into a set for efficient O(1) average time complexity lookups.
# This ensures that checking if a word exists in the dictionary is very fast.
DICTIONARY_FILE_PATH = pkg_resources.resource_filename(__name__, 'data/geser_word.txt')
DICTIONARY_WORDS: Set[str] = set()

try:
    if not os.path.exists(DICTIONARY_FILE_PATH):
        raise FileNotFoundError(f"Dictionary file not found at: {DICTIONARY_FILE_PATH}")

    with open(DICTIONARY_FILE_PATH, 'r', encoding='utf-8') as file:
        # Assuming one word per line in the dictionary file.
        # .strip() removes leading/trailing whitespace, including newline characters.
        # Ensure only non-empty lines are added.
        DICTIONARY_WORDS = {line.strip() for line in file if line.strip()}
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure the dictionary file exists and is accessible.")
    # The DICTIONARY_WORDS set will remain empty, preventing further errors.
except Exception as e:
    print(f"An unexpected error occurred while loading the dictionary: {e}")
    # The DICTIONARY_WORDS set will remain empty.

def find_unmatched_words(words: List[str]) -> List[str]:
    """
    Identifies words from a list that are not present in the globally loaded dictionary.

    Args:
        words (List[str]): A list of tokenized words to check against the dictionary.

    Returns:
        List[str]: A list of words that are not found in the dictionary.
    
    Raises:
        TypeError: If the input 'words' is not a list.
        ValueError: If the input 'words' list is empty.
    """
    if not isinstance(words, list):
        raise TypeError("Input 'words' must be a list.")
    
    if not words:
        raise ValueError("Input 'words' cannot be an empty list.")
    
    unmatched_words: List[str] = []
    for word in words:
        # Convert word to lowercase for case-insensitive matching if desired,
        # or keep as is for case-sensitive matching.
        # For now, assuming case-sensitive as per original code.
        if word not in DICTIONARY_WORDS:
            unmatched_words.append(word)
            
    return unmatched_words