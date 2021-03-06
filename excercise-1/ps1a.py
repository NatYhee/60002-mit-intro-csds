###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:
import copy
import time

from ps1_partition import get_partitions
from utils import greedy_gen_trasport_trip, delete_transported_cows, is_trip_feasible, record_dict_trip_with_cost

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename:str) -> dict:
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    dict_of_cow = {}

    with open(filename, 'r') as open_file:
        content = open_file.read()
    
    ls_line = content.split('\n')

    for line in ls_line:
        ls_context = line.split(',')
        dict_of_cow[ls_context[0]] =  int(ls_context[1])

    return dict_of_cow

# Problem 2
def greedy_cow_transport(cows:dict, limit:int=10) -> list:
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    dict_transport_cow = copy.deepcopy(cows)
    sorted_dict_transport_cow = dict(sorted(dict_transport_cow.items(), key=lambda item_cow: item_cow[1], reverse=True))

    ls_all_trip = []

    while len(sorted_dict_transport_cow.keys()) > 0:

        trip = greedy_gen_trasport_trip(sorted_dict_cow=sorted_dict_transport_cow, limit_weight=limit)
        ls_all_trip.append(trip)

        delete_transported_cows(sorted_dict_cow=sorted_dict_transport_cow, transported_cows=trip)

    print(f"Greedy: minimum number of trip from greedy is {str(len(ls_all_trip))}")

    return ls_all_trip

# Problem 3
def brute_force_cow_transport(cows:dict, limit:int=10) -> list:
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #Using get_partitions module will provide all passible trip
    all_possible_combination_trip = get_partitions(cows)
    dict_trip_cost_detail = {}

    #Create dictionary of number of trip and trip detail combination
    for possible_combination_trip in all_possible_combination_trip:
        if is_trip_feasible(possible_combination_trip=possible_combination_trip, cows=cows, weight_limit=limit):
            record_dict_trip_with_cost(possible_combination_trip=possible_combination_trip, dict_trip_cost_detail=dict_trip_cost_detail)

    #Finding mininum cost of trip (least number of trip)
    min_trip_cost = min(list(dict_trip_cost_detail.keys()))
    ls_trip_detail_least_cost = dict_trip_cost_detail[min_trip_cost]
    print(f"Brute Force: minimum number of trip from brute force is {str(min_trip_cost)}")

    return ls_trip_detail_least_cost

            
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    dict_cows_info = load_cows('ps1_cow_data.txt')
    
    greedy_start = time.time()
    greedy_result = greedy_cow_transport(cows=dict_cows_info)
    greedy_end = time.time()
    greedy_execution_time = greedy_end - greedy_start
    print(f"greedy take time {str(greedy_execution_time)}")
    print(greedy_result)

    bruteforce_start = time.time()
    bruteforce_result = brute_force_cow_transport(cows=dict_cows_info)
    bruteforce_end = time.time()
    bruteforce_execution_time = bruteforce_end - bruteforce_start
    print(f"greedy take time {str(bruteforce_execution_time)}")
    print(bruteforce_result)

if __name__ == "__main__":
    compare_cow_transport_algorithms()
