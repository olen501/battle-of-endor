
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

