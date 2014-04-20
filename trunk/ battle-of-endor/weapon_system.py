# from ship import Ship
from weapon import *
from panda3d.core import Vec3, Vec2

class WeaponSystem(object):
	def __init__(self, ship, weaponClose, weaponLong):
		
		# Ship weapons - in order to make a unique name so that other ships may
		# be less susceptiable to a certain weapon, each weapon has a name
		# related to the ship. This requires a ship.getName() function in the
		# Ship() class.

		# Close range weapon
		self.weaponCloseRange = weaponClose
		# Long range weapon
		self.weaponLongRange  = weaponLong

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
	def update(self, task):

		# XXX need to get the DT
		dt = 0.5

		# target = self.getTarget()
		# print target
		nextState = self.currentState
		if self.target is None:
			self.target = self.aquireTarget()
			#self.currentState = self.STATE_IDLE
			nextState = self.STATE_IDLE	

		if (self.currentState == self.STATE_IDLE):
			if(self.target is not None):
				self.setTarget(self.target)
				self.activateDt = 0
				nextState = self.STATE_ACTIVATE

		if (self.currentState == self.STATE_ACTIVATE):
			if(self.activateDt > self.weaponActivate):
				self.selectWeapon(self.target)
				self.activateDt = 0
				nextState = self.STATE_READY
			else:
				self.activateDt += dt

		if (self.currentState == self.STATE_READY):
			
			# New target assignment
			# if((self.target is not None) and (self.target != self.target)):
				# self.setTarget(target)				
			
			# Check if we need to change weapons
			lastActWeap = self.activeWeapon
			self.selectWeapon(self.target)			
			if(self.activeWeapon != lastActWeap):
				# Change of weapon, must activate it
				self.activateDt = 0
				nextState = self.STATE_ACTIVATE
			elif(self.isGoodShot()):
				# Take a shot
				self.fireWeapon()
				self.cooldownDt = 0
				nextState = self.STATE_COOLDOWN

		if (self.currentState == self.STATE_COOLDOWN):
			if(self.cooldownDt > self.activeWeapon.getCooldown()):
				self.cooldownDt = 0
				nextState = self.STATE_READY
			else:
				self.cooldownDt += dt

		# Update our state
		self.currentState = nextState


	# Prototype method - ultimately how the weapon system selects a target	
	def aquireTarget(self):
		for nearByShip in self.ship.nearBySwActors:
			if self.ship.team != nearByShip.team:
				if self.getDistanceToTarget(nearByShip) <= self.weaponLongRange.getRange():
					return nearByShip
		return None

	# Weapon system setting a specific ship as its target
	def setTarget(self, target):
		self.targetSet = True
		self.target = target
	def getTarget(self):
		return self.target

	# Remove a ship from its target
	def removeTarget(self):
		self.targetSet = False
		self.target = None

	# Select a weapon to use based soley on the distance to the target	
	def selectWeapon(self, target):
		distToTarget = self.getDistanceToTarget(target)
		
		if(distToTarget > self.weaponCloseRange.getRange()):
			self.activeWeapon = self.weaponLongRange
		else:
			self.activeWeapon = self.weaponCloseRange

	# Returns the distance from the weapon system's ship to the target's ship.
	# This may want to be moved to static utility class.
	def getDistanceToTarget(self, target):
		return Vec3(self.ship.getPos()-target.getPos()).length()

	# Prototype for firing a message
	def fireWeapon(self):
		self.activeWeapon.fire(self.ship, self.target)

	def isGoodShot(self):
		localTargetPos = self.ship.coordinateTransform(self.target.getPos())

		# difference in heading
		dh = self.ship.navSystem.getAngle(Vec2(0, 1), Vec2(localTargetPos.getX(), localTargetPos.getY()))

		# difference in pitch
		dp = self.ship.navSystem.getAngle(Vec2(0, 1), Vec2(localTargetPos.getZ(), localTargetPos.getY()))

		if ((dh < 10) and (dh > -10)) and ((dp < 10) and (dp > -10)):
			return True
		else:
			return False

	def destroy(self):
		for gun in self.weaponCloseRange.gunList:
			gun.detachNode()
		for gun in self.weaponLongRange.gunList:
			gun.detachNode()


class XwingWeaponSystem(WeaponSystem):
	def __init__(self, ship):
		weaponClose = XwingWeapon(ship, ship.getName() + '-wClose', RedLaserShort, 50)
		weaponLong = XwingWeapon(ship, ship.getName() + '-wLong', RedLaserLong, 100)
		super(XwingWeaponSystem, self).__init__(ship, weaponClose, weaponLong)


class YwingWeaponSystem(WeaponSystem):
	def __init__(self, ship):
		weaponClose = YwingWeapon(ship, ship.getName() + '-wClose', RedLaserShort, 50)
		weaponLong = YwingWeapon(ship, ship.getName() + '-wLong', RedLaserLong, 100)
		super(YwingWeaponSystem, self).__init__(ship, weaponClose, weaponLong)


class AwingWeaponSystem(WeaponSystem):
	def __init__(self, ship):
		weaponClose = AwingWeapon(ship, ship.getName() + '-wClose', RedLaserShort, 50)
		weaponLong = AwingWeapon(ship, ship.getName() + '-wLong', RedLaserLong, 100)
		super(AwingWeaponSystem, self).__init__(ship, weaponClose, weaponLong)


class BwingWeaponSystem(WeaponSystem):
	def __init__(self, ship):
		weaponClose = BwingWeapon(ship, ship.getName() + '-wClose', RedLaserShort, 50)
		weaponLong = BwingWeapon(ship, ship.getName() + '-wLong', RedLaserLong, 100)
		super(BwingWeaponSystem, self).__init__(ship, weaponClose, weaponLong)


class TieFighterWeaponSystem(WeaponSystem):
	def __init__(self, ship):
		weaponClose = TieFighterWeapon(ship, ship.getName() + '-wClose', GreenLaserShort, 50)
		weaponLong = TieFighterWeapon(ship, ship.getName() + '-wLong', GreenLaserLong, 100)
		super(TieFighterWeaponSystem, self).__init__(ship, weaponClose, weaponLong)


class TieInterceptorWeaponSystem(WeaponSystem):
	def __init__(self, ship):
		weaponClose = TieInterceptorWeapon(ship, ship.getName() + '-wClose', GreenLaserShort, 50)
		weaponLong = TieInterceptorWeapon(ship, ship.getName() + '-wLong', GreenLaserLong, 100)
		super(TieInterceptorWeaponSystem, self).__init__(ship, weaponClose, weaponLong)

