import numpy as np
from collections import Counter

def calculate_prob_distribution(tokens):
    """
    Calculate the probability distribution of tokens.

    Arguments:
    tokens -- List of tokens

    Returns:
    prob_dict -- Dictionary representing the probability distribution (token: probability)
    """
    # Handle empty input
    if not tokens:
        return {}

    # Compute frequency distribution of tokens
    freq_dist = Counter(tokens)
    
    # Total number of tokens
    total_tokens = len(tokens)
    
    # Normalize frequencies to obtain probabilities
    prob_dict = {token: freq / total_tokens for token, freq in freq_dist.items()}
    
    return prob_dict

def dict_to_array(prob_dict):
    """
    Convert a probability dictionary into an array of numerical values.

    Arguments:
    prob_dict -- Dictionary representing the probability distribution (token: probability)

    Returns:
    prob_array -- Array of numerical values (probabilities)
    """
    # Extract numerical values (probabilities) from the dictionary
    prob_array = list(prob_dict.values())
    
    return prob_array

def shannon_entropy(prob_dist, base=None):
    """
    Calculate the Shannon entropy of a probability distribution.

    Arguments:
    prob_dist -- Array-like object representing the probability distribution
    base -- Base of the logarithm (default: natural logarithm)

    Returns:
    entropy_val -- Shannon entropy
    """
    prob_dist = np.array(prob_dist)

    # Filter out zero probabilities
    non_zero_probs = prob_dist[prob_dist != 0]

    # Calculate entropy based on the specified base or default to natural logarithm
    if base is None:
        entropy_val = -np.sum(non_zero_probs * np.log(non_zero_probs))
    else:
        entropy_val = -np.sum(non_zero_probs * np.log(non_zero_probs) / np.log(base))
    return entropy_val

def renyi_entropy(prob_dist, alpha, base=None):
    """
    Calculate the Rényi entropy of a probability distribution.

    Arguments:
    prob_dist -- Array-like object representing the probability distribution
    alpha -- Rényi entropy parameter
    base -- Base of the logarithm (default: natural logarithm)

    Returns:
    entropy_val -- Rényi entropy
    """
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

def total_cross_entropy(prob_dicts, calc='avg'):
    """
    Calculate the average cross entropy given an array of probability dictionaries.

    Arguments:
    prob_dicts -- Array of probability dictionaries
    calc -- Calculation method: 'avg' for average, 'sum' for sum

    Returns:
    cross_entropy_value -- Cross entropy value
    """
    num_dicts = len(prob_dicts)
    total_cross_ent = 0.0
    total_pairs = 0

    # Calculate cross entropy for all pairs of probability distributions
    for i in range(num_dicts):
        for j in range(num_dicts):
            if i != j:
                if prob_dicts[i] and prob_dicts[j]:  # Check if dictionaries are not empty
                    size_i = len(prob_dicts[i])
                    size_j = len(prob_dicts[j])
                    cross_ent_ij = cross_entropy(prob_dicts[i], prob_dicts[j])
                    total_cross_ent += (size_i / (size_i + size_j)) * cross_ent_ij
                    total_pairs += 1
    
    if calc == 'sum':
        return total_cross_ent
    elif calc == 'avg':
        avg_cross_ent = total_cross_ent / total_pairs if total_pairs > 0 else 0.0
        return avg_cross_ent
    else:
        raise ValueError("Invalid calculation method. Use 'sum' or 'avg'.")

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

def total_kl_divergence(prob_dicts, calc='avg'):
    """
    Calculate the total or average Kullback-Leibler (KL) divergence across an array of probability dictionaries.

    Arguments:
    prob_dicts -- Array of probability dictionaries
    calc -- Calculation method: 'avg' for average, 'sum' for total (default: 'avg')

    Returns:
    kl_divergence_value -- Total or average KL divergence
    """
    num_dicts = len(prob_dicts)
    total_kl_divergence = 0.0
    total_pairs = 0

    # Calculate KL divergence for all pairs of probability distributions
    for i in range(num_dicts):
        for j in range(num_dicts):
            if i != j:
                common_tokens = set(prob_dicts[i].keys()) & set(prob_dicts[j].keys())
                for token in common_tokens:
                    prob_p = prob_dicts[i][token]
                    prob_q = prob_dicts[j][token]
                    total_kl_divergence += prob_p * np.log(prob_p / prob_q)
                    total_pairs += 1

    if calc == 'sum':
        return total_kl_divergence
    elif calc == 'avg':
        avg_kl_divergence = total_kl_divergence / total_pairs if total_pairs > 0 else 0.0
        return avg_kl_divergence
    else:
        raise ValueError("Invalid calculation method. Use 'sum' or 'avg'.")

def cosine_similarity(prob_dict1, prob_dict2):
    """
    Calculate the cosine similarity between two probability dictionaries.

    Arguments:
    prob_dict1 -- First probability dictionary
    prob_dict2 -- Second probability dictionary

    Returns:
    cosine_similarity -- Cosine similarity between the probability distributions
    """
    # Get unique tokens from both probability distributions
    all_tokens = set(prob_dict1.keys()) | set(prob_dict2.keys())
    
    # Initialize arrays to store probabilities
    prob_dist1_arr = np.zeros(len(all_tokens))
    prob_dist2_arr = np.zeros(len(all_tokens))
    
    # Fill arrays with probabilities
    for idx, token in enumerate(all_tokens):
        prob_dist1_arr[idx] = prob_dict1.get(token, 0)
        prob_dist2_arr[idx] = prob_dict2.get(token, 0)

    # Compute cosine similarity
    dot_product = np.dot(prob_dist1_arr, prob_dist2_arr)
    norm_prob_dist1 = np.linalg.norm(prob_dist1_arr)
    norm_prob_dist2 = np.linalg.norm(prob_dist2_arr)
    
    # Avoid division by zero
    if norm_prob_dist1 == 0 or norm_prob_dist2 == 0:
        return 0.0
    
    cosine_similarity = dot_product / (norm_prob_dist1 * norm_prob_dist2)

    return cosine_similarity

def total_cosine_similarity(prob_dicts, calc="avg"):
    """
    Calculate the cosine similarity across an array of probability dictionaries.

    Arguments:
    prob_dicts -- Array of probability dictionaries
    calc -- Calculation method: 'avg' for average, 'sum' for sum

    Returns:
    cosine_similarity_value -- Cosine similarity value
    """
    num_dicts = len(prob_dicts)
    total_cosine_similarity = 0.0
    total_pairs = 0

    # Calculate cosine similarity for all pairs of probability distributions
    for i in range(num_dicts):
        for j in range(num_dicts):
            if i != j:
                # Get unique tokens from both probability distributions
                all_tokens = set(prob_dicts[i].keys()) | set(prob_dicts[j].keys())
                
                # Convert probability distributions to numpy arrays
                prob_dist1_arr = np.array([prob_dicts[i][token] if token in prob_dicts[i] else 0 for token in all_tokens])
                prob_dist2_arr = np.array([prob_dicts[j][token] if token in prob_dicts[j] else 0 for token in all_tokens])

                # Compute cosine similarity
                dot_product = np.dot(prob_dist1_arr, prob_dist2_arr)
                norm_prob_dist1 = np.linalg.norm(prob_dist1_arr)
                norm_prob_dist2 = np.linalg.norm(prob_dist2_arr)
                cosine_similarity = dot_product / (norm_prob_dist1 * norm_prob_dist2)

                total_cosine_similarity += cosine_similarity
                total_pairs += 1

    if calc == 'sum':
        return total_cosine_similarity
    elif calc == 'avg': 
        avg_cosine_similarity = total_cosine_similarity / total_pairs if total_pairs > 0 else 0.0
        return avg_cosine_similarity
    else:
        raise ValueError("Invalid calculation method. Use 'sum' or 'avg'.")

def jaccard_similarity(prob_dict1, prob_dict2):
    """
    Calculate the Jaccard similarity between two probability dictionaries.

    Arguments:
    prob_dict1 -- First probability dictionary
    prob_dict2 -- Second probability dictionary

    Returns:
    jaccard_similarity -- Jaccard similarity between the probability distributions
    """
    # Get unique tokens from both probability distributions
    tokens1 = set(prob_dict1.keys())
    tokens2 = set(prob_dict2.keys())
    
    # Compute intersection and union of tokens
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    
    # Calculate Jaccard similarity
    jaccard_similarity = len(intersection) / len(union)

    return jaccard_similarity

def total_jaccard_similarity(prob_dicts, calc='avg'):
    """
    Calculate the Jaccard similarity across an array of probability dictionaries.

    Arguments:
    prob_dicts -- Array of probability dictionaries
    calc -- Calculation method: 'sum' for summing similarities, 'avg' for average (default: 'avg')

    Returns:
    jaccard_similarity -- Total or average Jaccard similarity
    """
    num_dicts = len(prob_dicts)
    total_jaccard_similarity = 0.0
    total_pairs = 0

    # Calculate Jaccard similarity for all pairs of probability dictionaries
    for i in range(num_dicts):
        for j in range(i + 1, num_dicts):  # Avoid comparing the same pairs again
            tokens1 = set(prob_dicts[i].keys())
            tokens2 = set(prob_dicts[j].keys())
            
            # Compute intersection and union of tokens
            intersection = len(tokens1.intersection(tokens2))
            union = len(tokens1.union(tokens2))
            
            # Calculate Jaccard similarity
            if union != 0:
                jaccard_similarity = intersection / union
                total_jaccard_similarity += jaccard_similarity
                total_pairs += 1

    if calc == 'sum':
        return total_jaccard_similarity
    elif calc == 'avg': 
        avg_jaccard_similarity = total_jaccard_similarity / total_pairs if total_pairs > 0 else 0.0
        return avg_jaccard_similarity
    else:
        raise ValueError("Invalid calculation method. Use 'sum' or 'avg'.")   
    
def levenshtein_distance(prob_dict_p, prob_dict_q):
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

def total_levenshtein_distance(prob_dicts, calc='avg'):
    """
    Calculate the Levenshtein distance between strings represented by probability distributions in an array.

    Arguments:
    prob_dicts -- Array of probability dictionaries
    calc -- Calculation method: 'sum' for summing similarities, 'avg' for average (default: 'avg')

    Returns:
    weighted_distance -- Sum or average levenshtein distances across the probability distributions
    """
    num_dicts = len(prob_dicts)
    total_weighted_distance = 0.0
    total_pairs = 0

    # Calculate Levenshtein distance for all pairs of probability dictionaries
    for i in range(num_dicts):
        for j in range(i + 1, num_dicts):  # Avoid comparing the same pairs again
            weighted_distance = levenshtein_distance(prob_dicts[i], prob_dicts[j])
            total_weighted_distance += weighted_distance
            total_pairs += 1

    if calc == 'sum':
        return total_weighted_distance
    elif calc == 'avg': 
        avg_weighted_distance = total_weighted_distance / total_pairs if total_pairs > 0 else float('inf')
        return avg_weighted_distance
    else:
        raise ValueError("Invalid calculation method. Use 'sum' or 'avg'.") 

# Sørensen-Dice Coefficient
def sorensen_dice_coefficient(prob_dict_p, prob_dict_q):
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

def total_sorensen_dice_coefficient(prob_dicts, calc='avg'):
    """
    Calculate the Sørensen–Dice coefficient across an array of probability dictionaries.

    Arguments:
    prob_dicts -- Array of probability dictionaries
    calc -- Calculation method: 'sum' for summing coefficients, 'avg' for average (default: 'avg')

    Returns:
    dice_coefficient -- Sum or average Sørensen–Dice coefficient
    """
    num_dicts = len(prob_dicts)
    total_dice_coefficient = 0.0
    total_pairs = 0

    # Calculate Sørensen–Dice coefficient for all pairs of probability dictionaries
    for i in range(num_dicts):
        for j in range(i + 1, num_dicts):  # Avoid comparing the same pairs again
            tokens1 = set(prob_dicts[i].keys())
            tokens2 = set(prob_dicts[j].keys())
            
            # Calculate intersection and sizes of token sets
            intersection = len(tokens1.intersection(tokens2))
            size_tokens1 = len(tokens1)
            size_tokens2 = len(tokens2)
            
            # Calculate Dice coefficient
            if size_tokens1 + size_tokens2 != 0:
                dice_coefficient = (2.0 * intersection) / (size_tokens1 + size_tokens2)
                total_dice_coefficient += dice_coefficient
                total_pairs += 1

    if calc == 'sum':
        return total_dice_coefficient
    elif calc == 'avg': 
        avg_dice_coefficient = total_dice_coefficient / total_pairs if total_pairs > 0 else 0.0
        return avg_dice_coefficient
    else:
        raise ValueError("Invalid calculation method. Use 'sum' or 'avg'.") 

# Conditional Entropy with epilson protection
def conditional_entropy(prob_dict_p, prob_dict_q, epsilon=1e-10):
    """
    Calculate the conditional entropy between two probability distributions.

    Arguments:
    prob_dict_p -- First probability dictionary
    prob_dict_q -- Second probability dictionary
    epsilon -- Smoothing parameter to avoid division by zero (default: 1e-10)

    Returns:
    conditional_entropy_val -- Conditional entropy between the probability distributions
    """
    # Compute frequency distributions of tokens in both probability dictionaries
    freq_dist_p = Counter(prob_dict_p.keys())
    freq_dist_q = Counter(prob_dict_q.keys())
    
    # Get unique tokens from both frequency distributions
    all_tokens = set(freq_dist_p.keys()) | set(freq_dist_q.keys())
    
    # Compute probability distributions
    total_tokens_p = sum(freq_dist_p.values())
    total_tokens_q = sum(freq_dist_q.values())
    
    # Initialize conditional probability distribution P(tokens_p | tokens_q)
    conditional_prob_dist = np.zeros(len(all_tokens))
    
    # Compute conditional probabilities and fill the conditional probability distribution
    for i, token in enumerate(all_tokens):
        prob_token_p = freq_dist_p.get(token, 0) / total_tokens_p
        prob_token_q = freq_dist_q.get(token, 0) / total_tokens_q
        
        if prob_token_q != 0:
            conditional_prob_dist[i] = prob_token_p / prob_token_q
    
    # Handle zero probabilities (add epsilon to avoid division by zero)
    conditional_prob_dist += epsilon
    
    # Compute conditional entropy
    conditional_entropy_val = -np.sum(conditional_prob_dist * np.log2(conditional_prob_dist))
    
    return conditional_entropy_val

def total_conditional_entropy(prob_dicts, epsilon=1e-10, calc='avg'):
    """
    Calculate the conditional entropy across an array of probability distributions.

    Arguments:
    prob_dicts -- Array of probability dictionaries
    epsilon -- Smoothing parameter to avoid division by zero (default: 1e-10)
    calc -- Calculation method: 'sum' for summing coefficients, 'avg' for average (default: 'avg')

    Returns:
    conditional_entropy -- Sum or average conditional entropy
    """
    num_dicts = len(prob_dicts)
    total_conditional_entropy = 0.0
    total_pairs = 0

    # Calculate conditional entropy for all pairs of probability dictionaries
    for i in range(num_dicts):
        for j in range(num_dicts):
            if i != j:
                # Compute frequency distributions of tokens in both probability dictionaries
                freq_dist_p = Counter(prob_dicts[i].keys())
                freq_dist_q = Counter(prob_dicts[j].keys())
                
                # Get unique tokens from both frequency distributions
                all_tokens = set(freq_dist_p.keys()) | set(freq_dist_q.keys())
                
                # Compute probability distributions
                total_tokens_p = sum(freq_dist_p.values())
                total_tokens_q = sum(freq_dist_q.values())
                
                # Initialize conditional probability distribution P(tokens_p | tokens_q)
                conditional_prob_dist = np.zeros(len(all_tokens))
                
                # Compute conditional probabilities and fill the conditional probability distribution
                for k, token in enumerate(all_tokens):
                    prob_token_p = freq_dist_p.get(token, 0) / total_tokens_p
                    prob_token_q = freq_dist_q.get(token, 0) / total_tokens_q
                    
                    if prob_token_q != 0:
                        conditional_prob_dist[k] = prob_token_p / prob_token_q
                
                # Handle zero probabilities (add epsilon to avoid division by zero)
                conditional_prob_dist += epsilon
                
                # Compute conditional entropy
                conditional_entropy_val = -np.sum(conditional_prob_dist * np.log2(conditional_prob_dist))
                total_conditional_entropy += conditional_entropy_val
                total_pairs += 1

    if calc == 'sum':
        return total_conditional_entropy
    elif calc == 'avg': 
        avg_conditional_entropy = total_conditional_entropy / total_pairs if total_pairs > 0 else 0.0
        return avg_conditional_entropy
    else:
        raise ValueError("Invalid calculation method. Use 'sum' or 'avg'.")    

'''
# Example usage:
p = "I like to read books"
q = "She is reading books"
r = "They enjoy reading novels everyday."

p_dict = calculate_prob_distribution(p.split())
q_dict = calculate_prob_distribution(q.split())
r_dict = calculate_prob_distribution(q.split())

p_prob = dict_to_array(p_dict)
q_prob = dict_to_array(q_dict)
r_prob = dict_to_array(r_dict)
pqr_probs = [p_dict, q_dict, r_dict]

print(f"p distribution = {p_prob}")
print(f"q distribution = {q_prob}")
print(f"r distribution = {r_prob}")

print("ENTROPY METHODS:")
print(f"\tShannon Entropy: {shannon_entropy(p_prob)}")
print(f"\tRenyi Entropy: {renyi_entropy(p_prob, alpha = 1)}")
print(f"\tCross Entropy: {cross_entropy(p_dict, q_dict)}")
print(f"\tKL Divergence: {kl_divergence(p_dict, q_dict)}")
print(f"\tConditional Entropy: {conditional_entropy(p_dict, q_dict)}")

print("SIMILARITY METHODS:")
print(f"\tCosine Similarity: {cosine_similarity(p_dict, q_dict)}")
print(f"\tJaccard Similarity: {jaccard_similarity(p_dict, q_dict)}")
print(f"\tLevenshtein Distance: {levenshtein_distance(p_dict, q_dict)}")
print(f"\tDice Coefficient: {sorensen_dice_coefficient(p_dict, q_dict)}")

print("MULTI-DISTRIBUTIONS INPUT:")
print(f"\tSum Cross Entropy: {total_cross_entropy(pqr_probs, calc='sum')}")
print(f"\tAvg Cross Entropy: {total_cross_entropy(pqr_probs, calc='avg')}")
print(f"\tSum KL Divergence: {total_kl_divergence(pqr_probs, calc='sum')}")
print(f"\tAvg KL Divergence: {total_kl_divergence(pqr_probs, calc='avg')}")
print(f"\tSum Cosine: {total_cosine_similarity(pqr_probs, calc='sum')}")
print(f"\tAvg Cosine: {total_cosine_similarity(pqr_probs, calc='avg')}")
print(f"\tSum Jaccard: {total_jaccard_similarity(pqr_probs, calc='sum')}")
print(f"\tAvg Jaccard: {total_jaccard_similarity(pqr_probs, calc='avg')}")
print(f"\tSum Levenshtein: {total_levenshtein_distance(pqr_probs, calc='sum')}")
print(f"\tAvg Levenshtein: {total_levenshtein_distance(pqr_probs, calc='avg')}")
print(f"\tSum Sorensen Dice: {total_sorensen_dice_coefficient(pqr_probs, calc='sum')}")
print(f"\tAvg Sorensen Dice: {total_sorensen_dice_coefficient(pqr_probs, calc='avg')}")
print(f"\tSum Conditional Entropy: {total_conditional_entropy(pqr_probs, calc='sum')}")
print(f"\tAvg Conditional Entropy: {total_conditional_entropy(pqr_probs, calc='avg')}")
'''