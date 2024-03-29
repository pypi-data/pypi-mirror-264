import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

def preprocess_text(text):
    """
    Preprocesses the input text.
    
    Parameters:
        text (str): The input text to be preprocessed.
        
    Returns:
        str: The preprocessed text.
    """
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Lowercasing
    tokens = [token.lower() for token in tokens]
    
    return tokens

def remove_stopwords(tokens):
    """
    Removes stopwords from a list of tokens.
    
    Parameters:
        tokens (list): List of tokens.
        
    Returns:
        list: Tokens with stopwords removed.
    """
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens

def lemmatize_tokens(tokens):
    """
    Lemmatizes a list of tokens.
    
    Parameters:
        tokens (list): List of tokens.
        
    Returns:
        list: Lemmatized tokens.
    """
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

# Example usage:
# text = "This is an example sentence for text preprocessing!"
# preprocessed_text = preprocess_text(text)
# filtered_text = remove_stopwords(preprocessed_text)
# lemmatized_text = lemmatize_tokens(filtered_text)

# print("Preprocessed Text:", preprocessed_text)
# print("Filtered Text:", filtered_text)
# print("Lemmatized Text:", lemmatized_text)