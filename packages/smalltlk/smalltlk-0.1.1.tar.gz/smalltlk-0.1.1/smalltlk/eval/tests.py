# tests/tests_evaluation.py

import unittest
from similarity import *

class TestSimilarityMethods(unittest.TestCase):

    def setUp(self):
        self.sentences = [
            "I like to read books",
            "She is reading books",
            "They enjoy reading novels",
            "We love literature"
        ]
        self.prob_distributions = [calculate_prob_distribution(sentence.split()) for sentence in self.sentences]

    def test_prob_distribution(self):
        self.assertEqual(len(self.prob_distributions), 4)
        self.assertEqual(len(self.prob_distributions[0]), 5)

    def test_dict_to_array(self):
        p_prob = dict_to_array(self.prob_distributions[0])
        self.assertEqual(len(p_prob), 5)

    def test_shannon_entropy(self):
        entropy_p = shannon_entropy(dict_to_array(self.prob_distributions[0]))
        self.assertAlmostEqual(entropy_p, 2.321928094887362)

    def test_renyi_entropy(self):
        entropy_p = renyi_entropy(dict_to_array(self.prob_distributions[0]), alpha=1)
        self.assertAlmostEqual(entropy_p, 2.321928094887362)

    def test_cross_entropy(self):
        cross_ent = cross_entropy(self.prob_distributions[0], self.prob_distributions[1])
        self.assertAlmostEqual(cross_ent, 1.049606003654768)

    def test_kl_divergence(self):
        kl_div = kl_divergence(self.prob_distributions[0], self.prob_distributions[1])
        self.assertAlmostEqual(kl_div, 0.5567796494470396)

    def test_conditional_entropy(self):
        cond_entropy = conditional_entropy(self.prob_distributions[0], self.prob_distributions[1])
        self.assertAlmostEqual(cond_entropy, 1.219672610340792)

    def test_cosine_similarity(self):
        cos_sim = calculate_cosine_similarity(self.prob_distributions[0], self.prob_distributions[1])
        self.assertAlmostEqual(cos_sim, 0.8366600265340755)

    def test_jaccard_similarity(self):
        jacc_sim = calculate_jaccard_similarity(self.prob_distributions[0], self.prob_distributions[1])
        self.assertAlmostEqual(jacc_sim, 0.6)

    def test_levenshtein_distance(self):
        lev_dist = calculate_levenshtein_distance(self.prob_distributions[0], self.prob_distributions[1])
        self.assertAlmostEqual(lev_dist, 2)

    def test_sorensen_dice_coefficient(self):
        dice_coeff = calculate_sorensen_dice_coefficient(self.prob_distributions[0], self.prob_distributions[1])
        self.assertAlmostEqual(dice_coeff, 0.75)

if __name__ == '__main__':
    unittest.main()