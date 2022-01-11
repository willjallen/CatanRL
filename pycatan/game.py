import cProfile
import pstats
from pstats import SortKey


from pycatan.default_board import DefaultBoard
from pycatan.player import Player
from pycatan.statuses import Statuses
from pycatan.card import ResCard, DevCard
from pycatan.building import Building
from pycatan.harbor import Harbor
from human_agent import HumanAgent
from random_agent import RandomAgent
from display import Display

import random
import math

colors = ['Red', 'Cyan', 'Green', 'Yellow']

action_types = ["no_op", "roll", "purchase_resource", "purchase_and_play_building", "purchase_dev_card", "play_dev_card", "play_robber", "start_trade", "accept_trade", "deny_trade", "forfeit_cards", "end_turn", "initial_placement_road", "initial_placement_building", "place_road"]
NO_OP = 0
ROLL = 1
PURCHASE_RESOURCE = 2
PURCHASE_AND_PLAY_BUILDING = 3
PURCHASE_DEV_CARD = 4
PLAY_DEV_CARD = 5
PLAY_ROBBER = 6
START_TRADE = 7
ACCEPT_TRADE = 8
DENY_TRADE = 9
FORFEIT_CARDS = 10
END_TURN = 11
INITIAL_PLACE_ROAD = 12
INITIAL_PLACE_BUILDING = 13
PLACE_ROAD = 14


class Game:

    # initializes the  game
    def __init__(self, num_of_players=4, print_mode=False, user_mode=False, agent_type_arr=['R','R','R','R'], on_win=None, starting_board=False, headless=False):

        # Game properties
        # Number of players
        self.num_of_players = num_of_players
        
        # Use a display
        self.headless = False

        # Set if print statements are enabled
        self.print_mode = print_mode
        
        # Set in-person user mode
        self.user_mode = user_mode
        
        # Array of size num_of_players, determining which player is which agent type
        self.agent_type_arr = agent_type_arr

        # creates a board
        self.board = DefaultBoard(game=self);

        # Game Display Object
        if(not headless):
            self.display = Display(self)
        
        # creates players
        self.agents = []
        self.players = []
        for i in range(num_of_players):
            if(agent_type_arr[i] == 'H'):
                self.players.append(HumanAgent(num=i, game=self, agent_type=agent_type_arr[i]))
            if(agent_type_arr[i] == 'R'):
                self.players.append(RandomAgent(num=i, game=self, agent_type=agent_type_arr[i]))

        # Set onWin method
        self.on_win = on_win

        # creates a new Developement deck
        self.dev_deck = []
        for i in range(14):
            # Add 2 Road, Monopoly and Year of Plenty cards
            if i < 2:
                self.dev_deck.append(DevCard.Road)
                self.dev_deck.append(DevCard.Monopoly)
                self.dev_deck.append(DevCard.YearOfPlenty)
            # Add 5 Victory Point cards
            if i < 5:
                self.dev_deck.append(DevCard.VictoryPoint)
            # Add 14 knight cards
            self.dev_deck.append(DevCard.Knight)
        # Shuffle the developement deck
        random.shuffle(self.dev_deck)

        # the longest road owner and largest army owner
        self.longest_road_owner = None
        self.largest_army = None

        # whether the game is in initial placement mode
        self.initial_placement_mode = False
        self.initial_placement_ended = False
        # Set initial placement mode flag
        self.give_initial_yield = False
        
        # Play order
        self.set_initial_placement_play_order()

        # Initialization Vars
        self.initial_player_index = 0
        # Set initial placement mode flag
        self.initial_placement_mode = True
        self.give_initial_yield = False

        self.initial_placement_curr_player_index = 0

        # whether the game has finished or not
        self.has_ended = False

        # whether a player can roll
        self.can_roll = False

        # Current roll
        self.last_roll = 0

        # whether a rolled 7 is in effect
        self.rolled_seven = False

        # whether robber has been moved yet after rolling a 7
        self.robber_moved = True

        self.allowed_actions = []
        self.full_action = []

        # Turn counter
        self.turn_counter = 0

        self.player_with_turn = None
        self.player_with_turn_index = 0

        self.curr_player = None
        self.curr_player_index = 0


        self.turn_over = False

        self.game_over = False
        self.cycle_complete = False   
        self.player_index = 0



        self.init = True



    def set_initial_placement_play_order(self):
        ''''
            Sets a random initial starting order
            Args:                        
        '''

        self.initial_placement_play_order = []

        player_index = chosen_player = random.randint(0, self.num_of_players-1)

        # Starting placements
        # 8 total turns, 2 placements per player
        # Snake means: 0, 1, 2, 3, 3, 2, 1, 0

        switch = False
        for i in range(0, self.num_of_players * 2):
            # Done three times:
            # Twice for playing settlement and road in the same turn, a third time to end turn
            self.initial_placement_play_order.append(player_index)
            self.initial_placement_play_order.append(player_index)
            self.initial_placement_play_order.append(player_index)

            if(not i == self.num_of_players-1):
                if(not switch):
                    if(player_index == self.num_of_players-1):
                        player_index = 0
                    else:
                        player_index += 1
                else:
                    if(player_index == 0):
                        player_index = self.num_of_players-1
                    else:
                        player_index -= 1
            else:
                switch = True



    def set_play_order(self):
        ''''
            Determine a random play order
            Args:

            Returns: starting_play_order
                arr of size 4 denoting indices of players in snake order
        '''

        self.play_order = []


        player_index = self.initial_placement_play_order[0]

        for i in range(0, self.num_of_players):
            self.play_order.append(player_index)
            if(player_index == self.num_of_players-1):
                player_index = 0
            else:
                player_index += 1


    def set_next_turn_player(self):


        if(self.player_with_turn_index == self.num_of_players-1):
            self.player_with_turn_index = 0
        else:
            self.player_with_turn_index += 1

        self.player_with_turn = self.players[self.play_order[self.player_with_turn_index]]


    def set_next_curr_player(self):

        if(self.curr_player_index == self.num_of_players-1):
            self.curr_player_index = 0
        else:
            self.curr_player_index += 1

        self.curr_player = self.players[self.play_order[self.curr_player_index]]

    def add_initial_placement_yield(self):
        ''''
                When the game begins, add resources of all tiles that player initially settled on
                Args:

                Returns: 
        '''
        for i in range(2, 13):
            if i != 7:
                self.board.add_yield(i)


    def step(self):

        ## INITIAL PLACEMENT PHASE ##
        '''
        During the initial phase of the game, a random player is selected to begin by choosing a location
        for a settlement and an attached road. The procress iterates through all the players exactly twice 
        by means of snake order [0,1,2,3,3,2,1,0] or [2,3,0,1,1,0,3,2] 
        '''

        if(self.initial_placement_mode):


            # if(self.print_mode):
            #     print('Starting play order: ')
            #     print(starting_play_order)

            # Set the current player
            if(self.print_mode):
                print(self.players)
                print(self.initial_placement_curr_player_index)
                print(self.initial_placement_play_order)
            self.player_with_turn = self.curr_player = self.players[self.initial_placement_play_order[self.initial_placement_curr_player_index]]


            if(self.print_mode):
                self.display.displayBoard()
                self.display.printBlankLines(8)
                print('Player with turn: ' + colors[self.curr_player.num])

            self.allowed_actions = self.get_allowed_actions(self.curr_player)
            self.full_action = self.curr_player.do_turn(allowed_actions)

            self.do_action(self.curr_player, self.full_action)

            self.initial_placement_curr_player_index += 1

            if(self.turn_over):
                self.turn_over = False

                self.curr_player.has_placed_initial_settlement = False
                self.curr_player.has_placed_initial_road = False

                if(self.initial_placement_curr_player_index == self.num_of_players * 3 * 2):
                    # Each player has placed a settlement, road and ended their turn twice
                    # Initial placement mode is over
                    self.initial_placement_mode = False

                    # Add initial yields
                    self.add_initial_placement_yield()

                    # Set play order
                    self.set_play_order()


            return





        ## MAIN GAME LOOP ##

        # # Set the current player
        # self.curr_player = self.players[player_index]

        # Get allowed actions from player 
        self.allowed_actions = self.get_allowed_actions(self.curr_player)

        # If the only allowed action is no_op, we can skip to the next loop
        if(len(allowed_actions['allowed_actions']) == 1 and NO_OP in allowed_actions['allowed_actions']):
            self.set_next_curr_player()
            return
        #     #TODO

        if(self.print_mode):
            self.display.displayBoard()
            self.display.displayGameInfo()
            self.display.displayPlayerGameInfo(self.curr_player)

        if(self.print_mode):
            print('Allowed Actions')
            actions = [action_types[x] for x in allowed_actions['allowed_actions']]
            print(actions)

        # Agent conducts its turn and produces actions
        # TODO: self.full_action?
        self.full_action = self.curr_player.do_turn(allowed_actions)

        #     print('Allowed Actions')
        #     print(allowed_actions['allowed_actions'])
        if(self.print_mode):
            print('Full action:')
            print(self.full_action)
            print(action_types[self.full_action[0]])
            for i in self.full_action:
                if(isinstance(i, Player)):
                    print('player: ' + str(i.num))

        # Set post action state
        
        # Game registers the action
        self.do_action(self.curr_player, self.full_action)

        self.set_longest_road()
        if(self.rolled_seven):
                self.rolled_seven = False
                self.robber_moved = False
                for p in self.players:
                    if(len(p.cards) >= 8):
                        # print('player', p.num)
                        # print(p.cards)
                        # print(len(p.cards))
                        # print()
                        p.forfeited_cards_left = math.floor(len(p.cards)/2)



        
        # Win condition
        if(self.player_with_turn.get_VP(True) >= 10):
            self.has_ended = True
            self.winner = self.player_with_turn
            self.player_with_turn.turn_over = True
            print('Winner: ' + str(colors[self.winner.num]))

   
        if(self.turn_over):
            self.turn_counter += 1

            self.set_next_turn_player()
            self.curr_player_index = self.player_with_turn_index
            self.player_with_turn.num_trades_in_turn = 0

            self.can_roll = True
            self.rolled_seven = False
            self.turn_over = False
        else:
            self.set_next_curr_player()



        # Cycle over all players per turn steps to allow for responses to trades
        # self.turn_counter = 0
        # self.game_over = False
        # self.turn_over = False
        # self.cycle_complete = False        

        # Reset roll
        # self.can_roll = True

        # Iterate to next player with turn
        # self.curr_player = self.players[player_index]
        # self.player_with_turn = curr_player
        # self.player_with_turn_index = player_index
        # self.player_with_turn.turn_over = turn_over = False

        # Reset number of trades the player has conducted

        # Cycle, starting with the player playing their turn, through all other players



        # If the player only has one available action, and that action is NO_OP
        # Skip their step
        # if(len(allowed_actions['allowed_actions']) == 1 and (NO_OP in allowed_actions['allowed_actions'])):
        #     action_okay = True
        #     continue


        # Save Game state 








        # Pause
        # if(self.user_mode):
        #     response = input("type anything to continue")


             # Display turn relevant info
            # self.display.displayBoard()
            # print('Turn: ' + str(self.turn_counter))
            # print('Player with turn: ' + colors[self.player_with_turn_index])
            # print('Roll: ' + str(self.roll))
            # print()






    def run(self):

        # Set up the game
        if(not self.init):
            self.setup()

        player_index = self.initial_player_index

        # Game Loop

        # Initial Placements loop
        # in this loop, we



        # Cycle over all players per turn steps to allow for responses to trades
        self.turn_counter = 0
        game_over = False
        turn_over = False
        cycle_complete = False        
        while(not self.has_ended):
            # Reset roll
            self.can_roll = True

            # Iterate to next player with turn
            curr_player = self.players[player_index]
            self.player_with_turn = curr_player
            self.player_with_turn_index = player_index
            self.player_with_turn.turn_over = turn_over = False

            # Reset number of trades the player has conducted
            self.player_with_turn.num_trades_in_turn = 0

            # Cycle, starting with the player playing their turn, through all other players
            while(not turn_over):

                curr_player = self.players[player_index]

                # Check if the action taken is valid 
                action_okay = False
                while(not action_okay):

                    allowed_actions = self.get_allowed_actions(curr_player)

                    # If the player only has one available action, and that action is NO_OP
                    # Skip their step
                    if(len(allowed_actions['allowed_actions']) == 1 and (NO_OP in allowed_actions['allowed_actions'])):
                        action_okay = True
                        continue

                    if(self.print_mode):
                        self.display.displayBoard()
                        self.display.displayGameInfo()
                        self.display.displayPlayerGameInfo(curr_player)

                    # Save Game state 


                    full_action = curr_player.do_turn(allowed_actions)



                    if(self.print_mode):
                        print('Allowed Actions')
                        print(allowed_actions['allowed_actions'])
                        print('Full action:')
                        print(full_action)
                        print(action_types[full_action[0]])
                        for i in full_action:
                            if(isinstance(i, Player)):
                                print('player: ' + str(i.num))




                    status = self.do_action(curr_player, full_action)

                    self.set_longest_road()

                    if status == Statuses.ALL_GOOD:
                        action_okay = True
                    elif status == Statuses.ROLLED_SEVEN:
                        self.rolled_seven = True
                        self.robber_moved = False
                        for p in self.players:
                            if(len(p.cards) >= 8):
                                # print('player', p.num)
                                # print(p.cards)
                                # print(len(p.cards))
                                # print()
                                p.forfeited_cards_left = math.floor(len(p.cards)/2)
                    else:
                        if(self.print_mode):
                            print('Error: ')
                            print(Statuses.status_list[int(status)])

                    # If the player still has cards to forfeit, stay on this player
                    if(curr_player.forfeited_cards_left > 0):
                        action_okay = False

                    # Pause
                    if(self.user_mode):
                        response = input("type anything to continue")

                if(self.player_with_turn.get_VP(True) >= 10):
                    self.has_ended = True
                    self.winner = self.player_with_turn
                    self.player_with_turn.turn_over = True

                     # Display turn relevant info
                    self.display.displayBoard()
                    print('Turn: ' + str(self.turn_counter))
                    print('Player with turn: ' + colors[self.player_with_turn_index])
                    print('Roll: ' + str(self.roll))
                    print()


                turn_over = self.player_with_turn.turn_over 
                self.rolled_seven = False
                if(not turn_over):
                    # 2 -> 3 -> 0 -> 1 -> 2
                    if(player_index == 3):
                        player_index = 0
                    else:
                        player_index += 1


            # Turn has ended
            player_index = self.player_with_turn_index
            self.turn_counter += 1


            # 2 -> 3 -> 0 -> 1 -> 2
            if(player_index == 3):
                player_index = 0
            else:
                player_index += 1

        print('Winner: ' + str(colors[self.winner.num]))

    def do_action(self, player, args):
        action_type = args[0]

        # No op
        if(action_type == NO_OP):
            return Statuses.ALL_GOOD
        # Roll
        if(action_type == ROLL):
            if(self.can_roll):
                self.last_roll = roll = self.get_roll()
                self.can_roll = False
                if(roll != 7):
                    self.board.add_yield(roll)
                else:
                    self.rolled_seven = True
                return Statuses.ALL_GOOD
            else:
                return Statuses.ERR_ROLL
        # Purchase Resource
        if(action_type == PURCHASE_RESOURCE):
            requested_resource = args[1]
            forfeited_resource = args[2]
            status = self.trade_to_bank(player, forfeited_resource, requested_resource)
            return status

        # Purchase & play building
        if(action_type == PURCHASE_AND_PLAY_BUILDING):
            building_response = args[1]
            loc_r_response = args[2]
            loc_i_response = args[3]
            if(building_response == 0):
                status = player.build_settlement(self.board.points[loc_r_response][loc_i_response])
            if(building_response == 1):
                loc_r_response_2 = args[4]
                loc_i_response_2 = args[5]     
                status = player.build_road(self.board.points[loc_r_response][loc_i_response], self.board.points[loc_r_response_2][loc_i_response_2])
            if(building_response == 2):
                status = self.add_city(self.board.points[loc_r_response][loc_i_response], player)
            return status

        # Purchase dev card
        if(action_type == PURCHASE_DEV_CARD):
            status_and_card = self.build_dev(player.num)
            player.last_bought_dev_card = status_and_card[0] 
            return status_and_card[1]

        # Play Dev Card
        if(action_type == PLAY_DEV_CARD):
            dev_card_response = args[1]

            if(dev_card_response == DevCard.Road.value):
                player.played_road_building = True
                player.roads_remaining = 2
                player.remove_dev_card(DevCard.Road)

            if(dev_card_response == DevCard.Knight.value):
                loc_x_response = args[2]
                loc_y_response = args[3]
                victim_player_response = args[4]

                status = self.use_dev_card(player.num, DevCard.Knight, {'robber_pos': [loc_x_response, loc_y_response], 'victim': victim_player_response})
                return status

            if(dev_card_response == DevCard.Monopoly.value):
                resource_response = args[2]

                status = self.use_dev_card(player.num, DevCard.Monopoly, {'card_type': ResCard(resource_response)})
                return status

            if(dev_card_response == DevCard.YearOfPlenty.value):
                first_resource_response = args[2]
                second_resource_response = args[3]


                status = self.use_dev_card(player.num, DevCard.YearOfPlenty, {'card_one': ResCard(first_resource_response), 'card_two': ResCard(second_resource_response)})
                return status
        # Play robber
        if(action_type == PLAY_ROBBER):
            loc_x_response = args[1]
            loc_y_response = args[2]
            victim_player_response = args[3]

            status = self.move_robber(self.board.tiles[loc_x_response][loc_y_response], player.num, victim_player_response)
            self.robber_moved = True
            return status

        # Do trade
        if(action_type == START_TRADE):
            player.num_trades_in_turn += 1
            # Which player
            other_player = args[1]
            player_forfieted_resource = args[2]
            player_received_resource = args[3]

            other_player.trading_player = player
            other_player.pending_trade = True
            other_player.trade_forfeit_card = player_received_resource
            other_player.trade_receive_card = player_forfieted_resource


        # Accept Trade
        if(action_type == ACCEPT_TRADE):
            status = self.trade(player.num, player.trading_player.num, [player.trade_forfeit_card], [player.trade_receive_card])
            player.pending_trade = False
            return status
        # Deny trade
        if(action_type == DENY_TRADE):
            player.pending_trade = False

        # Forfeit cards
        if(action_type == FORFEIT_CARDS):
            player.remove_cards([args[1]])
            player.forfeited_cards_left -= 1

        # End turn
        if(action_type == END_TURN):
            player.turn_over = True
            self.turn_over = True
            return Statuses.ALL_GOOD

        # Initial placements
        # Road
        if(action_type == INITIAL_PLACE_ROAD):
            loc_r_response = args[1]
            loc_i_response = args[2]     
            loc_r_response_2 = args[3]
            loc_i_response_2 = args[4]     
            status = player.build_road(self.board.points[loc_r_response][loc_i_response], self.board.points[loc_r_response_2][loc_i_response_2], is_starting=True)
            player.has_placed_initial_road = True

        # Building
        if(action_type == INITIAL_PLACE_BUILDING):
            loc_r_response = args[1]
            loc_i_response = args[2]
            status = player.build_settlement(self.board.points[loc_r_response][loc_i_response], is_starting=True)
            player.has_placed_initial_settlement = True
            player.initial_settlement = self.board.points[loc_r_response][loc_i_response]

        # Road building 
        if(action_type == PLACE_ROAD):
            loc_r_response = args[1]
            loc_i_response = args[2]     
            loc_r_response_2 = args[3]
            loc_i_response_2 = args[4]     
            status = player.build_road(self.board.points[loc_r_response][loc_i_response], self.board.points[loc_r_response_2][loc_i_response_2], is_starting=True)
            if(player.roads_remaining > 0):
                player.roads_remaining -= 1
            else:
                player.played_road_building = False

        return Statuses.ALL_GOOD




    # Get allowed actions
    def get_allowed_actions(self, player):
        actions = {
        'allowed_actions': [],
        'allowed_forfeit_cards': [],
        'allowed_bank_trade_cards': [],
        'allowed_dev_cards': [],
        'allowed_buildings': [],
        'allowed_robber_tiles': [],
        'allowed_road_point_pairs': [],
        'allowed_intial_settlement_points': [], 
        'allowed_settlement_points': [], 
        'allowed_city_points': [],
        'allowed_victim_players': [],
        'allowed_trade_pairs': [],
        'allowed_trade_partners': [],
        'allowed_trade_forfeit_cards': [],
        'allowed_trade_partner_forfeit_cards': []
        }

        is_players_turn = (player.num == self.player_with_turn.num)


        ## INITIAL_PLACEMENT (Priority action, others ignored)
        # - It is players turn
        # - initial_placement_mode is true
        if(is_players_turn and self.initial_placement_mode):
            if(player.has_placed_initial_settlement and player.has_placed_initial_road):
                actions['allowed_actions'].append(END_TURN)
                return actions
            if(player.num_initial_settlements > 0 and not player.has_placed_initial_settlement):
                actions['allowed_actions'].append(INITIAL_PLACE_BUILDING)
                actions['allowed_settlement_points'] = player.get_available_initial_settlement_points()
            if(player.num_initial_roads > 0 and player.has_placed_initial_settlement and not player.has_placed_initial_road):
                actions['allowed_actions'].append(INITIAL_PLACE_ROAD)
                actions['allowed_road_point_pairs'] = player.get_available_initial_road_point_pairs()

            return actions


        ## PLACE_ROAD (Priority action, others ignored)
        if(player.played_road_building and player.roads_remaining > 0):
            actions['allowed_road_point_pairs'] = player.get_available_road_point_pairs()

            if(actions['allowed_road_point_pairs']):
                actions['allowed_actions'].append(PLACE_ROAD)
                return actions
        ## FORFEIT_CARDS (Priority action, others ignored)
        # - A 7 is active player has cards left to forfeit
        if(player.forfeited_cards_left > 0):
            actions['allowed_actions'].append(FORFEIT_CARDS)
            actions['allowed_forfeit_cards'] = player.get_types_of_cards_possessed()
            # print(actions['allowed_forfeit_cards'])
            # print(player.cards)
            return actions

        ## PLAY_ROBBER (Priority action, others ignored)
        # - It is the players turn
        # - A 7 is active and robber has not been moved
        if(is_players_turn and not self.robber_moved):
            actions['allowed_actions'].append(PLAY_ROBBER)
            possible_robber_tiles_and_victims = player.get_available_robber_placement_tiles_and_victims()
            actions['allowed_robber_tiles'] = possible_robber_tiles_and_victims
            actions['allowed_victim_players'] = possible_robber_tiles_and_victims
            return actions

        ## ACCEPT_TRADE (Priority action, others ignored)
        ## DENY_TRADE
        # - Player has a pending trade
        if(player.pending_trade):
            actions['allowed_actions'].append(ACCEPT_TRADE)
            actions['allowed_actions'].append(DENY_TRADE)
            return actions

        ## NO_OP
        # - It is not the player's turn
        # - There are no pending trades
        if(not is_players_turn and not player.pending_trade):
            actions['allowed_actions'].append(NO_OP)
            return actions

        ## PLAY_DEV_CARD
        # - It is the players turn
        # - Player has at least one development card
        if(is_players_turn):
            playable_dev_card = False
            for card in DevCard:
                if(card in player.dev_cards):
                    # Check for playing purchased dev card on the same turn
                    sameTurn = False
                    if(card == player.last_bought_dev_card):
                        if(len([x for x in player.dev_cards if x == card]) <= 2):
                            sameTurn = True

                    if(not sameTurn):
                        if(card == DevCard.Knight or card == DevCard.YearOfPlenty or card == DevCard.Monopoly or card == DevCard.Road):
                            actions['allowed_dev_cards'].append(card)
                            playable_dev_card = True

                        if(card == DevCard.Knight):
                            possible_robber_tiles_and_victims = player.get_available_robber_placement_tiles_and_victims()
                            actions['allowed_robber_tiles'] = possible_robber_tiles_and_victims
                            actions['allowed_victim_players'] = possible_robber_tiles_and_victims
                            # print('possible vitctims:', possible_robber_tiles_and_victims)
            if(playable_dev_card):
                actions['allowed_actions'].append(PLAY_DEV_CARD)

        ## ROLL (Priority action, others (except play dev card) ignored)
        # - It is the players turn
        # - The dice has not been rolled
        if(is_players_turn and self.can_roll):
            actions['allowed_actions'].append(ROLL)
            return actions

        ## PURCHASE_RESOURCE
        # - It is the players turn
        # - The dice has been rolled
        # - Player can exchange resource
        if(is_players_turn and not self.can_roll):
            # Check every resource and append those which are eligable
            cards = self.cards_tradable_to_bank(player)
            if cards:
                # card_types = [card[0] for card in cards] 
                # card_nums = [card[1] for card in cards] 
                card_tuples = [(card[0], card[1]) for card in cards]
                actions['allowed_actions'].append(PURCHASE_RESOURCE)
                for card in cards:
                    actions['allowed_bank_trade_cards'].append(card)



            #self.can_trade_to_bank(player, cards, request)

        ## PURCHASE_AND_PLAY_BUILDING
        # - It is the players turn
        # - The dice has been rolled                
        # - Player has relevant cards
        if(is_players_turn and not self.can_roll):
            available_buildings = player.get_available_buildings()

            if(available_buildings):
                if(Building.BUILDING_SETTLEMENT in available_buildings):
                    settlement_points = player.get_available_settlement_points()
                    actions['allowed_settlement_points'] = settlement_points

                    if(settlement_points):
                        if not(Building.BUILDING_SETTLEMENT in actions['allowed_buildings']):
                            actions['allowed_actions'].append(PURCHASE_AND_PLAY_BUILDING)
                            actions['allowed_buildings'].append(Building.BUILDING_SETTLEMENT)

                if(Building.BUILDING_ROAD in available_buildings):
                    available_road_pairs = player.get_available_road_point_pairs()
                    actions['allowed_road_point_pairs'] = available_road_pairs


                    if(available_road_pairs):
                        if not(Building.BUILDING_ROAD in actions['allowed_buildings']):
                            if not(PURCHASE_AND_PLAY_BUILDING in actions['allowed_actions']):
                                actions['allowed_actions'].append(PURCHASE_AND_PLAY_BUILDING)
                            actions['allowed_buildings'].append(Building.BUILDING_ROAD)


                if(Building.BUILDING_CITY in available_buildings):
                    available_cities = player.get_available_upgrade_points()
                    actions['allowed_city_points'] = available_cities
                    if(available_cities):
                        if not(Building.BUILDING_CITY in actions['allowed_buildings']):
                            if not(PURCHASE_AND_PLAY_BUILDING in actions['allowed_actions']):
                                actions['allowed_actions'].append(PURCHASE_AND_PLAY_BUILDING)
                            actions['allowed_buildings'].append(Building.BUILDING_CITY)                                


        ## PURCHASE_DEV_CARD
        # - It is the players turn
        # - The dice has been rolled                
        # - Player has relevant cards
        if(is_players_turn and player.can_build_dev()==Statuses.ALL_GOOD and not self.can_roll):
            actions['allowed_actions'].append(PURCHASE_DEV_CARD)


        ## START_TRADE
        # - It is the players turn
        # - Player has attempted 4 or less trades this turn
        # - Player actually has the card they are forfeiting
        # - Receiving player actually has the card they are forfeiting 
        if(is_players_turn and player.num_trades_in_turn < 4):

            player_card_types = player.get_types_of_cards_possessed()

            if(player_card_types):
                for other_player in self.players:
                    if(other_player == player):
                        continue

                    card_pairs = []

                    # If other player has any cards
                    if(other_player.cards):
                        # Iterate through all card types available to player
                        for card in player_card_types:
                            # Get all card types available to other player
                            other_player_forfeit_cards = other_player.get_types_of_cards_possessed()

                            # Remove duplicate card (prevent trading sheep for sheep)
                            if card in other_player_forfeit_cards:
                                other_player_forfeit_cards.remove(card)
                                # If the other player still has cards to forfeit after this
                            if(other_player_forfeit_cards):
                                card_pairs.append((card, other_player_forfeit_cards))
                    if(card_pairs):                   
                        actions['allowed_trade_partners'].append(other_player)
                        actions['allowed_trade_pairs'].append((other_player.num, card_pairs))

            if(len(actions['allowed_trade_partners']) > 0):
                actions['allowed_actions'].append(START_TRADE)

        ## END_TURN
        # - It is the players turn
        # - The dice has been rolled                
        if(is_players_turn and not self.can_roll):
            actions['allowed_actions'].append(END_TURN)

        return actions

    # creates a new settlement belong to the player at the coodinates
    def add_settlement(self, player, point, is_starting=False):
        # builds the settlement
        status = self.players[player].build_settlement(point=point, is_starting=is_starting)
        # If successful, check if the player has now won
        if status == Statuses.ALL_GOOD:
            if self.players[player].get_VP() >= 10:
            # End the game
                self.has_ended = True
                self.winner = player

        return status

    # builds a road going from point start to point end
    def add_road(self, player, start, end, is_starting=False):
        # builds the road
        stat = self.players[player].build_road(start=start, end=end, is_starting=is_starting)
        # checks for a new longest road segment
        self.set_longest_road()
        # returns the status
        return stat

    # builds a new developement cards for the player
    def build_dev(self, player):

        status = self.players[player].can_build_dev()
        if(status != Statuses.ALL_GOOD):
            return status

        needed_cards = [
        ResCard.Wheat,
        ResCard.Sheep,
        ResCard.Ore
        ]
        # removes the cards
        self.players[player].remove_cards(needed_cards)
        # gives the player a dev card
        dev_card = self.dev_deck[0]
        self.players[player].add_dev_card(dev_card)
        # removes that dev card from the deck
        del self.dev_deck[0]

        return (dev_card, Statuses.ALL_GOOD)

    # gives players the proper cards for a given roll
    def add_yield_for_roll(self, roll):
        self.board.add_yield(roll)

    def can_trade(self, player_one, player_two, cards_one, cards_two):
        # check if they players have the cards they are trading
        # Needs to do this before deleting because one might have the cards while the other does not
        if not self.players[player_one].has_cards(cards_one):
            return Statuses.ERR_CARDS

        elif not self.players[player_two].has_cards(cards_two):
            return Statuses.ERR_CARDS
        return Statuses.ALL_GOOD


    # trades cards (given in an array) between two players
    def trade(self, player_one, player_two, cards_one, cards_two):
        # status = self.can_trade(player_one, player_two, cards_one, cards_two)
        status = Statuses.ALL_GOOD
        if(status != Statuses.ALL_GOOD):
            return status
        else:
            # removes the cards
            self.players[player_one].remove_cards(cards_one)
            self.players[player_two].remove_cards(cards_two)
            # add the new cards
            self.players[player_one].add_cards(cards_two)
            self.players[player_two].add_cards(cards_one)
            return Statuses.ALL_GOOD

    # moves the robber
    # Note that player is the player moving the robber
    # and victim is the player whose card is being taken
    def move_robber(self, tile, player, victim):
        # checks the player wants to take a card from somebody
        if victim != None:
            # checks the victim has a settlement on the tile
            has_settlement = False
            # Iterate over points and check if there is a settlement/city on any of them
            points = tile.points
            for p in points:
                if p != None and p.building != None:
                # print(p.building.owner)
                # Check the victim owns the settlement/city
                    if p.building.owner == victim:
                        has_settlement = True

            if not has_settlement:
                return Statuses.ERR_INPUT

        # moves the robber
        self.board.move_robber(tile)
        # takes a random card from the victim
        if victim != None:
            # removes a random card from the victim
            index = round(random.random() * (len(self.players[victim].cards) - 1))
            card = self.players[victim].cards[index]
            self.players[victim].remove_cards([card])
            # adds it to the player
            self.players[player].add_cards([card])

        return Statuses.ALL_GOOD

    def cards_tradable_to_bank(self, player):
        tradable_cards = []

        harbor_types = self.players[player.num].get_connected_harbor_types()

        has_3_1_harbor = False
        two_one_harbors = []


        for card_type in ResCard:
            for h_type in harbor_types:
                if Harbor.get_card_from_harbor_type(h_type) == card_type.value:
                    two_one_harbors.append(card_type)
                elif Harbor.get_card_from_harbor_type(h_type) == None:
                    has_3_1_harbor = True


        for card_type in ResCard:
            if(card_type in two_one_harbors):
                if(player.has_at_least_num_cards(card_type, 2)):
                    tradable_cards.append([card_type, 2])
            elif(has_3_1_harbor):
                if(player.has_at_least_num_cards(card_type, 3)):
                    tradable_cards.append([card_type, 3])
            elif(player.has_at_least_num_cards(card_type, 4)):
                tradable_cards.append([card_type, 4])

        return tradable_cards                    


    # trades cards from a player to the bank
    # either by 4 for 1 or using a harbor
    def trade_to_bank(self, player, card, request):
        tradable_cards_with_values = self.cards_tradable_to_bank(player)

        found = False
        num = 0

        if tradable_cards_with_values:
            for i in range(0, len(tradable_cards_with_values)):
                if(tradable_cards_with_values[i][0] == ResCard(card)):
                    found = True
                    num = tradable_cards_with_values[i][1]

        if(not found):
            return Statuses.ERR_CARDS


        cards = [ResCard(card)] * num 
        # removes cards
        self.players[player.num].remove_cards(cards)
        # adds the new card
        self.players[player.num].add_cards([ResCard(request)])

        return Statuses.ALL_GOOD

    # gives the longest road to the correct player
    def set_longest_road(self):
        # The length of the current longest road segment
        longest = 0
        owner = self.longest_road_owner

        for p in self.players:
            # longest road needs to be longer than anbody else's
            # and at least 5 road segments long
            if p.longest_road_length > longest and p.longest_road_length >= 5:
                longest = p.longest_road_length
                owner = self.players.index(p)

        self.longest_road_owner = owner
        # # checks if the player has won now that they has longest road
        # if self.players[owner].get_VP() >= 10:
        #     self.has_ended = True
        #     self.winner = owner

    # changes a settlement on the board for a city
    def add_city(self, point, player):
        status = self.board.upgrade_settlement(player.num, point)

        if status == Statuses.ALL_GOOD:
            # checks if the player won
            if self.players[player.num].get_VP() >= 10:
                self.winner = player

        return status

    # uses a developement card
    # the required args will vary between different dev cards
    def use_dev_card(self, player, card, args):
        # checks the player has the development card
        if not self.players[player].has_dev_cards([card]):
            return Statuses.ERR_CARDS

        # applies the action
        if card == DevCard.Road:
            # checks the correct arguments are given
            road_names = [
                    "road_one",
                    "road_two"
            ]
            for r in road_names:
                if not r in args:
                    return Statuses.ERR_INPUT

                else:
                    # Check the roads have a start and an end
                    if not "start" in args[r] or not "end" in args[r]:
                        return Statuses.ERR_INPUT

            # checks the road location is valid

            # whether the other road is completely isolated but is connected to this road
            other_road_is_isolated = False

            for r in road_names:
                location_status = self.players[player].road_location_is_valid(args[r]['start'], args[r]['end'])

                # if the road location is not OK
                # since the player can build two roads, some
                # locations that would be invalid are valid depending on the other road location
                if not location_status == Statuses.ALL_GOOD:
                    # checks if it is isolated, but would be connected to the other road
                    if location_status == Statuses.ERR_ISOLATED:
                        # if the other road is also isolated, just return an error
                        if other_road_is_isolated:
                            return location_status

                        # checks if the two roads are connected
                        # (since the other one is connected, this road is connected through it)
                        road_points = [
                                "start",
                                "end"
                        ]
                        roads_are_connected = False
                        for p_one in road_points:
                            for p_two in road_points:
                                if args["road_one"][p_one] == args['road_two'][p_two]:
                                    other_road_is_isolated = True
                                    # doesn't return an isolated error
                                    roads_are_connected = True

                        if not roads_are_connected:
                            return location_status
                    else:
                        return location_status

            # builds the roads
            for r in road_names:
                self.board.add_road(Building(point_one=args[r]["start"], point_two=args[r]["end"], owner=player, type=Building.BUILDING_ROAD))

            return Statuses.ALL_GOOD

        elif card == DevCard.Knight:
            # checks there are the right arguments
            if not ("robber_pos" in args and "victim" in args):
                return Statuses.ERR_INPUT

            # checks the victim input is valid
            if args["victim"] != None:
                if args["victim"] < 0 or args["victim"] >= len(self.players) or args["victim"] == player:
                    return Statuses.ERR_INPUT

            # moves the robber
            result = self.move_robber(tile=self.board.tiles[args["robber_pos"][0]][args["robber_pos"][1]], player=player, victim=args["victim"])

            if result != Statuses.ALL_GOOD:
                return result

            # adds one to the player's knight count
            (self.players[player]).knight_cards += 1

            # checks for the largest army
            if self.largest_army == None:
                # if nobody has the largest army, the player needs at least 3 cards
                if self.players[player].knight_cards >= 3:
                    self.largest_army = player

            else:
                # the player needs to have more than anybody else
                current_longest = self.players[self.largest_army].knight_cards

                if self.players[player].knight_cards > current_longest:
                    self.largest_army = player

        elif card == DevCard.Monopoly:
            # gets the type of card
            card_type = args['card_type']
            # for each player, checks if they have the card
            for p in self.players:
                if p.has_cards([card_type]):
                    # gets how many this player has
                    number_of_cards = p.cards.count(card_type)
                    cards_to_give = [card_type] * number_of_cards
                    # removes the cards
                    p.remove_cards(cards_to_give)
                    # adds them to the user's cards
                    self.players[player].add_cards(cards_to_give)

        elif card == DevCard.VictoryPoint:
            # players do not play developement cards, so it returns an error
            return Statuses.ERR_INPUT

        elif card == DevCard.YearOfPlenty:
            # checks the player gave two development cards
            if not 'card_one' in args and not 'card_two' in args:
                return Statuses.ERR_INPUT

            # gives the player 2 resource cards of their choice
            self.players[player].add_cards([
                    args['card_one'],
                    args['card_two']
            ])

        else:
            # error here
            return Statuses.ERR_INPUT

        # removes the card
        self.players[player].remove_dev_card(card)

        return Statuses.ALL_GOOD

    # simulates 2 dice rolling
    def get_roll(self):
        return (random.randint(1, 6) + random.randint(1, 6))

