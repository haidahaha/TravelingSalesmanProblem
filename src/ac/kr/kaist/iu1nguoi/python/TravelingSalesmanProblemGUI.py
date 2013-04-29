from Tkinter import *
import math
import threading
import time

class TravelingSalesmanProblemGUI(threading.Thread):
    root = ''
    canvas = ''
    speed = 0
    tsp = ''
    
    
    def __init__(self, tsp, speed, h, w):
        self.tsp = tsp
        tsp.registerGUI(self)
        
        self.root = Tk()
               
        self.canvas = Canvas(self.root, height = h, width = w)
        self.canvas.pack()
        
        self.root.title("KAIST IE362 Traveling Salesman Problem")
        self.layoutCities()
        self.speed = 1 / speed
        threading.Thread.__init__(self)
            
    def run(self):
        self.root.mainloop()
    
    def update(self):
        time.sleep(self.speed)
        
        width = int( self.canvas.cget("width") )
        height = int( self.canvas.cget("height") )
        self.canvas.create_rectangle(0,0,width,height,fill='white')
        
        self.layoutCities()
        self.layoutRoutes()
        
    def stop(self):
        self.root.quit()
        
    def layoutCities(self):
        cities = self.tsp.dicLocations.keys()
        for itr in range(len(cities)):
            coordinate = self.tsp.dicLocations[cities[itr]]
            self.canvas.create_rectangle(coordinate[0], coordinate[1],coordinate[0]+3, coordinate[1]+3,fill='black')

    def layoutRoutes(self):
        genotype = self.tsp.best.getGenotype()
        for itr in range(len(genotype)):
            currentCity = itr
            nextCity = genotype[itr]
            coord1 = self.tsp.dicLocations[currentCity]
            coord2 = self.tsp.dicLocations[nextCity]
            self.canvas.create_line(coord1[0],coord1[1],coord2[0],coord2[1])
            
