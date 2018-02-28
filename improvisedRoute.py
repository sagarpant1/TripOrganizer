# put your routing program here!
"""
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

"""

import sys
import heapq
import math
import copy
#import queue to implement priority queue
try:
    import Queue as Q 
except ImportError:
    import queue as Q

#structure for road-segments file data
dict = {}
#structure to store geo-cordinates of cities
gpsDict = {}
#structure to store geo-cordinates of state
stateDict = {}
#check if each state has been visited or not
routeEachStateDict = {}

citiesTraversedCheckList = {}
#this dict stores the path from source to destination, total distance, and the total time taken
solutionDict = {}

#read data from the file
def readData(fileName):
    file = open(fileName, "r")
    #count=0
    for line in file:
	#count+=1
	#if count > 6:
	 #   break;
	populateToDict(line)

def populateToDict(line):
    data = line.split(" ")
    data = appendGenericData(data, len(data))

    populateRoadStructure(data[0], data[1], data[2], data[3], data[4])
	
def appendGenericData(data, len):
    count=0
    for count in range(0,len):
	if data[count] == '' and (count < 2 or count > 3):
	    data[count] = "Unknown Data"
	elif (not data[count]) or data[count] == "0":
	    data[count] = "45"
	count+=1
    return data


#read co-ordinates data from the file
def readGpsData(fileName):
    file = open(fileName, "r")
    #count=0
    for line in file:
        #count+=1
        #if count > 6:
         #   break;
        populateToGpsDict(line)

def populateToGpsDict(line):
    data = line.split(" ")
#    data = appendGenericData(data, len(data))
    populateGpsStructure(data[0], data[1], data[2])
    populateGpsStateStructure(data[0], data[1], data[2])

#convert lat and lon to float and store the data for the state
def populateGpsStateStructure(city, lat, lon):
    state = city.split(",")[1]
    if not state in stateDict:
	stateDict[state] = [1, float(lat), float(lon)]
    else:
	data = stateDict.get(state)
	stateDict[state] = [data[0]+1, data[1]+float(lat), data[2]+float(lon)]

#convert lat and lon into float and store them in a dict
def populateGpsStructure(city, lat, lon):
    gpsDict[city] = [float(lat),float(lon)]

#calculate distance between two geocordinates on the earth
def calDistance(lat1, lat2, lon1, lon2):
    radLat1 = math.radians(lat1)
    radLat2 = math.radians(lat2)
    radLon1 = math.radians(lon1)
    radLon2 = math.radians(lon2)
    diffLat = radLat2-radLat1
    diffLon = radLon2-radLon1
    aConstant = math.pow((math.sin(diffLat/2)),2) + (math.cos(radLat1)*math.cos(radLat2)*math.pow((math.sin(diffLon/2)),2))
    spatialDistance = 6371 * 2 * math.atan2(math.sqrt(aConstant), math.sqrt(1-aConstant))
    return spatialDistance

def populateRoadStructure(city1, city2, length, speed, nameOfHighway):
    list = []
    list.append(city2)
    list.append(int(length))
    list.append(int(speed))
    list.append(nameOfHighway)
    list = [list]
    if city1 in dict:
	value = dict.get(city1)
        value = value + list
	list = value
    dict[city1] = list
    list = []
    list.append(city1)
    list.append(length)
    list.append(speed)
    list.append(nameOfHighway)
    list = [list]
    if city2 in dict:
        value = dict.get(city2)
        value = value + list
        list = value
    dict[city2] = list
    if not city1 in citiesTraversedCheckList:
   	citiesTraversedCheckList[city1] = 0
    if not city2 in citiesTraversedCheckList:
        citiesTraversedCheckList[city2] = 0

    #populate state List for state routing cost function
    populateStateList(city1, city2)

#populate state List for state routing cost function
def populateStateList(city1, city2):
    state1 = city1.split(",")[1]
    state2 = city2.split(",")[1]
    if not state1 in routeEachStateDict:
	routeEachStateDict[state1] = 0
    if not state2 in routeEachStateDict:
	routeEachStateDict[state2] = 0

#succesor function to calculate to the next hop from the current cities
def successorForHeuristics(sCity, str1):
    finalList=[]
    list = dict.get(sCity)
    for item in list:
	if item[0] not in str1:
	    finalList = finalList + [item]
    return finalList

def successor(sCity):
    finalList=[]
    list = dict.get(sCity)
    for item in list:
        if citiesTraversedCheckList.get(item[0]) != 1:
            finalList = finalList + [item]
    return finalList
#successor for uniform
def successorForUniform(sCity, localDict):
    finalList=[]
    print "localDictinUniform"
    print localDict
    list = dict.get(sCity)
    for item in list:
	print item[0]
        if localDict.get(item[0]) != 1:
            finalList = finalList + [item]
    return finalList


####print the result in the specified manner
"""def organisedPrint(solution, costfunction):
    if costFunction == "segments":
	route = sortBySegment(solution)
    elif costFunction == "distance":
	rote = sortByDistance(solution)
    else:
	route = sortByTime(solution)
"""
#sort the solution based on number of segments
"""def sortBySegment(sol):
    minSegmentLength = 9999999
    for item in sol:
	if minSegmentLength > len(item[1].split("-")):
	    minLengthRoute = item
	    minSegmentLength = len(item[1].split("-"))
"""

#sort the solution based on the shortest distance
"""def sortByDistance(sol):
    minDistance = 9999999
    for item in sol:
        if minDistance > solutionDict.get(item[1])[0]:
            minLengthRoute = item
	    minDistannce = 
"""

#sort the solution based on the shortest time
"""def sortByTime(sol):
    minSegmentLength = 9999999
    for item in sol:
        if minSegmentLength > len(item[1].split("-"))
            minLengthRoute = item
"""

def checkForEachState(solution):
    stateVisitedCount=0
    cityCount=0
    cities = solution[0][1].split("=")
    while cityCount < len(cities):
	state = cities[cityCount].split(",")[1]
	if routeEachStateDict.get(state) == 0:
	    routeEachStateDict[state] = 1
	    stateVisitedCount+=1
	cityCount+=1
    #print stateVisitedCount
    if stateVisitedCount == 48:
	return True
    else:
	routeEachStateDict.fromkeys(routeEachStateDict, 0)
	return False
    

#add city to the visited list
def addCityToVisitedList(city):
    citiesTraversedCheckList[city] = 1


#add city to the visited List for Uniform
def addCityToVisitedListUniform(dict, city):
    dict[city] = 1

#solve function initiated
def solve(startCity, destCity, routingAlgo):
    routeHops = []
    routingHopsSolution = []
    routeHops = routeHops + [[startCity, startCity]]
    solutionDict[startCity] = [0, 0]
    addCityToVisitedList(startCity)
    if startCity == destCity:
	routingHopsSolution = routeHops
	return routingHopsSolution 
    while len(routeHops) > 0:
    	if routingAlgo == "bfs":
	    poppedItem = routeHops.pop(0)
	elif routingAlgo == "dfs":
	    poppedItem = routeHops.pop()
	successorList = successor(poppedItem[0])
	if len(successorList) > 0:
	    for item in successorList:
		routeHops = routeHops + [[item[0], poppedItem[1]+"="+item[0]]]
	        addCityToVisitedList(item[0])
	    	distAndTimeUntilNow = solutionDict.get(poppedItem[1])
	    	solutionDict[poppedItem[1]+"="+item[0]] = [distAndTimeUntilNow[0]+int(item[1]), distAndTimeUntilNow[1] + (int(item[1])/int(item[2]))]
		#solutionDict[poppedItem[1]+"-"+item[0]] = [distAndTimeUntilNow[0]+item[1], distAndTimeUntilNow + item[1]/item[2]]            
	    	if checkGoal(item[0], destCity):
	            routingHopsSolution = routingHopsSolution + [[item[0], poppedItem[1]+"="+item[0]]]
		    return routingHopsSolution

#solving for uniform search routing algorithm
def solveForUniform(startCity, destCity, routingAlgo,costFunction):
    routeHops = []
    routingHopsSolution = []
    #print localDict.get(startCity)
    heapq.heappush(routeHops, (0,[[startCity, startCity]]))
    solutionDict[startCity] = [0, 0]
    addCityToVisitedList(startCity)
    if startCity == destCity:
        routingHopsSolution = routeHops[1]
        return routingHopsSolution
    while len(routeHops) > 0:
        if routingAlgo == "bfs":
            poppedItem = routeHops.pop(0)
        elif routingAlgo == "dfs":
            poppedItem = routeHops.pop()
	poppedItem = heapq.heappop(routeHops)
	#print poppedItem
	successorList = successor(poppedItem[1][0][0])
        if len(successorList) > 0:
            for item in successorList:
		if costFunction == 'segment':
		    priority = len((poppedItem[1][0][1]+"="+item[0]).split("="))
		elif costFunction == 'distance' or costFunction == 'statetour':
		    distAndTime = solutionDict.get(poppedItem[1][0][1])
		    priority = distAndTime[0] + int(item[1])
		elif costFunction == 'time':
		    distAndTime = solutionDict.get(poppedItem[1][0][1])
		    priority = distAndTime[1] + (1.0* int(item[1])/int(item[2]))
		else:
		    distAndTime = solutionDict.get(poppedItem[1][0][1])
                    priority = -1 * (distAndTime[0] + int(item[1]))
                heapq.heappush(routeHops,(priority,[[item[0], poppedItem[1][0][1]+"="+item[0]]]))
                addCityToVisitedList(item[0])
                distAndTimeUntilNow = solutionDict.get(poppedItem[1][0][1])
                solutionDict[poppedItem[1][0][1]+"="+item[0]] = [distAndTimeUntilNow[0]+int(item[1]), distAndTimeUntilNow[1] + (1.0* int(item[1])/int(item[2]))]
                if (checkGoal(item[0], destCity) and costFunction != 'statetour') or checkGoal(item[0], destCity) and costFunction == 'statetour' and checkForEachState(routingHopsSolution + [[item[0], poppedItem[1][0][1]+"="+item[0]]]):
                    routingHopsSolution = routingHopsSolution + [[item[0], poppedItem[1][0][1]+"="+item[0]]]
                    return routingHopsSolution

#find coordinates for junctions
def checkForCoordinates(city):
    adjoiningCitiesList = dict.get(city)
    lat = 0
    lon = 0
    count =0
    for item in adjoiningCitiesList:
	if item[0] in gpsDict:
	    position = gpsDict.get(item[0])
	    lat = lat + float(position[0])
	    lon = lon + float(position[1])
	    count = count +1;
    if count > 0:
    	return [lat/count, lon/count]
    else:
	return [-200,-200]

#solving for heuristic search routing algorithm
def solveForHeuristic(startCity, destCity, routingAlgo):
    routeHops = []
    coordinates = []
    routingHopsSolution = []
    flag = False
    if startCity in gpsDict:
	originLat = gpsDict.get(startCity)[0]
        originLon = gpsDict.get(startCity)[1]
    else:
        coordinates = checkForCoordinates(startCity)
        if coordinates[0] == -200:
	    flag = True
	else:
	    originLat = coordinates[0]
	    originLon = coordinates[1]
	#originLat = stateDict.get(startCity.split(",")[1])[1]/(stateDict.get(startCity.split(",")[1])[0])
        #originLon = stateDict.get(startCity.split(",")[1])[2]/(stateDict.get(startCity.split(",")[1])[0])

    if destCity in gpsDict:
	destLat = gpsDict.get(destCity)[0]
        destLon = gpsDict.get(destCity)[1]
    else:
        coordinates = checkForCoordinates(destCity)
        if coordinates[0] == -200:
            flag = True
        else:
            originLat = coordinates[0]
            originLon = coordinates[1]
    if flag:
	solveForUniform(startCity, destCity, routingAlgo, "segment")
    else:
	priority = calDistance(originLat, destLat, originLon, destLon)
	heapq.heappush(routeHops, (priority,[[startCity, startCity]]))
        solutionDict[startCity] = [0, 0]
    	addCityToVisitedList(startCity)
    	if startCity == destCity:
            routingHopsSolution = routeHops[1]
            return routingHopsSolution
    	while len(routeHops) > 0:
            if routingAlgo == "bfs":
            	poppedItem = routeHops.pop(0)
            elif routingAlgo == "dfs":
            	poppedItem = routeHops.pop()
            poppedItem = heapq.heappop(routeHops)
            successorList = successorForHeuristics(poppedItem[1][0][0], poppedItem[1][0][1])
            if len(successorList) > 0:
            	for item in successorList:
		    flag = False
		    if item[0] in gpsDict:
		    	stateLat = gpsDict.get(item[0])[0]
                    	stateLon = gpsDict.get(item[0])[1]
		    else:
		        coordinates = checkForCoordinates(item[0])
		        if coordinates[0] == -200:
		            flag = True
		        else:
		            originLat = coordinates[0]
		            originLon = coordinates[1]
		    if flag:
		    	continue
		    priority = calDistance(destLat, stateLat, destLon, stateLon)
		    
		    if costFunction == 'segment':
                        priority = priority + len((poppedItem[1][0][1]+"="+item[0]).split("="))
                    elif costFunction == 'distance' or costFunction == 'statetour':
                        distAndTime = solutionDict.get(poppedItem[1][0][1])
                    	priority = priority + distAndTime[0] + int(item[1])
                    elif costFunction == 'time':
    	                distAndTime = solutionDict.get(poppedItem[1][0][1])
        	        priority = priority + distAndTime[1] + (1.0* int(item[1])/int(item[2]))
                    else:
                    	distAndTime = solutionDict.get(poppedItem[1][0][1])
                    	priority = priority + (-1 * (distAndTime[0] + int(item[1])))

		    heapq.heappush(routeHops,(priority,[[item[0], poppedItem[1][0][1]+"="+item[0]]]))
                    addCityToVisitedList(item[0])
                    distAndTimeUntilNow = solutionDict.get(poppedItem[1][0][1])
                    solutionDict[poppedItem[1][0][1]+"="+item[0]] = [distAndTimeUntilNow[0]+int(item[1]), distAndTimeUntilNow[1] + (1.0* int(item[1])/int(item[2]))]
                    if checkGoal(item[0], destCity):
                    	routingHopsSolution = routingHopsSolution + [[item[0], poppedItem[1][0][1]+"="+item[0]]]
                    	return routingHopsSolution


#check if the destination is reached
def checkGoal(currentCity, goalCity):
    if currentCity == goalCity:
	return True
    else:
	return False

#print output in the desired format
def formatOutput(routingSolution):
    str1 = ""
    str1+=str(solutionDict.get(routingSolution[0][1])[0])+ " "
    str1+=str(solutionDict.get(routingSolution[0][1])[1])+ " "
    citiesList = routingSolution[0][1].split("=")
    count = 0
    while count < len(citiesList):
	str1+=citiesList[count]+" "
	count+=1
    print str1

startCity = str(sys.argv[1])
destCity = str(sys.argv[2])
routingAlgo = str(sys.argv[3])
costFunction = str(sys.argv[4])

#to read data from the file
readData("road-segments.txt")
#print routeEachStateDict
#read data from city gps file only if the routingAlgo is heuristic
readGpsData("city-gps.txt")
#print gpsDict
#initiate solution
if routingAlgo == 'dfs' or routingAlgo == 'bfs':
    routingSolution = solve(startCity, destCity,routingAlgo)
elif routingAlgo == 'uniform':
    routingSolution = solveForUniform(startCity, destCity,routingAlgo,costFunction)
else:
    routingSolution = solveForHeuristic(startCity, destCity,routingAlgo)
#get the fromatted output
formatOutput(routingSolution)
#organisedPrint(routingSolution, costFunction)
####print dict
