import os
import sys
import math
import pygame as pg 
from pygame.locals import *



def find_path(tmap, start_pos, goal_pos, heuristic):

	x_bounds, y_bounds = tmap.num_tiles_x, tmap.num_tiles_y


	closed_set = []
	open_set = []
	closed_set += get_obstacles(tmap)

	came_from = {}

	g_scores = {}
	f_scores = {}
	for y in range(y_bounds):
		for x in range(x_bounds):
			g_scores[(x, y)] = 1000
			f_scores[(x, y)] = 1000


	g_scores[start_pos] = 0
	f_scores[start_pos] = heuristic(start_pos, goal_pos)

	open_set.append(start_pos)

	while len(open_set) > 0:
		current = lowest_score_node(open_set, f_scores)
		if current == goal_pos:
			return reconstruct_path(came_from, current)

		
		open_set.remove(current)
		closed_set.append(current)

		neighbors = get_neighbors(current, (x_bounds, y_bounds))
		for neighbor in neighbors:
			if neighbor in closed_set:
				continue

			tent_g_score = g_scores[current] + get_passability(tmap, neighbor)

			if neighbor not in open_set:
				open_set.append(neighbor)
			elif tent_g_score >= g_scores[neighbor]:
				continue

			came_from[neighbor] = current
			g_scores[neighbor] = tent_g_score
			f_scores[neighbor] = heuristic(neighbor, goal_pos)

	return []

def reconstruct_path(came_from, current):
	path = []
	path.append(current)

	while current in came_from.keys():
		current = came_from[current]
		path.append(current)

	return path



def direct_distance(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def lowest_score_node(l, scores):
	lowest_v = 100000
	lowest_k = 100000
	for k in l:
		score = scores[k]
		if lowest_v > score:
			lowest_v = score
			lowest_k = k

	return lowest_k

	'''
	lowest_v = list(scr.values())[0]
	lowest_k = list(scr.keys())[0]
	for key, val in scr.items():
		if lowest_v > val:
			lowest_v = val
			lowest_k = key 
	return lowest_k
	'''

def remove_by_pos(d, pos):
	for k, v in d.items():
		if d[k] == v:
			del d[k]
			return

def get_neighbors(pos, bounds):
	n = []
	x, y = pos
	x_max, y_max = bounds[0] - 1, bounds[1] - 1

	if x > 0:
		n.append((x - 1, y))

	if x < x_max:  
		n.append((x + 1, y))

	if y > 0:
		n.append((x, y - 1))

	if y < y_max:
		n.append((x, y + 1))

	
	if x > 0 and y > 0:
		n.append((x - 1, y - 1))

	if x > 0 and y < y_max:
		n.append((x - 1, y + 1))

	if x < x_max and y > 0:
		n.append((x + 1, y - 1))

	if x < x_max and y < y_max:
		n.append((x + 1, y + 1))
	

	return n

def get_obstacles(tmap):
	x_max, y_max = tmap.num_tiles_x, tmap.num_tiles_y
	obstacles = []

	for y in range(y_max):
		for x in range(x_max):
			for tile in tmap.map[y][x]:
				if tile.is_obstacle:
					obstacles.append((x, y))
					break

	return obstacles


def get_passability(tmap, pos):
	x, y = pos

	return tmap.map[y][x][0].passability