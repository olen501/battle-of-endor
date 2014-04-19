# Navigation system
from panda3d.core import Point2,Point3,Vec2,Vec3
from direct.task.Task import Task
from math import sin, cos, pi

from filter import *

class NavigationSystem(object):
	#-------------------------------------------------------------------------#
	def __init__(self, swActor, timestep):
	#-------------------------------------------------------------------------#
		self.swActor = swActor

		self.position = Vec3()

		# Velocity and acceleration are defined in 'ship coordinates'
		self.velocity = Vec3(0.001,1,0.001)
		self.accel = Vec3(0, 0, 0)
		self.hpr = Vec3(0,0,1)
		self.velFilter = LpfVec3(Vec3(0,0,0),4)
		self.hprFilter = LpfVec3(Vec3(0,0,0),2)

		# Coordinate axes for global
		self.xh = Vec3(1,0,0)
		self.yh = Vec3(0,1,0)
		self.zh = Vec3(0,0,1)

		# Update our heading right away
		self.updateHeading()

		self.wayPoints = []
		self.curWayPoint = None
		self.wayPointLoc = 0
		self.i = 0

		self.turningRadius = 0.1

	#-------------------------------------------------------------------------#
	def flyInCircle(self):
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
		self.wayPoints.append(point)

	#-------------------------------------------------------------------------#
	def gotoNextWaypoint(self):
		self.curWayPoint = self.wayPoints.pop(0)
	
	#-------------------------------------------------------------------------#
	def followWayPoints(self):

		if(self.curWayPoint is not None):
			if((Vec3(self.position) - Vec3(self.curWayPoint)).length() < 20):
				self.gotoNextWaypoint()
				
			self.goToLocation(self.curWayPoint)

	#-------------------------------------------------------------------------#
	def goToLocation(self, loc):

#### This could be a bug, because coordinateTransform is only in Ship, not in StarWarActor!!!!!!	
		newVel = self.swActor.coordinateTransform(loc)	

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

		# Check the change in rotation about x
		dThetaX = self.getAngle(Vec2(vy, vz), Vec2(vyn, vzn))

		# Determine allowed rotation about the X axis		
		angles = self.limitAngle(dThetaX, self.turningRadius)
		cx = angles[0]
		sx = angles[1]

		# If we add roll, we will need to maybe incorporate these?
		cy = 1
		sy = 0

		# Put it all together into a single rotation
		delVx = ( cy*cz)           *vx + (-cy*sz)           *vy + ( sy   )*vz
		delVy = ( sx*sy*cz + cx*sz)*vx + (-sx*sy*sz + cx*cz)*vy + (-sx*cy)*vz
		delVz = (-cx*sy*cz + sx*sz)*vx + ( cx*sy*sz + sx*cz)*vy + ( cx*cy)*vz

		finalVel = Vec3(delVx, delVy, delVz)
		finalVel.normalize()

		velF = self.velFilter.filter(finalVel * max(1,min(4, newVel.length)))
		self.velocity = velF 

		self.updatePosition()
		self.updateHeading()

	#-------------------------------------------------------------------------#
	def getAngle(self, v1, v2):
		v1.normalize()
		v2.normalize()
		return v1.signedAngleDeg(v2)

	#-------------------------------------------------------------------------#
	def limitAngle(self, val, maxVal):

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
	
	#-------------------------------------------------------------------------#
	def updateHeading(self):

		newHpr = Vec3(self.getDirection(self.velocity))
		self.hpr = self.hprFilter.filter(newHpr)

		# Update the heading and pitch of the actor
		self.swActor.setHpr(self.hpr)

	#-------------------------------------------------------------------------#
	def getDirection(self, vel):
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

		r = -self.getAngle(Vec2(velocity.getY(),velocity.getX()),Vec2(1,1))
		# r = 0
		return Vec3(h-90, 90-p, r)

	#-------------------------------------------------------------------------#
	def evade(self, attacker):
		
		veln = Vec3(self.velocity)
		velAn = Vec3(attacker.getVelocity())
		veln.normalize()
		velAn.normalize()
		thetaV = veln.angleDeg(velAn)

		# Get distance between the ships
		aPos = attacker.getPos()
		posD = self.getPos()-attacker.getPos()

		if(posD.length() < 100 or abs(thetaV) < 90):
			self.goToLocation(aPos - Vec3(0,0,aPos.getZ()*10))
		else:
			self.updatePosition()
			self.updateHeading()


	#-------------------------------------------------------------------------#
	def pursue(self, target):
		self.goToLocation(target.getPos()-target.getVelocity()*15)

	#-------------------------------------------------------------------------#
	def avoidAread(self, Vec3, r):
		pass
	
	#-------------------------------------------------------------------------#
	def removeAvoidArea(self, area):
		pass

	#-------------------------------------------------------------------------#
	def checkCollisionCourse(self):
		pass

	#-------------------------------------------------------------------------#
	def findNearbyShips(self):
		pass
		
	#-------------------------------------------------------------------------#
	def getPos(self):
		return self.position
	
	#-------------------------------------------------------------------------#
	def setPos(self, pos):
		self.position = pos

	#-------------------------------------------------------------------------#
	def getVelocity(self):
		return self.velocity
	
	#-------------------------------------------------------------------------#
	def setVelocity(self, vel):
		self.velocity = vel

	#-------------------------------------------------------------------------#
	def getTurningRadius(self):
		return self.turningRadius
	
	#-------------------------------------------------------------------------#
	def setTurningRadius(self, radius):
		self.turningRadius = radius

	#-------------------------------------------------------------------------#
	def getHpr(self):
		return self.hpr