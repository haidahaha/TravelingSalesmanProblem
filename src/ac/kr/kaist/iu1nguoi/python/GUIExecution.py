from ac.kr.kaist.iu1nguoi.python.TravelingSalesmanProblem import *
from ac.kr.kaist.iu1nguoi.python.TravelingSalesmanProblemGUI import *

speed = 1000
height = 500
width = 700
cities = 30
mutationFactor = 0.5
time = 120

tsp = TravelingSalesmanProblem(cities,height, width, time)
gui = TravelingSalesmanProblemGUI(tsp, speed, height, width)
routes, utility, distance, elapsedTime = tsp.performEvolution(100, 49, 50, mutationFactor)
print "Routes : "
currentCity = 0
for itr in range(len(routes.keys())):
    print currentCity,
    currentCity = routes[currentCity]
print
print "Distance : ", distance
print "Elaspsed time : ", elapsedTime, "secs"                
