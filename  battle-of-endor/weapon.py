

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
		laser = Laser(parent, target, self.damage)
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
	def __init__(self, parent, target, damage):
		self.parent = parent
		self.target = target
		self.damage = damage

		px = self.parent.center.getX() 
		py = self.parent.center.getY() 
		pz = self.parent.center.getZ()
		tx = self.target.getX()
		ty = self.target.getY()
		tz = self.target.getZ()


