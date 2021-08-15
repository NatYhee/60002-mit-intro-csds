###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================
from typing import Tuple
from utils import get_available_egg_for_knapsack, put_item_in_knapsack

# Problem 1
def dp_make_weight(egg_weights:tuple, target_weight:int, memo:dict = {}) -> int:
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    ls_egg_for_knapsack = get_available_egg_for_knapsack(egg_weights=egg_weights, target_weight=target_weight)
    num_eggs, selectedEggs = put_item_in_knapsack(ls_for_knapsack=ls_egg_for_knapsack, target_weight=target_weight, memo=memo)
    print(f"Detail of eggs selected in the basket: {selectedEggs}")

    return num_eggs


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = ( 1, 5, 10, 25)
    n = 99
    # print("Egg weights = (1, 5, 10, 25)")
    # print("n = 99")
    # print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    # print()

    print(dp_make_weight(egg_weights=egg_weights, target_weight=n))