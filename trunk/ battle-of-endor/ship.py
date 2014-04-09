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

# import direct.directbase.DirectStart


class Ship(Actor):
	def __init__(self, model, timestep, name, hitpoints, shields, commandLevel):
		super(Ship, self).__init__(model)

		self.name = name

		self.navSystem = NavigationSystem(self, timestep)
		# self.weaponSystem = WeaponSystem()
		# self.commandSystem = CommandSystem()

		self.hitpoints = hitpoints
		self.shields = shields
		self.commandLevel = commandLevel
		self.t = 0

	def update(self):

		self.navSystem.goToLocation(Vec3(10,10,10))

	def goTo(self, loc):
		self.navSystem.goToLocation(loc)

	def getName(self):
		return self.name
	def setName(self, name):
		self.name = name



class Xwing(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100
		shields = 100
		commandLevel = 1
		super(Xwing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)


class Ywing(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100
		shields = 100
		commandLevel = 1
		super(Ywing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)


class Awing(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100
		shields = 100
		commandLevel = 1
		super(Awing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)


class Bwing(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100
		shields = 100
		commandLevel = 1
		super(Bwing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)


class TieFighter(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100
		shields = 100
		commandLevel = 1
		super(TieFighter, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)


class TieInterceptor(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100
		shields = 100
		commandLevel = 1
		super(TieInterceptor, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)	


# s = Ship(1)