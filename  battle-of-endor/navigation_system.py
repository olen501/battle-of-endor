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
from panda3d.core import *

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

# from navigation_system import NavigationSystem

class NavigationSystem(object):
	def __init__(self, timestep):
		self.position = Vec3()
		self.velocity = Vec3()
		self.errorOld = Vec3()
		self.integralErr = Vec3()
		self.timestep = timestep

	def goToLocation(self, ship, loc):

		curLoc = ship.getPos()
		error = loc - curLoc

		print error.getX()

		kp = 0.2
		ki = 0.1
		kd = 0.1

		# Proportional eror
		prop = error*kp

		# Integral of accumlated error
		self.integralErr = self.integralErr+error
		integral = self.integralErr*ki

		# Derivative of error
		der = (error - self.errorOld)*kd

		# Final PID calculation
		accel = prop+integral+der
		
		# Calculate the new position and update ships position
		self.position = self.position*self.timestep + accel*self.timestep*self.timestep/2
		ship.setPos(self.position)

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
		