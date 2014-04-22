from panda3d.core import Point2,Point3,Vec3,Vec4
from direct.task.Task import Task
from panda3d.core import Camera
from panda3d.core import AmbientLight, PointLight

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor, VBase4, DirectionalLight, PerspectiveLens

from central_controller import CentralController
from ship import *
from weapon import *
from space import space
from filter import LpfVec3

class test(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		base.disableMouse()
		
		# base.camera.setPos(0, 0, 0)
		

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


		xwing = Xwing("xwing1")
		tie = TieFighter("tie1")
		awing = Awing('awing1')

		self.shipList = [xwing, tie, awing]
		
		# xwing.weaponSystem.fireWeapon()

		for i, ship in enumerate(self.shipList):
			ship.reparentTo(render)
			ship.setScale(2)
			ship.setPos(Point3(i*0,i*400,i*0))
			# ship.setLight(dlNP)
			ship.setLight(alNP)

		base.camera.setPos(tie.getPos()+Vec3(20,400,0))
		base.camera.lookAt(xwing.getPos())
		taskMgr.add(self.clearSpaceFlag, 'clearFlags')

		self.camFilter = LpfVec3(Vec3(0,0,0),10)

	def clearSpaceFlag(self, task):
		space.clearFlag()
		# space.printSpace() # WARNING THIS WILL CAUSE THINGS TO LOCK UP
		base.camera.lookAt(Point3(self.camFilter.filter(self.shipList[0])))
		return Task.cont


t = test()
t.run()
