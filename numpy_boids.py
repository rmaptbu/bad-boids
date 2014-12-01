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
	diff_pos_x=np.subtract.outer(boids[0],boids[0])
	diff_pos_y=np.subtract.outer(boids[1],boids[1])
	diff_vel_x=np.subtract.outer(boids[2],boids[2])
	diff_vel_y=np.subtract.outer(boids[3],boids[3])
	diff_pos=np.array([diff_pos_x,diff_pos_y])
	diff_vel=np.array([diff_vel_x,diff_vel_y])
	positions=boids[:2].transpose()
	velocities=boids[2:].transpose()
	
	# Fly towards the middle	
	velocities+=diff_pos.sum(axis=1).T*0.01/len(positions)
	
	for i in range(len(positions)):		
		
		# Fly away from nearby boids	
		nearby_push = ((positions[i]-positions)**2).sum(axis=1)<100
		velocities[nearby_push]+=positions[nearby_push]-positions[i]
	
		# Try to match speed with nearby boids
		nearby_pull=((positions[i]-positions)**2).sum(axis=1)<10000
		velocities[nearby_pull]+=(velocities[i]-velocities[nearby_pull])*0.125/len(positions)
				
	# Move according to velocities
	positions+=velocities
