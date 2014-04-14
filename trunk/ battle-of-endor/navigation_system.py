# Navigation system
from panda3d.core import TextNode
from panda3d.core import Point2,Point3,Vec2,Vec3,Vec4
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

from filter import Lpf

# from navigation_system import NavigationSystem

class NavigationSystem(object):
	#-------------------------------------------------------------------------#
	def __init__(self, swActor, timestep):
	#-------------------------------------------------------------------------#
		self.swActor = swActor

		self.position = Vec3()

		# Velocity and acceleration are defined in 'ship coordinates'
		self.velocity = Vec3(0.001,1,1)
		self.accel = Vec3(0, 0, 0)

		# Position control
		self.errorOld = Vec3()
		self.integralErr = Vec3()

		# PID controller for the swactor acceleration
		self.accControl = PID(1, 0, 0)

		self.i = 0

		# Coordinate axes for global
		self.xh = Vec3(1,0,0)
		self.yh = Vec3(0,1,0)
		self.zh = Vec3(0,0,1)

		self.uvwOld = Vec3()

		self.updateHeading()

		self.iter = 0

		self.wayPoints = []
		self.curWayPoint = Vec3()
		self.wayPointLoc = 0

		self.turningRadius = 0.1

		self.hpr = Vec3(0,0,0)

	#-------------------------------------------------------------------------#
	def flyInCircle(self):
	#-------------------------------------------------------------------------#
		theta = self.i / ((2*pi)) % (4*pi);
		self.i = self.i + 0.1
		r = 1

		# Determine new velocity
		x = r*cos(theta)
		y = -r*sin(theta)
		z = -r*sin(theta)
		vel = Vec3(x,y,z)

		self.velocity = vel;
		self.updatePosition()
		self.updateHeading()

	#-------------------------------------------------------------------------#
	def addWayPoint(self, point):
	#-------------------------------------------------------------------------#
		self.wayPoints.append(point)
	
	#-------------------------------------------------------------------------#
	def followWayPoints(self):
	#-------------------------------------------------------------------------#
		# print Vec3(self.position - self.curWayPoint).length()
		if(Vec3(self.position - self.curWayPoint).length() < 20):
			self.wayPointLoc += 1
			self.curWayPoint = self.wayPoints[self.wayPointLoc]
		
		if(self.wayPointLoc == 0):
			self.curWayPoint = self.wayPoints[self.wayPointLoc]

		self.goToLocation(self.curWayPoint)

	#-------------------------------------------------------------------------#
	def goToLocation(self, loc):
	#-------------------------------------------------------------------------#
		# print loc
		# Define the ship coordinate system
		shipCoords = Vec3(self.velocity)
		shipCoords.normalize()
	
		# Map location into ship coordinates
		uh = Vec3(shipCoords.getX(), 0, 0)
		vh = Vec3(0, shipCoords.getY(), 0)
		wh = Vec3(0, 0, shipCoords.getZ())

		u = (loc-self.position).project(uh).getX()
		v = (loc-self.position).project(vh).getY()
		w = (loc-self.position).project(wh).getZ()

		# This is a hack, but it prevents NaN from getting through
		if(isnan(u)): u = self.uvwOld.getX()
		if(isnan(v)): v = self.uvwOld.getY()
		if(isnan(w)): w = self.uvwOld.getZ()
		self.uvwOld = Vec3(u,v,w)

		# Error in each direction
		error = Vec3(u,v,w)		

		# Run the PID controller for the acceleration
		newVel = error #self.accControl.run(error)

		# Get the individual current velocity components
		vx = self.velocity.getX()
		vy = self.velocity.getY()
		vz = self.velocity.getZ()

		# Get the individual new velocity components
		vxn = newVel.getX()
		vyn = newVel.getY()
		vzn = newVel.getZ()

		# Check the change in rotation about z
		dThetaZ = self.getAngle(Vec2(vx,vy), Vec2(vxn, vyn)) 
		# Determine allowed rotation about the Z axis
		angles = self.limitAngle(dThetaZ, self.turningRadius)
		cz = angles[0]
		sz = angles[1]

		# Check the change in rotation about y
		#dThetaY = self.getAngle(Vec2(vx, vz), Vec2(vxn, vzn))
		# Determine allowed rotation about the Y axis
		#angles = self.limitAngle(dThetaY, self.turningRadius)
		#cy = angles[0]
		#sy = angles[1]

		# Check the change in rotation about x
		dThetaX = self.getAngle(Vec2(vy, vz), Vec2(vyn, vzn))
		# Determine allowed rotation about the X axis
		angles = self.limitAngle(dThetaX, self.turningRadius)
		cx = angles[0]
		sx = angles[1]

		# cz = 1
		cy = 1
		# sz = 0
		sy = 0

		#######################################
		# Put it all together into a single rotation
		#######################################
		delVx = ( cy*cz)           *vx + (-cy*sz)           *vy + ( sy   )*vz
		delVy = ( sx*sy*cz + cx*sz)*vx + (-sx*sy*sz + cx*cz)*vy + (-sx*cy)*vz
		delVz = (-cx*sy*cz + sx*sz)*vx + ( cx*sy*sz + sx*cz)*vy + ( cx*cy)*vz

		finalVel = Vec3(delVx, delVy, delVz)
		finalVel.normalize()

		# Scale final Vel by the length of the 'wanted' velocity
		finalVel = finalVel * min(2,newVel.length())

		self.velocity = finalVel
		# self.velocity = Vec3(newVel)
		self.updatePosition()
		self.updateHeading()

		# print dThetaZ, dThetaY, dThetaX

		self.iter += 1

	#-------------------------------------------------------------------------#
	def getAngle(self, v1, v2):
	#-------------------------------------------------------------------------#
		v1.normalize()
		v2.normalize()
		return v1.signedAngleDeg(v2)

	#-------------------------------------------------------------------------#
	def limitAngle(self, val, maxVal):
	#-------------------------------------------------------------------------#
		if(val > maxVal):
			c = cos(maxVal)
			s = sin(maxVal)
		elif(val < -maxVal):
			c = cos(-maxVal)
			s = sin(-maxVal)
		else:
			c = cos(val)
			s = sin(val)

		return [c,s]

	#-------------------------------------------------------------------------#
	def updatePosition(self):
	#-------------------------------------------------------------------------#
		# Normalize the velocity for later
		velNorm = Vec3(self.velocity)
		velNorm.normalize()

		# Project the velocity onto the coordinate axes
		px = self.velocity.project(self.xh)
		py = self.velocity.project(self.yh)
		pz = self.velocity.project(self.zh)

		# Determine the change in position...maybe add acceleration?
		posDelta = Vec3(px.getX(), py.getY(), pz.getZ())#*time + 1/2at^2

		# Store the updated position
		self.position = self.position + posDelta
		self.swActor.setPos(self.position)

		# self.updateHeading(velNorm)
		

		# print self.position.getX(), self.position.getY(), self.position.getZ()
	
	#-------------------------------------------------------------------------#
	def updateHeading(self):
	#-------------------------------------------------------------------------#
		
		# velocity = Vec3(self.velocity)
		# velocity.normalize()

		# # Project velocity onto the xy plane, then calcualte the angle to x
		# hProj = Vec3(velocity.getX(), velocity.getY(), 0)
		# hProjN = Vec3(hProj)
		# hProjN.normalize()

		# # Determine the angle between the projection of the velocity onto the
		# # XY plane and xh
		# h = hProjN.angleDeg(self.xh)
		
		# # Panda3D will return the smaller of the two angles. We need complete
		# # rotation, and this calculation gives us the correct heading
		# if(velocity.getY() <= 0):
		# 	h = 360 - h

		# # Determine the pitch
		# p = velocity.angleDeg(self.zh)
	
		# self.hpr = Vec3(h-90, 90-p, 0)

		self.hpr = self.getDirection(self.velocity)
		
		# Update the heading and pitch of the actor
		self.swActor.setHpr(self.hpr)

	#-------------------------------------------------------------------------#
	def getDirection(self, vel):
	#-------------------------------------------------------------------------#
		velocity = Vec3(vel)
		velocity.normalize()

		# Project velocity onto the xy plane, then calcualte the angle to x
		hProj = Vec3(velocity.getX(), velocity.getY(), 0)
		hProjN = Vec3(hProj)
		hProjN.normalize()

		# Determine the angle between the projection of the velocity onto the
		# XY plane and xh
		h = hProjN.angleDeg(self.xh)
		
		# Panda3D will return the smaller of the two angles. We need complete
		# rotation, and this calculation gives us the correct heading
		if(velocity.getY() <= 0):
			h = 360 - h

		# Determine the pitch
		p = velocity.angleDeg(self.zh)

		return Vec3(h-90, 90-p, 0)

	#-------------------------------------------------------------------------#
	def evade(self, attacker):
	#-------------------------------------------------------------------------#
		pass

	#-------------------------------------------------------------------------#
	def pursue(self, target):
	#-------------------------------------------------------------------------#
		self.goToLocation(target.getPos()-target.getVelocity()*15)

	#-------------------------------------------------------------------------#
	def avoidAread(self, Vec3, r):
	#-------------------------------------------------------------------------#
		pass
	
	#-------------------------------------------------------------------------#
	def removeAvoidArea(self, area):
	#-------------------------------------------------------------------------#
		pass

	#-------------------------------------------------------------------------#
	def checkCollisionCourse(self):
	#-------------------------------------------------------------------------#
		pass

	#-------------------------------------------------------------------------#
	def findNearbyShips(self):
	#-------------------------------------------------------------------------#
		pass
		
	#-------------------------------------------------------------------------#
	def getPos(self):
	#-------------------------------------------------------------------------#
		return self.position
	
	#-------------------------------------------------------------------------#
	def setPos(self, pos):
	#-------------------------------------------------------------------------#
		self.position = pos

	#-------------------------------------------------------------------------#
	def getVelocity(self):
	#-------------------------------------------------------------------------#
		return self.velocity
	
	#-------------------------------------------------------------------------#
	def setVelocity(self, vel):
	#-------------------------------------------------------------------------#
		self.velocity = vel

	#-------------------------------------------------------------------------#
	def getTurningRadius(self):
	#-------------------------------------------------------------------------#
		return self.turningRadius
	
	#-------------------------------------------------------------------------#
	def setTurningRadius(self, radius):
	#-------------------------------------------------------------------------#
		self.turningRadius = radius

	#-------------------------------------------------------------------------#
	def getHpr(self):
	#-------------------------------------------------------------------------#
		return self.hpr