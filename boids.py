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
		self.x_position=x
		self.y_position=y
		self.x_velocity=xv
		self.y_velocity=yv

class Boids(object):
	#define initial conditions
	def __init__(self):
		self.flocking_coeff=config["flocking_coeff"]/config["boids_number"]
		self.match_speed_coeff=config["match_speed_coeff"]/config["boids_number"]

	def initialise_random(self):
		self.boids=[]
		self.x_positions=[]
		self.y_positions=[]
		self.x_velocities=[]
		self.y_velocities=[]
		for i in range(config["boids_number"]):
			x=(random.uniform(*config["x_position_range"]))
			y=(random.uniform(*config["y_position_range"]))
			xv=(random.uniform(*config["x_velocity_range"]))
			yv=(random.uniform(*config["y_velocity_range"]))
			self.boids.append(Boid(x,y,xv,yv))
		for boid in self.boids:
			self.x_positions.append(boid.x_position)
			self.y_positions.append(boid.y_position)
			self.x_velocities.append(boid.x_velocity)
			self.y_velocities.append(boid.y_velocity)

	def initialise_from_data(self,data):
		self.boids=[]
		self.x_positions=[]
		self.y_positions=[]
		self.x_velocities=[]
		self.y_velocities=[]
		xs,ys,xvs,yvs=data
		for i in range(config["boids_number"]):
			self.boids.append(Boid(xs[i],ys[i],xvs[i],yvs[i]))
		for boid in self.boids:
			self.x_positions.append(boid.x_position)
			self.y_positions.append(boid.y_position)
			self.x_velocities.append(boid.x_velocity)
			self.y_velocities.append(boid.y_velocity)

	def update(self):
		for i in range(len(self.x_positions)):
			for j in range(len(self.x_positions)):
				#define relevant variables
				distance_x=self.x_positions[j]-self.x_positions[i]
				distance_y=self.y_positions[j]-self.y_positions[i]
				distance_total_sq=distance_x**2+distance_y**2
				speed_diff_x=self.x_velocities[j]-self.x_velocities[i]
				speed_diff_y=self.y_velocities[j]-self.y_velocities[i]

				# Fly towards the middle
				self.x_velocities[i]+=distance_x*self.flocking_coeff
				self.y_velocities[i]+=distance_y*self.flocking_coeff

				# Fly away from nearby boids
				if distance_total_sq < config["dispersion_threshold"]:
					self.x_velocities[i]-=distance_x
					self.y_velocities[i]-=distance_y

				# Try to match speed with nearby boids
				if distance_total_sq < config["match_speed_threshold"]:
					self.x_velocities[i]+=speed_diff_x*self.match_speed_coeff
					self.y_velocities[i]+=speed_diff_y*self.match_speed_coeff

		# Move according to velocities
		for i in range(len(self.x_positions)):
			self.x_positions[i]+=self.x_velocities[i]
			self.y_positions[i]+=self.y_velocities[i]
