from numpy_boids import update_boids
import numpy as np
from nose.tools import assert_almost_equal
import os
import yaml

def test_bad_boids_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    boid_data=np.array(regression_data["before"])
    update_boids(boid_data)
    for after,before in zip(np.array(regression_data["after"]),boid_data):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.01)
	
