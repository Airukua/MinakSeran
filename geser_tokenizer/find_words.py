# Part of this code inspired by https://github.com/OpenNMT/Tokenizer/blob/master/bindings/python/README.md
import re
from typing import List, Set
import pkg_resources

DICTIONARY_FILE_PATH = pkg_resources.resource_filename(__name__, 'data/geser_word.txt')
DICTIONARY_WORDS: Set[str] = set()

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
    
    if not words: # Check for empty list more pythonically
        raise ValueError("Input 'words' cannot be an empty list.")
    
    unmatched_words: List[str] = []
    for word in words:
        # Convert word to lowercase for case-insensitive matching if desired,
        # or keep as is for case-sensitive matching.
        # For now, assuming case-sensitive as per original code.
        if word not in DICTIONARY_WORDS:
            unmatched_words.append(word)
            
    return unmatched_words