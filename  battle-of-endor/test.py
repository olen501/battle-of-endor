from panda3d.core import TextNode
from panda3d.core import Point2,Point3,Vec3,Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from math import sin, cos, pi
from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait,Func
from math import *
from math import pi, sin, cos
from panda3d.core import Camera
from panda3d.core import Spotlight

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor, VBase4, DirectionalLight, PerspectiveLens


import cPickle, sys


from ship import *

class test(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")

		base.disableMouse()
		
		base.camera.setPos(0, -100, 70)
		base.camera.lookAt(20,0,0)

		slight = Spotlight('slight')
		slight.setColor(VBase4(1, 1, 1, 1))
		lens = PerspectiveLens()
		slight.setLens(lens)

		self.shipList = [
			Xwing("models/ship",0.3, "xwing1"),
			Ywing("models/ship", 0.3, "ywing1"),
			Awing("models/ship", 0.3, "awing1"),
			Bwing("models/ship", 0.3, "bwing1"),
			TieFighter("models/ship", 0.3, "tiefighter1"),
			TieInterceptor("models/ship", 0.3, "tieinterceptor1")]

		lightColors = [
			Vec4(0.9, 0.9, 0.9, 1),
			Vec4(1, 1, 0, 1),
			Vec4(1, 0, 0, 1),
			Vec4(0, 0, 1, 1),
			Vec4(0.4, 0.4, 0.4, 1),
			Vec4(0.1, 0.1, 0.1, 1)]

		for i, ship in enumerate(self.shipList):
			ship.reparentTo(render)
			ship.setScale(2)
			ship.setPos(Point3(i*10, 0, 0))

			directionalLight = DirectionalLight('directionalLight')
			directionalLight.setColor(lightColors[i])
			directionalLightNP = render.attachNewNode(directionalLight)

			directionalLightNP.setHpr(180, -20, 0)
			ship.setLight(directionalLightNP)

		self.count = 0


	def gameLoop(self, task):

		for i, ship in enumerate(self.shipList):
			if self.count < 100:
				ship.goTo(Vec3(i*10,10,10))
			elif self.count < 200:
				ship.goTo(Vec3(i*20,20,00))
			elif self.count < 300:
				ship.goTo(Vec3(00,00,i*30))
			elif self.count < 400:
				ship.goTo(Vec3(i*10,0,0))
		
		if(self.count >= 400):
			self.count = 0
		self.count = self.count + 1

		#print self.count

		#self.directionalLightNP.setPos(self.ship.getPos() + Vec3(0,10,10))
		#self.directionalLightNP.lookAt(self.ship.getPos())
		return Task.cont


t= test()
t.run()