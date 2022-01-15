import os
import pygame as pg
import thorpy
import math
import random
from display.old_display import Display
import thorpy

DESERT_COLOR = (0,0,0)
FIELDS_COLOR = (211, 181, 29)
PASTURE_COLOR = (40,255,55)
MOUNTAINS_COLOR = (139, 236, 244)
HILLS_COLOR = (165, 96, 21)
FOREST_COLOR = (0,43,0)

TILE_COLORS = {0: DESERT_COLOR, 1: FIELDS_COLOR, 2: PASTURE_COLOR, 3: MOUNTAINS_COLOR, 4: HILLS_COLOR, 5: FOREST_COLOR}
# ['Red', 'Cyan', 'Green', 'Yellow']
PLAYER_RGB_COLORS = {0: (255, 0, 0), 1: (0, 255, 255), 2: (0, 128, 0), 3: (0, 0, 255)}
PLAYER_COLORS = ['Red', 'Cyan', 'Green', 'Yellow']

# Returns the indexes of the tiles connected to a certain points
# on the default, tileagonal Catan board
@staticmethod
def get_tile_indexes_for_point(r, i):
    # the indexes of the tiles
    tile_indexes = []
    # Points on a tileagonal board
    points = [
        [None] * 7,
        [None] * 9,
        [None] * 11,
        [None] * 11,
        [None] * 9,
        [None] * 7
    ]
    # gets the adjacent tiles differently depending on whether the point is in the top or the bottom
    if r < len(points) / 2:
        # gets the tiles below the point ------------------

        # adds the tiles to the right
        if i < len(points[r]) - 1:
            tile_indexes.append([r, math.floor(i / 2)])

        # if the index is even, the number is between two tiles
        if i % 2 == 0 and i > 0:
            tile_indexes.append([r, math.floor(i / 2) - 1])

        # gets the tiles above the point ------------------

        if r > 0:
            # gets the tile to the right
            if i > 0 and i < len(points[r]) - 2:
                tile_indexes.append([r - 1, math.floor((i - 1) / 2)])

            # gets the tile to the left
            if i % 2 == 1 and i < len(points[r]) - 1 and i > 1:
                tile_indexes.append([r - 1, math.floor((i - 1) / 2) - 1])

    else:

        # adds the below -------------

        if r < len(points) - 1:
            # gets the tile to the right or directly below
            if i < len(points[r]) - 2 and i > 0:
                tile_indexes.append([r, math.floor((i - 1) / 2)])

            # gets the tile to the left
            if i % 2 == 1 and i > 1 and i < len(points[r]):
                tile_indexes.append([r, math.floor((i - 1) / 2 - 1)])

        # gets the tiles above ------------

        # gets the tile above and to the right or directly above
        if i < len(points[r]) - 1:
            tile_indexes.append([r - 1, math.floor(i / 2)])

        # gets the tile to the left
        if i > 1 and i % 2 == 0:
            tile_indexes.append([r - 1, math.floor((i - 1) / 2)])

    return tile_indexes



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
	def __init__(self, game_tile):

		self.game_tile = game_tile
		self.tile_type = self.game_tile.type
		self.roll_sum = self.game_tile.token_num
		if(self.roll_sum == None):
			self.roll_sum = 0
		# sysfont = pg.font.get_default_font()

		self.tile_color = TILE_COLORS[self.tile_type.value]

		self.hex_vertices = []
		self.hex_vertices_ordered_by_points = []

		self.row = 0

		self.radius = 0
		self.big_r = 0

		self.font_size = 0
		self.font = pg.font.SysFont('5', self.font_size)
		self.roll_sum_img = self.font.render('5', True, (255,0,0))

		self.origin_x = 0
		self.origin_y = 0



	def update_hexagon_vertices(self):

		# Update vertices
		hex_vertices = []
		for i in range(0, 6):
			hex_vertices.append((self.origin_x + math.sin((i/6.0)*2*math.pi)*self.big_radius, self.origin_y + math.cos((i/6.0)*2*math.pi)*self.big_radius));
		self.hex_vertices = hex_vertices
		
		# Update point ordered vertices

		self.point_ordered_hex_vertices = [self.hex_vertices[4], self.hex_vertices[3], self.hex_vertices[2], self.hex_vertices[5], self.hex_vertices[0], self.hex_vertices[1]]



		# Update roll sum img
		self.font_size = int(self.radius)
		self.font = pg.font.SysFont(None, self.font_size)
		ran = random.randint(1,12)
		self.roll_sum_img = self.font.render(str(self.roll_sum), True, (255,0,0))


	def render(self, screen):
		# Tile
		pg.draw.polygon(pg.display.get_surface(), self.tile_color, self.hex_vertices)

		# Border
		pg.draw.polygon(pg.display.get_surface(), (0,0,0), self.hex_vertices, 4)
		
		# Rollsum
		screen.blit(self.roll_sum_img, (self.origin_x - self.font_size/4, self.origin_y - self.font_size/4))



		# pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x, self.origin_y), 1)
		# pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x+self.radius, self.origin_y), 1)
		# pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x, self.origin_y+self.big_radius), 1)

class HexBoard(Container):
	def __init__(self, screen, game_tiles, roads):
		super().__init__()
		self.screen = screen
		# Will be implemented as a container later
		self.width = 500
		self.height = 500

		self.origin_x = 100
		self.origin_y = 50

		self.tiles = []
		self.roads = roads

		# Create board
		for game_tile_row in game_tiles:
			for game_tile in game_tile_row:
				self.tiles.append(HexTile(game_tile))

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
		min_r_height  = self.height/(10 * inv_sqrt3o2)

		r = min(min_r_width, min_r_height)

		t = big_r = r * inv_sqrt3o2

		big_r_o_2 = big_r/2

		itr = 0
		# Start with the middle row, then do top then bottom

		# top
		origin_x = genesis_x + (3 * r)
		origin_y = genesis_y + big_r
		for i in range(0, 3):
			tile_obj = self.tiles[itr]
			tile_obj.radius = r
			tile_obj.big_radius = big_r
			tile_obj.origin_x = origin_x
			tile_obj.origin_y = origin_y
			tile_obj.row = 2
			origin_x += 2 * r
			tile_obj.update_hexagon_vertices()
			itr += 1

		# 2nd from top
		origin_x = genesis_x + (2 * r)
		origin_y = genesis_y + (2 * big_r) + big_r_o_2
		for i in range(0, 4):
			tile_obj = self.tiles[itr]
			tile_obj.radius = r
			tile_obj.big_radius = big_r
			tile_obj.origin_x = origin_x
			tile_obj.origin_y = origin_y
			tile_obj.row = 1
			origin_x += 2 * r
			tile_obj.update_hexagon_vertices()
			itr += 1


		# Middle
		# Set the origin as the origin of the leftmost middle tile in the grid, such that the tile is aligned middle and justified left
		origin_x = genesis_x + (1 * r)
		origin_y = genesis_y + (4 * big_r)
		for i in range(0, 5):
			tile_obj = self.tiles[itr]
			tile_obj.radius = r
			tile_obj.big_radius = big_r
			tile_obj.origin_x = origin_x
			tile_obj.origin_y = origin_y
			tile_obj.row = 0
			origin_x += 2 * r
			tile_obj.update_hexagon_vertices()
			itr += 1


		# 2nd from bottom
		origin_x = genesis_x + (2 * r)
		origin_y = genesis_y + (5 * big_r) + big_r_o_2
		for i in range(0, 4):
			tile_obj = self.tiles[itr]
			tile_obj.radius = r
			tile_obj.big_radius = big_r
			tile_obj.origin_x = origin_x
			tile_obj.origin_y = origin_y
			tile_obj.row = 3
			origin_x += 2 * r
			tile_obj.update_hexagon_vertices()
			itr += 1



		# bottom
		origin_x = genesis_x + (3 * r)
		origin_y = genesis_y + (7 * big_r)
		for i in range(0, 3):
			tile_obj = self.tiles[itr]
			tile_obj.radius = r
			tile_obj.big_radius = big_r
			tile_obj.origin_x = origin_x
			tile_obj.origin_y = origin_y
			tile_obj.row = 4
			origin_x += 2 * r
			tile_obj.update_hexagon_vertices()
			itr += 1

	def render(self):
		self.render_tiles(self.screen)
		self.render_settlements_cities_roads(self.screen)

	def render_tiles(self, screen):
		for tile_obj in self.tiles:
			if(tile_obj.hex_vertices):
				tile_obj.render(screen)
		pg.draw.circle(pg.display.get_surface(), (255, 255, 0), (self.origin_x, self.origin_y), 10)


	def render_settlements_cities_roads(self, screen):
		# Roads and cities
		# print(self.game_tile.points)

		# Cities and roads
		for tile_obj in self.tiles:
			# pg.draw.circle(pg.display.get_surface(), (255, 255, 0), tile_obj.point_ordered_hex_vertices[5], 10)

			for itr in range(0, len(tile_obj.game_tile.points)):
				point = tile_obj.game_tile.points[itr]
				
				# Road
				for road in self.roads:
					if(road.point_one == point):
						for j in range(0, len(tile_obj.game_tile.points)):
							if(road.point_two == tile_obj.game_tile.points[j]):
								point_one = point
								point_one_coords = tile_obj.point_ordered_hex_vertices[itr]
								point_two = road.point_two
								point_two_coords = tile_obj.point_ordered_hex_vertices[j]
								pg.draw.line(pg.display.get_surface(), PLAYER_RGB_COLORS[road.owner], point_one_coords, point_two_coords, 5)
				# print(point)
				if(not point.building == None):
					# Settlement
					if(point.building.type == 0):
						# print(point)
						pg.draw.circle(pg.display.get_surface(), PLAYER_RGB_COLORS[point.building.owner], tile_obj.point_ordered_hex_vertices[itr], 10)
					# City
					if(point.building.type == 2):
						pg.draw.circle(pg.display.get_surface(), PLAYER_RGB_COLORS[point.building.owner], tile_obj.point_ordered_hex_vertices[itr], 10)
						pg.draw.circle(pg.display.get_surface(), (0,0,0), tile_obj.point_ordered_hex_vertices[itr], 5)


class InfoDisplay:
	def __init__(self, screen, game):
		self.screen = screen
		self.game = game
		#declaration of some ThorPy elements ...

		# Game Info decided at game init
		# game_info_label = thorpy.make_text("GAME INFO")

		# num_of_players_label = thorpy.make_text("Number of players: ")
		# agent_type_arr_label = thorpy.make_text("Agent Types: ")
		
		# initial_play_order_label = thorpy.make_text()
		# play_order = thorpy.make_text()

		# # Game info updated every step
		self.make_text(self.game)









	def make_text(self, game):
		# # Game flags
		self.game_flags_header = thorpy.make_text("GAME FLAGS")
		self.initial_placement_mode_label = thorpy.make_text("Initial Placement Mode: " + str(game.initial_placement_mode))
		self.give_initial_yield_label = thorpy.make_text("Give initial yield flag: " + str(game.give_initial_yield))

		if(game.longest_road_owner == None):
			self.longest_road_owner_label = thorpy.make_text("Longest Road Owner: None")
		else:
			self.longest_road_owner_label = thorpy.make_text("Longest Road Owner: " + PLAYER_COLORS[game.longest_road_owner] + "(" + str(game.longest_road_owner) + ")")

		if(game.largest_army == None):
			self.largest_army_owner_label = thorpy.make_text("Largest Army Owner: None")
		else:
			self.largest_army_owner_label = thorpy.make_text("Largest Army Owner: " + PLAYER_COLORS[game.largest_army] + "(" + str(game.largest_army) + ")")
		self.game_has_ended_label = thorpy.make_text("Game Ended: " + str(game.has_ended))
		self.dev_card_deck_label = thorpy.make_text("Dev Card Deck: ")

		self.game_flags_header_box = thorpy.Box(elements=[self.game_flags_header])
		# Formatting
		# thorpy.store(game_flags_header_box, mode="v", align="center")

		self.game_flags_label_box = thorpy.Box(elements=[self.initial_placement_mode_label, self.give_initial_yield_label, self.longest_road_owner_label, self.largest_army_owner_label, self.game_has_ended_label])
		# Formatting
		thorpy.store(self.game_flags_label_box, mode="v", align="center")

		self.game_flags_box = thorpy.Box(elements=[self.game_flags_header_box, self.game_flags_label_box])


		# # Turn flags
		self.turn_flags_header = thorpy.make_text("TURN FLAGS")

		self.turn_flags_header_box = thorpy.Box(elements=[self.turn_flags_header])

		if(game.player_with_turn == None):
			self.player_with_turn_label = thorpy.make_text("Player w/ Turn: None")
		else:
			self.player_with_turn_label = thorpy.make_text("Player w/ Turn: " + PLAYER_COLORS[game.player_with_turn.num] + "(" + str(game.player_with_turn.num) + ")")
 

		self.can_roll_label = thorpy.make_text("Can Roll: " + str(game.can_roll))
		self.last_roll_label = thorpy.make_text("Last Roll: " + str(game.last_roll))
		self.rolled_seven_label = thorpy.make_text("Rolled Seven: " + str(game.rolled_seven))
		self.robber_moved_label = thorpy.make_text('Robber Moved: ' + str(game.robber_moved))

		# Formatting
		# thorpy.store(game_flags_header_box, mode="v", align="center")

		self.turn_flags_label_box = thorpy.Box(elements=[self.player_with_turn_label, self.can_roll_label, self.last_roll_label, self.rolled_seven_label, self.robber_moved_label])
		# Formatting
		thorpy.store(self.turn_flags_label_box, mode="v", align="center")

		self.turn_flags_box = thorpy.Box(elements=[self.turn_flags_header_box, self.turn_flags_label_box])
		# text = thorpy.make_text("GAME INFO")

		# slider = thorpy.SliderX(100, (12, 35), "My Slider")
		# button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)

		# self.game_info_text_box = thorpy.Box(elements=[text])

		# self.box = thorpy.Box(elements=[text,slider,button])
		#we regroup all elements on a menu, even if we do not launch the menu
		self.master_box = thorpy.Box(elements=[self.game_flags_box, self.turn_flags_box])
		# thorpy.store(self.master_box, mode="v", align="left")
		# self.master_box.fit_children()
		# self.master_box.refresh_lift()




		self.menu = thorpy.Menu(self.master_box)
		#important : set the screen as surface for all elements
		for element in self.menu.get_population():
		    element.surface = self.screen
		#use the elements normally...
		self.master_box.set_topleft((600,100))




	def render(self):
		self.make_text(self.game)
		self.master_box.blit()
		# self.box.update()


class VisualDisplay:

	def __init__(self):

		# An array of tiles, where the vertices of each exist in rendering surface space
		pg.init()
		self.screen = pg.display.set_mode((860, 860), pg.SCALED | pg.RESIZABLE)
		pg.display.set_caption("Monkey Fever")
		# pg.mouse.set_visible(False)
		background = pg.Surface(self.screen.get_size())
		background = background.convert()
		background.fill((38, 13, 23))
		self.background = background
		self.clock = pg.time.Clock()
		self.old_display = None

		self.info_display = None





	def new_game(self, game):
		self.game = game
		self.hex_board = HexBoard(self.screen, self.game.board.tiles, self.game.board.roads)
		self.old_display = Display(self.game)
		self.info_display = InfoDisplay(self.screen, self.game)

	def render(self):
		self.hex_board.render()
		self.info_display.render()
		# print(self.game.board.tiles)
		# self.old_display.displayBoard()

				



	def tick(self):
		self.clock.tick()

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
		# self.old_display.displayBoard()
		pg.display.flip()
		


