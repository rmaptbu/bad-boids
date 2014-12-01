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
	pos_diff=-np.subtract.outer(boids[:2],boids[:2]).diagonal(axis1=0,axis2=2).T
	vel_diff=-np.subtract.outer(boids[2:],boids[2:]).diagonal(axis1=0,axis2=2).T
	positions=boids[:2].T
	velocities=boids[2:].T
	
	# Fly towards the middle	
	velocities+=pos_diff.sum(axis=1).T*0.01/len(positions)
	
	# Fly away from nearby boids	
	nearby_push = np.sum((pos_diff**2),axis=0,keepdims=True)<100
	pos_diff_masked=np.zeros((2,50,50))
	pos_diff_masked[np.tile(nearby_push,(2,1,1))]+=pos_diff[np.tile(nearby_push,(2,1,1))]
	velocities+=pos_diff_masked.sum(axis=2).T
	
	# Try to match speed with nearby boids
	nearby_pull = np.sum((pos_diff**2),axis=0,keepdims=True)<10000
	vel_diff_masked=np.zeros((2,50,50))
	vel_diff_masked[np.tile(nearby_pull,(2,1,1))]+=vel_diff[np.tile(nearby_pull,(2,1,1))]
	velocities+=vel_diff_masked.sum(axis=1).T*0.125/len(positions)	
				
	# Move according to velocities
	positions+=velocities
