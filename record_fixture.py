import yaml
import numpy_boids as bd
from copy import deepcopy
boids=bd.init_boids()
before=boids.tolist()
bd.update_boids(boids)
after=boids.tolist()
fixture={"before":before,"after":after}
fixture_file=open("fixture.yml",'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
