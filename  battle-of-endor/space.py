from grid import * grid
from grid import * star_wars_actor

#Space class representing grid layout of space
class Space
	#creates an heap structure to access grid cells
	def __init__(self, c_size, c_dim, ship_list):
		self.s_size = s_size
		self.s_dim = s_dim
		num_grids = s_dim * s_dim* s_dim
		self.Space = [[[s_dim]s_dim]s_dim]
		x = 0
		x1 = grid_size
		y = 0
		y1 = grid_size
		z = 0
		z1 = grid_size
		grid_id = 0
		for index range(0,num_grids):
			grid.__init__(x,x1,y,y1,z,z1,grid_id)
			x1 = x1+c_size
			x = x + c_size
			if(x == c_dim):
				x = 0
				x1 = c_size
				y = y+c_size
				y1 = y+c_size
			if( y == c_size):
				z = c_size
				z1 = z + c_size
			grid_id= grid_id+1	
			self.Space.append(grid)
		for grid in Space.list:
			g_coor = grid.getCoordinates()
			for ship in self.ship_list:
				pos = ship.getPos()
				if((pos.getX() >= g_coor[0] && pos.getX() <= g_coor[1])
				&&(pos.getY() >= g_coor[2] && pos.getY() <= g_coor[3])
				&&(pos.getZ() >= g_coor[4] && pos.getZ() <= g_coor[5])):
						grid.addShip()

	#still need to complete this method
	def getNeighbors(self,ship):
		grid = ship.getGridID()
		neighbors = []
		#gets right neigbor
		neighbors.append.(grid.getShips())

		return neighbors


