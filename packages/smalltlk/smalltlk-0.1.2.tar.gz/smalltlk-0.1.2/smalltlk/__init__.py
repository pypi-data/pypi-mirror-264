# __init__.py
import nltk
from smalltlk.preprocessing import preprocess_text, remove_stopwords, lemmatize_tokens
from smalltlk.gen.gen_text import generate_text
from smalltlk.eval.similarity import *

# Expose preprocessing and generation functions
__all__ = ['preprocess_text', 'remove_stopwords', 'lemmatize_tokens', 'generate_text', 
           'calculate_prob_distribution', 'dict_to_array', 'shannon_entropy', 'renyi_entropy', 
           'cross_entropy', 'total_cross_entropy', 'kl_divergence', 'total_kl_divergence', 
           'cosine_similarity', 'total_cosine_similarity', 'jaccard_similarity', 'total_jaccard_similarity'
           'levenshtein_distance', 'total_levenshtein_distance', 'sorensen_dice_coefficient', 'total_sorensen_dice_coefficient', 
           'conditional_entropy', 'total_conditional_entropy'
           ]

def initialize_nltk_resources():
    """
    Download NLTK resources if not already downloaded.
    """
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('taggers/averaged_perceptron_tagger')
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

# Perform initialization if the file is executed as a script
if __name__ == "__main__":
    initialize_nltk_resources()