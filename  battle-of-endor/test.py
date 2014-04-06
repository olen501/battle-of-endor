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


from ship import Ship

class test(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")

		self.ship = Ship("models//ship",0.3, "ship1")
		self.ship.reparentTo(render)
		self.ship.setPos(Point3(0,0,0))
		self.ship.setScale(2)

		self.i = 0

		base.disableMouse()
		
		base.camera.setPos(0, -80, 30)
		base.camera.lookAt(10,10,10)

		slight = Spotlight('slight')
		slight.setColor(VBase4(1, 1, 1, 1))
		lens = PerspectiveLens()
		slight.setLens(lens)

		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(Vec4(0.8, 0.2, 0.2, 1))
		self.directionalLightNP = render.attachNewNode(directionalLight)

		# This light is facing backwards, towards the camera.
		self.directionalLightNP.setHpr(180, -20, 0)
		render.setLight(self.directionalLightNP)
		self.count = 0


	def gameLoop(self, task):

		if self.count < 100:
			self.ship.goTo(Vec3(10,10,10))
		elif self.count < 200:
			self.ship.goTo(Vec3(20,20,00))
		elif self.count < 300:
			self.ship.goTo(Vec3(00,00,30))
		elif self.count < 400:
			self.ship.goTo(Vec3(0,0,0))
		
		if(self.count >= 400):
			self.count = 0
		self.count = self.count + 1

		print self.count

		self.directionalLightNP.setPos(self.ship.getPos() + Vec3(0,10,10))
		self.directionalLightNP.lookAt(self.ship.getPos())
		return Task.cont


t= test()
t.run()