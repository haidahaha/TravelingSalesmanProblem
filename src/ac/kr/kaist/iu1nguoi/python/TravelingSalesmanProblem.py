from ac.kr.kaist.iu1nguoi.python.GeneticAlgorithmProblem import *
import random
import math
import time
import csv

class TravelingSalesmanProblem(GeneticAlgorithmProblem):

    genes = []
    dicLocations = {}
    gui = ''
    best = ''
    time = 0

    def __init__(self, time):
        self.time = time

        datasetReader = csv.reader(open('TSP-Open-dataset.csv', 'rb'), delimiter=',')

        cnt = 0
        for row in datasetReader:
            self.dicLocations[cnt] = [float(row[1]), float(row[2])]
            cnt += 1

    def registerGUI(self, gui):
        self.gui = gui

    # calculate 1/distance of a solution. longer distance, lower fitness
    def fitness(self, instance):
        genotype = instance.getGenotype()
        currentCity = 0
        distance = 0.0
        for itr in range(len(genotype) - 1):
            nextCity = genotype[currentCity]
            distance = distance + self.calculateDistance(self.dicLocations[currentCity], self.dicLocations[nextCity])
            currentCity = nextCity
        utility = 10000.0 / distance
        return utility

    def calculateTotalDistance(self, instance):
        genotype = instance.getGenotype()
        currentCity = 0
        distance = 0.0
        for itr in range(len(genotype) - 1):
            nextCity = genotype[currentCity]
            distance = distance + self.calculateDistance(self.dicLocations[currentCity], self.dicLocations[nextCity])
            currentCity = nextCity
        return distance

    def calculateDistance(self, coordinate1, coordinate2):
        distance = math.sqrt(math.pow(coordinate1[0] - coordinate2[0], 2) + math.pow(coordinate1[1] - coordinate2[1], 2))
        return distance

    def performEvolution(self, numOffsprings, numPopulation, mutationFactor):
        if self.gui != '':
            self.gui.start()

        startTime = time.time()
        # population is list of GeneticAlgorithmInstance data type
        population = self.createInitialPopulation(numPopulation, len(self.dicLocations.keys()))
        while True:
            currentTime = time.time()
            if (currentTime - startTime) >= self.time:  # stop when out of time
                break
            offsprings = {}
            for itr2 in range(numOffsprings):
                p1, p2 = self.selectParents(population)
                offsprings[itr2] = self.crossoverParents(p1, p2)
                self.mutation(offsprings[itr2], int(mutationFactor * len(self.dicLocations.keys())))
            self.substritutePopulation(population, offsprings)
            mostFittest = self.findBestSolution(population)
            # print self.fitness(mostFittest)
            # print mostFittest.getGenotype()
            self.best = mostFittest
            if self.gui != '':
                self.gui.update()
        endTime = time.time()
        return self.best.getGenotype(), self.fitness(self.best), self.calculateTotalDistance(self.best), (endTime - startTime)

    def createInitialPopulation(self, numPopulation, numCities):
        population = []
        for itr in range(numPopulation):  # create Population with predefined size
            genotype = range(numCities)  # initialize new genotype (solution)
            while self.isInfeasible(genotype) == False:  # randomize until this genotype is accepted
                random.shuffle(genotype)
            instance = GeneticAlgorithmInstance()
            instance.setGenotype(genotype)
            population.append(instance)  # add this solution to population
        return population

    # check if a genotype is accepted or not
    def isInfeasible(self, genotype):
        currentCity = 0
        visitedCity = {}
        for itr in range(len(genotype)):
            visitedCity[currentCity] = 1
            currentCity = genotype[currentCity]

        if len(visitedCity.keys()) == len(genotype):
            return True
        else:
            return False

    def findBestSolution(self, population):
        idxMaximum = -1
        max = -99999
        for itr in range(len(population)):
            if max < self.fitness(population[itr]):
                max = self.fitness(population[itr])
                idxMaximum = itr
        return population[idxMaximum]

#    def selectParents(self, population):
#        rankFitness = {}
#        originalFitness = {}  # list of solutions' fitness (based on population)
#        maxUtility = -999999
#        minUtility = 999999
#        for itr in range(len(population)):
#            originalFitness[itr] = self.fitness(population[itr])
#            if maxUtility < originalFitness[itr]:
#                maxUtility = originalFitness[itr]
#            if minUtility > originalFitness[itr]:
#                minUtility = originalFitness[itr]
#
#        # asc sort population based on its fitness
#        for itr1 in range(len(population)):
#            for itr2 in range(itr1 + 1, len(population)):
#                if originalFitness[itr1] < originalFitness[itr2]:
#                    originalFitness[itr1], originalFitness[itr2] = originalFitness[itr2], originalFitness[itr1]
#                    population[itr1], population[itr2] = population[itr2], population[itr1]
#
#        # selection using rank-based
#        size = float(len(population))
#        total = 0.0  # sum of rankFitness
#        for itr in range(len(population)):
#            rankFitness[itr] = (maxUtility + (float(itr) - 1.0) * (maxUtility - minUtility)) / (size - 1)
#            total = total + rankFitness[itr]
#
#        idx1 = -1
#        idx2 = -1
#        # select random pivot between 0 - sum of rankFitness
#        # pick solution whose sum of rankFirness from population[first] to it > pivot -> parent
#        while idx1 == idx2:
#            dart = random.uniform(0, total)
#            sum = 0.0
#            for itr in range(len(population)):
#                sum = sum + rankFitness[itr]
#                if dart <= sum:
#                    idx1 = itr
#                    break
#            dart = random.uniform(0, total)
#            sum = 0.0
#            for itr in range(len(population)):
#                sum = sum + rankFitness[itr]
#                if dart <= sum:
#                    idx2 = itr
#                    break
#        return population[idx1], population[idx2]


    def selectParents(self, population):
        probFitness = {}
        sampling = {}
        originalFitness = {}  # list of solutions' fitness (based on population)
        totalFitness = 0.0
        for itr in range(len(population)):
            originalFitness[itr] = self.fitness(population[itr])
            totalFitness += originalFitness[itr]

        size = float(len(population))
        for itr in range(len(population)):
            probFitness[itr] = originalFitness[itr] / totalFitness
            sampling[itr] = int(round(probFitness[itr] * size) + 1)

        pool = []
        for itr in range(len(population)):
            for itr2 in range(sampling[itr]):
                pool.append(population[itr])

        pool = sorted(pool, key=self.fitness, reverse=True)

        idx1 = -1
        idx2 = -1
        while idx1 == idx2:
            idx1 = random.randint(0, len(pool) - 1)
            idx2 = random.randint(0, len(pool) - 1)
        return pool[idx1], pool[idx2]

#    def crossoverParents(self, instance1, instance2):
#        genotype1 = instance1.getGenotype()
#        genotype2 = instance2.getGenotype()
#        newInstance = GeneticAlgorithmInstance()
#
#        dicNeighbor = {}
#        # for every city in parent1 and parent2, get its neighbors
#        for itr in range(len(genotype1)):  # itr = city-th in genotype
#            neighbor = {}
#            neighbor1 = self.getNeighborCity(instance1, itr)
#            neighbor2 = self.getNeighborCity(instance2, itr)
#            neighbor[neighbor1[0]] = 1
#            neighbor[neighbor1[1]] = 1
#            neighbor[neighbor2[0]] = 1
#            neighbor[neighbor2[1]] = 1
#            dicNeighbor[itr] = neighbor.keys()
#
#        # crossover using edge-recombination crossover
#        currentCity = 0
#        visitedCity = {}
#        path = {}
#        for itr in range(len(genotype1)):
#            visitedCity[currentCity] = 1
#            nextCity = self.getMinimumNeighborNotVisitedCity(visitedCity.keys(), dicNeighbor)
#            if nextCity == -1:
#                nextCity = 0
#            path[currentCity] = nextCity  # new solution
#            currentCity = nextCity
#
#        newInstance.setGenotype(path)
#
#        return newInstance


    def crossoverParents(self, instance1, instance2):
        genotype1 = instance1.getGenotype()
        genotype2 = instance2.getGenotype()
        newInstance = GeneticAlgorithmInstance()

        while True:
            child = {}
            idx1 = -1
            idx2 = -1
            while idx1 == idx2:
                idx1 = random.randint(0, len(genotype1) - 1)
                idx2 = random.randint(0, len(genotype2) - 1)

            if idx1 > idx2:
                idx1, idx2 = idx2, idx1

            for itr in range(idx1, idx2):
                child[itr] = genotype1[itr]

            itr2 = idx2
            for itr in range(len(genotype1)):
                i = (itr + idx2) % len(genotype1)
                if not genotype2[i] in child.values():
                    child[itr2] = genotype2[i]
                    itr2 = (itr2 + 1) % len(genotype1)

            if self.isInfeasible(child.values()):
                newInstance.setGenotype(child)
                return newInstance

    # mutation using random & swap
    def mutation(self, instance, factor):
        genotype = instance.getGenotype()
        mutationDone = False
        while mutationDone == False:
            for itr in range(factor):
                idxSwap1 = random.randint(0, len(genotype) - 1)
                idxSwap2 = random.randint(0, len(genotype) - 1)
                genotype[idxSwap1], genotype[idxSwap2] = genotype[idxSwap2], genotype[idxSwap1]
            if self.isInfeasible(genotype) == True:
                mutationDone = True

        instance.setGenotype(genotype)

    # substitution for fast convergence
    def substritutePopulation(self, population, children):
        # asc sort population
        for itr1 in range(len(population)):
            for itr2 in range(itr1 + 1, len(population)):
                if self.fitness(population[itr1]) > self.fitness(population[itr2]):
                    population[itr1], population[itr2] = population[itr2], population[itr1]

        # desc sort population
        for itr1 in range(len(children)):
            for itr2 in range(itr1 + 1, len(children)):
                if self.fitness(children[itr1]) < self.fitness(children[itr2]):
                    children[itr1], children[itr2] = children[itr2], children[itr1]

        # mix old and new generation
        for itr in range(len(children)):
            if self.fitness(population[itr]) < self.fitness(children[itr]):
                population[itr] = children[itr]
            else:
                break

