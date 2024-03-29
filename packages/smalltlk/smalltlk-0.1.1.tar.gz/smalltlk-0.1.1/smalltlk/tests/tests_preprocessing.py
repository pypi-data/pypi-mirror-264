# tests/test_preprocessing.py

import unittest
from smalltlk.preprocessing import preprocess_text, remove_stopwords, lemmatize_tokens

class TestPreprocessing(unittest.TestCase):
    def test_preprocess_text(self):
        text = "This is a test sentence for preprocessing."
        result = preprocess_text(text)
        self.assertEqual(result, ['this', 'is', 'a', 'test', 'sentence', 'for', 'preprocessing'])

    def test_remove_stopwords(self):
        tokens = ['this', 'is', 'a', 'test', 'sentence', 'for', 'preprocessing']
        result = remove_stopwords(tokens)
        self.assertEqual(result, ['test', 'sentence', 'preprocessing'])

    def test_lemmatize_tokens(self):
        tokens = ['running', 'dogs', 'are', 'barking']
        result = lemmatize_tokens(tokens)
        self.assertEqual(result, ['running', 'dog', 'are', 'barking'])

if __name__ == '__main__':
    unittest.main()
