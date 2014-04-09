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

		self.radius = 0.05

		self.nearByShips = None

		self.navSystem = NavigationSystem(self, timestep)

	def update(self, nearByShips):
		self.nearByShips = nearByShips
		self.checkCollision()

	def checkCollision(self):
		# Check all nearby ships for a collision
		for ship in self.nearByShips:
			# Calculate distance between two ships
			diff = Vec3(self.navSystem.getPosition() - 
				ship.navSystem.getPosition())
			print self.name, self.navSystem.getPosition(), \
				  ship.name, ship.navSystem.getPosition(), \
				  diff
			minNoCol = self.radius + ship.radius

			# if(diff < minNoCol):
				# print 'Collision!'

	def checkCollision(self):
		pass

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def setPosition(self, pos):
		super(Ship, self).setPosition(pos)
		print 'here'
		navSystem.setPosition(pos)