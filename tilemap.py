import os
import sys
import pygame as pg 
from pygame.locals import *

class Event:

	def __init__(self):
		self.listeners = []

	def connect(listener):
		listeners.append(listener)

	def disconnect(listener):
		listeners.remove(listener)

	def fire(params):
		for listener in listeners:
			listener(params)


TT_EMPTY = 0

class Tile:

	def __init__(self, pos, layer, img_id, is_destructible, is_obstacle, tile_type, hp):
		self.pos = pos
		self.layer = layer
		self.img_id = img_id

		self.is_destructible = is_destructible
		self.tile_type = tile_type
		self.hp = 100
		self.is_obstacle = is_obstacle

		# Events
		# sig_destryoed params: self
		self.sig_destroyed = Event()

	@classmethod 
	def empty(cls, pos):
		return cls(pos, 0, 24, False, False, TT_EMPTY, 100)

	def remove_health(value):
		hp -= value

		if hp < 1:
			sig_destroyed.fire(self)




class Tilemap:

	def __init__(self, num_tiles_x, num_tiles_y, tilesize, img):
		self.num_tiles_x = num_tiles_x
		self.num_tiles_y = num_tiles_y
		self.tilesize = tilesize
		self.img = img

		''' 
		' Creates a 3D list of tiles 
		' Rows and cols are for the individual fields
		' while the depth is for stacking tile layers
		' Everytime the arangement is changed, the tiles will be sorted by depth accordingly
		' On initialization the list is empty
		'''	
		self.map = [[[Tile.empty((x, y))] for x in range(num_tiles_x)] for y in range(num_tiles_y)]


	def add_tile(self, pos, tile):
		"""
		Adds a tile to the designated map block and 
		sorts the tiles in the block in descending according to layer 
		returns nothing
		"""
		x, y = pos
		block = self.map[y][x]
		block.append(tile)
		block.sort(key = lambda t: t.layer, reverse=True) #operator.attrgetter('layer')
		
	def remove_tile(self, **kwargs):
		"""
		Removes a tile from the map
		kwargs: tile -> removes tile from map
		kwargs: pos, type -> removes the designated tile_type at position 
		"""
		if "tile" in kwargs:
			self.map.remove(kwargs["tile"])
			return

		if "pos" in kwargs and "type" in kwargs:
			remove_list = []
			for tile in self.map[y][x]:
				if tile.tile_type == kwargs["type"]:
					remove_list.append(tile)

			for tile in remove_list:
				self.map[y][x].remove(tile)


	

	def render_block(self, pos, surf):
		'''
		Renders all tiles in a block giving by (x, y) onto the designated surface
		'''
		x, y = pos
		for tile in self.map[y][x]:
			img_x, img_y = self.tile_id_to_img_coords(tile.img_id)
			map_pos = (x * self.tilesize, y * self.tilesize)
			img_pos = tuple([self.tilesize * n for n in (img_x, img_y, 1, 1)])
			surf.blit(self.img, map_pos, img_pos)

	def render_map(self, surf):
		'''
		Renders all the tiles onto the given surface
		'''
		for y in range(self.num_tiles_y):
			for x in range(self.num_tiles_x):
				self.render_block((x, y), surf)


	def tile_id_to_img_coords(self, img_id):
		'''
		Returns the (x, y) coordinates on the tilemap image for a given img_id
		'''
		tiles_x = self.img.get_rect().size[0]
		tiles_x /= self.tilesize

		return (int(img_id % tiles_x), int(img_id / tiles_x))



pg.init()
TILESIZE = 16
NUM_TILES_X = 100
NUM_TILES_Y = 100
tilemap_img = pg.image.load("tiles.png")
disp = pg.display.set_mode((NUM_TILES_X * TILESIZE, NUM_TILES_X * TILESIZE))


tmap = Tilemap(NUM_TILES_X, NUM_TILES_Y, TILESIZE, tilemap_img)

while True:

	for ev in pg.event.get():
		if ev.type == QUIT:
			pg.quit()
			sys.exit()

	tmap.render_map(disp)

	pg.display.update()







