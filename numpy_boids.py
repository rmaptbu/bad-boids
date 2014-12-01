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
	pos_diff_x=np.subtract.outer(boids[0],boids[0])
	pos_diff_y=np.subtract.outer(boids[1],boids[1])
	vel_diff_x=np.subtract.outer(boids[2],boids[2])
	vel_diff_y=np.subtract.outer(boids[3],boids[3])
	pos_diff=np.array([pos_diff_x,pos_diff_y])
	vel_diff=np.array([vel_diff_x,vel_diff_y])
	positions=boids[:2].transpose()
	velocities=boids[2:].transpose()
	
	# Fly towards the middle	
	velocities+=pos_diff.sum(axis=1).T*0.01/len(positions)
	
	# Fly away from nearby boids	
	nearby_push = np.sum((pos_diff**2),axis=0,keepdims=True)<100
	pos_diff_masked=np.zeros((2,50,50))
	pos_diff_masked[np.tile(nearby_push,(2,1,1))]+=pos_diff[np.tile(nearby_push,(2,1,1))]
	velocities+=pos_diff_masked.sum(axis=1).T
		
	for i in range(len(positions)):		
		
	
		# Try to match speed with nearby boids
		nearby_pull=((positions[i]-positions)**2).sum(axis=1)<10000
		velocities[nearby_pull]+=(velocities[i]-velocities[nearby_pull])*0.125/len(positions)
				
	# Move according to velocities
	positions+=velocities
