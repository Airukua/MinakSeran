# Part of this code inspired by https://github.com/OpenNMT/Tokenizer/blob/master/bindings/python/README.md
import re
from typing import List, Set, Dict
from .find_reduplication import extract_reduplications

class GeserTokenizer:
    """
    A tokenizer for Geser text, designed to handle reduplicated words and preserve punctuation as separate tokens.
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
        self.token_pattern = re.compile(r'\w+|[^\w\s]')

    def tokenize(self) -> List[str]:
        """
        Tokenizes the input text into words and punctuation tokens,
        handling reduplicated words with placeholders to preserve structure.

        Returns:
            List[str]: A list of tokenized words and punctuation.
        """
        if not self.text:
            return []  # Return empty list for empty input text

        # Step 1: Detect reduplications and replace them with unique placeholders
        reduplications: List[str] = extract_reduplications(self.text)
        placeholder_map: Dict[str, str] = {}
        processed_text = self.text

        for i, word in enumerate(reduplications):
            placeholder = f"__REDUPLICATION_PLACEHOLDER_{i}__"
            processed_text = re.sub(re.escape(word), placeholder, processed_text)
            placeholder_map[placeholder] = word

        # Step 2: Tokenize including punctuation as separate tokens
        raw_tokens = self.token_pattern.findall(processed_text)

        # Step 3: Restore reduplications from placeholders
        final_tokens: List[str] = []
        for token in raw_tokens:
            for placeholder, original_word in placeholder_map.items():
                token = token.replace(placeholder, original_word)
            final_tokens.append(token)

        return final_tokens

