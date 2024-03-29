import numpy as np
from collections import Counter

def calculate_prob_distribution(tokens):
    # Compute frequency distribution of tokens
    freq_dist = Counter(tokens)
    
    # Calculate total number of tokens
    total_tokens = len(tokens)
    
    # Calculate probability distribution
    prob_dict = {token: freq_dist[token] / total_tokens for token in freq_dist}
    
    return prob_dict

def dict_to_array(prob_dict):
    # Extract numerical values (probabilities) from the dictionary
    prob_array = list(prob_dict.values())
    
    return prob_array

############################################
#   Entropy of Probability Distributions   #
############################################

# Shannon Entropy
def shannon_entropy(prob_dist, base=None):
    prob_dist = np.array(prob_dist)
    non_zero_probs = prob_dist[prob_dist != 0]
    if base is None:
        entropy_val = -np.sum(non_zero_probs * np.log(non_zero_probs))
    else:
        entropy_val = -np.sum(non_zero_probs * np.log(non_zero_probs) / np.log(base))
    return entropy_val

# Renyi Entropy
def renyi_entropy(prob_dist, alpha, base=None):
    prob_dist = np.array(prob_dist)
    if alpha == 1:
        return shannon_entropy(prob_dist, base)
    if alpha <= 0:
        raise ValueError("Alpha must be greater than zero.")
    sum_term = np.sum(np.power(prob_dist, alpha))
    if base is None:
        entropy_val = 1 / (1 - alpha) * np.log(sum_term)
    else:
        entropy_val = 1 / (1 - alpha) * np.log(sum_term) / np.log(base)
    return entropy_val

# Cross Entropy
def cross_entropy(prob_dict_p, prob_dict_q, base=None):
    """
    Calculate the cross-entropy between two probability dictionaries, considering only the common elements.

    Arguments:
    prob_dict_p -- Dictionary representing the true probability distribution (token: probability)
    prob_dict_q -- Dictionary representing the estimated probability distribution (token: probability)
    base -- Base for the logarithm (default is None for natural logarithm)

    Returns:
    Cross-entropy between prob_dict_p and prob_dict_q for common elements
    """
    # Find common tokens
    common_tokens = set(prob_dict_p.keys()) & set(prob_dict_q.keys())

    # Initialize cross entropy
    cross_entropy_val = 0

    # Calculate cross entropy for common elements
    for token in common_tokens:
        prob_p = prob_dict_p[token]
        prob_q = prob_dict_q[token]
        if base is None:
            cross_entropy_val -= prob_p * np.log(prob_q)
        else:
            cross_entropy_val -= prob_p * np.log(prob_q) / np.log(base)

    return cross_entropy_val

# KL Divergence
def kl_divergence(prob_dict_p, prob_dict_q):
    """
    Calculate the Kullback-Leibler (KL) divergence between two probability dictionaries, considering only the common elements.

    Arguments:
    prob_dict_p -- Dictionary representing the true probability distribution (token: probability)
    prob_dict_q -- Dictionary representing the estimated probability distribution (token: probability)

    Returns:
    KL divergence between prob_dict_p and prob_dict_q for common elements
    """
    # Find common tokens
    common_tokens = set(prob_dict_p.keys()) & set(prob_dict_q.keys())

    # Initialize KL divergence
    kl_div = 0

    # Calculate KL divergence for common elements
    for token in common_tokens:
        prob_p = prob_dict_p[token]
        prob_q = prob_dict_q[token]
        kl_div += prob_p * np.log(prob_p / prob_q)

    return kl_div

######################################
#   Similarity Between Two Strings   #
######################################

# Cosine Similiarity
def calculate_cosine_similarity(prob_dict1, prob_dict2):
    # Get unique tokens from both probability distributions
    all_tokens = set(prob_dict1.keys()) | set(prob_dict2.keys())
    
    # Convert probability distributions to numpy arrays
    prob_dist1_arr = np.array([prob_dict1[token] if token in prob_dict1 else 0 for token in all_tokens])
    prob_dist2_arr = np.array([prob_dict2[token] if token in prob_dict2 else 0 for token in all_tokens])

    # Compute cosine similarity
    dot_product = np.dot(prob_dist1_arr, prob_dist2_arr)
    norm_prob_dist1 = np.linalg.norm(prob_dist1_arr)
    norm_prob_dist2 = np.linalg.norm(prob_dist2_arr)
    cosine_similarity = dot_product / (norm_prob_dist1 * norm_prob_dist2)

    return cosine_similarity

# Jaccard Similarity
def calculate_jaccard_similarity(prob_dict1, prob_dict2):
    # Get unique tokens from both probability distributions
    tokens1 = set(prob_dict1.keys())
    tokens2 = set(prob_dict2.keys())
    
    # Compute intersection and union of tokens
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    
    # Calculate Jaccard similarity
    jaccard_similarity = len(intersection) / len(union)

    return jaccard_similarity

# Levenshtein Distance
def calculate_levenshtein_distance(prob_dict_p, prob_dict_q):
    """
    Calculate the Levenshtein distance between two strings represented by probability distributions.

    Arguments:
    prob_dict_p -- Dictionary representing the first string's probability distribution (token: probability)
    prob_dict_q -- Dictionary representing the second string's probability distribution (token: probability)

    Returns:
    Weighted Levenshtein distance between the two strings
    """
    # Extract tokens from probability dictionaries
    tokens_p = list(prob_dict_p.keys())
    tokens_q = list(prob_dict_q.keys())

    # Initialize the matrix for Levenshtein distance calculation
    n = len(tokens_p)
    m = len(tokens_q)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize the first row and column
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    # Calculate Levenshtein distance with probabilities
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if tokens_p[i - 1] == tokens_q[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,  # Deletion
                           dp[i][j - 1] + 1,  # Insertion
                           dp[i - 1][j - 1] + cost)  # Substitution

    # Calculate weighted Levenshtein distance
    weighted_distance = 0
    total_weight = 0
    for i in range(n):
        for j in range(m):
            if tokens_p[i] == tokens_q[j]:
                weight_p = prob_dict_p[tokens_p[i]]
                weight_q = prob_dict_q[tokens_q[j]]
                weighted_distance += weight_p * weight_q * dp[i + 1][j + 1]
                total_weight += weight_p * weight_q

    if total_weight == 0:
        return float('inf')  # Avoid division by zero
    else:
        return weighted_distance / total_weight

# Sørensen-Dice Coefficient
def calculate_sorensen_dice_coefficient(prob_dict_p, prob_dict_q):
    # Extract tokens from probability dictionaries
    tokens1 = list(prob_dict_p.keys())
    tokens2 = list(prob_dict_q.keys()) 

    # Calculate intersection and sizes of token sets
    intersection = len(set(tokens1) & set(tokens2))
    size_tokens1 = len(tokens1)
    size_tokens2 = len(tokens2)
    
    # Calculate Dice coefficient
    dice_coefficient = (2.0 * intersection) / (size_tokens1 + size_tokens2)
    
    return dice_coefficient

# Conditional Entropy with epilson protection
def conditional_entropy(prob_dict_p, prob_dict_q, epsilon=1e-10):
    # Extract tokens from probability dictionaries
    tokens1 = list(prob_dict_p.keys())
    tokens2 = list(prob_dict_q.keys()) 

    # Compute frequency distributions of tokens in both sequences
    freq_dist1 = Counter(tokens1)
    freq_dist2 = Counter(tokens2)
    
    # Get unique tokens from both sequences
    all_tokens = set(freq_dist1.keys()) | set(freq_dist2.keys())
    
    # Convert frequency distributions to probability distributions
    prob_dist1 = np.array([freq_dist1[token] / len(tokens1) for token in all_tokens])
    prob_dist2 = np.array([freq_dist2[token] / len(tokens2) for token in all_tokens])
    
    # Compute conditional probability distribution P(tokens1 | tokens2)
    conditional_prob_dist = np.zeros_like(prob_dist1)
    for i, token in enumerate(all_tokens):
        if freq_dist2[token] != 0:
            conditional_prob_dist[i] = freq_dist1[token] / freq_dist2[token]

    # Handle zero probabilities (add epsilon to avoid division by zero)
    conditional_prob_dist += epsilon

    # Compute conditional entropy
    conditional_entropy_val = -np.sum(prob_dist2 * conditional_prob_dist * np.log2(conditional_prob_dist))

    return conditional_entropy_val

'''
# Example usage:
p = "I like to read books"
q = "She is reading books"

p_dict = calculate_prob_distribution(p.split())
q_dict = calculate_prob_distribution(q.split())

p_prob = dict_to_array(p_dict)
q_prob = dict_to_array(q_dict)

print(f"p distributions \n\twords = {p_prob}")
print(f"q distributions \n\twords = {q_prob}")

print("ENTROPY METHODS:")
print(f"\tShannon Entropy: {shannon_entropy(p_prob)}")
print(f"\tRenyi Entropy: {renyi_entropy(p_prob, alpha = 1)}")
print(f"\tCross Entropy: {cross_entropy(p_dict, q_dict)}")
print(f"\tKL Divergence: {kl_divergence(p_dict, q_dict)}")
print(f"\tConditional Entropy: {conditional_entropy(p_dict, q_dict)}")

print("SIMILARITY METHODS:")
print(f"\tCosine Similarity: {calculate_cosine_similarity(p_dict, q_dict)}")
print(f"\tJaccard Similarity: {calculate_jaccard_similarity(p_dict, q_dict)}")
print(f"\tLevenshtein Distance: {calculate_levenshtein_distance(p_dict, q_dict)}")
print(f"\tDice Coefficient: {calculate_sorensen_dice_coefficient(p_dict, q_dict)}")
'''