import os
import sys
import pygame as pg 
from pygame.locals import *

class Camera:

	def __init__(self, pos):
		self.pos = pos

	def update(self, event_queue):
		
		for ev in event_queue:
			if ev.type == pg.KEYDOWN:
				if ev.key == pg.K_UP:
					x_off, y_off = self.pos
					y_off -= 1
					self.pos = (x_off, y_off)
				elif ev.key == pg.K_DOWN:
					x_off, y_off = self.pos
					y_off += 1
					self.pos = (x_off, y_off)
				elif ev.key == pg.K_LEFT:
					x_off, y_off = self.pos
					x_off -= 1
					self.pos = (x_off, y_off)
				elif ev.key == pg.K_RIGHT:
					x_off, y_off = self.pos
					x_off += 1
					self.pos = (x_off, y_off)

	def set_pos(self, pos):
		self.pos = pos

	def get_pos(self):
		return self.pos

			 