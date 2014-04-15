from grid import  GridSpace
from star_wars_actor import StarWarsActor

#Space class representing grid layout of space
class Space():
	#creates an heap structure to access grid cells
	def __init__(self, c_size, c_dim, ship_list):
		self.c_size = c_size
		self.c_dim = c_dim
		num_grids = c_dim * c_dim* c_dim
		self.Space = [num_grids]
		self.ship_list = ship_list
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

		#determines what grid the ship is located in
		for ship in self.ship_list:
			pos = ship.getPos()
			grid_id = (((pos.getX()%self.c_dim)*(pos.getX()/self.c_dim))+ ((pos.getY()%self.c_dim)*(pos.getY()/self.c_dim))+((pos.getZ()%self.c_dim)*(pos.getZ()/self.c_dim)))*self.c_dim
			self.Space[grid_id].addShip(ship)
	
	def setNeighbors(self,ship):
		neighbors = []
		grid_id = (((pos.getX()%self.c_dim)*(pos.getX()/self.c_dim))+ ((pos.getY()%self.c_dim)*(pos.getY()/self.c_dim))+((pos.getZ()%self.c_dim)*(pos.getZ()/self.c_dim)))*self.c_dim
		right = grid_id+1
		left = grid_id-1
		tmiddle = grid_id+ self.c_dim
		tleft = tmiddle -1
		tright = tmiddle + 1
		bmiddle = grid_id - self.c_dim
		bright = bmiddle+1
		bleft = bmmiddle - 1
		bgrid_id = grid_id + c_dim*c_dim
		bgrid_id_right = bgrid_id +1
		bgrid_id_left = bgrid_id-1
		bgrid_id_bmid = bgrid_id-c_dim
		bgrid_id_bright = bgrid_id_bmid + 1
		bgrid_id_bleft = bgrid_id_bmid - 1
		bgrid_id_tmid = bgrid_id+c_dim
		bgrid_id_tright = bgrid_id_tmid + 1
		bgrid_id_tleft = bgrid_id_tmid - 1
		fgrid_id = grid_id - c_dim*c_dim
		fgrid_id_right = fgrid_id +1
		fgrid_id_left = fgrid_id-1
		fgrid_id_bmid = fgrid_id-c_dim
		fgrid_id_bright = fgrid_id_bmid + 1
		fgrid_id_bleft = fgrid_id_bmid - 1
		fgrid_id_tmid = fgrid_id+c_dim
		fgrid_id_tright = fgrid_id_tmid + 1
		fgrid_id_tleft = fgrid_id_tmid - 1
		neighbors.append(self.Space[grid_id].objects)
		neighbors.append(self.Space[right].objects)
		neighbors.append(self.Space[left].objects)
		neighbors.append(self.Space[tmiddle].objects)		
		neighbors.append(self.Space[bmmiddle].objects)
		neighbors.append(self.Space[bright].objects)
		neighbors.append(self.Space[bleft].objects)
		neighbors.append(self.Space[bgrid_id].objects)
		neighbors.append(self.Space[bgrid_id_right].objects)
		neighbors.append(self.Space[bgrid_id_left].objects)
		neighbors.append(self.Space[bgrid_id_bmid].objects)
		neighbors.append(self.Space[bgrid_id_bright].objects)
		neighbors.append(self.Space[bgrid_id_bleft].objects)
		neighbors.append(self.Space[bgrid_id_tmid].objects)
		neighbors.append(self.Space[bgrid_id_tright].objects)
		neighbors.append(self.Space[bgrid_id_tleft].objects)
		neighbors.append(self.Space[fgrid_id].objects)
		neighbors.append(self.Space[fgrid_id_right].objects)
		neighbors.append(self.Space[fgrid_id_left].objects)
		neighbors.append(self.Space[fgrid_id_bmid].objects)
		neighbors.append(self.Space[fgrid_id_bright].objects)
		neighbors.append(self.Space[fgrid_id_bleft].objects)
		neighbors.append(self.Space[fgrid_id_tmid].objects)
		neighbors.append(self.Space[fgrid_id_tright].objects)
		neighbors.append(self.Space[fgrid_id_tleft].objects)
		ship.nearBySwActors = neighbors



