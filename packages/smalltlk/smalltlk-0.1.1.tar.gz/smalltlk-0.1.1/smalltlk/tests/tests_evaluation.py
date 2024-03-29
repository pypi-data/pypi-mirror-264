# tests/tests_evaluation.py

import unittest
from smalltlk.eval.similarity import cosine_similarity, jaccard_similarity, levenshtein_distance, sorensen_dice_coefficient

class TestSimilarityFunctions(unittest.TestCase):
    def test_cosine_similarity(self):
        similarity_score = cosine_similarity("I like apples", "I like oranges")
        self.assertAlmostEqual(similarity_score, 0.5, places=2)

    def test_jaccard_similarity(self):
        similarity_score = jaccard_similarity("I like apples", "I like oranges")
        self.assertAlmostEqual(similarity_score, 0.5, places=2)

    def test_levenshtein_distance(self):
        distance = levenshtein_distance("kitten", "sitting")
        self.assertEqual(distance, 3)

    def test_sorensen_dice_coefficient(self):
        similarity_score = sorensen_dice_coefficient("I like apples", "I like oranges")
        self.assertAlmostEqual(similarity_score, 0.5, places=2)

if __name__ == '__main__':
    unittest.main()