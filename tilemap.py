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
	def empty(cls, pos, img_id):
		return cls(pos, 0, img_id, False, False, TT_EMPTY, 100)

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

		self.render_offset = (0, 0)

		''' 
		' Creates a 3D list of tiles 
		' Rows and cols are for the individual fields
		' while the depth is for stacking tile layers
		' Everytime the arangement is changed, the tiles will be sorted by depth accordingly
		' On initialization the list is empty
		'''	
		self.map = [[[Tile.empty((x, y), 24)] for x in range(num_tiles_x)] for y in range(num_tiles_y)]
		self.map[30][30] = [Tile.empty((30, 30), 23)]


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
		x_off, y_off = self.render_offset

		if x < 0 or x >= self.num_tiles_x or y < 0 or y >= self.num_tiles_y:
			return

		for tile in self.map[y][x]:
			x_r, y_r = tile.pos
			img_x, img_y = self.tile_id_to_img_coords(tile.img_id)
			map_pos = ((x_r - x_off) * self.tilesize, (y_r - y_off) * self.tilesize)
			img_pos = tuple([self.tilesize * n for n in (img_x, img_y, 1, 1)])
			surf.blit(self.img, map_pos, img_pos)

	def render_map(self, surf):
		'''
		Renders all the tiles onto the given surface
		'''

		# Only render stuff that is visible on the screen
		x_off, y_off = tuple([self.tilesize * n for n in self.render_offset])
		x_start = int(x_off / self.tilesize)
		y_start = int(y_off / self.tilesize)
		w, h = pg.display.get_surface().get_size()
		x_end = x_start + int(w / self.tilesize)
		y_end = y_start + int(h / self.tilesize)

		for y in range(y_start, y_end+1, 1):
			for x in range(x_start, x_end+1, 1):
				self.render_block((x, y), surf)


	def tile_id_to_img_coords(self, img_id):
		'''
		Returns the (x, y) coordinates on the tilemap image for a given img_id
		'''
		tiles_x = self.img.get_rect().size[0]
		tiles_x /= self.tilesize

		return (int(img_id % tiles_x), int(img_id / tiles_x))


	def move_view_up(self):
		x_off, y_off = self.render_offset
		y_off -= 1
		self.render_offset = (x_off, y_off)

	def move_view_down(self):
		x_off, y_off = self.render_offset
		y_off += 1
		self.render_offset = (x_off, y_off)

	def move_view_left(self):
		x_off, y_off = self.render_offset
		x_off -= 1
		self.render_offset = (x_off, y_off)

	def move_view_right(self):
		x_off, y_off = self.render_offset
		x_off += 1
		self.render_offset = (x_off, y_off)

pg.init()
TILESIZE = 16
NUM_TILES_X = 100
NUM_TILES_Y = 100
tilemap_img = pg.image.load("tiles.png")
disp = pg.display.set_mode((800, 600))


tmap = Tilemap(NUM_TILES_X, NUM_TILES_Y, TILESIZE, tilemap_img)
clk = pg.time.Clock()

clk.tick()
stop = False
while True:

	for ev in pg.event.get():
		if ev.type == QUIT:
			pg.quit()
			sys.exit()
		if ev.type == pg.KEYDOWN:
			if ev.key == pg.K_UP:
				tmap.move_view_up()
			elif ev.key == pg.K_DOWN:
				tmap.move_view_down()
			elif ev.key == pg.K_LEFT:
				tmap.move_view_left()
			elif ev.key == pg.K_RIGHT:
				tmap.move_view_right()


	disp.fill((0, 0, 0))

	tmap.render_map(disp)

	pg.display.update()

	clk.tick()

	#print(clk.get_time())





