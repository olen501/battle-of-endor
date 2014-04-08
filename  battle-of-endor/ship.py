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
	def __init__(self, model, timestep, name):
		super(Ship, self).__init__(model)

		self.name = name

		self.navSystem = NavigationSystem(self, timestep)
		# self.weaponSystem = WeaponSystem()
		# self.commandSystem = CommandSystem()

		self.hitpoints = 100
		self.shields = 100
		self.commandLevel = 1
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
	def __init__(self, *args, **kwargs):
		super(Xwing, self).__init__(*args, **kwargs)
		self.hitpoints = 100
		self.shields = 100
		self.commandLevel = 1
		self.t = 0


class Ywing(Ship):
	def __init__(self, *args, **kwargs):
		super(Ywing, self).__init__(*args, **kwargs)
		self.hitpoints = 100
		self.shields = 100
		self.commandLevel = 1
		self.t = 0


class Awing(Ship):
	def __init__(self, *args, **kwargs):
		super(Awing, self).__init__(*args, **kwargs)
		self.hitpoints = 100
		self.shields = 100
		self.commandLevel = 1
		self.t = 0


class Bwing(Ship):
	def __init__(self, *args, **kwargs):
		super(Bwing, self).__init__(*args, **kwargs)
		self.hitpoints = 100
		self.shields = 100
		self.commandLevel = 1
		self.t = 0


class TieFighter(Ship):
	def __init__(self, *args, **kwargs):
		super(TieFighter, self).__init__(*args, **kwargs)
		self.hitpoints = 100
		self.shields = 100
		self.commandLevel = 1
		self.t = 0


class TieInterceptor(Ship):
	def __init__(self, *args, **kwargs):
		super(TieInterceptor, self).__init__(*args, **kwargs)
		self.hitpoints = 100
		self.shields = 100
		self.commandLevel = 1
		self.t = 0	


# s = Ship(1)