from panda3d.core import Point3,Vec3
from direct.task.Task import Task

class CentralController:
	
	def __init__(self):
		self.swActors = []


	def addObject(self, swActor):
		self.swActors.append(swActor)
	
	# This will need to be replaced by the actual function once the tree is 
	# up and running
	def findNearbyObjects(self, swActor):
		nearByObjects = []
		# Loop over all objects
		for curActor in self.swActors:
			# If not the current object and object is attached tp the simulation
			if(curActor != swActor and curActor.detached == False):
				# Check the distance
				dist = (curActor.getPos() - swActor.getPos()).length()
				# If object is in sight-range, add to nearby objects
				if(dist < swActor.getSight()):
					nearByObjects.append(curActor)

		return nearByObjects

	# Iterate over all objects in the simulation
	def run(self, task):
		dt = globalClock.getDt()

		for curActor in self.swActors:
			# Clean up any actors that are no longer being rendered
			if(curActor.detached == True):
				curActor = None
				continue
			# Find the nearby objects
			near = self.findNearbyObjects(curActor)
			curActor.update(dt, near)

		return Task.cont