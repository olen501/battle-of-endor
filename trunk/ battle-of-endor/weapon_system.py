# from ship import Ship
from weapon import *
from panda3d.core import Vec3

class WeaponSystem(object):
	def __init__(self, ship):
		
		# Ship weapons - in order to make a unique name so that other ships may
		# be less susceptiable to a certain weapon, each weapon has a name
		# related to the ship. This requires a ship.getName() function in the
		# Ship() class.

		if ship.team:
			weaponClose = GreenLaserShort
			weaponLong = GreenLaserLong
		else:
			weaponClose = RedLaserShort
			weaponLong = RedLaserLong

		# Close range weapon
		self.weaponCloseRange = Weapon(ship.getName()+'-wClose', weaponClose)
		# Long range weapon
		self.weaponLongRange  = Weapon(ship.getName()+'-wLong', weaponLong)

		# Time required to switch from one weapon to another. Don't know if we
		# want/need this, but felt it might be good to have the framework for
		# it.
		self.weaponChangeDelay = 5

		# Time required to activate the weapons
		self.weaponActivate = 5

		# Store which weapon is currently activated.
		self.activeWeapon = self.weaponLongRange

		# Reference to the weapon system's ship
		self.ship = ship

		# Does the weapon system current have a target
		self.targetSet = False

		# Reference to a ship that is the target of the weapon system
		self.target = None

		# Weapon System states
		self.STATE_IDLE = 0
		self.STATE_ACTIVATE = 1
		self.STATE_READY = 2
		self.STATE_COOLDOWN = 3

		# Initial states
		self.currentState = 0

		self.cooldownDt = 0
		self.activateDt = 0

	# Iterate through a state machine for the weapon system.
	# Need an elapsed time since the last frame
	# This is not final, but a rough outline
	def run(self, ship, dt):

		nextState = self.currentState
		target = self.getTarget()

		if(self.currentState == self.STATE_IDLE):
			if(target is not None):
				self.setTarget(target)
				self.activateDt = 0
				nextState = self.STATE_ACTIVATE

		if(self.currentState == self.STATE_ACTIVATE):
			if(self.activateDt > self.weaponActivate):
				self.selectWeapon()
				self.activateDt = 0
				nextState = self.STATE_READY
			else:
				self.activateDt += dt

		if(self.currentState == self.STATE_READY):
			
			# New target assignment
			if((target is not None) and (target != self.target)):
				self.setTarget(target)				
			
			# Check if we need to change weapons
			lastActWeap = self.activeWeapon
			self.selectWeapon()			
			if(self.activeWeapon != lastActWeap):
				# Change of weapon, must activate it
				self.activateDt = 0
				nextState = self.STATE_ACTIVATE
			elif(self.isGoodShot()):
				# Take a shot
				self.fireWeapon()
				self.cooldownDt = 0
				self.nextState = self.STATE_COOLDOWN

		if(self.currentState == self.STATE_COOLDOWN):
			if(self.cooldownDt > self.activeWeapon.getCooldown()):
				self.cooldownDt = 0
				self.nextState = self.STATE_READY
			else:
				self.cooldownDt += dt

		# Update our state
		self.currentState = nextState


	# Prototype method - ultimately how the weapon system selects a target	
	def getTarget(self):
		pass

	# Weapon system setting a specific ship as its target
	def setTarget(self, target):
		self.targetSet = True
		self.target = target

	# Remove a ship from its target
	def removeTarget(self):
		self.targetSet = False
		self.target = None

	# Select a weapon to use based soley on the distance to the target	
	def selectWeapon(self):
		distToTarget = self.getDistanceToTarget()
		
		if(distToTarget > self.weaponCloseRange.getRange()):
			self.activeWeapon = self.weaponLongRange
		else:
			self.activeWeapon = self.weaponCloseRange

	# Returns the distance from the weapon system's ship to the target's ship.
	# This may want to be moved to static utility class.
	def getDistanceToTarget(self):
		return Vec3(self.ship.getPos()-self.target.getPos()).length()

	# Prototype for firing a message
	def fireWeapon(self):
		self.activeWeapon.fire(self.ship, self.target)	
