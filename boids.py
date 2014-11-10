"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import yaml

#import config file
config=yaml.load(open("config.yml"))

# Deliberately terrible code for teaching purposes

boid_x_positions=[]
boid_y_positions=[]
boid_x_velocities=[]
boid_y_velocities=[]
for i in range(config["boids_number"]):
	boid_x_positions.append(random.uniform(*config["x_position_range"]))
	boid_y_positions.append(random.uniform(*config["y_position_range"]))
	boid_x_velocities.append(random.uniform(*config["x_velocity_range"]))
	boid_y_velocities.append(random.uniform(*config["y_velocity_range"]))
boid_data=(boid_x_positions,boid_y_positions,boid_x_velocities,boid_y_velocities)

def update_boids(boid_data):
	x_positions,y_positions,x_velocities,y_velocities=boid_data
	# Fly towards the middle
	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			x_velocities[i]=x_velocities[i]+(x_positions[j]-x_positions[i])*config["flocking_coeff"]/len(x_positions)
	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			y_velocities[i]=y_velocities[i]+(y_positions[j]-y_positions[i])*config["flocking_coeff"]/len(x_positions)
	# Fly away from nearby boids
	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			if (x_positions[j]-x_positions[i])**2 + (y_positions[j]-y_positions[i])**2 < config["dispersion_distance"]:
				x_velocities[i]=x_velocities[i]+(x_positions[i]-x_positions[j])
				y_velocities[i]=y_velocities[i]+(y_positions[i]-y_positions[j])
	# Try to match speed with nearby boids
	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			if (x_positions[j]-x_positions[i])**2 + (y_positions[j]-y_positions[i])**2 < config["match_speed_distance"]:
				x_velocities[i]=x_velocities[i]+(x_velocities[j]-x_velocities[i])*config["match_speed_coeff"]/len(x_positions)
				y_velocities[i]=y_velocities[i]+(y_velocities[j]-y_velocities[i])*config["match_speed_coeff"]/len(x_positions)
	# Move according to velocities
	for i in range(len(x_positions)):
		x_positions[i]=x_positions[i]+x_velocities[i]
		y_positions[i]=y_positions[i]+y_velocities[i]


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
