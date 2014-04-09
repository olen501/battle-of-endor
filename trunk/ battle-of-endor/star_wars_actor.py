from panda3d.core import TextNode
from panda3d.core import Point2,Point3,Vec3,Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from math import sin, cos, pi
from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait,Func
from math import *
from math import pi, sin, cos
from panda3d.core import Camera
# from panda3d.core import *

# from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

from navigation_system import NavigationSystem

# import direct.directbase.DirectStart

class StarWarsActor(Actor):
	def __init__(self, model, timestep, name):
		super(StarWarsActor, self).__init__(model)

		self.name = name
		self.timestep = timestep

		self.radius = 5
		self.nearBySwActors = None
		self.navSystem = NavigationSystem(self, timestep)

		self.detached = False

	def update(self, nearBySwActors):
		self.nearBySwActors = nearBySwActors
		self.checkCollision()

	def checkCollision(self):
		# Check all nearby ships for a collision
		for swactor in self.nearBySwActors:

			# Calculate distance between two ships
			diff = Vec3(self.getPos() - 
				swactor.getPos()).length()

			minNoCol = self.radius + swactor.radius

			if(diff < minNoCol):
				swactor.onCollision(self)				
				self.onCollision(swactor)

	def onCollision(self, swactor):
		pass

	def destroy(self):
		self.detachNode()
		self.detached = True

	def getName(self):
		return self.name
		
	def setName(self, name):
		self.name = name

	def setPos(self, pos):
		super(StarWarsActor, self).setPos(pos)
		self.navSystem.setPos(pos)
	def getPos(self):
		return self.navSystem.getPos()

	def setHeading(self, heading):
		self.navSystem.setHeading(heading)
	def getHeading(self):
		return self.navSystem.getHeading()

	def setVelocity(self, vel):
		self.navSystem.setVelocity(vel)
	def getVelocity(self):
		return self.navSystem.getVelocity()