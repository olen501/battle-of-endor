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

from star_wars_actor import StarWarsActor
from weapon_system import WeaponSystem
from navigation_system import NavigationSystem

# import direct.directbase.DirectStart


class Ship(StarWarsActor):
	def __init__(self, model, timestep, name, hitpoints, shields, commandLevel):
		super(Ship, self).__init__(model, timestep, name)

		
		self.weaponSystem = WeaponSystem(self)
		# self.commandSystem = CommandSystem()

		self.hitpoints = hitpoints
		self.shields = shields  # this is a percentage of how much damage gets through (1.0 is 100% of damage)
		self.commandLevel = commandLevel
		self.t = 0
		self.nearByShips = None

		self.target = None

	def goTo(self, loc):
		self.navSystem.goToLocation(loc)

	def onCollision(self, swActor):
		if isinstance(swActor, Ship):
			self.destroy()
		else:
			self.hitpoints = self.hitpoints - (swActor.damage * self.shields)
			swActor.remove()
			if self.hitpoints <= 0:
				self.destroy()


class Xwing(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 200.0
		shields = 0.5
		commandLevel = 1
		super(Xwing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

class Ywing(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 300.0
		shields = 0.5
		commandLevel = 1
		super(Ywing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0


class Awing(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100.0
		shields = 1.0
		commandLevel = 1
		super(Awing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0


class Bwing(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 300.0
		shields = 0.5
		commandLevel = 1
		super(Bwing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0


class TieFighter(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100.0
		shields = 1.0
		commandLevel = 1
		super(TieFighter, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 1


class TieInterceptor(Ship):
	def __init__(self, model, timestep, name):
		hitpoints = 100.0
		shields = 1.0
		commandLevel = 1
		super(TieInterceptor, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)	

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 1


# s = Ship(1)