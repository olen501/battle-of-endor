from grid import  GridSpace
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
		num_grids = c_dim * c_dim* c_dim
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
			
   
	def update(self,stwa,old_location,new_location):
		opos = old_location.getPos()
		npos = new_location.getPos()

		old_grid = (((opos.getX()%self.c_dim)*(opos.getX()/self.c_dim))+ 
			(((opos.getY()%self.c_dim)*(opos.getY()/self.c_dim))*self.c_dim)+
			(opos.getZ()/self.c_dim*(self.c_dim*self.c_dim)*((opos.getZ()%self.c_dim)*(opos.getZ()/self.c_dim))))

		new_grid = (((npos.getX()%self.c_dim)*(npos.getX()/self.c_dim))+ 
			(((npos.getY()%self.c_dim)*(npos.getY()/self.c_dim))*self.c_dim)+
			(npos.getZ()/self.c_dim*(self.c_dim*self.c_dim)*((npos.getZ()%self.c_dim)*(npos.getZ()/self.c_dim))))

		if old_grid =='None':
			self.Space[new_grid].addShip(stwa)
		else:
			for ship in self.Space[old_grid].objects:
				if( stwa == ship):
					self.Space[old_grid].delete_Star_Wars_Actor(stwa)
			self.Space[old_grid].addShip(stwa)

	def getNeighbors(self,ship):
		neighbors = []
		pos = ship.getPos()
		grid_id = (((pos.getX()%self.c_dim)*(pos.getX()/self.c_dim))+ 
			(((pos.getY()%self.c_dim)*(pos.getY()/self.c_dim))*self.c_dim)+
			(pos.getZ()/self.c_dim*(self.c_dim*self.c_dim)*((pos.getZ()%self.c_dim)*(pos.getZ()/self.c_dim))))
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
		grid_indexes = [grid_id,right,left,tmiddle,tleft,bmmiddle,bright,bleft,bgrid_id,bgrid_id_right,bgrid_id_left,
		bgrid_id_bmid,bgrid_id_bright,bgrid_id_bleft,bgrid_id_tmid,bgrid_id_tright,bgrid_id_tleft,fgrid_id,fgrid_id_right,
		fgrid_id_left,fgrid_id_bmid,fgrid_id_bright,fgrid_id_bleft,fgrid_id_tmid, fgrid_id_tright,fgrid_id_tleft]
		for index in grid_indexes:
					neighbors.append(self.Space[index].getShips())
		star_wars_actor.nearBySwActors = neighbors

	



