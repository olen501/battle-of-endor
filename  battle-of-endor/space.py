from grid import  GridSpace
from star_wars_actor import StarWarsActor

#Space class representing grid layout of space
class Space(Object):
	#creates an heap structure to access grid cells
	def __init__(self, c_size, c_dim, ship_list):
		self.s_size = s_size
		self.s_dim = s_dim
		num_grids = s_dim * s_dim* s_dim
		self.Space = [num_grids]
		x = 0
		x1 = grid_size
		y = 0
		y1 = grid_size
		z = 0
		z1 = grid_size
		grid_id = 0
		for index in range(0,num_grids):
			grid.__init__(x,x1,y,y1,z,z1,grid_id)
			x1 = x1+c_size
			x = x + c_size
			if(x == c_dim):
				x = 0
				x1 = c_size
				y = y+c_size
				y1 = y+c_size
			if( y == c_size):
				x = 0
				x1 = c_size
				y = 0
				y1 = y + c_size
				z = z +c_size
				z1 = z + c_size
			grid_id= grid_id+1	
			self.Space[index] = grid
		for grid in Space.list:
			g_coor = grid.getCoordinates()
			for ship in self.ship_list:
				pos = ship.getPos()
				if(((pos.getX() >= g_coor[0]) and (pos.getX() <= g_coor[1]))
				and((pos.getY() >= g_coor[2]) and (pos.getY() <= g_coor[3]))
				and((pos.getZ() >= g_coor[4]) and (pos.getZ() <= g_coor[5]))):
						grid.addShip()
						ship.gridLocation(g_coor)

	#still need to complete this method
	def getNeighbors(self,ship):
		neighbors = []
		#grid = ship.getGridID()
		right = grid+1
		left = grid-1
		fmright = grid+self.c_dim+1
		fmmiddle = grid+ self.c_dim
		fmleft = grid+self.c_dim-1
		ftright = grid+(self.c_dim*2)+1
		ftleft = grid+(self.c_dim*2)-1
		ftmiddle = grid+self.c_dim*2
		bmright = grid+(self.c_dim*self.c_dim)+1
		bmleft = grid+(self.c_dim*self.c_dim)-1
		bmmiddle= grid+(self.c_dim*self.c_dim)
		

		neighbors.append(self.Space[grid].getShips())
		neighbors.append(self.Space[right].getShips())
		neighbors.append(self.Space[fmright].getShips())
		neighbors.append(self.Space[fmleft].getShips())
		neighbors.append(self.Space[ftright].getShips())
		neighbors.append(self.Space[ftright].getShips())
		neighbors.append(self.Space[ftleft].getShips())
		neighbors.append(self.Space[ftmiddle].getShips())
		neighbors.append(self.Space[bmright].getShips())
		neighbors.append(self.Space[bmleft].getShips())
		neighbors.append(self.Space[bmmiddle].getShips())
		return neighbors


