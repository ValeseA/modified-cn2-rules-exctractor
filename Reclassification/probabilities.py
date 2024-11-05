import numpy as np

def probabilistic_sum(prob1, prob2):
    """
    Combines two probabilities using limited probabilistic sum.
    
    This method ensures that the combined probability does not exceed 1.
    """
    return prob1 + prob2 - prob1 * prob2

def normalized_probabilistic_sum(probs):
    """
    Combines probabilities using normalized probabilistic sum.
    
    This method normalizes the sum of the probabilities to ensure that
    the result does not exceed 1 and that all true conditions lead 
    to a combined probability of 1.
    """
    combined_prob = sum(probs)
    n = len(probs)
    if combined_prob > n:
        combined_prob = n
    return combined_prob / n

def s_curve_combine(probs):
    """
    Combines probabilities using S-Curve method.
    
    This method calculates the product of the complementary probabilities
    and subtracts it from 1, ensuring that the combined probability increases
    significantly with more true conditions.
    """
    product_complement = np.prod([1 - p for p in probs])
    return 1 - product_complement

def modified_s_curve_combine(probs, validities):
    """
    Combines probabilities using a modified S-Curve.
    
    :param probs: List of probabilities.
    :param validities: List of booleans indicating if a probability is valid.
    :return: Combined probability.
    """
    if len(probs) != len(validities):
        raise ValueError("Length of probabilities must match the length of validities.")
    
    product_complement_valid = np.prod([1 - p if valid else 1 + p for p, valid in zip(probs, validities)])
    return 1 - product_complement_valid

def normalized_probabilistic_sum_with_validity(probs, validities):
    """
    Combines probabilities using a modified normalized probabilistic sum.
    
    :param probs: List of probabilities.
    :param validities: List of booleans indicating if a probability is valid.
    :return: Combined probability.
    """
    if len(probs) != len(validities):
        raise ValueError("Length of probabilities must match the length of validities.")
    
    adjusted_probs = [(p if valid else 1 - p) for p, valid in zip(probs, validities)]
    combined_prob = sum(adjusted_probs)
    n = len(adjusted_probs)
    if combined_prob > n:
        combined_prob = n
    return combined_prob / n

def new_prob(probs, validities):
    """
    Combines probabilities using a new approach with validity.
    
    :param probs: List of probabilities.
    :param validities: List of booleans indicating if a probability is valid.
    :return: Combined probability.
    """
    if len(probs) != len(validities):
        raise ValueError("Length of probabilities must match the length of validities.")

    val = sum(validities)  # Count of valid probabilities
    unval = len(validities) - val  # Count of invalid probabilities
    
    # Calculate combined probability for valid conditions
    product_complement_valid = np.prod([1 - p for p, valid in zip(probs, validities) if valid])
    combined_prob1 = 1 - product_complement_valid

    # Calculate combined probability for invalid conditions
    adjusted_probs = [1 - p for p, valid in zip(probs, validities) if not valid]
    combined_prob2 = sum(adjusted_probs)
    if unval > 0:
        combined_prob2 /= unval
    else:
        combined_prob2 = 0  # Avoid division by zero if there are no invalid probabilities

    # Final combined probability
    combined_prob = (combined_prob1 * val + combined_prob2 * unval) / (val + unval)
    return combined_prob

def main():
    # Individual probabilities
    prob_sex_woman = 0.80
    prob_civically_engaged = 0.70
    prob_another_condition = 0.90

    # Example for probabilistic sum
    combined_prob_sum = probabilistic_sum(prob_sex_woman, prob_civically_engaged)
    print(f"Combination (Limited Probabilistic Sum): {combined_prob_sum}")

    # Example for normalized probabilistic sum
    combined_prob_normalized = normalized_probabilistic_sum([prob_sex_woman, prob_civically_engaged, prob_another_condition])
    print(f"Combination (Normalized Probabilistic Sum): {combined_prob_normalized}")

    # Example for S-Curve combination
    combined_prob_s_curve = s_curve_combine([prob_sex_woman, prob_civically_engaged, prob_another_condition])
    print(f"Combination (S-Curve): {combined_prob_s_curve}")

    # Example for modified S-Curve combination
    validities = [True, True, False]  # Last condition is not valid
    combined_prob_modified_s_curve = modified_s_curve_combine([prob_sex_woman, prob_civically_engaged, prob_another_condition], validities)
    print(f"Combination (Modified S-Curve): {combined_prob_modified_s_curve}")

    # Example for normalized probabilistic sum with validity
    combined_prob_norm_with_validity = normalized_probabilistic_sum_with_validity(
        [prob_sex_woman, prob_civically_engaged, prob_another_condition], [True, True, False]
    )
    print(f"Combination (Normalized Probabilistic Sum with Validity): {combined_prob_norm_with_validity}")

    # Example for new probability approach
    combined_prob_new = new_prob([prob_sex_woman, prob_civically_engaged, prob_another_condition], [True, True, False])
    print(f"Combination (New Probability): {combined_prob_new}")

if __name__ == "__main__":
    main()
