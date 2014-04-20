from grid import  GridSpace
from panda3d.core import Point2,Point3,Vec3,Vec4
import math

#Space class representing central controller of space
class Space():
	#creates an heap structure to access grid cells
	def __init__(self, c_size, c_dim):
		self.c_size = c_size
		self.c_dim = c_dim
		self.Space = []
		self.numObjects = 0

		self.cellsWithChanges = []

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
			self.cellsWithChanges.append(oldLoc)
		else:
			self.numObjects += 1

		self.Space[nx][ny][nz].addActor(stwa)
		self.cellsWithChanges.append(newLoc)

	def remove(self, stwa, loc):
		x = int(loc.getX())
   		y = int(loc.getY())
   		z = int(loc.getZ())

   		self.Space[x][y][z].removeActor(stwa)
   		self.cellsWithChanges.append(loc)

   		self.numObjects -= 1


	def getNeighbors(self,gridLoc):

		x = int(gridLoc.getX())
		y = int(gridLoc.getY())
		z = int(gridLoc.getZ())

		neighbors = []

		for i in range(x - 1, x + 2):
			if(i >= 0 and i < self.c_dim):
				for j in range(y - 1, y + 2):
					if(j >= 0 and j < self.c_dim):
						for k in range(z - 1, z + 2):
							if(k >= 0 and k < self.c_dim):
								neighbors += self.Space[i][j][k].getShips()

		return neighbors


	def hasNewNeighbors(self, gridLoc):

		x = int(gridLoc.getX())
		y = int(gridLoc.getY())
		z = int(gridLoc.getZ())
		res = False
		for i in range(x - 1, x + 2):
			if(i >= 0 and i < self.c_dim):
				for j in range(y - 1, y + 2):
					if(j >= 0 and j < self.c_dim):
						for k in range(z - 1, z + 2):
							if(k >= 0 and k < self.c_dim):
								if(self.Space[i][j][k].getFlag() == True):
									return True	
		return False

	def printSpace(self):
		for i in range(0, self.c_dim):
			for j in range(0, self.c_dim):
				for k in range(0, self.c_dim):
					print i,j,k, len(self.Space[i][j][k].actors)

	# XXX Need a better way to clear flags. Probably store an index
	def clearFlag(self):
		for cell in self.cellsWithChanges:
			x = int(cell.getX())
			y = int(cell.getY())
			z = int(cell.getZ())
			self.Space[x][y][z].clearFlag()

	def getC_dim(self):
		return self.c_dim

	def getNumObjects(self):
		return self.numObjects

space = Space(500, 20)

