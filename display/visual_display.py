import os
import pygame as pg
import thorpy
import math

class Container():
	def __init__(self):
		# Origin is bottom left corner of rectangle
		self.origin_x = '0'
		self.origin_y = '0'

		self.width = '0'
		self.height = '0'

		self.min_width = '0'
		self.min_height = '0'


		self.paddingLeft = '0'
		self.paddingRight = '0'
		self.paddingTop = '0'
		self.paddingBottom = '0'

	def resize(self):
		pass


class FlexContainer():
	def __init__(self):
		self.containers = []

	def addContainer(self):
		pass

	def isFull(self):
		pass

class Percent():
	def __init__(self, parent_container, value)
		self.value = parent_container #TODO wtf, lol

class HexTile():
	def __init__(self):
		self.tile = tile
		self.hex_corner_vertices = []

		self.radius = 0

		self.boardHorizontalOffset = 0
		self.boardVerticalOffset = 0

		self.localHorizontalOffset = 0
		self.localVerticalOffset = 0

		self.hex_origin_x = 0
		self.hex_origin_y = 0


	def get_hexagon_vertices(self, horizontalOffset, verticalOffset, size):
		for i in range(0, 6):
			hex_vertices.append((horizontalOffset + math.sin(i/6.0*2*math.pi)*size, verticalOffset + math.cos(i/6.0*2*math.pi)*size));
		return hex_vertices

class HexBoard():
	def __init__(self):
		pass


class VisualDisplay:
	def __init__(self):

		# An array of tiles, where the vertices of each exist in rendering surface space
		self.tiles = []


		pg.init()
		self.screen = pg.display.set_mode((480, 480), pg.SCALED | pg.RESIZABLE)
		pg.display.set_caption("Monkey Fever")
		# pg.mouse.set_visible(False)
		background = pg.Surface(screen.get_size())
		background = background.convert()
		background.fill((170, 238, 187))
		screen.blit(background, (0, 0))
		pg.display.flip()

		clock = pg.time.Clock()

		hex_vertices = []





	def render(self):
		pg.draw.aalines(pg.display.get_surface(), 255, True, hex_vertices)
		for i in range(0, len(self.tiles)):
			for tile in tile_arr:


	def main(self):
		going = True
		while going:
			clock.tick(60)

			# Handle Input Events
			for event in pg.event.get():
				if event.type == pg.QUIT:
					going = False
				elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					going = False
				elif event.type == pg.VIDEORESIZE:
					# screen.blit(pygame.transform.scale(pic, event.dict['size']), (0, 0))
					pg.display.update()

			screen.blit(background, (0, 0))
			self.render()
			pg.display.flip()
			


VisualDisplay()