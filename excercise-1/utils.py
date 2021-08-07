
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
