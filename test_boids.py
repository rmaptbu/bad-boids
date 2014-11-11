from boids import Boids
from nose.tools import assert_almost_equal
import os
import yaml

def test_bad_boids_regression():
	regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
	boids=Boids()
	boids.initialise_from_data(regression_data["before"])
	boids.update()
	boids.update_output()
	boid_data=boids.x_positions, boids.y_positions, boids.x_velocities, boids.y_velocities
	for after,before in zip(regression_data["after"],boid_data):
		for after_value,before_value in zip(after,before): 
			assert_almost_equal(after_value,before_value,delta=0.01)
	
