
# Weapon - the base weapon class for all weapons in the simulation
class Weapon():
	def __init__(self, name, damage, range, cooldown = 5):
		self.name = name
		self.damage = damage
		self.range = range
		self.cooldown = cooldown

	# Construct a message that this weapon was fired. Likely called from the
	# weapon system, with the message passed on somehow.
	def fire():
		pass

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