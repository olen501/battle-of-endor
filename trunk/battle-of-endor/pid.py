
from panda3d.core import Vec3


class PID():
	def __init__(self, kp, ki, kd):
		self.kp = kp
		self.ki = ki
		self.kd = kd

		self.errOld = 0
		self.ie = Vec3(0,0,0)

		self.maxIntErr = -1
		self.deadband = 0

	def run(self, err):

		if(err.length() < self.deadband):
			return 0

		# Proportional eror
		prop = err*self.kp

		# Integral of accumlated error
		self.ie = self.runAntiWindup(err + self.ie + err)
		integral = self.ie*self.ki

		# Derivative of error
		der = (err - self.errOld)*self.kd

		self.errOld = err;

		# Final PID calculation
		return prop+integral+der

	def antiWindup(self, maxIntErr):
		self.maxIntErr = maxIntErr

	def runAntiWindup(self, integral):
		# Antiwind up  to prevent integral portion from becoming enormous
		if(self.maxIntErr > 0):
			if(integral.getX() > self.maxIntErr):
				integral.setX(self.maxIntErr)
			if(integral.getX() < -self.maxIntErr):
				integral.setX(-self.maxIntErr)

			if(integral.getY() > self.maxIntErr):
				integral.setY(self.maxIntErr)
			if(integral.getY() < -self.maxIntErr):
				integral.setY(-self.maxIntErr)

			if(integral.getZ() > self.maxIntErr):
				integral.setZ(self.maxIntErr)
			if(integral.getZ() < -self.maxIntErr):
				integral.setZ(-self.maxIntErr)

		return integral

	def setDeadband(self, deadband):
		self.deadband = deadband
