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

# INITIALIZE SETS
DICTIONARY_WORDS: Set[str] = set()

# Load Dictionary, Vocal, and Consonant letters from files
try:
    DICTIONARY_WORDS = load_word_set(DICTIONARY_FILE_PATH)
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure all necessary files exist.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Pre-filter dictionary words for efficiency
SINGLE_WORD_DICTIONARY_ENTRIES: Set[str] = {
    word for word in DICTIONARY_WORDS 
    if ' ' not in word  
}

LEMMA_WITH_NA: Set[str] = {
    word for word in SINGLE_WORD_DICTIONARY_ENTRIES 
    if word.startswith('na')
}

LEMMA_WITH_DA: Set[str] = {
    word for word in SINGLE_WORD_DICTIONARY_ENTRIES 
    if word.startswith('da')
}

class PrefixAnalyser:
    """
    A class to analyze suffixes in a string of text against a predefined dictionary.
    
    This class efficiently identifies words ending with specific suffixes ('ra' and 'a')
    that are not present in the predefined dictionary, indicating potential suffixed forms.
    
    Attributes:
        words (str): The original input string of space-separated words.
        split_words (List[str]): List of individual words from the input.
        da_words (List[str]): Words start with 'da' suffix.
        na_words (List[str]): Words start with 'na' suffix.
        checked_na (List[str]): 'da' words not found in dictionary lemmas.
        checked_da (List[str]): 'na' words not found in dictionary lemmas.
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
        self.na_words = []
        self.da_words = []
        self.checked_na = []
        self.checked_da = []
        
        for word in self.split_words:
            if word.startswith('na'):
                self.na_words.append(word)
                if word not in LEMMA_WITH_NA:
                    self.checked_na.append(word)
            elif word.startswith('da'):
                self.da_words.append(word)
                if word not in LEMMA_WITH_DA:
                    self.checked_da.append(word)
    
    def get_na_words(self) -> List[str]:
            """Get words starting with 'na'."""
            return self.checked_na
        
    def get_da_words(self) -> List[str]:
            """Get words starting with 'da'."""
            return self.checked_da

if __name__ == "__main__":
    # Dummy data untuk pengujian
    LEMMA_WITH_NA = {'naga', 'namira', 'naira'}
    LEMMA_WITH_DA = {'dadu', 'dana', 'dari'}

    # Teks masukan untuk diuji
    input_text = "naga namira naira nadia dadu dana dari dasar dalam"

    # Jalankan analisanya
    analyser = PrefixAnalyser(input_text)

    # Tampilkan hasil
    print("Kata dengan prefix 'na' yang tidak ada di lemma:")
    print(analyser.get_na_words())

    print("\nKata dengan prefix 'da' yang tidak ada di lemma:")
    print(analyser.get_da_words())