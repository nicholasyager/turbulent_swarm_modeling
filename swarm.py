#!/usr/bin/python2

import os
import time
import random
import math

def weibull(x,k,l):
    return (k/l) * math.pow(x/l,k-1) * math.exp( -math.pow( x/l, k) )


class Fish:
    def __init__(self, width, height, depth, density):
        """Initialize a Fish object, giving it a random position at start."""

        # Set a 

        self.x = random.gauss(width/2, density)
        self.y = random.gauss(height/2, density)
        self.z = random.gauss(depth/2, density)

        self.vector = [0,0,0]

        return

    def setVector(self, vector):
        self.vector = vector
        return

    def move(self, vector, timestep):
        """Read the vectors and move accordingly."""

        self.x += vector[0] * timestep
        self.y += vector[1] * timestep
        self.z += vector[2] * timestep

        print("Moving {0} x {1} x {2}".format(vector[0], vector[1], vector[2]))

        return

    # Reporter functons

    def getLocation(self):
        """Returns the x, y, and z coordinates of the fish."""
        return [self.x, self.y, self.z]

    def getVector(self):
        """Returns the x, y, and z coordinates of the fish."""
        return self.vector


    def getDistance(self, location):
        """Returns the cartesian distance between this fish and a different
        location."""

        return math.exp(  math.exp(location[0] - self.x,2) +  math.exp(location[1] - self.y,2) +  math.exp(location[2] - self.z,2), -2)


class Swarm:
    def __init__(self, n, d, r, width, height, depth, dampen):
        """In a world of a given width, height, and depth, create a swarm of n 
        size, with a start density d which equilibriates through swarm 
        mentality to a desired radius r."""
        
        self.r = r

        print("Creating a swarm of {0} with d={1}".format(n,d))

        # Iterate through the loop and create fish.
        self.swarm = []
        self.dampen = dampen
        for x in range(0, n):
            self.swarm.append(Fish(width, height, depth, d))

    def evaluate(self, timestep):
        """Evaluate the swarm as individuals, choosing each randomly with 
        exclusion."""

        for locus in range(0,len(self.swarm)):
            vector = [0,0,0]
            
            position = self.swarm[locus].getLocation()

            for fish in self.swarm:
                location = fish.getLocation()
             

                for coord in range(0,3):

                    # For the sake of this version, I'm using a Weibull
                    # distribution to handle coheasion

                    k = 6
                    l = 5

                    magnatude = abs(location[coord] - position[coord])
                    direction = 1

                    if location[coord] - position[coord] < 0:
                        direction = -direction

                    if magnatude > 0 :
                        vector[coord] += direction * weibull(magnatude, k, l)
                        vector[coord] += -direction * weibull(magnatude, 1, 0.125) / 20
                    else:
                        vector[coord] +=  0

                #print("{0} + {1} = {2}".format(position[0], location[0], vector[0]))

            self.swarm[locus].setVector(vector)

        for index in range(0,len(self.swarm)):
        
            self.swarm[index].move(self.swarm[index].getVector(), timestep)

        return


    def write(self, t):
        """Write the current state of the swarm at time t to a csv file of 
        location."""

        if t < 100:
            spacer = 0
        else:
            spacer = ""
        if t < 10:
            spacer2 = 0
        else:
            spacer2 = ""

        global TIME
        swarmFile = file(TIME + '/swarm_{0}{1}{2}.csv'.format(spacer,spacer2,t), 'w')

        swarmFile.write('"fish","x","y","z","i","j","k"\n')
        for f in range(0,len(self.swarm)):
            location = self.swarm[f].getLocation()
            vector = self.swarm[f].getVector()
            swarmFile.write('{3},{0},{1},{2},{4},{5},{6}\n'.format(location[0], 
                                           location[1], 
                                           location[2],
                                           f,
                                           vector[0],
                                           vector[1],
                                           vector[2]))

        swarmFile.close()
        return 



# Set the world variables
WORLD_WIDTH = 10 # Arbitrarily set width
WORLD_HEIGHT = 10
WORLD_DEPTH = 10

SIMULATION_TIMESTEP = 0.5
SIMULATION_TIME = 100

SWARM_NUMBER_FISH = 20
SWARM_DENSITY = 3
SWARM_RADIUS = 1
SWARM_DAMPEN = 1

global TIME
TIME = time.strftime("%Y-%m-%dT%H%M%S", time.gmtime())

os.makedirs(TIME)

# Create a swarm
swarm = Swarm(SWARM_NUMBER_FISH, 
              SWARM_DENSITY,
              SWARM_RADIUS,
              WORLD_WIDTH, 
              WORLD_HEIGHT, 
              WORLD_DEPTH,
              SWARM_DAMPEN)

for tick in range(0,SIMULATION_TIME):
    
    swarm.write(tick)
    swarm.evaluate(SIMULATION_TIMESTEP)
    print("==========")
