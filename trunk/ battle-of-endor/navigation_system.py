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
	def __init__(self, swActor, timestep):

		self.swActor = swActor
		self.timestep = timestep

		self.position = Vec3()
		self.velocity = Vec3()
		self.heading = Vec3(1,0,0)
		self.headingGlobal = Vec3(0,1,0)

		# Position control
		self.errorOld = Vec3()
		self.integralErr = Vec3()

		# PID controller for the swactor acceleration
		self.accControl = PID(0.2, 0.1, 0.1)

		self.i = 0

	def flyInCircle(self):
		theta = self.i / ((2*pi)) % (4*pi);
		self.i = self.i + 0.1
		r = 0.50

		# Determine new velocity
		x = r*cos(theta)
		y = -r*cos(theta)
		z = -r*sin(theta)
		vel = Vec3(x,y,z)
		
		# Normalize the velocity for later
		velNorm = Vec3(vel)
		velNorm.normalize()

		# Coordinate axes for global
		xh = Vec3(1,0,0)
		yh = Vec3(0,1,0)
		zh = Vec3(0,0,1)

		# Project the velocity onto the coordinate axes
		px = vel.project(xh)
		py = vel.project(yh)
		pz = vel.project(zh)

		# Determine the change in position...maybe add acceleration?
		posDelta = Vec3(px.getX(), py.getY(), pz.getZ())#*time + 1/2at^2

		# Store the updated position
		self.position = self.position + posDelta
		self.swActor.setPos(self.position)

		# Project velocity onto the xy plane, then calcualte the angle to x
		hProj = Vec3(vel.getX(), vel.getY(), 0)
		hProjN = Vec3(hProj)
		hProjN.normalize()

		# Determine the angle between the projection of the velocity onto the
		# XY plane and xh
		h = hProjN.angleDeg(xh)
		
		# Panda3D will return the smaller of the two angles. We need complete
		# rotation, and this calculation gives us the correct heading
		if(vel.getY() <= 0):
			h = 360 - h

		# Determine the pitch
		p = velNorm.angleDeg(zh)
		
		# Update the heading and pitch of the actor
		# The -90 is an artifact of all models not being aligned. This needs to be
		# resolved!
		self.swActor.setH(h-90)
		self.swActor.setP(90-p)



	def goToLocation(self, loc):

		curLoc = self.swActor.getPos()
		error = loc - curLoc

		# Run the PID controller for the acceleration
		accel = self.accControl.run(error)

		# Calculate the new position and update ships position
		self.velocity = self.velocity + accel * self.timestep
		self.heading = self.velocity / self.velocity.length()

		self.position = self.position*self.timestep + accel*self.timestep*self.timestep/2
		self.swActor.setPos(self.position)

		# Store error
		self.errorOld = error


	def updatePosition(self):
		self.position = self.position + self.velocity*dt
		

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