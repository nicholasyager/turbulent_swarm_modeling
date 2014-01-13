#!/usr/bin/python2

import os
import time
import random
import math

def weibull(x,k,l):
    return (k/l) * math.pow(x/l,k-1) * math.exp( -math.pow( x/l, k) )

def gaussian(x, mu, sigma):
    return (1/(sigma * math.pow(2*3.14159,2)) * \
            math.exp( -( math.pow(x - mu,2) / ( 2 * math.pow(sigma,2)  ))))

def generateCurrent(position, currentType, w):

        # In these intial stages, it may be best to use a form of
        # circular current. Vector velocity is based on angular
        # velocity w.

        distance = math.sqrt( math.pow(5 - position[0],2) + \
                             math.pow(5 - position[2],2))

        v = w *  gaussian(distance, 5, 3) * 5
        angle =  math.atan( (position[2] - 5 ) /  (position[0] - 5) )

        # Quadrant II
        if position[0] < 5 and position[2] > 5:
            angle = 3.14159 + angle

        # Quadrant III
        elif position[0] < 5 and position[2] < 5:
            angle = 3.14159 + angle

        # Quadrant IV
        elif position[0] > 5 and position[2] < 5:
            angle = (2 * 3.14159) + angle

        angle -= (3.14159/2)

        vector = [0,0,0]

        vector[0] += v * math.cos(angle)
        vector[2] +=  v * math.sin(angle)

        return vector


class Fish:
    def __init__(self, width, height, depth, density):
        """Initialize a Fish object, giving it a random position at start."""

        # Set a

        self.ID = 0
        self.x = random.gauss(width/2, density)
        self.y = random.gauss(height/2, density)
        self.z = random.gauss(depth/2, density)

        self.vector = [0,0,0]

        return

    def setID(self, ID):
        """Save the ID number for this fish for later calculations."""

        self.ID = ID

        return

    def setVector(self, vector):
        """Write the fish's vector to a buffer to be used on the next timestep.
        """

        self.future_vector = vector
        return

    def move(self, timestep):
        """Read the vectors and move accordingly."""

        self.vector = self.future_vector

        self.x += self.vector[0] * timestep
        self.y += self.vector[1] * timestep
        self.z += self.vector[2] * timestep

        #print("Moving {0} x {1} x {2}".format(self.vector[0],
        #                                      self.vector[1],
        #                                      self.vector[2])
        #                                      )

        return

    def findClosest(self, swarm, n):
        """Return the closest n fish to a given fish within a swarm."""

        position = self.getLocation()

        partners = []

        for otherFish in swarm:
            if otherFish.ID != self.ID:
                otherLocation = otherFish.getLocation()
                distance = self.getDistance( otherLocation )
                partners.append( (distance,otherFish) )


        partners.sort()


        return partners[:n]


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

        return math.sqrt(  math.pow(location[0] - self.x,2) + \
                          math.pow(location[1] - self.y,2) + \
                          math.pow(location[2] - self.z,2))


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
            newFish = Fish(width, height, depth, d)
            newFish.setID(x)
            self.swarm.append(newFish)

    def evaluate(self, w, timestep):
        """Evaluate the swarm as individuals, choosing each randomly with
        exclusion."""

        for locus in range(0,len(self.swarm)):
            vector = [0,0,0]

            locusFish = self.swarm[locus]

            position = locusFish.getLocation()

            closestFish = locusFish.findClosest(self.swarm,5)


            for distance, fish in closestFish:
                location = fish.getLocation()

                magnatude = gaussian(distance, 3, 2) * 10
                magnatude -= gaussian(distance, 0, 1) * 3

                for coord in range(0,3):

                    # For the sake of this version, I'm using a Gaussian and
                    # Weibull distributions to handle coheasion.

                    vector[coord] += magnatude * ( (location[coord] - position[coord]) / \
                                      distance )

            #print w, distance, v, (angle * 180)/3.14159, v *  math.cos(angle), v * math.sin(angle)

            currentVector = generateCurrent( position, "circle", w)

            for coord in range(0, 3):
                vector[coord] += currentVector[coord]

            #print(vector)
            self.swarm[locus].setVector(vector)

        for fish in self.swarm:

            fish.move(timestep)

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

        swarmFile.write('"x","y","z","i","j","k"\n')
        for fish in self.swarm:
            location = fish.getLocation()
            vector = fish.getVector()
            swarmFile.write('{0},{1},{2},{3},{4},{5}\n'.format(location[0],
                                           location[1],
                                           location[2],
                                           vector[0],
                                           vector[1],
                                           vector[2]))
            #print location
        swarmFile.close()
        return



# Set the world variables
WORLD_WIDTH = 10 # Arbitrarily set width
WORLD_HEIGHT = 10
WORLD_DEPTH = 10

SIMULATION_TIMESTEP = 1
SIMULATION_TIME = 100
SIMULATION_SPIN = 10

SWARM_NUMBER_FISH = 100
SWARM_DENSITY = 4
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
    swarm.evaluate(SIMULATION_SPIN,SIMULATION_TIMESTEP)
    print("Tick: " + str(tick))
