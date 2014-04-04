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
	def __init__(self, model, timestep):
		Actor.__init__(self, model)

		self.navSystem = NavigationSystem(timestep)
		# self.weaponSystem = WeaponSystem()
		# self.commandSystem = CommandSystem()

		self.hitpoints = 100
		self.shields = 100
		self.commandLevel = 1
		self.t = 0

	def update(self):

		self.navSystem.goToLocation(self, Vec3(10,10,10))

	def goTo(self, loc):
		self.navSystem.goToLocation(self, loc)




# s = Ship(1)