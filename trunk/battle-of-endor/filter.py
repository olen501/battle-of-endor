from panda3d.core import Point3, Vec3

class Lpf():
	#-------------------------------------------------------------------------#
	def __init__(self, val, length):
	#-------------------------------------------------------------------------#
		self.val = val
		self.cnt = 0
		self.len = length

		self.vals = []

		self.lastEntry = 0

	#-------------------------------------------------------------------------#
	def filter(self, val):
	#-------------------------------------------------------------------------#
		
		# If the filter has all entries filled, subtract the oldest entry
		if(self.cnt == self.len):
			self.val -= self.vals[self.lastEntry]
			self.vals[self.lastEntry] = val
		else:
			# If the filter does not have all entries filled, increment the
			# number filled since we are adding one
			self.vals.append(val)
			self.cnt = self.cnt + 1

		self.val += self.vals[self.lastEntry]
		self.lastEntry = (self.lastEntry + 1)%self.len

		return self.val/self.cnt

	#-------------------------------------------------------------------------#
	def getVals(self):
	#-------------------------------------------------------------------------#
		return ', '.join([str(x) for x in self.vals])


class LpfVec3():
	def __init__(self, val, length):
		self.lpfx = Lpf(val.getX(), length)
		self.lpfy = Lpf(val.getY(), length)
		self.lpfz = Lpf(val.getZ(), length)

	def filter(self, val):
		return Vec3(self.lpfx.filter(val.getX()),
					self.lpfy.filter(val.getY()),
					self.lpfz.filter(val.getZ()))



class Hysteresis():
	def __init__(self, lb, hb):
		self.lb = lb
		self.hb = hb

		self.STATE_ABOVE_HB = 0
		self.STATE_BELOW_HB_ABOVE_LB = 1
		self.STATE_BELOW_LB = 2

		self.state = self.STATE_ABOVE_HB

		self.minVal = float("inf")

	def filter(self, val):
		
		nextState = self.state
		rVal = val

		if(self.state == self.STATE_ABOVE_HB):
			if(val < self.lb):
				nextState = self.STATE_BELOW_LB
				rVal = val
			elif(val < self.hb):
				nextState = self.STATE_BELOW_HB_ABOVE_LB
				rVal = val

		elif(self.state == self.STATE_BELOW_HB_ABOVE_LB):
			if(val < self.lb):
				nextState = self.STATE_BELOW_LB
				if(val < self.minVal):
					self.minVal = val
				rVal = self.minVal

		elif(self.state == self.STATE_BELOW_LB):
			if(val > self.hb):
				nextState = self.STATE_ABOVE_HB
				rVal = val
			elif(val < self.lb):
				if(val < self.minVal):
					self.minVal = val
				rVal = self.minVal
			else:
				rVal = self.minVal

		self.state = nextState
		return max(rVal,0)

	def getState(self):
		return self.state



