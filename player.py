import os
import sys
import pygame as pg 
from pygame.locals import *


class Player:

	def __init__(self, tilemap, can_move):
		self.tmap = tilemap
		self.pos = pos
		self.can_move = can_move

		self.img = pg.image.load("player.png")


	def update(self, dt):
		ev = pg.event.get()
		x, y = self.pos
		if ev.type == pg.KEYDOWN:
			if ev.key == pg.K_UP:
				#y -= 1
				tmap.move_view_up()
			elif ev.key == pg.K_DOWN:
				#y += 1
				tmap.move_view_down()
			elif ev.key == pg.K_LEFT:
				#x -= 1
				tmap.move_view_left()
			elif ev.key == pg.K_RIGHT:
				#x += 1
				tmap.move_view_right()
			self.pos = (x, y)


	def render(self, surf):
		surf.blit(self.img, self.pos)