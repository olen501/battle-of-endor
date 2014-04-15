from star_wars_actor import StarWarsActor
class GridSpace():
	def __init__(self, x, x1, y, y1, z,z1,id):
		self.x = x
		self.x1 = x1
		self.y = y
		self.y1 = y1
		self.z = z
		self.z1 = z1
		self.id = None 
		self.objects = []

	def addShip(self,star_wars_actor):
			self.objects.append(star_wars_actor)


	def deleteShip(self,star_wars_actor):
		for index in range(len(objects)):
			if(self.objects[index] == star_wars_actor):
				self.objects.remove(star_wars_actor)

	def getCoordinates(self):
		coor = []
		coor.append(self.x,self.x1,self.y,self.y1,self.z,self.z1);
		return coor

	def getNeighbors(self):
		return self.objects