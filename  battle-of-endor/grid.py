from star_wars_actor import * star_wars_actor

class GridSpace
	def __init__(self, x, x1, y, y1, z,z1):
		self.x = x
		self.x1 = x1
		self.y = y
		self.y1 = y1
		self.z = z
		self.z1 = z1
		self.objects = []

	def addShip(self,star_wars_actor):
		if(self.star_wars_actor):
			self.objects.append(star_wars_actor)


	def deleteShip(self,star_wars_actor,objects):
		for index in range(len(objects)):
			if(objects[index] == star_wars_actor)
				objects.remove(star_wars_actor)

	def getCoordinates(self):
		coor = []
		coor.append(x,x1,y,y1,z,z1);
		return coor

	