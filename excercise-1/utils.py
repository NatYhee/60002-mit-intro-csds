import math


def greedy_gen_trasport_trip(sorted_dict_cow:dict, limit_weight:int) -> list:
    """
    Using greedy algorithm to generate trip for cows transportion which 
    the total weight of cows need to be less that the pre-determined limit weight

    Parameters:
    - sorted_dict_cow: dictionary of cows sorted by its weight. Having key as cow's name while its weight as value 
    - limit_weight: integer value of total weight of cows that can be carried per trip 

    Returns:
    A list of cows' name in the trip selected by greedy algorithm
    """
    trip = []
    total_trip_weight = 0

    for cow in sorted_dict_cow.keys():
        if total_trip_weight + sorted_dict_cow[cow] <= limit_weight:
            trip.append(cow)
            total_trip_weight += sorted_dict_cow[cow]
    
    return trip


def delete_transported_cows(sorted_dict_cow:dict, transported_cows:list) -> None:
    """
    Elimination cows name that already transported from dictionary of all cows

    Parameters:
    - sorted_dict_cow: dictionary of cows sorted by its weight. Having key as cow's name while its weight as value 
    - transported_cows: list of cow's name transported in the trip
    """
    for cow in transported_cows:
        del sorted_dict_cow[cow]


def is_trip_feasible(possible_combination_trip:list, cows:dict, weight_limit:int) -> bool:
    """
    Verify whether the combination of trip is feasible or not

    Parameters:
    - all_possible_trip (list): list of possible combination trip (list of trip(list))
    - cows (dict): a dictionary of name (string), weight (int) pairs
    - weight_limit (int): integer value of total weight of cows that can be carried per trip

    Returns:
    - feasibility_check(bool): Boolean value that represent whether the combination of trip is feasible or not
    """
    feasibility_check = True

    for trip in possible_combination_trip:
        trip_weight = 0

        for cow_name in trip:
            trip_weight += cows[cow_name]
        
            if trip_weight > weight_limit:
                feasibility_check = False
                break
        
        if feasibility_check == False:
            break
    
    return feasibility_check


def record_dict_trip_with_cost(possible_combination_trip:list, dict_trip_cost_detail:dict) -> dict:
    """
    Create dictionary contains with 'trip cost'(number of round) as key and 'trip detail' as value

    Parameters:
    - possible_combination_trip (list): list of all trip that feasible in terms of weight per trip round
    - dict_trip_cost_detail (dict): dictionary contains with 'trip cost'(number of round) as key and 'trip detail' as value

    Returns:
    - dict_trip_cost_detail (dict): update dictionary contains with 'trip cost'(number of round) as key and 'trip detail' as value
    """
    trip_cost = len(possible_combination_trip)

    if trip_cost not in dict_trip_cost_detail.keys():
        dict_trip_cost_detail[trip_cost] = [possible_combination_trip]
    else:
        dict_trip_cost_detail[trip_cost].append(possible_combination_trip)
    
    return dict_trip_cost_detail


def get_available_egg_for_knapsack(egg_weights: tuple, target_weight:int) -> list:
    """
    Create list that contains with all possible optiona that can be select to store in knapsack

    Parameters:
    - egg_weights (tuple): tuple contain type of egg weight (with assumption of unlimit amount per 'weights')
    - target_weight (int): total weight of egg that can be carry per transportation

    Returns:
    - ls_egg_for_knapsack (list): list of available egg to put in knapsack. Its weight value represent an identity of individual egg
    """

    ls_egg_for_knapsack = []

    for weight in egg_weights:

        max_possible_amount = int(math.floor(target_weight/weight))
        egg_for_knapsack = [weight for _ in range(max_possible_amount)]
        ls_egg_for_knapsack.extend(egg_for_knapsack)
        
    return ls_egg_for_knapsack