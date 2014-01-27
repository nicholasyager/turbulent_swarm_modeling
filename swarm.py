#!/usr/bin/python2

import os
import time
import random
import math
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axis3d
import matplotlib.animation as animation
from subprocess import call

def weibull(x,k,l):
    """Determine the probability at x with k and l."""
    return (k/l) * math.pow(x/l,k-1) * math.exp( -math.pow( x/l, k) )

def gaussian(x, mu, sigma):
    """Determine the probability at x with mu and sigma."""
    return (1/(sigma * math.pow(2*3.14159,2)) * \
            math.exp( -( math.pow(x - mu,2) / ( 2 * math.pow(sigma,2)  ))))

def generateCurrent(position, currentType, w):
    """Generate a current of a particular geometry with velocity w."""

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

def configure_figure(ax, tick, SWARM_NUMBER_FISH,width):
    """Configure the matplotlib plot to the proper constraints."""

    # Write the details of the current tick onto the image.
    ax.text2D(0.05, 0.9, TIME + "\nTick: " + str(tick) + "\nPop: "+str(SWARM_NUMBER_FISH) , 
              transform=ax.transAxes)

    # Assign labels to the graph
    ax.set_xlabel('X') 
    ax.set_ylabel('Z')
    ax.set_zlabel('Y')

    # Padding
    pad = 2

    # Set the limits for the graph
    ax.set_xlim3d(0-pad, width+pad)
    ax.set_ylim3d(0-pad, width+pad)
    ax.set_zlim3d(0-pad, width+pad)

    return ax

def pad(n, symbol, string):
    """Pad the string with a symbol n times."""

    while len(string) < n:
        string = symbol + string
   
    return string

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

        # Store the vector for future use without commiting it within this
        # current step. This would create a bias in future heading detection.

        self.future_vector = vector

    def move(self, timestep):
        """Read the vectors and move accordingly."""

        self.vector = self.future_vector

        self.x += self.vector[0] * timestep
        self.y += self.vector[1] * timestep
        self.z += self.vector[2] * timestep

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

        # Evaluation.
        #
        # For evaluation, each fish is examined at the current time and a new
        # heading and velocity is calculated. This heading and velocity is
        # determined in this order:
        # 
        # 1. Find the 5 closest fish (the local group) and move to within an
        #    "equilibrium" distance, as defined by two opposing Gaussian
        #    distributions. This serves to keep a local and macro swarm
        #    together as well as moving in similar directions in turbulent
        #    fluids.
        # 2. Turbulent forces will move the fish in a particular direction
        #    based on their respective positions. This is currently the major
        #    factor in swarm movement within the simulation.
        # 3. The average heading of the swarm should be considered so that
        #    members of the swarm move in similar directions as their
        #    neighbors. This is a tricky problem that I have yet to implement
        #    into the simulation until I have found a way to bypass bias.

        for locus in range(0,len(self.swarm)):

            vector = [0,0,0]                        # The new vector
            locusFish = self.swarm[locus]           # The fish to be examined
            position = locusFish.getLocation()

            # Local group swarming

            closestFish = locusFish.findClosest(self.swarm,5)
            localHeading = [0,0,0]

            for distance, fish in closestFish:
                location = fish.getLocation()
                heading = fish.getVector()
                localHeading[0] += heading[0]
                localHeading[1] += heading[1]
                localHeading[1] += heading[1]
                local_magnatude = gaussian(distance, 3, 2) * 10   # Attractor
                local_magnatude -= gaussian(distance, 0, 1) * 3   # Repulsor

            localHeading[0] = localHeading[0] / 5
            localHeading[1] = localHeading[1] / 5
            localHeading[2] = localHeading[2] / 5

            # Turbulent swarming

            currentVector = generateCurrent( position, "circle", w)


            # Sum the vector components
            for coord in range(0, 3):
                local_component = local_magnatude * ( 
                                        (location[coord] - position[coord]) / \
                                      distance )

                vector[coord] += ((currentVector[coord] + local_component) + \
                                 localHeading[coord])/2
                # Check for boundries

                

                if (position[coord] < 0 and vector[coord] < 0):
                    vector[coord] += position[coord]/2 * vector[coord]
                if (position[coord] >= 10 and vector[coord] > 0):
                    vector[coord] -= (position[coord] - 10) /2 * vector[coord]


            locusFish.setVector(vector)

        for fish in self.swarm:

            fish.move(timestep)

        return

    def visualize(self, ax):
        """Plot the current locations of each fish."""

        # Clear the previous graph
        ax.clear()
 
        # Create empty lists for the current tick
        xvalues, yvalues, zvalues = [], [], []
        
        # Fill the lists with fish positions.
        for fish in self.swarm:
            xvalues.append(fish.x)
            yvalues.append(fish.y)
            zvalues.append(fish.z)

        # Plot the fish on a new graph
        ax.scatter(xvalues, zvalues, yvalues)

        # I must return the updated axis object.
        return ax

    def write(self, t):
        """Write the current state of the swarm at time t to a csv file of
        location."""

        #DEV: A relic from an older time. This should be updated soon.
        if t < 100:
            spacer = 0
        else:
            spacer = ""
        if t < 10:
            spacer2 = 0
        else:
            spacer2 = ""

        # Create a .csv file.
        global TIME
        swarmFile = file(TIME + '/swarm_{0}{1}{2}.csv'.format(spacer,spacer2,t), 'w')

        # Write the location and vector of each fish to the .csv file.
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
        swarmFile.close()
        return



# Set the world variables
WORLD_WIDTH = 10 # Arbitrarily set width
WORLD_HEIGHT = 10
WORLD_DEPTH = 10

SIMULATION_TIMESTEP = 0.5
SIMULATION_TIME = 1000
SIMULATION_SPIN = 1

SWARM_NUMBER_FISH = 100
SWARM_DENSITY = 4
SWARM_RADIUS = 1
SWARM_DAMPEN = 1

global TIME
TIME = time.strftime("%Y-%m-%dT%H%M%S", time.gmtime())

os.makedirs(TIME)

#################### Handle Plotting ###########################

fig = plt.figure(figsize=(12,9))
ax = fig.add_subplot(111, projection='3d')

for axis in ax.w_xaxis, ax.w_yaxis, ax.w_zaxis: 
    for elt in axis.get_ticklines() + axis.get_ticklabels(): 
        #elt.set_visible(False) 

        #axis.pane.set_visible(False) 
        axis.gridlines.set_visible(False) 
        #axis.line.set_visible(False) 

#plt.show(block=False)

################### Simulate ###################################

# Create a swarm
swarm = Swarm(SWARM_NUMBER_FISH,
              SWARM_DENSITY,
              SWARM_RADIUS,
              WORLD_WIDTH,
              WORLD_HEIGHT,
              WORLD_DEPTH,
              SWARM_DAMPEN)


# Simulation Loop
#
# For each tick in the simulation, evaluate the swarm at it's current location,
# and then render and save a 3D plot of the state.

for tick in range(0,SIMULATION_TIME):
    
    #swarm.write(tick) # Write the positions of the fish at the given timestep.
    swarm.evaluate(SIMULATION_SPIN,SIMULATION_TIMESTEP)

    ## Visualize the swarm behavior, and save the images ##
    ax = swarm.visualize(ax)
    ax = configure_figure(ax, tick, SWARM_NUMBER_FISH, WORLD_WIDTH)

    ## Properly name the file in a way to animate in the correct order.
    filenumber = pad( len(str(SIMULATION_TIME)) , "0", str(tick))
    plt.savefig(TIME+'/swarm_{0}.png'.format(filenumber),
                bbox_inches='tight')

    plt.draw()


    print("Tick: " + str(tick))



# Image Modification:
# 
# This step takes the produced images, and from them creates a .gif animation
# of the simulation. This modification takes three steps:
# 
# 1. Trim the images to remove all excess white and transparent space.
# 2. Resize the images to a more manageable format. More careful production of
#       initial images will reduce the need for resizing in the future.
# 3. Take all of the processed images and merge them into a .gif file.

#print("Triming images..."),
#call(["mogrify","-trim","+repage", TIME+"/*"])
#print(" Complete")

print("Resizing Images..."),
call(["mogrify","-resize","600x478!",TIME+"/*"])
print(" Complete")

print("Generating animation..."),
call(["ffmpeg","-r", "15", "-pattern_type", "glob","-i", TIME+"/*.png",
    "-c:v", "libx264", "pix_fmt", "yuv420p",
    TIME+"/swarm.mp4"])
print(" Complete")

print("Simulation saved to "+TIME+"/")
print("Simulation complete.")
