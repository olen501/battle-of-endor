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
from weapon_system import *
from navigation_system import NavigationSystem

# import direct.directbase.DirectStart


# Ships should only update their neighbors list when a ship crosses into or out of the neighboring
# cells around it. Otherwise they don't need to update. Because, for example, if it just happens
# that the same set of ships stay in the same set of cells, you never need to actually update
# their neighbors, because they are always the same. Only when a new ship enters those cells, or
# one ship leaves those cells, do we need to update.
class Ship(StarWarsActor):
	def __init__(self, model, timestep, name, hitpoints, shields, commandLevel, weaponSystem):
		super(Ship, self).__init__(model, timestep, name)

		self.weaponSystem = weaponSystem(self)
		# self.commandSystem = CommandSystem()

		self.hitpoints = hitpoints
		self.shields = shields
		self.commandLevel = commandLevel
		self.t = 0
		self.nearByShips = None
		self.grid_id = None
		self.type = 'ship'
		self.target = None

	def coordinateTransform(self, loc):
		shipCoords = Vec3(self.navSystem.getVelocity())
		shipCoords.normalize()
	
		# Map location into ship coordinates
		uh = Vec3(shipCoords.getX(), 0, 0)
		vh = Vec3(0, shipCoords.getY(), 0)
		wh = Vec3(0, 0, shipCoords.getZ())

		u = (loc-self.navSystem.getPos()).project(uh).getX()
		v = (loc-self.navSystem.getPos()).project(vh).getY()
		w = (loc-self.navSystem.getPos()).project(wh).getZ()

		return Vec3(u, v, w)

	def goTo(self, loc):
		self.navSystem.goToLocation(loc)

	def onCollision(self, swActor):
		if (swActor.type == 'ship'):
			self.weaponSystem.destroy()
			self.destroy()
		else:
			self.hitpoints = self.hitpoints - (swActor.damage * (1.0 - self.shields))
			if self.hitpoints <= 0:
				self.weaponSystem.destroy()
				self.destroy()

	def onTargeted(self, attacker):
		self.attackers.append(attacker)

	def onUnTargeted(self, attacker):
		if(attacker in self.attackers): 
			self.attackers.remove(attacker)

	def getNumAttackers(self):
		return self.attackers.length()


class Xwing(Ship):
	def __init__(self, name):
		hitpoints = 200.0
		shields = 0.5
		commandLevel = 1
		model = "models/xwing"
		timestep = 0.3
		weaponSystem = XwingWeaponSystem

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

		super(Xwing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel, weaponSystem)
		self.setScale(3)

		self.setTurningRadius(0.05)


class Ywing(Ship):
	def __init__(self, name):
		hitpoints = 300.0
		shields = 0.5
		commandLevel = 1
		model = "models/ywing"
		timestep = 0.3
		weaponSystem = YwingWeaponSystem

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

		super(Ywing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel, weaponSystem)
		self.setScale(3)



class Awing(Ship):
	def __init__(self, name):
		hitpoints = 100.0
		shields = 0.0
		commandLevel = 1
		model = "models/awing"
		timestep = 0.3
		weaponSystem = AwingWeaponSystem

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

		super(Awing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel, weaponSystem)
		self.setScale(2)



class Bwing(Ship):
	def __init__(self, name):
		hitpoints = 300.0
		shields = 0.5
		commandLevel = 1
		model = "models/bwing"
		timestep = 0.3
		weaponSystem = BwingWeaponSystem

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 0

		super(Bwing, self).__init__(model, timestep, name, hitpoints, shields, commandLevel, weaponSystem)
		self.setScale(2)

		self.setTurningRadius(0.15)



class TieFighter(Ship):
	def __init__(self, name):
		hitpoints = 100.0
		shields = 0.0
		commandLevel = 1
		model = "models/tie"
		timestep = 0.3
		weaponSystem = TieFighterWeaponSystem

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 1

		super(TieFighter, self).__init__(model, timestep, name, hitpoints, shields, commandLevel, weaponSystem)
		self.setScale(2)

		self.setTurningRadius(0.2)



class TieInterceptor(Ship):
	def __init__(self, name):
		hitpoints = 100.0
		shields = 0.0
		commandLevel = 1
		model = "models/tie_int"
		timestep = 0.3
		weaponSystem = TieInterceptorWeaponSystem

		# team is which side you are on. 0 is rebels, 1 is empire
		self.team = 1

		super(TieInterceptor, self).__init__(model, timestep, name, hitpoints, shields, commandLevel, weaponSystem)
		self.setScale(2)	



# s = Ship(1)