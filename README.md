                                                    

(1) Which search algorithm seems to work best for each routing options?
Heuristics search algorithm works best for each routing algorithm. As the heuristics function takes into account an estimated cost to reach the goal state
rather than considering only the cost to the next hop which might result in a nonoptimal answer.

(2) Which algorithm is fastest in terms of the amount of computation time required by your the program, and by how much, according to your experiments?
bfs: 0m0.174s
dfs: 0m0.184s
uniform: 0m0.198s
heuristics: 0m0.125s
Thus heuristics algorithm takes the least computation time.

(3) Which algorithm requires the least memory, and by how much, according to your experiments?
Bfs requires the maximum memory for its computation. If b is the branching factor and d is the depth of the tree, then bfs requires memory of the order
b^h.

(4) Which heuristic function(s) did you use, how good is it, and how might you make it/them better?
The hueristic function that I used is based on the difference in the geo-cordinates of the source and the destination cities. The distance between 
two points on the earth is calculated using the haversine formula. The haversine formula is as follows-
dlon = lon2 - lon1 
dlat = lat2 - lat1 
a = (sin(dlat/2))^2 + cos(lat1) * cos(lat2) * (sin(dlon/2))^2 
c = 2 * atan2( sqrt(a), sqrt(1-a) ) 
d = R * c (where R is the radius of the Earth)
(Reference: MIT License)

Since the latitude and longitude information of the cities was available from the city-gps.txt, calculating the distance between these cities was way.
However, for junction (geo-coordinates) were not provided. So for these, I made an assumption and took an average of the co-ordinates of the cities
directly connected to the junction.

Moreover, the other assumptions that were made during the implementation of this problem are-
Road segments for which data was not given, I assumed the distance to be 45 and the speed between the segments to be 45 as well.

********************************** Approach to tackle the problem****************************************

While reading the data, I created a dictionary of containing the cities as the keys and their adjoining cities along with the distance and 
the speed. This was done to bring down the time complexity while searching an element through the list. Then I checked for the routing 
algorithm to call the function specific to those and within those functions, I created multiple conditions to check there cost function.

The successor function gives the list of adjoining cities to the current city.
The cost function depends upon the cost function as defined by the user.
The fringe is a list/queue/heapq which contain the successor nodes as returned by the successor function. The fringe contains data in the 
following format [current city, names of cities traversed from starting to this city separated by '=' sign]. The if the goal state is 
reached, the second part of the fringe i.e. names of cities traversed from starting to this city separated by '=' sign is used as a 
key to fetch data from the solutionDict (a dictionary) about the distance traversed from start to the destination city and also the 
time is taken to reach the destination city.
