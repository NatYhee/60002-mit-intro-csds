# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge
from utils import textfile_to_list

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    digraph = Digraph()

    ls_line = textfile_to_list(map_filename)

    for line in ls_line:

        if line == '':
            pass

        key_info = ['source', 'destination', 'totalEdge', 'outdoor']
        value_info = line.split(' ')
        dict_graph = dict(zip(key_info, value_info))

        src_node = Node(name=dict_graph['source'])
        dest_node = Node(name=dict_graph['destination'])

        if not digraph.has_node(src_node):
            digraph.add_node(src_node)
        if not digraph.has_node(dest_node):
            digraph.add_node(dest_node)

        digraph.add_edge(
            WeightedEdge(src=src_node,\
                dest=dest_node,\
                total_distance=int(dict_graph['totalEdge']),\
                outdoor_distance=int(dict_graph['outdoor']))\
            )
    
    print("Loading map from file...")
    
    return digraph

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#

# Problem 3b: Implement get_best_path
def get_distance(digraph, path):
    """
    Finding total distance and outdoor distance by retriving the number from created class

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        path: list composed of [[list of node]
            list of Nodename
    
    Returns:
        - totalDistance: float
            The total distance from initiated node to destination node
        - totalOutdoor: float
            The total outdoor distance from initiated node to destination node
    """
    lsTravelPath = path
    totalDistance = 0
    totalOutdoor = 0

    for numPath in range(len(lsTravelPath)):
        if numPath == (len(lsTravelPath) - 1):
            pass
        else:
            for edge in digraph.get_edges_for_node(lsTravelPath[numPath]):
                if edge.get_destination() == lsTravelPath[numPath + 1]:
                    totalDistance += edge.get_total_distance()
                    totalOutdoor += edge.get_outdoor_distance()
    return totalDistance, totalOutdoor
    
    
def get_best_path(digraph:object, start:object, end:object, path:list, max_dist_outdoors:int, best_dist:int,
                  best_path:list, distance=0, outdoor=0):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of node]
            list of Nodename
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    path = path + [start]

    if not digraph.has_node(start) or not digraph.has_node(end):
        raise ValueError('Verify Node start and end')
    elif start == end:
        #When arriving destination node
        return path
    else:
        for nodeEdge in digraph.get_edges_for_node(start):
            #destination can not be duplicate with the path that already pass
            if nodeEdge.get_destination() not in path:
                    #destination of edge is new source of next traveling
                    new_src = nodeEdge.get_destination()

                    newBestPath = get_best_path(digraph=digraph, start=new_src, end=end, path=path, 
                                                max_dist_outdoors=max_dist_outdoors,\
                                                best_dist=best_dist, best_path=best_path)
                    
                    if newBestPath != None:
                        """
                        best_path will be a return for even a parent node of direction that lead to get_destination
                        To get the total distance and outdoor, we need to cal the distance with full path that lead to destination.

                        Need to cal after recursion to get the result of fullpath instead of only number before entering to recursion
                        """
                        totalDistance, totalOutdoor = get_distance(digraph, newBestPath)

                        if totalDistance <= best_dist and totalOutdoor <= max_dist_outdoors:
                            best_path = newBestPath
                            best_dist = totalDistance

    return best_path

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph:object, start:str, end:str, max_total_dist:int, max_dist_outdoors:int):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    start_node = Node(start)
    end_node = Node(end)
    shortest_path_node = get_best_path(digraph=digraph, start=start_node, end=end_node, path=[],\
                            max_dist_outdoors=max_dist_outdoors, best_dist=max_total_dist, best_path=None)

    if shortest_path_node is None:
        raise ValueError
    
    shortest_path = [node.get_name() for node in shortest_path_node]

    return shortest_path






# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()

    # graph = load_map('test_map.txt')
    # print(directed_dfs(digraph=graph, start='1', end='3', max_total_dist=20, max_dist_outdoors=5))
