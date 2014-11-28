"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""
import random
import numpy as np
# Deliberately terrible code for teaching purposes

def init_boids():
	boids_x=[random.uniform(-450,50.0) for x in range(50)]
	boids_y=[random.uniform(300.0,600.0) for x in range(50)]
	boid_x_velocities=[random.uniform(0,10.0) for x in range(50)]
	boid_y_velocities=[random.uniform(-20.0,20.0) for x in range(50)]
	boids=np.array([boids_x,boids_y,boid_x_velocities,boid_y_velocities])
	return boids

def update_boids(boids):
	positions=boids[:2].transpose()
	velocities=boids[2:].transpose()
	
	for i in range(len(positions)):
		# Fly towards the middle	
		velocities+=(positions[i]-positions)*0.01/len(positions)
		
		# Fly away from nearby boids	
		nearby_push = ((positions[i]-positions)**2).sum(axis=1)<100
		velocities[nearby_push]+=positions[nearby_push]-positions[i]
	
		# Try to match speed with nearby boids
		nearby_pull=((positions[i]-positions)**2).sum(axis=1)<10000
		velocities[nearby_pull]+=(velocities[i]-velocities[nearby_pull])*0.125/len(positions)
				
	# Move according to velocities
	positions+=velocities
