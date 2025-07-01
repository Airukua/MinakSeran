import re

class GeserParagogNormalizer:
    """
    A class to normalize paragogs in Geser text.
    A paragog is defined as a word ending with 'a' or 'ra'.
    """

    def __init__(self, text_list: list):
        """
        Initializes the ParagogNormalizer with a list of sentences.

        Args:
            text_list (list): A list of sentences (strings) to be normalized.
        """
        if not isinstance(text_list, list):
            raise TypeError("Input must be a list of strings.")
        
        for sentence in text_list:
            if not isinstance(sentence, str):
                raise TypeError("All elements in the list must be strings.")
            if len(sentence.strip().split()) < 2:
                raise ValueError(f"Each sentence must contain at least two words: '{sentence}'")
        
        self.text_list = text_list
        self.paragog_pattern = re.compile(r'(\w+)\s+(a|ra)(?=\s|$)')

    def normalize(self) -> list:
        """
        Normalizes paragogs by merging word + 'a'/'ra' into a single token.
        Returns:
            list: A list of normalized sentences.
        """
        normalized_text = []      
        for text in self.text_list:
            new_text = text
            matches = self.paragog_pattern.findall(text)

            for word, suffix in matches:
                original = f"{word} {suffix}"
                merged = f"{word}{suffix}"
                new_text = new_text.replace(original, merged)
            normalized_text.append(new_text)

        return normalized_text
            
    