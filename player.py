import os
import sys
import pygame as pg 
from pygame.locals import *


class Player:

	def __init__(self, pos, tilemap, can_move, cam):
		self.pos = pos
		self.tmap = tilemap
		self.pos = pos
		self.can_move = can_move

		self.img = pg.image.load("player.png")
		self.camera = cam


	def update(self, event_queue, dt):
		old_x, old_y = x, y = self.pos
		step = self.tmap.tilesize
		for ev in event_queue:
			if ev.type == pg.KEYDOWN:
				if ev.key == pg.K_w:
					y -= step
				elif ev.key == pg.K_s:
					y += step
				elif ev.key == pg.K_a:
					x -= step
				elif ev.key == pg.K_d:
					x += step
				self.pos = (x, y)

				for tile in self.tmap.get_tiles_in_block((int(x / step), int(y / step))):
					if tile.is_obstacle:
						self.pos = (old_x, old_y)
						break




	def render(self, surf):
		x, y = self.pos
		x_off, y_off = self.camera.get_pos()
		surf.blit(self.img, (x - x_off * self.tmap.tilesize, y - y_off * self.tmap.tilesize))