import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from geser_tokenizer import GeserTokenizer
from geser_tokenizer.find_words import find_unmatched_words
from geser_tokenizer.find_words import DICTIONARY_WORDS

class TestGeserTokenizer(unittest.TestCase):
    def test_empty_text(self):
        tokenizer = GeserTokenizer("")
        self.assertEqual(tokenizer.tokenize(), [])

    def test_basic_tokenization(self):
        tokenizer = GeserTokenizer("Ini adalah contoh sederhana")
        self.assertEqual(tokenizer.tokenize(), ["Ini", "adalah", "contoh", "sederhana"])

    def test_punctuation_removal(self):
        tokenizer = GeserTokenizer("Kata,dengan.tanda?!seru...kurung(tutup).")
        expected_tokens = ["Kata",",","dengan",".","tanda","?","!","seru",".",".",".","kurung","(","tutup",")","."]
        self.assertEqual(tokenizer.tokenize(), expected_tokens)

    def test_hyphenated_words(self):
        tokenizer = GeserTokenizer("ini-kata dan -itu-")
        self.assertEqual(tokenizer.tokenize(), ["ini-kata", "dan", "-","itu","-"])

    def test_mixed_case_tokenization(self):
        tokenizer = GeserTokenizer("Ini TEKS BeSaR kEcIl.")
        self.assertEqual(tokenizer.tokenize(), ["Ini", "TEKS", "BeSaR", "kEcIl","."])

    def test_multiple_spaces(self):
        tokenizer = GeserTokenizer("Kata   dengan    banyak    spasi")
        self.assertEqual(tokenizer.tokenize(), ["Kata", "dengan", "banyak", "spasi"])

    def test_text_with_numbers(self):
        tokenizer = GeserTokenizer("Ini ada 123 angka dan 456 huruf.")
        self.assertEqual(tokenizer.tokenize(), ["Ini", "ada", "123", "angka", "dan", "456", "huruf","."])

    def test_reduplication_handling(self):
        text = "Dia suka lari-lari di pagi hari dan makan-makan yang enak."
        tokenizer = GeserTokenizer(text)
        tokens = tokenizer.tokenize()
        self.assertIn("lari-lari", tokens)
        self.assertIn("makan-makan", tokens)
        self.assertNotIn("lari-lari.", tokens)
        self.assertNotIn("makan-makan.", tokens)
        expected_subset = {"Dia", "suka", "lari-lari", "di", "pagi", "hari", "dan", "makan-makan", "yang", "enak"}
        self.assertTrue(expected_subset.issubset(set(tokens)))

class TestFindUnmatchedWords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_dictionary_words = set(DICTIONARY_WORDS) 
        DICTIONARY_WORDS.clear()
        DICTIONARY_WORDS.update({"kata", "ada", "geser", "suka", "lari-lari", "makan-makan"})

    @classmethod
    def tearDownClass(cls):
        DICTIONARY_WORDS.clear()
        DICTIONARY_WORDS.update(cls.original_dictionary_words)

    def test_all_words_match(self):
        words = ["abi-abis", "nina", "baba"]
        self.assertEqual(find_unmatched_words(words), [])

    def test_some_words_unmatch(self):
        words = ["kata", "tidak-ada", "geser", "belum-ada"]
        unmatched = find_unmatched_words(words)
        self.assertCountEqual(unmatched, ["tidak-ada", "belum-ada"])

    def test_empty_input_list(self):
        with self.assertRaises(ValueError):
            find_unmatched_words([])

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            find_unmatched_words("ini bukan list")
        with self.assertRaises(TypeError):
            find_unmatched_words(123)

    def test_case_sensitivity(self):
        words = ["Kata", "kata"]
        unmatched = find_unmatched_words(words)
        self.assertIn("Kata", unmatched)
        self.assertNotIn("kata", unmatched)

    def test_words_with_hyphens(self):
        words = ["lari-lari", "makan-makan", "kata-baru"]
        unmatched = find_unmatched_words(words)
        self.assertCountEqual(unmatched, ["kata-baru"])

if __name__ == '__main__':
    unittest.main()