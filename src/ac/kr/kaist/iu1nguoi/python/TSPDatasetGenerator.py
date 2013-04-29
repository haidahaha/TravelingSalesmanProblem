import random
import csv

def generator(numCities, width, height, filename):

    datasetFile = open(filename, 'w')

    for itr in range(numCities):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        coordinate = [x, y]
        datasetFile.write(str(itr) + "," + str(x) + "," + str(y) + "\n")

    datasetFile.close()

def readcsv(filename):
    datasetReader = csv.reader(open(filename, 'rb'), delimiter=',')
    dataset = {}

    cnt = 0
    for row in datasetReader:
        dataset[cnt] = [float(row[1]), float(row[2])]
        cnt += 1

    print dataset.items()

# generator(40, 800, 800, 'TSP-Open-dataset.csv')
# generator(40, 800, 800, 'TSP-Closed-dataset.csv')
readcsv('TSP-Open-dataset.csv')
