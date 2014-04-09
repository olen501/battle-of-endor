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
		laser = Laser(parent, target, self.damage, self.range)
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


class Laser(StarWarsActor):
	def __init__(self, parent, target, damage, range):
		super(Laser, self).__init__("models/beam", 0.3, "laser")
		self.parent = parent
		self.target = target
		self.damage = damage
		self.range = range
		self.speed = 10

		px = self.parent.center.getX() 
		py = self.parent.center.getY() 
		pz = self.parent.center.getZ()
		# tx = self.target.getX()
		# ty = self.target.getY()
		# tz = self.target.getZ()

		self.reparentTo(render)
		self.setScale(2)
		self.setPos(Point3(px, py, pz))

		#need to set velocity and heading
		self.setHeading(self.parent.getHeading())
		self.setVelocity((self.parent.getHeading() * self.speed) + self.parent.getVelocity())

	def onCollision(self, swactor):
		pass

	def update(self, task):
		dt = task.time - task.last  #obtains the time since that last frame.
		task.last = task.time
		
		return task.cont