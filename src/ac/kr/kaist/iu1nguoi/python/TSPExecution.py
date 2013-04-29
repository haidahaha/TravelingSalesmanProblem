from ac.kr.kaist.iu1nguoi.python.TravelingSalesmanProblem import *

mutationFactor = 0.01
time = 180


tsp = TravelingSalesmanProblem(time)
routes, utility, distance, elapsedTime = tsp.performEvolution(60, 100, mutationFactor)
print "Routes : "
currentCity = 0
for itr in range(len(routes.keys())):
    print currentCity,
    currentCity = routes[currentCity]
print
print "Distance : ", distance
print "Elapsed time : ", elapsedTime, "secs"

'''

for i in range(5):
    f = open('test0' + str(i) + '.txt', 'a')
    tsp = TravelingSalesmanProblem(time)
    routes, utility, distance, elapsedTime = tsp.performEvolution(60, 100, mutationFactor)
    f.write(str(i) + ' ' + str(distance) + '\t' + str(elapsedTime) + 'secs' + '\n')
    f.close()

'''
