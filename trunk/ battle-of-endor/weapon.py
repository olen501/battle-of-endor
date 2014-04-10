from panda3d.core import TextNode
from panda3d.core import Point2,Point3,Vec3,Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait,Func
from panda3d.core import Camera
from panda3d.core import Spotlight

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor, VBase4, DirectionalLight, PerspectiveLens

from math import sqrt

from star_wars_actor import StarWarsActor


# Weapon - the base weapon class for all weapons in the simulation
class Weapon():
	def __init__(self, name, damage, range, cooldown = 5):
		self.name = name
		self.damage = damage
		self.range = range
		self.cooldown = cooldown

		# this is a list of references to all laser objects that have been fired
		self.shotList = []

	# Construct a message that this weapon was fired. Likely called from the
	# weapon system, with the message passed on somehow.
	def fire(self, parent, target):
		laser = Laser(parent, target, self.name + str(len(self.shotList)), self.damage, self.range, self.removeShot)
		self.shotList.append(laser)

	def getName(self):
		return self.name
	def setName(self, name):
		self.name = name

	def getDamage(self):
		return self.damage
	def setDamage(self, damage):
		self.damage = damage

	def getRange(self):
		return self.range
	def setRange(self, range):
		self.range = range

	def getCooldown(self):
		return self.cooldown
	def setCooldown(self, cooldown):
		self.cooldown = cooldown1

	def removeShot(self, shot):
		try:
			self.shotList.remove(shot)
		except (ValueError, AttributeError):
			pass


class Laser(StarWarsActor):
	def __init__(self, parent, target, name, damage, range, callback):
		super(Laser, self).__init__("models/beamred", 0.3, "laser")
		self.parent = parent
		self.target = target
		self.name = name
		self.damage = damage
		self.range = range
		self.callback = callback
		
		self.speed = 70
		self.startPos = self.parent.getPos()
		# px = self.parent.center.getX()
		# py = self.parent.center.getY()
		# pz = self.parent.center.getZ()
		# tx = self.target.getX()
		# ty = self.target.getY()
		# tz = self.target.getZ()

		self.reparentTo(render)
		self.setScale(1)
		#self.setPos(Point3(px, py, pz))
		self.setPos(self.startPos)

		#need to set velocity and heading
		self.setHeading(self.parent.getHeading())
		self.setVelocity((self.parent.getHeading() * self.speed) + self.parent.getVelocity())

		# add the task of updating to the taskMgr
		self.tsk = taskMgr.add(self.update, self.name)

################## Take all of this out, this is just so I could see the laser during testing!!! ################
		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(Vec4(1, 0, 0, 1))
		directionalLightNP = render.attachNewNode(directionalLight)

		directionalLightNP.setHpr(180, -20, 0)
		self.setLight(directionalLightNP)

	def remove(self):
		taskMgr.remove(self.tsk)
		self.callback(self)
		self.destroy()		

	def onCollision(self, swactor):
		# need to check to make sure it's not another laser
		self.remove()

	def getDistance(self, x0, x1):
		return sqrt((x1.getX() - x0.getX())**2 + (x1.getY() - x0.getY())**2 + (x1.getZ() - x0.getZ())**2)

	def update(self, task):
		dt = task.time  #this is the elapsed time since the first call of this function
		#dt = task.time - task.last  #obtains the time since that last frame.
		#task.last = task.time

		pos = self.startPos + self.getVelocity()*dt
		self.setPos(pos)

		distance = self.getDistance(self.startPos, pos)
		if distance >= self.range:
			self.remove()
		else:
			self.checkCollision()

		return task.cont