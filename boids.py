"""
A better implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

import random
import yaml

#import config file
config=yaml.load(open("config.yml"))

class Boid(object):
	def __init__(self,x,y,xv,yv):
		self.flocking_coeff=config["flocking_coeff"]/config["boids_number"]
		self.match_speed_coeff=config["match_speed_coeff"]/config["boids_number"]
		self.x_position=x
		self.y_position=y
		self.x_velocity=xv
		self.y_velocity=yv
	
	def interaction(self,other):
		#define relevant variables
		distance_x=other.x_position-self.x_position
		distance_y=other.y_position-self.y_position
		distance_total_sq=distance_x**2+distance_y**2
		speed_diff_x=other.x_velocity-self.x_velocity
		speed_diff_y=other.y_velocity-self.y_velocity

		# Fly towards the middle
		self.x_velocity+=distance_x*self.flocking_coeff
		self.y_velocity+=distance_y*self.flocking_coeff

		# Fly away from nearby boids
		if distance_total_sq < config["dispersion_threshold"]:
			self.x_velocity-=distance_x
			self.y_velocity-=distance_y

		# Try to match speed with nearby boids
		if distance_total_sq < config["match_speed_threshold"]:
			self.x_velocity+=speed_diff_x*self.match_speed_coeff
			self.y_velocity+=speed_diff_y*self.match_speed_coeff

class Boids(object):
	#define initial conditions
	def __init__(self):
		pass

	def initialise_random(self):
		self.boids=[]
		for i in range(config["boids_number"]):
			x=(random.uniform(*config["x_position_range"]))
			y=(random.uniform(*config["y_position_range"]))
			xv=(random.uniform(*config["x_velocity_range"]))
			yv=(random.uniform(*config["y_velocity_range"]))
			self.boids.append(Boid(x,y,xv,yv))

	def initialise_from_data(self,data):
		self.boids=[]
		xs,ys,xvs,yvs=data
		for i in range(config["boids_number"]):
			self.boids.append(Boid(xs[i],ys[i],xvs[i],yvs[i]))

	def update(self):
		for boid in self.boids:
			for other in self.boids:
				boid.interaction(other)
		# Move according to velocities
		for boid in self.boids:
			boid.x_position+=boid.x_velocity
			boid.y_position+=boid.y_velocity
	
	def update_output(self):
		self.x_positions=[]
		self.y_positions=[]
		self.x_velocities=[]
		self.y_velocities=[]
		for boid in self.boids:
			self.x_positions.append(boid.x_position)
			self.y_positions.append(boid.y_position)
			self.x_velocities.append(boid.x_velocity)
			self.y_velocities.append(boid.y_velocity)
		
