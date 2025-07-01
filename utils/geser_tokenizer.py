# Part of this code inspired by https://github.com/OpenNMT/Tokenizer/blob/master/bindings/python/README.md
import re
import os
from typing import List, Set, Dict
from find_reduplication import extract_reduplications

# Load the dictionary words into a set for efficient O(1) average time complexity lookups.
# This ensures that checking if a word exists in the dictionary is very fast.
DICTIONARY_FILE_PATH = 'utils/data/geser_word.txt'
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
        # This pattern is used to remove punctuation from tokens.
        self.punctuation_pattern = re.compile(
            r"([.,!?;:\'\"(){}\[\]<>~`@#$%^&*/+=|\\])|(\.{3})|([^\s\w]|^)-|-([^\s\w]|$)"
        )
        # Regex pattern to split text by one or more whitespace characters.
        self.split_pattern = re.compile(r'\s+')
    
    def tokenize(self) -> List[str]:
        """
        Tokenizes the input text into words, handling punctuation and special cases like reduplication.

        The tokenization process involves:
        1. Identifying and temporarily replacing reduplicated words with unique placeholders.
        2. Splitting the text into tokens based on whitespace.
        3. Restoring the original reduplicated words from their placeholders.
        4. Removing specified punctuation from the resulting tokens.

        Returns:
            List[str]: A list of tokenized words.
        """
        if not self.text:
            return [] # Return empty list for empty input text

        # Step 1: Extract reduplicated words and prepare for replacement.
        # We use a dictionary to map unique placeholders back to original words,
        # ensuring correct restoration even if reduplicated words are substrings of others.
        reduplications: List[str] = extract_reduplications(self.text)
        
        # Create a mapping from a unique placeholder to the original reduplicated word.
        # This helps in safely replacing and restoring words without conflicts.
        placeholder_map: Dict[str, str] = {}
        processed_text = self.text
        
        for i, word in enumerate(reduplications):
            # Create a unique placeholder for each reduplicated word.
            placeholder = f"__REDUPLICATION_PLACEHOLDER_{i}__"
            # Replace the original word with its unique placeholder in the text.
            processed_text = processed_text.replace(word, placeholder)
            placeholder_map[placeholder] = word

        # Step 2: Split the text into tokens based on whitespace.
        tokens = self.split_pattern.split(processed_text)

        # Step 3: Restore the original reduplicated words from their placeholders.
        final_tokens: List[str] = []
        for token in tokens:
            restored_token = token
            # Iterate through the placeholder map to restore original words.
            for placeholder, original_word in placeholder_map.items():
                restored_token = restored_token.replace(placeholder, original_word)
            final_tokens.append(restored_token)

        # Step 4: Remove punctuation from tokens and filter out any empty strings.
        # The punctuation_pattern.sub('', token) replaces matched punctuation with an empty string.
        tokens_without_punctuation = [
            self.punctuation_pattern.sub('', token) for token in final_tokens if token
        ]
        
        return tokens_without_punctuation

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
