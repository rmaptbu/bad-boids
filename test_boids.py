from boids import Boids
from boids import Boid
from nose.tools import assert_almost_equal
import os
import yaml

def test_bad_boids_regression():
	regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
	boids=Boids(regression_data["before"])
	boids.update()
	boids.update_output()
	boid_data=boids.x_positions, boids.y_positions, boids.x_velocities, boids.y_velocities
	for after,before in zip(regression_data["after"],boid_data):
		for after_value,before_value in zip(after,before): 
			assert_almost_equal(after_value,before_value,delta=0.01)

def test_boid():
	boid_1=Boid(0,0,0,0)
	boid_2=Boid(1,0,0,0)
	boid_1.interaction(boid_2)
	assert_almost_equal(boid_1.x_velocity, -0.9998, delta=0.0001)