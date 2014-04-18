from panda3d.core import Point2,Point3,Vec3,Vec4
from direct.task.Task import Task
from panda3d.core import Camera
from panda3d.core import AmbientLight, PointLight

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor, VBase4, DirectionalLight, PerspectiveLens

from central_controller import CentralController
from ship import *

class test(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		self.gameTask = taskMgr.add(self.flyCircles, "circles")


		base.disableMouse()
		
		base.camera.setPos(50, 100, 800)
		base.camera.lookAt(0, 0, 0)

		dl = DirectionalLight('dLight')
		dl.setColor(Vec4(0.1,0.1,0.1,1))
		dlNP = render.attachNewNode(dl)
		dlNP.setPos(1000,1000,0)

		al = AmbientLight('alight')
		al.setColor(Vec4(0.3, 0.3, 0.3, 1))
		alNP = render.attachNewNode(al)

		pl = PointLight('plight')
		pl.setColor(VBase4(0.2,0.2,0.2,1))
		plNP = render.attachNewNode(pl)
		plNP.setPos(100,100,100)
		render.setLight(plNP)



		self.shipList = [
			Bwing("xwing1"), 
			TieInterceptor("tie1")
			]

		
		for i, ship in enumerate(self.shipList):
			ship.reparentTo(render)
			ship.setScale(2)
			ship.setPos(Point3(i*10,i*0,i*0))
			# ship.setLight(dlNP)
			ship.setLight(alNP)

		self.count = 0

		self.iter = 0
	

	def flyCircles(self, task):

		dt = globalClock.getDt()
		# self.shipList[1].navSystem.flyInCircle()
		self.shipList[0].navSystem.pursue(self.shipList[1])
		self.shipList[1].navSystem.pursue(self.shipList[0])

		stf = 0
		if False:
			camera.setPos(self.shipList[stf].getPos() - self.shipList[stf].getVelocity()*100)
			camera.setHpr(self.shipList[stf].navSystem.getHpr())
			camera.lookAt(self.shipList[stf].getPos())

		return Task.cont

t = test()
t.run()
