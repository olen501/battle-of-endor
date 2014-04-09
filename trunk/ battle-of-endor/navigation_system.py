# Navigation system
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
from pid import PID

# from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

# from navigation_system import NavigationSystem

class NavigationSystem(object):
	def __init__(self, swactor, timestep):

		self.swactor = swactor
		self.timestep = timestep

		self.position = Vec3()
		self.velocity = Vec3()
		self.heading = Vec3()

		# Position control
		self.errorOld = Vec3()
		self.integralErr = Vec3()

		# PID controller for the swactor acceleration
		self.accControl = PID(0.2, 0.1, 0.1)
				
	def goToLocation(self, loc):

		curLoc = self.swactor.getPos()
		error = loc - curLoc

		# Run the PID controller for the acceleration
		accel = self.accControl.run(error)

		# Calculate the new position and update ships position
		self.velocity = self.velocity + accel * self.timestep
		self.heading = self.velocity / self.velocity.length()

		self.position = self.position*self.timestep + accel*self.timestep*self.timestep/2
		self.swactor.setPos(self.position)

		# Store error
		self.errorOld = error

		

	def evade(self, attacker):
		pass

	def pursue(self, target):
		pass

	def avoidAread(self, Vec3, r):
		pass

	def removeAvoidArea(self, area):
		pass

	def checkCollisionCourse(self):
		pass

	def findNearbyShips(self):
		pass
		
	def getPos(self):
		return self.position
	def setPos(self, pos):
		self.position = pos

	def getVelocity(self):
		return self.velocity
	def setVelocity(self, vel):
		self.velocity = vel

	def getHeading(self):
		return self.heading
	def setHeading(self, heading):
		self.heading = heading