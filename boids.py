"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

import random
from numpy import array

# Will now add an Eagle to Boids

class Boid(object):
	def __init__(self,x,y,xv,yv,owner,species="Starling"):
		self.position=array([x,y])
		self.velocity=array([xv,yv])
		self.owner=owner
		self.species=species

	def interaction(self,other):
		self.delta_v=array([0.0,0.0])
		self.separation=other.position-self.position
		self.separation_sq=self.separation.dot(self.separation)

class Eagle(Boid):
	def __init__(self,x,y,xv,yv,owner):
		super(Eagle,self).__init__(x,y,xv,yv,owner,species="Eagle")
	def interaction(self,other):
		super(Eagle,self).interaction(other)
		self.delta_v+=self.separation*self.owner.eagle_hunt_strength
		return self.delta_v

class Starling(Boid):
	def __init__(self,x,y,xv,yv,owner):
		super(Starling,self).__init__(x,y,xv,yv,owner,species="Starling")
	def interaction(self,other):
		super(Starling,self).interaction(other)
		if other.species=="Eagle":
			# Flee the Eagle
			if self.separation_sq < self.owner.eagle_avoidance_radius**2:
				self.delta_v-=(self.separation*self.owner.eagle_fear)/self.separation.dot(self.separation)
				return self.delta_v
		else:
			# Fly towards the middle
			self.delta_v+=self.separation*self.owner.flock_attraction

			# Fly away from nearby boids
			if self.separation_sq < self.owner.avoidance_radius**2:
				self.delta_v-=self.separation

			# Try to match speed with nearby boids
			if self.separation_sq < self.owner.formation_flying_radius**2:
				self.delta_v+=(other.velocity-self.velocity)*self.owner.speed_matching_strength
		return self.delta_v

class BoidBuilder(object):
	def add_random_starling(self,owner):
		starling=Starling(0,0,0,0, owner)
		starling.position=array([random.uniform(-450,50.0),random.uniform(300.0,600.0)])
		starling.velocity=array([random.uniform(0,10.0),random.uniform(-20.0,20.0)])
		return starling
	def add_starling(self,owner,coords):
		x,y,xv,yv = coords
		return Starling(x,y,xv,yv,owner)
	def add_eagle(self,x,y,xv,yv,owner):
		return Eagle(x,y,xv,yv,owner)
		
class Boids(object):
	def __init__(self,
		   flock_attraction,avoidance_radius,
			formation_flying_radius,speed_matching_strength,
			eagle_avoidance_radius=100, eagle_fear=5000, eagle_hunt_strength=0.00005):
		self.flock_attraction=flock_attraction
		self.avoidance_radius=avoidance_radius
		self.formation_flying_radius=formation_flying_radius
		self.speed_matching_strength=speed_matching_strength
		self.eagle_avoidance_radius=eagle_avoidance_radius
		self.eagle_fear=eagle_fear
		self.eagle_hunt_strength=eagle_hunt_strength
		self.bb=BoidBuilder()		

	
	def initialise_random(self,count):
		self.boids=[self.bb.add_random_starling(self) for i in range(count)]

	def add_eagle(self,x,y,xv,yv):
		self.boids.append(self.bb.add_eagle(x,y,xv,yv,self))

	def initialise_from_data(self,data):
		self.boids=[self.bb.add_starling(self, coords) for coords in zip(*data)]

	def update(self):
		for me in self.boids:
			delta_v=array([0.0,0.0])
			for him in self.boids:
				delta_v+=me.interaction(him)
			# Accelerate as stated
			me.velocity+=delta_v
			# Move according to velocities
			me.position+=me.velocity
