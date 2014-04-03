from direct.actor.Actor import Actor


class Ship(Actor):
	def __init__(self):
		Actor.__init__(self)
		
		self.navSystem = NavigationSystem()
		self.weaponSystem = WeaponSystem()
		self.commandSystem = CommandSystem()

		self.hitpoints = 100;
		self.shields = 100;
		self.commandLevel = 1;		
