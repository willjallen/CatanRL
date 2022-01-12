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
	def __init__(self, parent_container, value):
		self.value = parent_container #TODO wtf, lol

class HexTile():
	def __init__(self, radius, big_radius, origin_x, origin_y):
		self.tile_type = None
		self.roll_sum = 0

		self.hex_vertices = []

		self.r = radius
		self.big_r = big_radius


		self.origin_x = origin_x
		self.origin_y = origin_y


	def update_hexagon_vertices(self):
		hex_vertices = []
		for i in range(0, 6):
			hex_vertices.append((self.origin_x + math.sin(i/6.0*2*math.pi)*self.big_radius, self.origin_y + math.cos(i/6.0*2*math.pi)*self.big_radius));
		self.hex_vertices = hex_vertices

	def render(self):
		pg.draw.polygon(pg.display.get_surface(), 255, self.hex_vertices, 2)
		pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x, self.origin_y), 1)
		pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x+self.radius, self.origin_y), 1)
		pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x, self.origin_y+self.big_radius), 1)

class HexBoard(Container):
	def __init__(self):
		super().__init__()
		# Will be implemented as a container later
		self.width = 500
		self.height = 500

		self.origin_x = 0
		self.origin_y = 0

		self.tiles = []

		# Create board
		for i in range(0, 19):
			self.tiles.append(HexTile(0,0,0,0))

		self.update_board()


	# As far as I am aware, this is the best way to render a grid of 3,4,5,4,3 hexagonal tiles without unncessary complexity
	def update_board(self):
		# constants
		sqrt3o2 = 0.866025403784
		inv_sqrt3o2 = 1.15470053838


		# container TODO
		genesis_x = self.origin_x
		genesis_y = self.origin_y

		# Find radius
		# 10 * r <= width
		# r <= width/10
		# or
		# 10 * R <= height
		# R <= height/10
		# r = R * sqrt3o2

		# take whichever is less
		
		min_r_width = self.width/10
		min_r_height  = self.height/10 * inv_sqrt3o2

		r = min(min_r_width, min_r_height)

		t = big_r = r * inv_sqrt3o2

		itr = 0
		# Start with the middle row, then do top then bottom

		# Middle
		# Set the origin as the origin of the leftmost middle tile in the grid, such that the tile is aligned middle and justified left
		origin_x = genesis_x + (1 * big_r)
		origin_y = genesis_y + (5 * r)
		for i in range(0, 5):
			tile_obj = self.tiles[itr]
			tile_obj.radius = r
			tile_obj.big_radius = big_r
			tile_obj.origin_x = origin_x
			tile_obj.origin_y = origin_y
			origin_x += 2 * r
			tile_obj.update_hexagon_vertices()
			itr += 1


		# # 2nd from top
		# origin_x = genesis_x + (2 * big_r)
		# origin_y = genesis_y + (3 * r)
		# for i in range(0, 4):
		# 	tile_obj = self.tiles[itr]
		# 	tile_obj.radius = big_r
		# 	tile_obj.origin_x = origin_x
		# 	tile_obj.origin_y = origin_y
		# 	origin_x += 2 * r
		# 	tile_obj.update_hexagon_vertices()
		# 	itr += 1



		# # top
		# origin_x = genesis_x + (3 * r)
		# origin_y = genesis_y + (9 * big_r)
		# for i in range(0, 3):
		# 	tile_obj = self.tiles[itr]
		# 	tile_obj.radius = r
		# 	tile_obj.origin_x = origin_x
		# 	tile_obj.origin_y = origin_y
		# 	origin_x += 2 * r
		# 	tile_obj.update_hexagon_vertices()
		# 	itr += 1



		# # 2nd from bottom
		# origin_x = genesis_x + (2 * r)
		# origin_y = genesis_y + (3 * big_r)
		# for i in range(0, 4):
		# 	tile_obj = self.tiles[itr]
		# 	tile_obj.radius = r
		# 	tile_obj.origin_x = origin_x
		# 	tile_obj.origin_y = origin_y
		# 	origin_x += 2 * r
		# 	tile_obj.update_hexagon_vertices()
		# 	itr += 1



		# # bottom
		# origin_x = genesis_x + (3 * r)
		# origin_y = genesis_y + (1 * big_r)
		# for i in range(0, 3):
		# 	tile_obj = self.tiles[itr]
		# 	tile_obj.radius = r
		# 	tile_obj.origin_x = origin_x
		# 	tile_obj.origin_y = origin_y
		# 	origin_x += 2 * r
		# 	tile_obj.update_hexagon_vertices()
		# 	itr += 1




	def render(self):
		for tile_obj in self.tiles:
			if(tile_obj.hex_vertices):
				tile_obj.render()

class VisualDisplay:
	def __init__(self):

		# An array of tiles, where the vertices of each exist in rendering surface space
		self.tiles = []


		pg.init()
		self.screen = pg.display.set_mode((1920, 1080), pg.SCALED | pg.RESIZABLE)
		pg.display.set_caption("Monkey Fever")
		# pg.mouse.set_visible(False)
		background = pg.Surface(self.screen.get_size())
		background = background.convert()
		background.fill((170, 238, 187))
		self.background = background
		self.screen.blit(self.background, (0, 0))
		pg.display.flip()

		self.clock = pg.time.Clock()

		self.hex_board = HexBoard()


		self.main()


	def render(self):
		self.hex_board.render()




	def main(self):
		going = True
		while going:
			self.clock.tick(60)

			# Handle Input Events
			for event in pg.event.get():
				if event.type == pg.QUIT:
					going = False
				elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					going = False
				elif event.type == pg.VIDEORESIZE:
					# screen.blit(pygame.transform.scale(pic, event.dict['size']), (0, 0))
					pg.display.update()

			self.screen.blit(self.background, (0, 0))
			self.render()
			pg.display.flip()
			


VisualDisplay()