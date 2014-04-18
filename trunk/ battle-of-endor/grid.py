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
		self.flag = None
		self.objects = []

	def addStar_Wars_Actor(self,star_wars_actor):
		self.objects.append(star_wars_actor)


	def delete_Star_Wars_Actor(self,star_wars_actor):
		for index in range(len(objects)):
			if(self.objects[index] == star_wars_actor):
				self.objects.remove(star_wars_actor)

	def getCoordinates(self):
		coor = []
		coor.append(self.x,self.x1,self.y,self.y1,self.z,self.z1);
		return coor

	def getShips(self):
		neighbors=[]
		for star_wars_actor in objects:
			if(star_wars_actor.type == 'ship'):
				neighbors.append(star_wars_actor)
		return neighbors