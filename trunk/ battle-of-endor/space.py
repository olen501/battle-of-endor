from grid import  GridSpace
from panda3d.core import Point2,Point3,Vec3,Vec4
import math

#store a reference to all star wars actors
#ships need to check if neighbors changed
	#flag if grids around you have changed

#when star wars actor crosses grid update ships
	#swactor tells space its new grid
	#space moves ship to new grid
	#set flag saying these 2 grids change
		#flag (someone was here or they left)
		#flag boolean
	

#Space class representing central controller of space
class Space():
	#creates an heap structure to access grid cells
	def __init__(self, c_size, c_dim):
		self.c_size = c_size
		self.c_dim = c_dim
		self.Space = []

		for k in range(0, c_dim):
			newLevel = []
			for i in range(0,c_dim):
				newCol = []
				for j in range(0, c_dim):
					grid = GridSpace()
					newCol.append(grid)
				newLevel.append(newCol)
			self.Space.append(newLevel)
		
   	def update(self,stwa,oldLoc,newLoc):		

   		

   		nx = int(newLoc.getX())
   		ny = int(newLoc.getY())
   		nz = int(newLoc.getZ())

   		if(oldLoc is not None):
   			ox = int(oldLoc.getX())
   			oy = int(oldLoc.getY())
   			oz = int(oldLoc.getZ())
			self.Space[ox][oy][oz].removeActor(stwa)

		self.Space[nx][ny][nz].addActor(stwa)	

	def getNeighbors(self,gridLoc):

		x = int(gridLoc.getX())
		y = int(gridLoc.getY())
		z = int(gridLoc.getZ())

		neighbors = []

		for i in range(x - 1, x + 1):
			if(i >= 0 and i < self.c_dim):
				for j in range(y - 1, y + 1):
					if(j >= 0 and j < self.c_dim):
						for k in range(z - 1, z + 1):
							if(k >= 0 and k < self.c_dim):
								neighbors += self.Space[i][j][k].getShips()

		return neighbors


	def hasNewNeighbors(self, gridLoc):
		x = int(gridLoc.getX())
		y = int(gridLoc.getY())
		z = int(gridLoc.getZ())

		res = False

		for i in range(x - 1, x + 1):
			if(i >= 0 and i < self.c_dim):
				for j in range(y - 1, y + 1):
					if(j >= 0 and j < self.c_dim):
						for k in range(z - 1, z + 1):
							if(k >= 0 and k < self.c_dim):
								if(self.Space[i][j][k].getFlag() == True):
									return True	

space = Space(100, 50)

