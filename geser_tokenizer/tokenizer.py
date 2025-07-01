# Part of this code inspired by https://github.com/OpenNMT/Tokenizer/blob/master/bindings/python/README.md
import re
import os
from typing import List, Set, Dict
from .find_reduplication import extract_reduplications
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

class GeserTokenizer:
    """
    A tokenizer for Geser text, designed to handle reduplicated words and punctuation.
    """

    def __init__(self, text: str):
        """
        Initializes the GeserTokenizer with the input text.

        Args:
            text (str): The input text to be tokenized.
        """
        if not isinstance(text, str):
            raise TypeError("Input 'text' must be a string.")
        self.text = text

        # Regex pattern to capture various punctuation marks and ellipses.
        # Updated to handle hyphens more carefully - only treat standalone hyphens as separators
        self.punctuation_pattern = re.compile(
            r"([.,!?;:\'\"(){}\[\]<>~`@#$%^&*/+=|\\])|(\.{3})|(\s-\s)"
        )
        # Regex pattern to split text by one or more whitespace characters.
        self.split_pattern = re.compile(r'\s+')
    
    def tokenize(self) -> List[str]:
        """
        Tokenizes the input text into words, handling punctuation and special cases like reduplication.

        The tokenization process involves:
        1. Identifying and temporarily replacing reduplicated words with unique placeholders.
        2. Replacing punctuation with spaces to act as delimiters.
        3. Splitting the text into tokens based on whitespace.
        4. Restoring the original reduplicated words from their placeholders.

        Returns:
            List[str]: A list of tokenized words.
        """
        if not self.text:
            return [] # Return empty list for empty input text

        # Step 1: Extract reduplicated words and prepare for replacement.
        reduplications: List[str] = extract_reduplications(self.text)
        
        # Create a mapping from a unique placeholder to the original reduplicated word.
        placeholder_map: Dict[str, str] = {}
        processed_text = self.text
        
        for i, word in enumerate(reduplications):
            # Create a unique placeholder for each reduplicated word.
            placeholder = f"__REDUPLICATION_PLACEHOLDER_{i}__"
            # Replace the original word with its unique placeholder in the text.
            # Use re.escape to handle special regex characters in the word itself.
            processed_text = re.sub(re.escape(word), placeholder, processed_text)
            placeholder_map[placeholder] = word
            # if re.match(r'\s?\-\w+\-\s?|\s?\-\w+\s?|\s?\w+\-\s?', word):

        # Step 2: Replace punctuation with spaces, then split by spaces.
        # This effectively treats punctuation as word delimiters and removes them from tokens.
        temp_text = self.punctuation_pattern.sub(' ', processed_text)
        
        # Split by one or more whitespace characters.
        # This handles multiple spaces and ensures clean token separation.
        tokens = self.split_pattern.split(temp_text)

        # Step 3: Restore the original reduplicated words from their placeholders.
        final_tokens: List[str] = []
        for token in tokens:
            restored_token = token
            # Iterate through the placeholder map to restore original words.
            for placeholder, original_word in placeholder_map.items():
                restored_token = restored_token.replace(placeholder, original_word)
            if restored_token:
                final_tokens.append(restored_token)  
        return final_tokens


