import yaml
import boids
from copy import deepcopy
before=deepcopy(boids.boid_data)
boids.update_boids(boids.boid_data)
after=boids.boid_data
fixture={"before":before,"after":after}
fixture_file=open("fixture.yml",'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
