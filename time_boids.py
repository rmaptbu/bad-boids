import boids as bd
import object_boids as obd
import numpy_boids as nbd
import time

def time_bad_boids():
	boids=bd.init_boids()
	start_time=time.clock()
	for x in xrange(100):
		bd.update_boids(boids)
	end_time=time.clock()
	#duration of update boids averaged 1000 times in micro seconds
	return (end_time-start_time)*10

def time_object_boids():
	boids=obd.Boids(
		flock_attraction=0.01/50,
		avoidance_radius=10,
		formation_flying_radius=100,
		speed_matching_strength=0.125/50
	)
	boids.initialise_random(50)
	start_time=time.clock()
	for x in xrange(100):
		boids.update()
	end_time=time.clock()
	#duration of update boids averaged 1000 times in micro seconds
	return (end_time-start_time)*10

def time_numpy_boids():
	boids=nbd.init_boids()
	start_time=time.clock()
	for x in xrange(100):
		nbd.update_boids(boids)
	end_time=time.clock()
	#duration of update boids averaged 1000 times in micro seconds
	return (end_time-start_time)*10
	
print 'numpy:', time_numpy_boids(), 'original:', time_bad_boids()