import os
import pygame as pg
import thorpy
import math
import random
from display.old_display import Display
import thorpy
from pycatan.card import ResCard, DevCard
from thorpy.painting.painters.imageframe import ImageButton
from pygame.event import Event, post
from thorpy.miscgui import constants

DESERT_COLOR = (237, 201, 175)
FIELDS_COLOR = (211, 181, 29)
PASTURE_COLOR = (92, 146, 2)
MOUNTAINS_COLOR = (162, 192, 210)
HILLS_COLOR = (193, 68, 91)
FOREST_COLOR = (41, 64, 6)

TILE_COLORS = {0: DESERT_COLOR, 1: FIELDS_COLOR, 2: PASTURE_COLOR, 3: MOUNTAINS_COLOR, 4: HILLS_COLOR, 5: FOREST_COLOR}
# ['Red', 'Cyan', 'Green', 'Yellow']
PLAYER_RGB_COLORS = {0: (255, 0, 0), 1: (255, 231, 112), 2: (0, 128, 0), 3: (0, 0, 255)}
PLAYER_COLORS = ['Red', 'Cyan', 'Green', 'Yellow']

action_types = ["no_op", "roll", "purchase_resource", "purchase_and_play_building", "purchase_dev_card", "play_dev_card", "play_robber", "start_trade", "accept_trade", "deny_trade", "forfeit_cards", "end_turn", "initial_placement_road", "initial_placement_building", "place_road"]


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
	def __init__(self, game_tile, game):

		self.game = game
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
		self.has_robber = False


		self.origin_x = 0
		self.origin_y = 0

	def set_tile(self, game_tile):
		self.game_tile = game_tile
		self.tile_type = self.game_tile.type
		self.roll_sum = self.game_tile.token_num
		if(self.roll_sum == None):
			self.roll_sum = 0




	def set_hexagon_vertices(self):

		# Update vertices
		hex_vertices = []
		for i in range(0, 6):
			hex_vertices.append((self.origin_x + math.sin((i/6.0)*2*math.pi)*self.big_radius, self.origin_y + math.cos((i/6.0)*2*math.pi)*self.big_radius));
		self.hex_vertices = hex_vertices
		
		# Update point ordered vertices

		self.point_ordered_hex_vertices = [self.hex_vertices[4], self.hex_vertices[3], self.hex_vertices[2], self.hex_vertices[5], self.hex_vertices[0], self.hex_vertices[1]]



		# Update roll sum img
	def set_rollsum_img(self):
		self.font_size = int(self.radius)
		self.font = pg.font.SysFont(None, self.font_size)
		ran = random.randint(1,12)

		if(self.has_robber):
			roll_sum_str = str(self.roll_sum) + '*'
		else:
			roll_sum_str = str(self.roll_sum)

		if(self.roll_sum == 6 or self.roll_sum == 8):
			roll_sum_color = (255,0,0)
		else:
			roll_sum_color = (0,0,0) 

		self.roll_sum_img = self.font.render(roll_sum_str, True, roll_sum_color)




	def render(self, screen):
		# Tile
		pg.draw.polygon(pg.display.get_surface(), self.tile_color, self.hex_vertices)

		# Border
		pg.draw.polygon(pg.display.get_surface(), (0,0,0), self.hex_vertices, 4)
		
		# Rollsum
		robber = self.game.board.robber
		

		if(robber.position == self.game_tile.position):
			self.has_robber = True
			self.render_rollsum = True
		else:
			self.has_robber = False
		

		self.set_rollsum_img()
		

		screen.blit(self.roll_sum_img, (self.origin_x - self.font_size/4, self.origin_y - self.font_size/4))
		


		# pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x, self.origin_y), 1)
		# pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x+self.radius, self.origin_y), 1)
		# pg.draw.circle(pg.display.get_surface(), (255, 0, 0), (self.origin_x, self.origin_y+self.big_radius), 1)

class HexBoard(Container):
	def __init__(self, screen, game):
		super().__init__()
		self.screen = screen
		# Will be implemented as a container later
		self.width = 500
		self.height = 500

		self.origin_x = 100
		self.origin_y = 50

		self.game = game

		self.tiles = []
		self.roads = self.game.board.roads

		# Create board
		for game_tile_row in self.game.board.tiles:
			for game_tile in game_tile_row:
				self.tiles.append(HexTile(game_tile, self.game))

		self.make_board()

	def set_game(self, game):
		self.game = game
		self.roads = game.board.roads
		# print('before')
		# for tile in self.tiles:
		# 	print(tile.game_tile)

		itr = 0	
		for i in range(0, len(self.game.board.tiles)):
			for j in range(0, len(self.game.board.tiles[i])):
				self.tiles[itr].set_tile(self.game.board.tiles[i][j])
				itr += 1
				
		# print('after')
		# for tile in self.tiles:
		# 	print(tile.game_tile)



		# self.tiles = []
		# for game_tile_row in self.game.board.tiles:
		# 	for game_tile in game_tile_row:
		# 		self.tiles.append(HexTile(game_tile))


	def make_board(self):
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
			tile_obj.set_hexagon_vertices()
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
			tile_obj.set_hexagon_vertices()
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
			tile_obj.set_hexagon_vertices()
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
			tile_obj.set_hexagon_vertices()
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
			tile_obj.set_hexagon_vertices()
			itr += 1

	def render(self):
		self.render_tiles(self.screen)
		self.render_settlements_cities_roads(self.screen)

	def render_tiles(self, screen):
		for tile_obj in self.tiles:
			if(tile_obj.hex_vertices):
				tile_obj.render(screen)
		# pg.draw.circle(pg.display.get_surface(), (255, 255, 0), (self.origin_x, self.origin_y), 10)



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


class ControlDisplay:
	def __init__(self, surface, game):
		self.surface = surface
		self.game = game

		self.speed_button_pressed = False

		self.make_buttons()

		self.step_back_button_toggled = False
		self.step_forward_button_toggled = False
		

		self.pause_button_toggled = False
		self.play_button_toggled = False

	def set_game(self, game):
		self.game = game

	def make_buttons(self):
		self.play_unpressed_img = ImageButton('display/img/play.png', alpha=255, force_convert_alpha=True)
		self.play_pressed_img = ImageButton('display/img/play-pressed.png', force_convert_alpha=True)

		# self.play_button = thorpy.make_("Play")	
		

		self.play_pressed = False
		# self.play_button = thorpy.make_image_button('display/img/play-pressed.png',alpha=0,colorkey=(255,255,255), force_convert_alpha=True)
			
		# img = self.play_button._normal_imgs
		# print(img)

		# print(dir(self.play_button))

		# pressed_reaction = thorpy.Reaction(reacts_to=pg.MOUSEBUTTONDOWN,
  #                             reac_func=self.update_button, params={'button': 'play_button'})

		# self.play_button = self.play_unpressed_img
		# self.play_button = thorpy.make_button("", func=self.update_button, params={'button': 'play_button'})


		self.rewind_button = thorpy.Togglable("<<")
		self.rewind_button.user_func = self.update_button
		self.rewind_button.user_params = {'speed_button': 'rewind_button'}	
		self.rewind_button.finish()

		self.step_back_button = thorpy.Clickable("<|")
		self.step_back_button.user_func = self.update_button
		self.step_back_button.user_params = {'speed_button': 'step_back_button'}	
		self.step_back_button.finish()

		self.pause_button = thorpy.Togglable("||")
		self.pause_button.user_func = self.update_button
		self.pause_button.user_params = {'speed_button': 'pause_button'}	
		self.pause_button.finish()

		self.step_forward_button = thorpy.Clickable("|>")
		self.step_forward_button.user_func = self.update_button
		self.step_forward_button.user_params = {'speed_button': 'step_forward_button'}	
		self.step_forward_button.finish()

		self.play_button = thorpy.Togglable(">>")
		self.play_button.user_func = self.update_button
		self.play_button.user_params = {'speed_button': 'play_button'}	
		self.play_button.finish()



		# self.

		# self.play_button.set_painter(self.play_unpressed_img)
		# self.play_button.set_size((512,512))
	


		# self.play_button_box = thorpy.Pressable(elements=[self.play_unpressed_img])
		# self.play_button_box.add_reaction(pressed_reaction)
		# self.play_button_box.finish()


		self.master_box = thorpy.Box(elements=[self.rewind_button, self.step_back_button, self.pause_button, self.step_forward_button, self.play_button])
		thorpy.store(self.master_box, mode='h')
		self.master_box.fit_children()
		self.menu = thorpy.Menu(self.master_box)

		for element in self.menu.get_population():
			element.surface = self.surface
		#use the elements normally...
		self.master_box.set_topleft((100,650))




	def update_button(self, **kwargs):
		# print(kwargs)
		# ev_untog = Event(constants.THORPY_EVENT,
		# 	id=constants.EVENT_UNTOGGLE, el=self)
		# post(ev_untog)		
		# self.play_button.toggled = False
		# print(self.play_button.toggled)

		if(kwargs['speed_button']):
			if(kwargs['speed_button'] == 'rewind_button'):
				if(self.pause_button.toggled):
					self.pause_button._force_unpress()
				if(self.play_button.toggled):
					self.play_button._force_unpress()


			if(kwargs['speed_button'] == 'step_back_button'):
				self.step_back_button_toggled = True

			if(kwargs['speed_button'] == 'pause_button'):
				if(self.play_button.toggled):
					self.play_button._force_unpress()
				if(self.rewind_button.toggled):
					self.rewind_button._force_unpress()

			if(kwargs['speed_button'] == 'step_forward_button'):
				self.step_forward_button_toggled = True

			if(kwargs['speed_button'] == 'play_button'):
				if(self.pause_button.toggled):
					self.pause_button._force_unpress()
				if(self.rewind_button.toggled):
					self.rewind_button._force_unpress()







				# self.play_button.set_size((512,512))
				# self.play_button.finish()
				# self.master_box = thorpy.Box(elements=[self.play_button], size=(100,100))
				# self.menu = thorpy.Menu(self.master_box)

				# for element in self.menu.get_population():
				# 	element.surface = self.surface
				# #use the elements normally...
				# self.master_box.set_topleft((100,500))


				# self.master_box.unblit_and_reblit()



	def render(self):
		self.master_box.blit()
		self.master_box.update()


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

	def set_game(self, game):
		self.game = game

	# This function is extremely slow, if this ever becomes an issue start with this
	# https://stackoverflow.com/questions/60469344/rendering-text-in-pygame-causes-lag
	def make_text(self, game):

		self.size_helper_one = thorpy.make_text("                                            ")
		self.size_helper_two = thorpy.make_text("                                            ")

		# # Game info
		self.game_info_header = thorpy.make_text("GAME INFO")

		# # Game flags
		self.game_flags_header = thorpy.make_text("GAME FLAGS")
		self.initial_placement_mode_label = thorpy.make_text("Initial Placement Mode: " + str(game.initial_placement_mode))
		self.give_initial_yield_label = thorpy.make_text("Give initial yield flag: " + str(game.give_initial_yield))
		# self.give_initial_yield_label_box = thorpy.Box(give_initial_yield_label)
		# thorpy.store(give_initial_yield_label_box,)
		# thorpy.store(self.give_initial_yield_label, align="left")


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

		self.turn_counter_label = thorpy.make_text("Turn Counter: " + str(game.turn_counter))
		self.step_counter_label = thorpy.make_text("Step Counter: " + str(game.step_count))


		self.game_flags_header_box = thorpy.Box(elements=[self.game_flags_header])
		# Formatting
		# thorpy.store(game_flags_header_box, mode="v", align="center")

		self.game_flags_label_box = thorpy.Box(elements=[self.size_helper_one, self.initial_placement_mode_label, self.give_initial_yield_label, self.longest_road_owner_label, self.largest_army_owner_label, self.game_has_ended_label, self.turn_counter_label, self.step_counter_label, self.size_helper_two])
		# Formatting
		# thorpy.store(self.game_flags_label_box, mode="v", align="left")

		self.game_flags_box = thorpy.Box(elements=[self.game_flags_header_box, self.game_flags_label_box])


		# # Turn flags
		self.turn_flags_header = thorpy.make_text("TURN FLAGS")

		self.turn_flags_header_box = thorpy.Box(elements=[self.turn_flags_header])

		if(game.player_with_turn == None):
			self.player_with_turn_label = thorpy.make_text("Player w/ Turn: None")
		else:
			self.player_with_turn_label = thorpy.make_text("Player w/ Turn: " + PLAYER_COLORS[game.player_with_turn.num] + "(" + str(game.player_with_turn.num) + ")")
		
		if(game.curr_player == None):
			self.curr_player_label = thorpy.make_text("Current player: None")
		else:
			self.curr_player_label = thorpy.make_text("Current Player: " + PLAYER_COLORS[game.curr_player.num] + "(" + str(game.curr_player.num) + ")")



		self.can_roll_label = thorpy.make_text("Can Roll: " + str(game.can_roll))
		self.last_roll_label = thorpy.make_text("Last Roll: " + str(game.last_roll))
		self.rolled_seven_label = thorpy.make_text("Rolled Seven: " + str(game.rolled_seven))
		self.robber_moved_label = thorpy.make_text('Robber Moved: ' + str(game.robber_moved))

		# Formatting
		# thorpy.store(game_flags_header_box, mode="v", align="center")
		# self.size_helper = thorpy.make_text("                                          ")
		self.turn_flags_label_box = thorpy.Box(elements=[self.size_helper_one, self.player_with_turn_label, self.curr_player_label, self.can_roll_label, self.last_roll_label, self.rolled_seven_label, self.robber_moved_label, self.size_helper_two])
		# Formatting
		# thorpy.store(self.turn_flags_label_box, mode="v", align="left")
		# self.turn_flags_label_box.set_size(self.game_flags_label_box.get_size())
		self.turn_flags_box = thorpy.Box(elements=[self.turn_flags_header_box, self.turn_flags_label_box])


		# # Player Flags

        # # used to track which initial placements the player has made        
        # self.num_initial_settlements = 2
        # self.num_initial_roads = 2
        # self.has_placed_initial_settlement = False
        # self.has_placed_initial_road = False

        # self.has_completed_initial_placement = False
        # self.initial_settlement = None
        # # used to determine the longest road
        # self.starting_roads = []
        # # the number of victory points
        # self.victory_points = 0
        # # the cards the player has
        # # each will be a number corresponding with the static variables CARD_<type>
        # self.cards = []
        # # the development cards this player has
        # self.dev_cards = []
        # # the number of knight cards the player has played
        # self.knight_cards = 0
        # # the longest road segment this player has
        # self.longest_road_length = 0
        # # whether the player has ended their turn
        # self.turn_over = True
        # # whether the player has a pending trade
        # self.pending_trade = False
        # # how many trades this player has requested in a turn
        # self.num_trades_in_turn = 0
        # # trading player
        # self.trading_player = None
        # # which card the trading player wants in trade
        # self.trade_forfeit_card = None
        # # which card the player will receive in trade
        # self.trade_receive_card = None
        # # number of cards the player must discard (from a 7 roll)
        # self.forfeited_cards_left = 0
        # # whether the player has played a road building dev card
        # self.played_road_building = False
        # # how many roads the player has left to place
        # self.roads_remaining = 0
        # # store the last bought dev card and the turn it was bought on 
        # self.last_bought_dev_card = 0
        # self.last_bought_dev_card_turn = 0

		curr_player = game.curr_player

		if(curr_player != None):

			self.curr_player_info_header = thorpy.make_text("CURR PLAYER INFO")

			self.player_label = thorpy.make_text("Player: " + PLAYER_COLORS[game.curr_player.num] + "(" + str(game.curr_player.num) + ")")
			self.agent_type_label = thorpy.make_text("Agent Type: " + str(curr_player.agent_type))

			self.has_placed_initial_settlement_label = thorpy.make_text("Placed init settlement: " + str(curr_player.has_placed_initial_settlement))
			self.has_placed_initial_road_label = thorpy.make_text("Placed initial road: " + str(curr_player.has_placed_initial_road))

			self.knight_cards_label = thorpy.make_text("Played knight cards: " + str(curr_player.knight_cards))
			self.longest_road_label = thorpy.make_text("Longest road: " + str(curr_player.longest_road_length))
			
			self.dev_cards_header = thorpy.make_text("Dev cards: ")
			self.road_building_dev_label = thorpy.make_text("Road Building: " + str(curr_player.dev_cards.count(DevCard.Road)))
			self.victory_point_dev_label = thorpy.make_text("Victory Point: " + str(curr_player.dev_cards.count(DevCard.VictoryPoint)))
			self.knight_card_dev_label = thorpy.make_text("Knight: " + str(curr_player.dev_cards.count(DevCard.Knight)))
			self.monopoly_dev_label = thorpy.make_text("Monopoly: " + str(curr_player.dev_cards.count(DevCard.Monopoly)))
			self.year_of_plenty_dev_label = thorpy.make_text("Year of Plenty: " + str(curr_player.dev_cards.count(DevCard.YearOfPlenty)))


			self.victory_points_label = thorpy.make_text("Victory points: " + str(curr_player.victory_points))
			


			self.allowed_actions_header_label = thorpy.make_text("Allowed Actions: ")

			if(game.allowed_actions):
				actions = ""
				for action in game.allowed_actions['allowed_actions']:
					actions += action_types[action]
				self.allowed_actions_label = thorpy.make_text(actions)
			else:
				self.allowed_actions_label = thorpy.make_text("None")

			self.curr_player_info_header_box = thorpy.Box(elements=[self.curr_player_info_header])
			self.curr_player_info_label_box = thorpy.Box(elements=[self.size_helper_one, self.player_label, self.agent_type_label, self.has_placed_initial_settlement_label,
			 self.has_placed_initial_road_label, self.knight_cards_label, self.longest_road_label, self.dev_cards_header, self.road_building_dev_label,
			 self.victory_point_dev_label, self.knight_card_dev_label, self.monopoly_dev_label, self.year_of_plenty_dev_label, self.victory_points_label, self.size_helper_two])
			self.curr_player_info_box = thorpy.Box(elements=[self.curr_player_info_header_box, self.curr_player_info_label_box])
			
			self.master_box = thorpy.Box(elements=[self.game_flags_box, self.turn_flags_box, self.curr_player_info_box])
		else:
			self.master_box = thorpy.Box(elements=[self.game_flags_box, self.turn_flags_box])


		# thorpy.store(self.master_box, mode="v", align="left")
		# self.master_box.fit_children()
		# self.master_box.refresh_lift()


		# self.master_box = thorpy.Draggable(elements=self.master_box)

		# self.menu = thorpy.Menu(self.master_box)
		#important : set the screen as surface for all elements
		for element in self.master_box.get_elements():
		    element.surface = self.screen
		#use the elements normally...
		self.master_box.set_topleft((600,50))

	def render(self):
		self.make_text(self.game)
		self.master_box.unblit()
		# self.box.update()


class VisualDisplay:

	def __init__(self):

		# An array of tiles, where the vertices of each exist in rendering surface space
		pg.init()
		self.screen = pg.display.set_mode((1280, 860), pg.SCALED | pg.RESIZABLE)
		pg.display.set_caption("CatanRL")
		# pg.mouse.set_visible(False)

		# self.control_surface = pg.Surface(self.screen.get_size())

		background = pg.Surface(self.screen.get_size())
		background = background.convert()
		background.fill((38, 13, 23))
		self.background = background
		self.clock = pg.time.Clock()
		# self.old_display = None

		self.info_display = None
		self.control_display = None

	def new_game(self, game):
		self.game = game
		self.hex_board = HexBoard(self.screen, self.game)
		self.info_display = InfoDisplay(self.screen, self.game)
		self.control_display = ControlDisplay(self.screen, self.game)


	def set_game(self, game):
		self.game = game
		self.hex_board.set_game(game)
		self.info_display.set_game(game)
		self.control_display.set_game(game)


	def render(self):
		self.hex_board.render()
		self.info_display.render()
		self.control_display.render()
		# self.control_display.menu.play()
		# print(self.game.board.tiles)

	def tick(self):
		self.clock.tick(45)

		# Handle Input Events
		for event in pg.event.get():
			# print(event)
			if event.type == pg.QUIT:
				exit()
			elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				exit()
			elif event.type == pg.VIDEORESIZE:
				# screen.blit(pygame.transform.scale(pic, event.dict['size']), (0, 0))
				pg.display.update()
			self.control_display.menu.react(event)


		self.screen.blit(self.background, (0, 0))
		self.render()
		pg.display.flip()
		


