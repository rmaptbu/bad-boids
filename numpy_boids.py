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
	
	xs,ys,xvs,yvs=boids
	# Fly towards the middle
	for i in range(len(positions)):
		velocities+=(positions[i]-positions)*0.01/len(positions)

		
	# Fly away from nearby boids	
	for i in range(len(positions)):
		nearby = ((positions[i]-positions)**2).sum(axis=1)<100
		velocities[nearby]+=positions[nearby]-positions[i]
		
	xs=positions[:,0]
	ys=positions[:,1]
	xvs=velocities[:,0]
	yvs=velocities[:,1]	

	for i in range(len(xs)):
		for j in range(len(xs)):
			if (xs[j]-xs[i])**2 + (ys[j]-ys[i])**2 < 10000:
				xvs[i]=xvs[i]+(xvs[j]-xvs[i])*0.125/len(xs)
				yvs[i]=yvs[i]+(yvs[j]-yvs[i])*0.125/len(xs)
	# Move according to velocities
	for i in range(len(xs)):
		xs[i]=xs[i]+xvs[i]
		ys[i]=ys[i]+yvs[i]
