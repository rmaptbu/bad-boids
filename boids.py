"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import animation
import random

# Deliberately terrible code for teaching purposes

boid_x_positions=[random.uniform(-450,50.0) for x in range(50)]
boid_y_positions=[random.uniform(300.0,600.0) for x in range(50)]
boid_x_velocities=[random.uniform(0,10.0) for x in range(50)]
boid_y_velocities=[random.uniform(-20.0,20.0) for x in range(50)]
boid_data=(boid_x_positions,boid_y_positions,boid_x_velocities,boid_y_velocities)

def update_boids(boid_data):
	x_positions,y_positions,x_velocitiess,y_velocitiess=boid_data
	# Fly towards the middle
	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			x_velocitiess[i]=x_velocitiess[i]+(x_positions[j]-x_positions[i])*0.01/len(x_positions)
	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			y_velocitiess[i]=y_velocitiess[i]+(y_positions[j]-y_positions[i])*0.01/len(x_positions)
	# Fly away from nearby boids
	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			if (x_positions[j]-x_positions[i])**2 + (y_positions[j]-y_positions[i])**2 < 100:
				x_velocitiess[i]=x_velocitiess[i]+(x_positions[i]-x_positions[j])
				y_velocitiess[i]=y_velocitiess[i]+(y_positions[i]-y_positions[j])
	# Try to match speed with nearby boids
	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			if (x_positions[j]-x_positions[i])**2 + (y_positions[j]-y_positions[i])**2 < 10000:
				x_velocitiess[i]=x_velocitiess[i]+(x_velocitiess[j]-x_velocitiess[i])*0.125/len(x_positions)
				y_velocitiess[i]=y_velocitiess[i]+(y_velocitiess[j]-y_velocitiess[i])*0.125/len(x_positions)
	# Move according to velocities
	for i in range(len(x_positions)):
		x_positions[i]=x_positions[i]+x_velocitiess[i]
		y_positions[i]=y_positions[i]+y_velocitiess[i]


figure=plt.figure()
axes=plt.axes(xlim=(-500,1500), ylim=(-500,1500))
scatter=axes.scatter(boid_data[0],boid_data[1])

def animate(frame):
   update_boids(boid_data)
   scatter.set_offsets(zip(boid_data[0],boid_data[1]))


anim = animation.FuncAnimation(figure, animate,
                               frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
