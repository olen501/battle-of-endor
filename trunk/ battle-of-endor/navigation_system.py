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
		self.velocity = Vec3(1,1,0)
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

	#-------------------------------------------------------------------------#
	def flyInCircle(self):
	#-------------------------------------------------------------------------#
		theta = self.i / ((2*pi)) % (4*pi);
		self.i = self.i + 0.1
		r = 1

		# Determine new velocity
		x = r*cos(theta)
		y = -r*sin(theta)
		z = 0#-r*sin(theta)
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
		print Vec3(self.position - self.curWayPoint).length()
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
		newVel = self.accControl.run(error)

		# Probably parameterize this value. It is essentially the turning
		# radius
		maxdTheta = self.turningRadius
		cm = cos(maxdTheta)
		sm = sin(maxdTheta)

		# Determine the angle between the new velocity and the old velocity
		newVelN = Vec3(newVel)
		newVelN.normalize()
		velN = Vec3(self.velocity) 
		velN.normalize()

		# Get the individual velocity components
		vx = self.velocity.getX()
		vy = self.velocity.getY()
		vz = self.velocity.getZ()

		# Check the change in heading component		
		velNz = Vec2(velN.getX(),velN.getY())
		velNz.normalize()
		velNewNz = Vec2(newVelN.getX(), newVelN.getY())
		velNewNz.normalize()
		dThetaZ = velNz.signedAngleDeg(velNewNz)

		# Determine allowed rotation about the Z axis
		if(dThetaZ > maxdTheta):
			c = cos(maxdTheta)
			s = sin(maxdTheta)
		elif(dThetaZ < -maxdTheta):
			c = cos(-maxdTheta)
			s = sin(-maxdTheta)
		else:
			c = cos(dThetaZ)
			s = sin(dThetaZ)

		# Limit the maximum that the ship can turn
		limitedVel = Vec3()
		limitedVel = limitedVel + Vec3(vx*c - vy*s,
             			  			   vx*s + vy*c,
             			  			   vz )

		# dThetaY = velN.angleDeg(vh)
		# dThetaZ = velN.angleDeg(wh)

		
		# limitedVel = limitedVel + Vec3(vx ,
#               			       vy*c - vz*s,
#               			       vy*s + vz*c)

		# limitedVel = limitedVel + Vec3(vx*c + vz*s,
  #             			  			   vy,
  #             			 			  -vx*s + vz*c)

		# limitedVel = limitedVel + Vec3(vx*c - vy*s,
  #            			  			   vx*s + vy*c,
  #            			  			   vz )

		newVel = Vec3(limitedVel)
		self.velocity = Vec3(newVel)
		self.updatePosition()
		self.updateHeading()

		self.iter += 1

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
		
		velocity = Vec3(self.velocity)
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
	
		# Update the heading and pitch of the actor
		self.swActor.setH(h-90)
		self.swActor.setP(90-p)

	#-------------------------------------------------------------------------#
	def evade(self, attacker):
	#-------------------------------------------------------------------------#
		pass

	#-------------------------------------------------------------------------#
	def pursue(self, target):
	#-------------------------------------------------------------------------#
		self.goToLocation(target.getPos()-target.getVelocity()*5)

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
	def getHeading(self):
	#-------------------------------------------------------------------------#
		return self.heading
	
	#-------------------------------------------------------------------------#
	def setHeading(self, heading):
	#-------------------------------------------------------------------------#
		self.heading = heading

	#-------------------------------------------------------------------------#
	def getTurningRadius(self):
	#-------------------------------------------------------------------------#
		return self.turningRadius
	
	#-------------------------------------------------------------------------#
	def setTurningRadius(self, radius):
	#-------------------------------------------------------------------------#
		self.turningRadius = radius