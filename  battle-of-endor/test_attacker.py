from panda3d.core import Point2,Point3,Vec3,Vec4
from direct.task.Task import Task
from panda3d.core import Camera
from panda3d.core import Spotlight

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor, VBase4, DirectionalLight, PerspectiveLens

from central_controller import CentralController
from ship import *

class test(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		self.cc = CentralController()

		self.gameTask = taskMgr.add(self.flyCircles, "circles")

		base.disableMouse()
		
		base.camera.setPos(1000, 500, 1000)
		base.camera.lookAt(200, 200, 0)

		slight = Spotlight('slight')
		slight.setColor(VBase4(1, 1, 1, 1))
		lens = PerspectiveLens()
		slight.setLens(lens)

		self.rebels = []
		self.imperials = []

		# add rebel ships
		self.rebels += [Xwing('xwing' + str(x)) for x in xrange(1)]
		#self.rebels += [Ywing('ywing' + str(x)) for x in xrange(1)]
		#self.rebels += [Awing('awing' + str(x)) for x in xrange(1)]
		#self.rebels += [Bwing('bwing' + str(x)) for x in xrange(1)]

		# add imperial ships
		self.imperials += [TieFighter('tiefighter' + str(x)) for x in xrange(1)]
		#self.imperials += [TieInterceptor('tieinterceptor' + str(x)) for x in xrange(2)]

		# add rebel ships
		self.rebels += [Xwing('xwing' + str(x) + 'second') for x in xrange(1)]
		#self.rebels += [Ywing('ywing' + str(x) + 'second') for x in xrange(1)]
		#self.rebels += [Awing('awing' + str(x) + 'second') for x in xrange(1)]
		#self.rebels += [Bwing('bwing' + str(x) + 'second') for x in xrange(1)]

		# add more imperial ships
		#self.imperials += [TieFighter('tiefighter' + str(x) + 'second') for x in xrange(2)]
		#self.imperials += [TieInterceptor('tieinterceptor' + str(x) + 'second') for x in xrange(2)]
		
		# create ship list
		self.shipList = self.rebels + self.imperials

		#self.shipList = [
		#	Xwing("xwing1"), TieFighter("tie1"), Bwing("xwing2")]

		lightColors = [
			Vec4(0.9, 0.9, 0.9, 1),
			Vec4(0.9, 0.9, 0.9, 1),]

		for i, ship in enumerate(self.shipList):
			ship.reparentTo(render)
			ship.setScale(2)
			ship.setPos(Point3(i*50+50,i*100+100,i*50+50))

			directionalLight = DirectionalLight('directionalLight')
			directionalLightNP = render.attachNewNode(directionalLight)

			directionalLightNP.setHpr(180, -20, 0)
			ship.setLight(directionalLightNP)
			#ship.navSystem.setPursue()

			self.cc.addObject(ship)

		self.count = 0

		self.iter = 0

		camera.lookAt(self.shipList[1].getPos())

	def flyCircles(self, task):

		dt = globalClock.getDt()

		# base.camera.lookAt(Point3(self.shipList[1].getPos()))


		return Task.cont

t = test()
t.run()
