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


# Ships should only update their neighbors list when a ship crosses into or out of the neighboring
# cells around it. Otherwise they don't need to update. Because, for example, if it just happens
# that the same set of ships stay in the same set of cells, you never need to actually update
# their neighbors, because they are always the same. Only when a new ship enters those cells, or
# one ship leaves those cells, do we need to update.
class Ship(StarWarsActor):
	def __init__(self, model, timestep, name, hitpoints, shields, commandLevel):
		super(Ship, self).__init__(model, timestep, name)

		
		self.weaponSystem = WeaponSystem(self)
		# self.commandSystem = CommandSystem()

		self.hitpoints = hitpoints
		self.shields = shields
		self.commandLevel = commandLevel
		self.t = 0
		self.nearByShips = None
		self.grid_id = None
		self.type = 'ship'
		self.target = None

	def goTo(self, loc):
		self.navSystem.goToLocation(loc)

	def onCollision(self, swActor):
		if (swActor.type == 'ship'):
			self.destroy()
		else:
			self.hitpoints = self.hitpoints - (swActor.damage * (1.0 - self.shields))
			if self.hitpoints <= 0:
				self.destroy()


class Xwing(Ship):
	def __init__(self, name):
		hitpoints = 200.0
		shields = 0.5
		commandLevel = 1
		model = "models/xwing"
		timestep = 0.3

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

		super(Xwing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)
		self.setScale(3)



class Ywing(Ship):
	def __init__(self, name):
		hitpoints = 300.0
		shields = 0.5
		commandLevel = 1
		model = "models/ywing"
		timestep = 0.3

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

		super(Ywing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)
		self.setScale(3)



class Awing(Ship):
	def __init__(self, name):
		hitpoints = 100.0
		shields = 0.0
		commandLevel = 1
		model = "models/ship"
		timestep = 0.3

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

		super(Awing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)
		self.setScale(2)



class Bwing(Ship):
	def __init__(self, name):
		hitpoints = 300.0
		shields = 0.5
		commandLevel = 1
		model = "models/ship"
		timestep = 0.3

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

		super(Bwing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)
		self.setScale(2)



class TieFighter(Ship):
	def __init__(self, name):
		hitpoints = 100.0
		shields = 0.0
		commandLevel = 1
		model = "models/tie"
		timestep = 0.3

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 1

		super(TieFighter, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)
		self.setScale(2)



class TieInterceptor(Ship):
	def __init__(self, name):
		hitpoints = 100.0
		shields = 0.0
		commandLevel = 1
		model = "models/ship"
		timestep = 0.3

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 1

		super(TieInterceptor, self).__init__(model, timestep, name, hitpoints, shields, commandLevel)
		self.setScale(2)	



# s = Ship(1)