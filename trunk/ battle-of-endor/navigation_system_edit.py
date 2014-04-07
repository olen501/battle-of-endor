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
	def __init__(self, ship, timestep):

		self.ship = ship
		self.timestep = timestep

		self.position = Vec3()
		self.velocity = Vec3(0,0.1,0)
		self.heading = Vec3(0,1,0)


		# PID controller for the ship acceleration
		self.accControl = PID(0.002, -0.00000, -0.000000)
		# self.accControl.antiWindup(100)

	def reset(self):
		self.accControl.reset()
				
	def goToLocation(self, loc):

		curLoc = self.ship.getPos()

		dist = Vec3(loc - curLoc)

		# Normalize distance
		dist = Vec3(dist/dist.length())

		angle = acos((dist.getX()*self.heading.getX() + \
			          dist.getY()*self.heading.getY() + \
			          dist.getZ()*self.heading.getZ())/ \
					  (dist.length() * self.heading.length()))
		# print angle
		if(angle > 0.5):
			angleChange = 0.5
		elif (angle < 0.5):
			angleChange = -0.5		
		else:
			angleChange = angle

		print self.heading

		# Run the PID controller for the acceleration
		# accel = self.accControl.run(dist)

		# if((headingNew - self.heading) > 0.1):
		# 	self.heading += 0.1
		# elif((headingNew - self.heading) < 0.1):
		# 	self.heading -= 0.1
		# else:
		# 	self.heading = headingNew

		# Calculate the new position and update ships position
		# self.velocity = Vec3(self.velocity + accel * self.timestep);

		# self.position = self.position + self.velocity*self.timestep + accel*self.timestep*self.timestep/2
		# self.ship.setPos(self.position)

		# Must avoid divide by zero
		# if(self.velocity.getX() != 0):
		# 	h = -90+(tan(self.velocity.getY()/self.velocity.getX()))*180/pi
		# else:
		# 	h = 90

		# if(self.velocity.getX() < 0):
			 # h = -h
		# self.ship.setH(h)
		# self.heading = self.velocity/self.velocity.length()

		self.ship.setHpr(self.heading)

		# print angle
	

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
		