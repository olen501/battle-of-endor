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

class Environment(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")

		base.disableMouse()
		
		base.camera.setPos(0, -300, 100)
		base.camera.lookAt(0,0,0)

		slight = Spotlight('slight')
		slight.setColor(VBase4(1, 1, 1, 1))
		lens = PerspectiveLens()
		slight.setLens(lens)

		# create rebel ships
		self.rebels = [Xwing('xwing' + str(x)) for x in xrange(100)]
		self.rebels += [Ywing('ywing' + str(x)) for x in xrange(100)]
		self.rebels += [Awing('awing' + str(x)) for x in xrange(100)]
		self.rebels += [Bwing('bwing' + str(x)) for x in xrange(100)]

		# create imperial ships
		self.imperials = [TieFighter('tiefighter' + str(x)) for x in xrange(400)]
		self.imperials += [TieInterceptor('tieinterceptor' + str(x)) for x in xrange(400)]
