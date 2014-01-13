Swarm
=====
Eash element in the swarm is a theoretical "fish" which follows a heading
vector based on it's surroundings.Swarm is a general simulation of swam behavior
as defined by three rules:
 1. Move in the same direction as your neighbors.
 2. Remain close to your neighbors.
 3. Aviod collisions with your neighbors.

Requirements
----
This simulation requires *Python 2.7* and is currently visualized using R 3.0.2
and the <code>rlg</code> package.

Usage
----
Run <code>swarm.py</code>, and a .csv file is output for each time step listing
the coordinates and headings of each fish. Run R with the working directory set
to the output folder, and source <code>swarm_vis.r</code> for the rgl output.

