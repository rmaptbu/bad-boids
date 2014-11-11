from boids import Boids
from nose.tools import assert_almost_equal
import os
import yaml

def test_bad_boids_regression():
	regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
	x_positions, y_positions, x_velocities, y_velocities = regression_data["before"]
	boids=Boids()
	boids.x_positions=x_positions
	boids.y_positions=y_positions
	boids.x_velocities=x_velocities
	boids.y_velocities=y_velocities
	boids.update()
	boid_data=boids.x_positions, boids.y_positions, boids.x_velocities, boids.y_velocities
	for after,before in zip(regression_data["after"],boid_data):
		for after_value,before_value in zip(after,before): 
			assert_almost_equal(after_value,before_value,delta=0.01)
	
