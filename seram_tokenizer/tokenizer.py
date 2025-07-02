# Part of this code inspired by https://github.com/OpenNMT/Tokenizer/blob/master/bindings/python/README.md
import re
from typing import List, Dict
from .find_reduplication import extract_reduplications
from .suffix_analayser import SuffixAnalyser
from .prefix_analyser import PrefixAnalyser

class SeramTokenizer:
    """
    A tokenizer for Seram text, designed to handle reduplicated words and preserve punctuation as separate tokens.
    """

    def __init__(self, text: str, use_suffix:bool = False, use_prefix:bool = False):
        """
        Initializes the SeramTokenizer with the input text.

        Args:
            text (str): The input text to be tokenized.
        """
        if not isinstance(text, str):
            raise TypeError("Input 'text' must be a string.")
        self.text = text
        self.use_suffix = use_suffix
        self.use_prefix = use_prefix
        self.token_pattern = re.compile(r'\w+|[^\w\s]')

    def tokenize(self) -> List[str]:
        """
        Tokenizes the input text into words and punctuation tokens,
        handling reduplicated words with placeholders to preserve structure.

        Returns:
            List[str]: A list of tokenized words and punctuation.
        """
        if not self.text:
            return []
        
        # Step 1: Detect reduplications and replace them with unique placeholders
        reduplications: List[str] = extract_reduplications(self.text)
        placeholder_map: Dict[str, str] = {}
        processed_text = self.text        

        for i, word in enumerate(reduplications):
            placeholder = f"__REDUPLICATION_PLACEHOLDER_{i}__"
            processed_text = re.sub(re.escape(word), placeholder, processed_text)
            placeholder_map[placeholder] = word

        # Step 4: Tokenize including punctuation as separate tokens
        raw_tokens = self.token_pattern.findall(processed_text)
        
        # Step 3: Affix Analysis Prep
        clean_tokens = [t for t in raw_tokens if t.isalpha()]
        ra_words, a_words, na_words, da_words = set(), set(), set(), set()

        if self.use_suffix:
            suffix_analyser = SuffixAnalyser(" ".join(clean_tokens))
            ra_words = suffix_analyser.find_ra_suffix_words()
            a_words = suffix_analyser.find_a_suffix_words()

        if self.use_prefix:
            prefix_analyser = PrefixAnalyser(" ".join(clean_tokens))
            na_words = prefix_analyser.get_na_words()
            da_words = prefix_analyser.get_da_words()

        # Step 4: Restore reduplications + apply affix splitting
        final_tokens = []
        for token in raw_tokens:
            for placeholder, original_word in placeholder_map.items():
                token = token.replace(placeholder, original_word)

            if self.use_suffix and token in ra_words and token.endswith('ra'):
                base = token[:-2]
                final_tokens.extend([base, '_ra'])
            elif self.use_suffix and token in a_words and token.endswith('a'):
                base = token[:-1]
                final_tokens.extend([base, '_a'])
            elif self.use_prefix and token in na_words and token.startswith('na'):
                base = token[2:]
                final_tokens.extend(['na_', base])
            elif self.use_prefix and token in da_words and token.startswith('da'):
                base = token[2:]
                final_tokens.extend(['da_', base])
            else:
                final_tokens.append(token)

        return final_tokens

