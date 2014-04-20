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
from space import space
# import direct.directbase.DirectStart

class StarWarsActor(Actor):
	def __init__(self, model, timestep, name):
		super(StarWarsActor, self).__init__(model)

		self.name = name
		self.timestep = timestep
		self.nearBySwActorsAll = []
		self.nearBySwActors = []
		self.navSystem = NavigationSystem(self, timestep)
		self.new_neighbors = None
		self.detached = False

		self.sight = 1000
		self.dt = 0
		self.gridLoc = None

		self.radius = 5

		self.task = taskMgr.add(self.update, name + '-task')

		self.firstLoad = True

	def update(self, task):

		if(space.hasNewNeighbors(self.gridLoc) or self.firstLoad == True):			
			self.nearBySwActorsAll = space.getNeighbors(self.gridLoc)

		self.nearBySwActors = []
		
		# Filter by sight
		for swActor in self.nearBySwActorsAll:
			dist = (swActor.getPos() - self.getPos()).length()
			if( dist < self.sight and swActor != self):
				self.nearBySwActors.append(swActor)

		self.checkCollision()
		self.firstLoad = False

	def checkCollision(self):
		# Check all nearby ships for a collision
		for swactor in self.nearBySwActors:
			
			# Calculate distance between two ships
			diff = Vec3(self.getPos() - 
				swactor.getPos()).length()

			minNoCol = self.radius + swactor.radius
			if(diff < minNoCol):
				self.onCollision(swactor)
				return

	def onCollision(self, swactor):
		pass

	def destroy(self):
		# XXX remove from central controller

		taskMgr.remove(self.task)
		self.detachNode()
		self.detached = True
		space.remove(self, self.gridLoc)

	def updateCellLocation(self):
		cSize = space.c_size
		x = self.limitCellLoc(floor(self.getPos().getX()/cSize))
		y = self.limitCellLoc(floor(self.getPos().getY()/cSize))
		z = self.limitCellLoc(floor(self.getPos().getZ()/cSize))

		if(self.gridLoc is None):
			newGridLoc = Vec3(x,y,z)
			space.update(self, self.gridLoc, newGridLoc)
			self.gridLoc = Vec3(newGridLoc)
		elif( (self.gridLoc.getX() != x) or
			  (self.gridLoc.getY() != y) or
			  (self.gridLoc.getZ() != y) ):
			newGridLoc = Vec3(x,y,z)
			space.update(self, self.gridLoc, newGridLoc)
			self.gridLoc = Vec3(newGridLoc)

	def limitCellLoc(self, val):
		if(val < 0):
			val = 0
		elif(val >= space.getC_dim()):
			val = space.getC_dim() - 1
		return val


	def getName(self):
		return self.name
		
	def setName(self, name):
		self.name = name

	def setPos(self, pos):
		super(StarWarsActor, self).setPos(pos)
		self.navSystem.setPos(pos)
		self.updateCellLocation()

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

	def setSight(self, sight):
		self.sight = sight
	def getSight(self):
		return self.sight

	def setTurningRadius(self, r):
		self.navSystem.setTurningRadius(r)
	def getTurningRadius(self):
		return self.navSystem.getTurningRadius()