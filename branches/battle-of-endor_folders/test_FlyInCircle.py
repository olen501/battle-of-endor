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
		
		base.camera.setPos(-50, 00, 200)
		base.camera.lookAt(0,0,-10)

		slight = Spotlight('slight')
		slight.setColor(VBase4(1, 1, 1, 1))
		lens = PerspectiveLens()
		slight.setLens(lens)

		self.shipList = [
			Xwing("xwing1")]

		lightColors = [
			Vec4(0.9, 0.9, 0.9, 1)]

		for i, ship in enumerate(self.shipList):
			ship.reparentTo(render)
			ship.setScale(2)
			ship.setPos(Point3(i*10, 0, 0))

			directionalLight = DirectionalLight('directionalLight')
			directionalLight.setColor(lightColors[i])
			directionalLightNP = render.attachNewNode(directionalLight)

			directionalLightNP.setHpr(180, -20, 0)
			ship.setLight(directionalLightNP)

			self.cc.addObject(ship)

		self.count = 0

	def flyCircles(self, task):

		dt = globalClock.getDt()

		self.shipList[0].navSystem.flyInCircle()
		return Task.cont

t = test()
t.run()