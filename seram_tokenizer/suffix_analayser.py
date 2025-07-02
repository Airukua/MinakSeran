import os
from typing import List, Set
from pathlib import Path
from importlib.resources import files


def get_resource_path(package: str, resource: str) -> str:
    return str(files(package) / resource)

def get_data_file_path(filename: str) -> str:
    """Get path to data file, trying multiple methods for compatibility."""
    try:
        return get_resource_path(__name__, f'data/{filename}')
    except Exception:
        # Fallback to relative path from current file
        current_dir = Path(__file__).parent
        data_path = current_dir / 'data' / filename
        return str(data_path)

# INSPIRED BY The implementation of https://github.com/AbdullahAlabbas/Wordle/blob/main/play_wordle.py
def load_word_set(file_path: str) -> Set[str]:
    """
    Load words from a file into a set for O(1) lookup performance.
    
    Args:
        file_path (str): Path to the file containing words
        
    Returns:
        Set[str]: Set of words from the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return {line.strip() for line in f if line.strip()}

# Define file paths using modern resource management
DICTIONARY_FILE_PATH = get_data_file_path('geser_word.txt')
VOCAL_FILE_PATH = get_data_file_path('vocal.txt')
CONSONANT_FILE_PATH = get_data_file_path('consonant.txt')

# INITIALIZE SETS
DICTIONARY_WORDS: Set[str] = set()
VOCAL_LETTERS: Set[str] = set()
CONSONANT_LETTERS: Set[str] = set()

# Load Dictionary, Vocal, and Consonant letters from files
try:
    DICTIONARY_WORDS = load_word_set(DICTIONARY_FILE_PATH)
    VOCAL_LETTERS = load_word_set(VOCAL_FILE_PATH)
    CONSONANT_LETTERS = load_word_set(CONSONANT_FILE_PATH)
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure all necessary files exist.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Pre-filter dictionary words for efficiency
SINGLE_WORD_DICTIONARY_ENTRIES: Set[str] = {
    word for word in DICTIONARY_WORDS 
    if ' ' not in word  
}

LEMMA_WITH_RA: Set[str] = {
    word for word in SINGLE_WORD_DICTIONARY_ENTRIES 
    if word.endswith('ra')
}

LEMMA_WITH_A: Set[str] = {
    word for word in SINGLE_WORD_DICTIONARY_ENTRIES 
    if word.endswith('a')
}

class SuffixAnalyser:
    """
    A class to analyze suffixes in a string of text against a predefined dictionary.
    
    This class efficiently identifies words ending with specific suffixes ('ra' and 'a')
    that are not present in the predefined dictionary, indicating potential suffixed forms.
    
    Attributes:
        words (str): The original input string of space-separated words.
        split_words (List[str]): List of individual words from the input.
        ra_words (List[str]): Words ending with 'ra' suffix.
        a_words (List[str]): Words ending with 'a' suffix.
        checked_ra (List[str]): 'ra' words not found in dictionary lemmas.
        checked_a (List[str]): 'a' words not found in dictionary lemmas.
    """
        
    def __init__(self, words: str):
        """
        Initialize the SuffixAnalyser with input text.
        
        Args:
            words (str): A string of space-separated words to analyze.
            
        Raises:
            TypeError: If input is not a string.
            ValueError: If input is an empty string.
        """
        if not isinstance(words, str):
            raise TypeError("Input 'words' must be a string.")
        if not words.strip():
            raise ValueError("Input 'words' cannot be an empty string.")
        
        self.words = words.lower()
        self.split_words = self.words.split()
        self.ra_words = []
        self.a_words = []
        self.checked_ra = []
        self.checked_a = []
        
        for word in self.split_words:
            if word.endswith('ra'):
                self.ra_words.append(word)
                if word not in LEMMA_WITH_RA:
                    self.checked_ra.append(word)
            elif word.endswith('a'):
                self.a_words.append(word)
                if word not in LEMMA_WITH_A:
                    self.checked_a.append(word)
        
    
    def find_ra_suffix_words(self) -> List[str]:
        """
        Find and return words ending with 'ra' that are not in the dictionary lemmas.
        
        Returns:
            List[str]: List of words ending with 'ra' not found in dictionary lemmas.
        """
        return [word for word in self.checked_ra 
                if len(word) >= 3 and word[-3] in VOCAL_LETTERS]
    
    def find_a_suffix_words(self) -> List[str]:
        """
        Identifies words that end with the suffix 'a' and are not present in the dictionary.
        
        Returns:
            List[str]: A list of words ending with 'a' (with consonant+'a' pattern) 
                      that aren't found in the dictionary.
        """
        return [word for word in self.checked_a 
                if len(word) >= 2 and word[-2] in CONSONANT_LETTERS]
    