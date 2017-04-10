import os
import sys
import pygame as pg 
from camera import Camera
from player import Player
from walker import Walker
import astar

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

		self.passability = 3

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

	def __init__(self, num_tiles_x, num_tiles_y, tilesize, img, cam):
		self.num_tiles_x = num_tiles_x
		self.num_tiles_y = num_tiles_y
		self.tilesize = tilesize
		self.img = img

		self.camera = cam

		''' 
		' Creates a 3D list of tiles 
		' Rows and cols are for the individual fields
		' while the depth is for stacking tile layers
		' Everytime the arangement is changed, the tiles will be sorted by depth accordingly
		' On initialization the list is empty
		'''	
		self.map = [[[Tile.empty((x, y), 24)] for x in range(num_tiles_x)] for y in range(num_tiles_y)]


		#debug
		self.calls = 0

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
		x_off, y_off = self.camera.get_pos()

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
		x_off, y_off = tuple([self.tilesize * n for n in self.camera.get_pos()])
		x_start = int(x_off / self.tilesize)
		y_start = int(y_off / self.tilesize)
		w1, h = pg.display.get_surface().get_size()
		x_end = x_start + int(w1 / self.tilesize)
		y_end = y_start + int(h / self.tilesize)

		if x_start < 0:
			x_start = 0

		if y_start < 0:
			y_start = 0

		if x_end >= self.num_tiles_x:
			x_end = self.num_tiles_x - 1

		if y_end >= self.num_tiles_y:
			y_end = self.num_tiles_y - 1

		self.calls = (y_end+1 - y_start) * (x_end+1 - x_start)

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

	def get_tiles_in_block(self, pos):
		x, y = pos
		return self.map[y][x]

	def render_hovered_tile_marker(self, pos, surf, dt):
		self.hover_opacity_counter += dt
		if self.hover_opacity_counter >= 500:
			self.hover_opacity_counter = 0

		rect = pygame.Surface((TILESIZE, TILESIZE), pg.SRCALPHA, 32)
		rect.fill((255, 0, 0, 150*(hover_opacity_counter/500)))
		surf.blit(rect, pos)


pg.init()
TILESIZE = 16
NUM_TILES_X = 50
NUM_TILES_Y = 50
tilemap_img = pg.image.load("tiles.png")
disp = pg.display.set_mode((800, 600))

cam = Camera((0, 0))

tmap = Tilemap(NUM_TILES_X, NUM_TILES_Y, TILESIZE, tilemap_img, cam)
clk = pg.time.Clock()

pg.time.set_timer(USEREVENT+1, 100)

#p = Player((0, 0), tmap, True, cam)
w1 = Walker((1, 0), tmap, 10)
w2 = Walker((2, 0), tmap, 10)
w3 = Walker((0, 0), tmap, 10)



stop = False



while True:
	
	event_queue = pg.event.get()
	cam.update(event_queue)

	for ev in event_queue:	
		if ev.type == QUIT:
			pg.quit()
			sys.exit()
		if ev.type == pg.KEYDOWN:
			if ev.key == pg.K_SPACE:
				
				x, y = pg.mouse.get_pos()
				#clk.tick()
				w1.move_to((int(x / TILESIZE), (int(y / TILESIZE))), True)
				w2.move_to((int(x / TILESIZE)+1, (int(y / TILESIZE))), True)
				w3.move_to((int(x / TILESIZE)-1, (int(y / TILESIZE))), True)
				#clk.tick()
				#print ("Time to find path:", clk.get_time())
				'''
				for b in path:
					x, y = b
					tmap.map[y][x][0] = Tile.empty(b, 20)
				'''


			'''
		if ev.type == USEREVENT+1:
			os.system("cls")
			print("Elapsed time per frame:\t", clk.get_time())
			print("Draw calls: \t", tmap.calls)
			tmap.calls = 0
			'''

	pressed = pg.mouse.get_pressed()
	if pressed[0]:
		x, y = pg.mouse.get_pos()
		x = int(x / TILESIZE)
		y = int(y / TILESIZE)

		tmap.map[y][x][0] = Tile.empty((x, y), 7)
		tmap.map[y][x][0].is_obstacle = True
	elif pressed[2]:
		x, y = pg.mouse.get_pos()
		x = int(x / TILESIZE)
		y = int(y / TILESIZE)

		tmap.map[y][x][0] = Tile.empty((x, y), 24)
		tmap.map[y][x][0].is_obstacle = False

	
	dt = clk.get_time()


	disp.fill((0, 0, 0))
	

	tmap.render_map(disp)

	w1.update(dt)
	w1.render(disp)

	w2.update(dt)
	w2.render(disp)

	w3.update(dt)
	w3.render(disp)

	pg.display.update()

	clk.tick()

	





