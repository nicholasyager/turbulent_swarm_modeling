Turbulent Swarm Modeling
=====
Eash element in the swarm is a theoretical "fish" which follows a heading
vector based on it's surroundings.Swarm is a general simulation of swam behavior
as defined by three rules:
 1. Move in the same direction as your neighbors.
 2. Remain close to your neighbors.
 3. Aviod collisions with your neighbors.

Requirements
----
This simulation requires *Python 2.7* and is currently visualized using 
*Matlibplot*. 

Usage
----
Execute <code>swarm.py</code>, and *matlibplot* will render the swarm location for
each tick of the simulation. After running the simulation the script will 
automatically scale and trim the rendered images, and splice the series into
and animated gif.

The deprecated .csv output can be reactivated by uncommenting the associated
line. All .csv outputs can be rendered with <code>rgl</code> by running
<code>swarmvis.R</code> with the output directory set as the R working 
directory.

