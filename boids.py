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
	flocking_coeff=config["flocking_coeff"]/config["boids_number"]
	match_speed_coeff=config["match_speed_coeff"]/config["boids_number"]

	for i in range(len(x_positions)):
		for j in range(len(x_positions)):
			distance_x=x_positions[j]-x_positions[i]
			distance_y=y_positions[j]-y_positions[i]
			distance_total_sq=distance_x**2+distance_y**2
			speed_diff_x=x_velocities[j]-x_velocities[i]
			speed_diff_y=y_velocities[j]-y_velocities[i]
			
			# Fly towards the middle
			x_velocities[i]+=distance_x*flocking_coeff
			y_velocities[i]+=distance_y*flocking_coeff
			
			# Fly away from nearby boids			
			if distance_total_sq < config["dispersion_threshold"]:
				x_velocities[i]-=distance_x
				y_velocities[i]-=distance_y
				
			# Try to match speed with nearby boids
			if distance_total_sq < config["match_speed_threshold"]:
				x_velocities[i]+=speed_diff_x*match_speed_coeff
				y_velocities[i]+=speed_diff_y*match_speed_coeff
				
	# Move according to velocities
	for i in range(len(x_positions)):
		x_positions[i]+=x_velocities[i]
		y_positions[i]+=y_velocities[i]

figure=plt.figure()
axes=plt.axes(xlim=(config["plot_dimensions"]['x']), ylim=(config["plot_dimensions"]['y']))
scatter=axes.scatter(boid_data[0],boid_data[1])

def animate(frame):
   update_boids(boid_data)
   scatter.set_offsets(zip(boid_data[0],boid_data[1]))


anim = animation.FuncAnimation(figure, animate,
                               frames=config["animation"]['frames'], interval=config["animation"]['interval'])

if __name__ == "__main__":
    plt.show()
