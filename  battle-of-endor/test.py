from panda3d.core import TextNode
from panda3d.core import Point2,Point3,Vec3,Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from math import sin, cos, pi
from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait,Func
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
		#setting background

		self.environ = self.loader.loadModel("models/world")

		#Reparent the model to render
		#self.environ.reparentTo(self.render)
		#Apply scale and position transforms on the model

		self.environ.setScale(1000, 1000, 1000)
		self.environ.setPos(0, 0, 0)

		
		self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")

		base.disableMouse()
		
		base.camera.setPos(0, -300, 100)
		base.camera.lookAt(0,0,0)

		slight = Spotlight('slight')
		slight.setColor(VBase4(1, 1, 1, 1))
		lens = PerspectiveLens()
		slight.setLens(lens)

		self.shipList = [
			Xwing("xwing1"),
			# Ywing("ywing1"),
			# Awing("awing1")#,
			# Bwing("bwing1"),
			# TieFighter("tiefighter1"),
			# TieInterceptor("tieinterceptor1")
		]

		lightColors = [
			Vec4(0.9, 0.9, 0.9, 1),
			Vec4(1, 1, 0, 1),
			Vec4(1, 0, 0, 1),
			Vec4(0, 0, 1, 1),
			Vec4(0.4, 0.4, 0.4, 1),
			Vec4(0.1, 0.1, 0.1, 1)]

		for i, ship in enumerate(self.shipList):
			ship.reparentTo(render)
			ship.setPos(Point3(i*10, 0, 0))

			directionalLight = DirectionalLight('directionalLight')
			directionalLight.setColor(lightColors[i])
			directionalLightNP = render.attachNewNode(directionalLight)

			directionalLightNP.setHpr(180, -20, 0)
			ship.setLight(directionalLightNP)

		self.count = 0

		self.fire = False


	def gameLoop(self, task):

		for i, ship in enumerate(self.shipList):
			j = i if i % 2 == 0 else -i

			if self.count < 100:
				#ship.weaponSystem.fireWeapon()
			 	#ship.goTo(Vec3(j*10,10,10))
				if not self.fire:
					ship.weaponSystem.fireWeapon()
					self.fire = True
			elif self.count == 100:
				self.fire = False
			elif self.count < 200:
				#ship.goTo(Vec3(j*20,20,00))
				if not self.fire:
					ship.weaponSystem.fireWeapon()
					self.fire = True
			elif self.count == 200:
				self.fire = False
			elif self.count < 300:
				#ship.goTo(Vec3(00,00,j*30))
				if not self.fire:
					ship.weaponSystem.fireWeapon()
					self.fire = True
			elif self.count == 300:
				self.fire = False
			elif self.count < 400:
				#ship.goTo(Vec3(i*10,0,0))
				if not self.fire:
					ship.weaponSystem.fireWeapon()
					self.fire = True
			elif self.count == 400:
				self.fire = False
		
		if(self.count >= 400):
			self.count = 0
		self.count = self.count + 1

		#print self.count

		#self.directionalLightNP.setPos(self.ship.getPos() + Vec3(0,10,10))
		#self.directionalLightNP.lookAt(self.ship.getPos())
		return Task.cont


t= test()
t.run()