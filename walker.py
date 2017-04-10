import os
import sys
import pygame as pg 
from camera import Camera
from player import Player
import math
import astar

from multiprocessing.pool import ThreadPool

from pygame.locals import *

class Walker:
	"""
	This class creates a 1x1 sized unit that will go as you please
	"""


	def __init__(self, pos, tmap, speed):
		"""
		Initializer for walker
		"""
		self.tmap = tmap
		self.pos = pos
		self.img = self.img = pg.image.load("player.png")

		self.has_path = False
		self.path = []
		self.counter_time = 0
		self.counter_path = 0
		self.speed = speed
		self.calculating = False

		self.pool = ThreadPool(processes=1)
		self.async_path = 0

	def render(self, surf):
		x, y = self.pos
		surf.blit(self.img, (x * self.tmap.tilesize, y * self.tmap.tilesize))

	def update(self, dt):

		if self.calculating:
			if self.async_path.get():
				path = self.async_path.get()
				self.calculating = False
				self.set_path(path)



		# Only do following if a path was assigned
		if not self.has_path:
			return

		# Reached the end of the path?
		if len(self.path) == self.counter_path + 1:
			self.has_path = False
			self.counter_path = 0
			return

		# Integral dt = t
		self.counter_time += dt
		threshold = self.counter_time


		x1, y1 = self.path[len(self.path) - self.counter_path - 1] 
		x2, y2 = self.path[len(self.path) - self.counter_path - 2]

		# Walk with set speed
		if self.counter_time >= 1000/self.speed * (math.sqrt(2) if (x2 - x1 != 0 and y2 - y1 != 0) else 1):
			self.counter_path += 1
			self.counter_time = 0
			self.pos = self.path[len(self.path) - self.counter_path - 1]

	def move_to(self, goal, diagonal=False):
		x, y = goal
		#path = astar.find_path(self.tmap, self.pos, goal, astar.heuristics.steven_van_dijk, diagonal)
		self.async_path = self.pool.apply_async(astar.find_path, (self.tmap, self.pos, goal, astar.heuristics.steven_van_dijk, diagonal))
		print("ASYNC")
		self.calculating = True
		


	def set_path(self, path):
		# Only do following if a path was assigned
		if self.has_path:
			return

		# Path having zero length means we are already there
		if len(path) == 0:
			return

		# Initiate path following
		self.has_path = True
		self.path = path
		self.pos = path[-1]

