from pycatan import Game
from pycatan import Statuses
from pycatan import Building
from pycatan.card import ResCard, DevCard
from board_renderer import BoardRenderer
from agent import Agent
from random_agent import RandomAgent
import random

colors = ['Red', 'Cyan', 'Green', 'Yellow']

action_types = ["no_op", "roll", "purchase_resource", "purchase_and_play_building", "purchase_dev_card", "play_dev_card", "play_robber", "start_trade", "accept_trade", "deny_trade", "forfeit_cards", "end_turn", "initial_placement_road", "initial_placement_building"]
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

def printBlankLines(num):
        for i in range(0, num):
                print()


class GameWrapper:
    def __init__(self):
        self.num_of_players = 0
        self.game = None
        self.boardRenderer = None
        self.agents = []

    def setup(self):
        # Game Set-up questions
        print('Manual Mode (y/n)')
        #manual_mode = input()
        
        #print('Number of players (2-4)')
        # Might just cap this at 4 for training
        # num_players = int(input())
        
        num_players = 4
        game = Game(num_players)
        self.game = game
        self.boardRenderer = BoardRenderer(game.board, [50, 10])
        
        # Other stuff here  
        # Maybe a manual board input, but thats sounds lame rn

        # Init
        debug = True
        if debug:
                # self.game.add_settlement(player=0, point=self.game.board.points[0][0], is_starting=True)                
                # self.game.add_settlement(player=0, point=self.game.board.points[1][2], is_starting=True)
                # self.game.add_settlement(player=1, point=self.game.board.points[3][3], is_starting=True)
                # self.game.add_settlement(player=1, point=self.game.board.points[2][6], is_starting=True)
                # self.game.add_settlement(player=2, point=self.game.board.points[4][3], is_starting=True)
                # self.game.add_settlement(player=2, point=self.game.board.points[3][8], is_starting=True)
                # self.game.add_settlement(player=3, point=self.game.board.points[4][6], is_starting=True)
                # self.game.add_settlement(player=3, point=self.game.board.points[1][6], is_starting=True)
                # # Add some roads
                # self.game.add_road(player=0, start=self.game.board.points[0][0], end=self.game.board.points[0][1], is_starting=True)
                # self.game.add_road(player=0, start=self.game.board.points[1][2], end=self.game.board.points[1][3], is_starting=True)
                # self.game.add_road(player=0, start=self.game.board.points[1][3], end=self.game.board.points[1][4], is_starting=True)
                # self.game.add_road(player=0, start=self.game.board.points[1][2], end=self.game.board.points[1][1], is_starting=True)
                # self.game.add_road(player=0, start=self.game.board.points[1][1], end=self.game.board.points[0][0], is_starting=True)
                # self.game.add_road(player=1, start=self.game.board.points[3][3], end=self.game.board.points[3][2], is_starting=True)
                # self.game.add_road(player=1, start=self.game.board.points[2][6], end=self.game.board.points[2][5], is_starting=True)
                # self.game.add_road(player=2, start=self.game.board.points[4][3], end=self.game.board.points[4][4], is_starting=True)
                # self.game.add_road(player=2, start=self.game.board.points[3][8], end=self.game.board.points[3][7], is_starting=True)
                # self.game.add_road(player=3, start=self.game.board.points[4][6], end=self.game.board.points[4][5], is_starting=True)
                # self.game.add_road(player=3, start=self.game.board.points[1][6], end=self.game.board.points[1][7], is_starting=True)
                
                self.game.players[0].add_dev_card(DevCard.Knight)
                self.game.players[0].add_dev_card(DevCard.YearOfPlenty)
                self.game.players[0].add_dev_card(DevCard.Monopoly)
                self.game.players[0].add_dev_card(DevCard.Road)                   
                # self.game.players[0].add_cards([ResCard.Wheat, ResCard.Ore, ResCard.Wood, ResCard.Brick, ResCard.Sheep])

                # self.game.players[0].add_cards([ResCard.Ore, ResCard.Ore, ResCard.Ore, ResCard.Wheat, ResCard.Wheat, ResCard.Wheat])   
                # self.game.players[0].add_cards([ResCard.Ore, ResCard.Ore, ResCard.Ore, ResCard.Wheat, ResCard.Wheat, ResCard.Wheat])   

                # self.game.board.upgrade_settlement(0, self.game.board.points[1][2])

        # Wrap players into agents
        
        for player in self.game.players:
                if debug:
                        print('Player ' + str(player.num) + ' human? (y/n)')
                        is_human = input()
                        if(is_human == 'y'):
                                self.agents.append(Agent(player, True, []))
                        else:
                                self.agents.append(RandomAgent(player))
                else:
                        self.agents.append(Agent(player, True, []))

        # Determine starting order for initial placements
        # Pick a random player then go in snake order
        chosen_player = player_index = random.randint(0, 3)

        # Starting placements
        # 8 total turns, 2 placements per player
        # Snake means: 0, 1, 2, 3, 3, 2, 1, 0

        starting_play_order = []
        switch = False
        for i in range(0, 8):
                starting_play_order.append(player_index)

                if(not i == 3):
                        if(not switch):
                                if(player_index == 3):
                                        player_index = 0
                                else:
                                        player_index += 1
                        else:
                                if(player_index == 0):
                                        player_index = 3
                                else:
                                        player_index -= 1
                else:
                        switch = True

        print('Starting play order: ')
        print(starting_play_order)
        placement_okay = False

        self.game.initial_placement_mode = True

        ## TODO
        # This is not debug

        for player_index in starting_play_order:
                CatanGame.displayBoard()
                printBlankLines(8)
                print('Player with turn: ' + colors[player_index])
                curr_agent = self.agents[player_index]
                curr_player = player_with_turn = curr_agent.player

                curr_player.has_completed_initial_placement = False
                curr_player.has_placed_initial_settlement = False

                # Two iterations for settlement and road
                for i in range(0, 2):
                        allowed_actions = CatanGame.getAllowedActions(curr_player, player_with_turn)
                        placement_okay = False
                        while(not placement_okay):
                                if(curr_agent.human):
                                    full_action = CatanGame.promptActions(curr_player, allowed_actions)
                                else:
                                    full_action = curr_agent.doTurn(allowed_actions)

                                status = CatanGame.doAction(curr_player, full_action)

                                if(status == Statuses.ALL_GOOD):
                                    placement_okay = True


        self.game.initial_placement_mode = False

        # Add initial placement yield
        # (This might be the wrong way to do it)
        for i in range(2, 13):
                if i != 7:
                        self.game.board.add_yield(i)

        player_index = chosen_player

        self.run(player_index)

    def run(self, player_index):
        # Game Loop
        # Cycle over all players per turn steps to allow for responses to trades
        turn_counter = 0
        game_over = False
        turn_over = False
        cycle_complete = False        
        while(not self.game.has_ended):
                # Reset roll
                self.game.can_roll = True

                # Iterate to next player with turn
                curr_agent = self.agents[player_index]
                player_with_turn = curr_player = curr_agent.player
                player_with_turn_index = player_index
                player_with_turn.turn_over = turn_over = False

                # Reset number of trades the player has conducted
                player_with_turn.num_trades_in_turn = 0

                # Cycle, starting with the player playing their turn, through all other players
                while(not turn_over):
                        curr_agent = self.agents[player_index]
                        curr_player = curr_agent.player 
                        # allowed_actions = CatanGame.getAllowedActions(player, player_with_turn)
                        
                        # Check if the action taken is valid 
                        action_okay = False
                        while(not action_okay):
                               
                                allowed_actions = CatanGame.getAllowedActions(curr_player, player_with_turn)
                                
                                # If the player only has one available action, and that action is NO_OP
                                # Skip their step
                                if(len(allowed_actions['allowed_actions']) == 1 and (NO_OP in allowed_actions['allowed_actions'])):
                                        action_okay = True
                                else:
                                        # Display turn relevant info
                                        CatanGame.displayBoard()
                                        print('Turn: ' + str(turn_counter))
                                        print('Player with turn: ' + colors[player_with_turn_index])
                                        print('Roll: ' + str(self.game.last_roll))
                                        print()
                                        if(self.game.largest_army != None):
                                                print('Largest Army: ' + colors[self.game.largest_army])
                                        else:
                                                print('Largest Army: None')

                                        if(self.game.longest_road_owner != None):
                                                print('Longest Road: ' + colors[self.game.longest_road_owner])
                                        else:
                                                print('Longest Road: None')

                                        print()
                                        # Display player relevant info
                                        CatanGame.displayPlayerGameInfo(curr_player)

                                        if(curr_agent.human):
                                                full_action = CatanGame.promptActions(curr_player, allowed_actions)
                                        else:
                                                full_action = curr_agent.doTurn(allowed_actions)
                                        print(full_action)
                                        print(action_types[full_action[0]])
                                        status = CatanGame.doAction(curr_player, full_action)

                                        self.game.set_longest_road()

                                        if status == Statuses.ALL_GOOD:
                                                action_okay = True
                                        elif status == Statuses.ROLLED_SEVEN:
                                                self.game.rolled_seven = True
                                                self.game.robber_moved = False
                                                for p in self.game.players:
                                                        if(len(p.cards) >= 8):
                                                                p.forfeited_cards_left = int(len(p.cards)/2)
                                        else:
                                                print('Error: ')
                                                print(Statuses.status_list[int(status)])

                                        # If the player still has cards to forfeit, stay on this player
                                        if(curr_player.forfeited_cards_left > 0):
                                                action_okay = False

                        if(player_with_turn.get_VP(True) >= 10):
                                self.game.has_ended = True
                                self.game.winner = player_with_turn
                                player_with_turn.turn_over = True

                        turn_over = player_with_turn.turn_over 
                        self.game.rolled_seven = False

                        if(not turn_over):
                                # 2 -> 3 -> 0 -> 1 -> 2
                                if(player_index == 3):
                                        player_index = 0
                                else:
                                        player_index += 1



                # Turn has ended
                player_index = player_with_turn_index
                turn_counter += 1


                # 2 -> 3 -> 0 -> 1 -> 2
                if(player_index == 3):
                        player_index = 0
                else:
                        player_index += 1

        print('Winner: ' + str(colors[self.game.winner.num]))

    # Get allowed actions
    def getAllowedActions(self, player, player_with_turn):
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

        is_players_turn = (player.num == player_with_turn.num)

        ## NO_OP
        # - It is not the player's turn
        # - There are no pending trades
        if(not is_players_turn and not player.pending_trade):
                actions['allowed_actions'].append(NO_OP)
                return actions

        ## INITIAL_PLACEMENT (Priority action, other ignors)
        # - It is players turn
        # - initial_placement_mode is true
        if(is_players_turn and self.game.initial_placement_mode):
                if(player.has_completed_initial_placement):
                        actions['allowed_actions'].append(END_TURN)
                        return actions
                if(player.num_initial_settlements > 0 and not player.has_placed_initial_settlement):
                        actions['allowed_actions'].append(INITIAL_PLACE_BUILDING)
                        actions['allowed_settlement_points'] = player.get_available_initial_settlement_points()
                if(player.num_initial_roads > 0 and player.has_placed_initial_settlement):
                        actions['allowed_actions'].append(INITIAL_PLACE_ROAD)
                        actions['allowed_road_point_pairs'] = player.get_available_initial_road_point_pairs()

                return actions

        ## FORFEIT_CARDS (Priority action, others ignored)
        # - A 7 is active and player has >= 8 cards
        if(player.forfeited_cards_left > 0):
                actions['allowed_actions'].append(FORFEIT_CARDS)
                actions['allowed_forfeit_cards'] = player.get_types_of_cards_possessed()
                return actions

        ## PLAY_ROBBER (Priority action, others ignored)
        # - It is the players turn
        # - A 7 is active and robber has not been moved
        if(is_players_turn and not self.game.robber_moved):
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

        ## PLAY_DEV_CARD
        # - It is the players turn
        # - Player has at least one development card
        if(is_players_turn):
                playable_dev_card = False
                for card in DevCard:
                        if(card in player.dev_cards):
                                if(card == DevCard.Knight or card == DevCard.YearOfPlenty or card == DevCard.Monopoly):
                                        actions['allowed_dev_cards'].append(card)
                                        playable_dev_card = True

                                if(card == DevCard.Knight):
                                        possible_robber_tiles_and_victims = player.get_available_robber_placement_tiles_and_victims()
                                        actions['allowed_robber_tiles'] = possible_robber_tiles_and_victims
                                        actions['allowed_victim_players'] = possible_robber_tiles_and_victims
                if(playable_dev_card):
                        actions['allowed_actions'].append(PLAY_DEV_CARD)

        ## ROLL (Priority action, others (except play dev card) ignored)
        # - It is the players turn
        # - The dice has not been rolled
        if(is_players_turn and self.game.can_roll):
                actions['allowed_actions'].append(ROLL)
                return actions

        ## PURCHASE_RESOURCE
        # - It is the players turn
        # - The dice has been rolled
        # - Player can exchange resource
        if(is_players_turn and not self.game.can_roll):
                # Check every resource and append those which are eligable
                cards = self.game.cards_tradable_to_bank(player)
                if cards:
                        # card_types = [card[0] for card in cards] 
                        # card_nums = [card[1] for card in cards] 
                        card_tuples = [(card[0], card[1]) for card in cards]
                        actions['allowed_actions'].append(PURCHASE_RESOURCE)
                        for card in cards:
                                actions['allowed_bank_trade_cards'].append(card)



                #self.game.can_trade_to_bank(player, cards, request)

        ## PURCHASE_AND_PLAY_BUILDING
        # - It is the players turn
        # - The dice has been rolled                
        # - Player has relevant cards
        if(is_players_turn and not self.game.can_roll):
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
        if(is_players_turn and player.can_build_dev()==Statuses.ALL_GOOD and not self.game.can_roll):
                actions['allowed_actions'].append(PURCHASE_DEV_CARD)

        ## START_TRADE
        # - It is the players turn
        # - Player has attempted 4 or less trades this turn
        # - Player actually has the card they are forfeiting
        # - Receiving player actually has the card they are forfeiting 
        if(is_players_turn and player.num_trades_in_turn < 4):
        
                player_card_types = player.get_types_of_cards_possessed()

                if(player_card_types):
                        for other_player in self.game.players:
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
        if(is_players_turn and not self.game.can_roll):
            actions['allowed_actions'].append(END_TURN)

        return actions

    # An interface for human players to interact with the game
    def promptActions(self, player, allowed_actions):
        print('Possible Actions')
        
        # print('0: No Op | 1: Roll | 2: Purchase Resource (From Bank/Port) | 3: Purchase Building | 4: Purchase Dev Card | 5: Play Dev Card |\n6: Play Robber | 7: Do Trade | 8: Accept Trade | 9: Reject Trade | 10: Forfeit Cards | 11: End Turn')
        for action in allowed_actions['allowed_actions']:
                print(str(action) + ': ' + action_types[action] + ' | ', end='')
        print()

        full_action = [] 

        response = int(input())

        full_action.append(response)
        
        print(action_types[response])
        # Roll
        if(response == 0):
                pass
        # Prompt No op
        if(response == 1):
                print(1)
        # Prompt Purchase Resource
        if(response == 2):
                print('Request Resource:')
                print('0: Wood | 1: Brick | 2: Ore | 3: Sheep | 4: Wheat')
                requested_resource = int(input())
                full_action.append(requested_resource)
                print('Forfeited Resource:')
                for allowed_card in allowed_actions['allowed_bank_trade_cards']:
                        print(str(allowed_card[0].value) + ': ' + allowed_card[0].name + '(' + str(allowed_card[1])  + ')' + ' | ', end='')
                print()
                forfeited_resource = int(input())
                full_action.append(forfeited_resource)
        # Prompt Purchase & play building
        if(response == 3):
                for allowed_building in allowed_actions['allowed_buildings']:
                        print(str(allowed_building) + ': ' + Building.BUILDINGS[allowed_building] + ' | ', end='')
                print()

                building_response = int(input())
                full_action.append(building_response)

                
                # Settlement
                if(building_response == 0):
                        print('Allowed Locations: (r, i)')
                        print(allowed_actions['allowed_settlement_points'])

                        print('r:')
                        loc_r_response = int(input())
                        full_action.append(loc_r_response)
                        print('i:')
                        loc_i_response = int(input())
                        full_action.append(loc_i_response)

                # Road
                if(building_response == 1):
                        print('Allowed Locations: (r, i)->(r2, i2)')
                        print(allowed_actions['allowed_road_point_pairs'])
                        
                        print('r:')
                        loc_r_response = int(input())
                        full_action.append(loc_r_response)
                        print('i:')
                        loc_i_response = int(input())
                        full_action.append(loc_i_response)

                        print('r 2:')
                        loc_r_response = int(input())
                        full_action.append(loc_r_response)
                        print('i 2:')
                        loc_i_response = int(input())
                        full_action.append(loc_i_response)

                # City
                if(building_response == 2):
                        print('Allowed Locations: (r, i)')
                        print(allowed_actions['allowed_city_points'])

                        print('r:')
                        loc_r_response = int(input())
                        full_action.append(loc_r_response)
                        print('i:')
                        loc_i_response = int(input())
                        full_action.append(loc_i_response)

        # Prompt Purchase dev card
        if(response == 4):
                pass
        # Prompt Play dev card
        if(response == 5):
                for allowed_card in allowed_actions['allowed_dev_cards']:
                        print(str(allowed_card.value) + ': ' + allowed_card.name + ' | ', end='')
                print()

                dev_card_response = int(input())
                full_action.append(dev_card_response)


                if(dev_card_response == 0):
                        print('Location X:')
                        loc_x_response = int(input())
                        full_action.append(loc_x_response)
                        print('Location Y:')
                        loc_y_response = int(input())
                        full_action.append(loc_y_response)

                if(dev_card_response == 2):
                        print('Allowed Locations: (r, i)')
                        for action in allowed_actions['allowed_robber_tiles']:
                            print('(', end='')
                            print(action[0], end='')
                            print(', ', end='')
                            print(colors[action[1].num], end='')
                            print('(' + str(action[1].num) + ')', end='')
                            print(') ', end='') 
                        
                        print()

                        print('r:')
                        loc_r_response = int(input())
                        full_action.append(loc_r_response)
                        print('i:')
                        loc_i_response = int(input())
                        full_action.append(loc_i_response)
                        
                        allowed_players = [y for x, y in allowed_actions['allowed_robber_tiles'] if (x.position[0] == loc_r_response and x.position[1] == loc_i_response)]

                        print('Player:')
                        for allowed_player in allowed_players:
                            print('Player ' + str(allowed_player.num) + '(' + colors[allowed_player.num] + ')' + ' | ', end='')
                        print()
                        player_response = int(input())
                        full_action.append(player_response)

                if(dev_card_response == 3):
                        print('0: Wood | 1: Brick | 2: Ore | 3: Sheep | 4: Wheat')
                        resource_response = int(input())
                        full_action.append(resource_response)

                if(dev_card_response == 4):
                        print('First resource:')
                        print('0: Wood | 1: Brick | 2: Ore | 3: Sheep | 4: Wheat')
                        first_resource_response = int(input())
                        full_action.append(first_resource_response)

                        print('Second resource:')
                        print('0: Wood | 1: Brick | 2: Ore | 3: Sheep | 4: Wheat')
                        second_resource_response = int(input())
                        full_action.append(second_resource_response)

        # Prompt Play robber
        if(response == 6):
            print('Allowed Locations: (r, i)')
            for action in allowed_actions['allowed_robber_tiles']:
                print('(', end='')
                print(action[0], end='')
                print(', ', end='')
                print(colors[action[1].num], end='')
                print('(' + str(action[1].num) + ')', end='')
                print(') ', end='') 
            
            print()

            print('r:')
            loc_r_response = int(input())
            full_action.append(loc_r_response)
            print('i:')
            loc_i_response = int(input())
            full_action.append(loc_i_response)
            
            allowed_players = [y for x, y in allowed_actions['allowed_robber_tiles'] if (x.position[0] == loc_r_response and x.position[1] == loc_i_response)]

            print('Player:')
            for allowed_player in allowed_players:
                print('Player ' + str(allowed_player.num) + '(' + colors[allowed_player.num] + ')' + ' | ', end='')
            print()
            player_response = int(input())
            full_action.append(player_response)
        # Prompt Do trade
        if(response == 7):

                for allowed_player in allowed_actions['allowed_trade_partners']:
                        print('Player ' + str(allowed_player.num) + '(' + colors[allowed_player.num] + ')' + ' | ', end='')
                print()
                which_player_response = int(input())
                full_action.append(self.game.players[which_player_response])
                

                allowed_cards = allowed_actions['allowed_trade_pairs']
                allowed_cards = [(x,y) for x, y in allowed_cards if x == which_player_response][0][1]
                allowed_cards = [x[0] for x in allowed_cards]


                print('You offer:') 
                for allowed_card in allowed_cards:
                        print(str(allowed_card.value) + ': ' + allowed_card.name + ' | ', end='')
                print()

                offered_resource_response = int(input())
                full_action.append(ResCard(offered_resource_response))  


                other_player_allowed_cards = allowed_actions['allowed_trade_pairs']
                other_player_allowed_cards = [(x,y) for x, y in other_player_allowed_cards if x == which_player_response][0][1]
                other_player_allowed_cards = [(x,y) for x, y in other_player_allowed_cards if x.value == offered_resource_response][0]

                print('You receive:')
                for allowed_card in other_player_allowed_cards[1]:
                        print(str(allowed_card.value) + ': ' + allowed_card.name + ' | ', end='')
                print()
                received_resource_response = int(input())
                full_action.append(ResCard(received_resource_response))
        # Accept Trade
        if(response == 8):
                pass
        # Deny trade
        if(response == 9):
                pass
        # Forfeit card
        if(response == 10):
                print('Forfeit(' + str(player.forfeited_cards_left) + ' left): ') 
                
                for allowed_card in allowed_actions['allowed_forfeit_cards']:
                        print(str(allowed_card.value) + ': ' + allowed_card.name + ' | ', end='')
                print()

                player_response = int(input())
                full_action.append(player_response)

        if(response == 11):
                pass

        # Prompt initial road placement
        if(response == 12):
            print('Place initial road')

            print('Allowed Locations: (r, i)->(r2, i2)')
            print(allowed_actions['allowed_road_point_pairs'])

            print('r:')
            loc_r_response = int(input())
            full_action.append(loc_r_response)
            print('i:')
            loc_i_response = int(input())
            full_action.append(loc_i_response)

            print('r 2:')
            loc_r_response = int(input())
            full_action.append(loc_r_response)
            print('i 2:')
            loc_i_response = int(input())
            full_action.append(loc_i_response)

        # Prompt initial settlement placement
        if(response == 13):
            print('Place initial settlement')
            
            # TODO
            # Get all places on the board which are >=2 distance to next player settlement
            
            print('Allowed Locations: (r, i)')
            print(allowed_actions['allowed_settlement_points'])

            print('r:')
            loc_r_response = int(input())
            full_action.append(loc_r_response)
            print('i:')
            loc_i_response = int(input())
            full_action.append(loc_i_response)

        return full_action        



    def doAction(self, player, args):
        action_type = args[0]

        # No op
        if(action_type == 0):
                return Statuses.ALL_GOOD
        # Roll
        if(action_type == 1):
                if(self.game.can_roll):
                        self.game.last_roll = roll = self.game.get_roll()
                        self.game.can_roll = False
                        if(roll != 7):
                                self.game.board.add_yield(roll)
                        else:
                                return Statuses.ROLLED_SEVEN
                        return Statuses.ALL_GOOD
                else:
                        return Statuses.ERR_ROLL
        # Purchase Resource
        if(action_type == 2):
                requested_resource = args[1]
                forfeited_resource = args[2]
                status = self.game.trade_to_bank(player, forfeited_resource, requested_resource)
                return status

        # Purchase & play building
        if(action_type == 3):
                building_response = args[1]
                loc_r_response = args[2]
                loc_i_response = args[3]
                if(building_response == 0):
                        status = player.build_settlement(self.game.board.points[loc_r_response][loc_i_response])
                if(building_response == 1):
                        loc_r_response_2 = args[4]
                        loc_i_response_2 = args[5]     
                        status = player.build_road(self.game.board.points[loc_r_response][loc_i_response], self.game.board.points[loc_r_response_2][loc_i_response_2])
                if(building_response == 2):
                        status = self.game.add_city(self.game.board.points[loc_r_response][loc_i_response], player)
                return status

        # Purchase dev card
        if(action_type == 4):
                status = self.game.build_dev(player.num)
                return status

        # Play Item
        if(action_type == 5):
                dev_card_response = args[1]
                # Knight
                if(dev_card_response == 2):
                        loc_x_response = args[2]
                        loc_y_response = args[3]
                        victim_player_response = args[4]

                        status = self.game.use_dev_card(player.num, DevCard.Knight, {'robber_pos': [loc_x_response, loc_y_response], 'victim': victim_player_response})
                        return status
                # Monopoly
                if(dev_card_response == 3):
                        resource_response = args[2]

                        status = self.game.use_dev_card(player.num, DevCard.Monopoly, {'card_type': ResCard(resource_response)})
                        return status
                # YOP
                if(dev_card_response == 4):
                        first_resource_response = args[2]
                        second_resource_response = args[3]
                        
                        
                        status = self.game.use_dev_card(player.num, DevCard.YearOfPlenty, {'card_one': ResCard(first_resource_response), 'card_two': ResCard(second_resource_response)})
                        return status
        # Play robber
        if(action_type == 6):
                loc_x_response = args[1]
                loc_y_response = args[2]
                victim_player_response = args[3]

                status = self.game.move_robber(self.game.board.tiles[loc_x_response][loc_y_response], player.num, victim_player_response)
                self.game.robber_moved = True
                return status

        # Do trade
        if(action_type == 7):
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
        if(action_type == 8):
                status = self.game.trade(player.num, player.trading_player.num, [player.trade_forfeit_card], [player.trade_receive_card])
                player.pending_trade = False
                return status
        # Deny trade
        if(action_type == 9):
                player.pending_trade = False
        if(action_type == 10):
                player.remove_cards([args[1]])
                player.forfeited_cards_left -= 1
        if(action_type == 11):
                player.turn_over = True
                return Statuses.ALL_GOOD

        # Initial placements
        # Road
        if(action_type == 12):
                loc_r_response = args[1]
                loc_i_response = args[2]     
                loc_r_response_2 = args[3]
                loc_i_response_2 = args[4]     
                status = player.build_road(self.game.board.points[loc_r_response][loc_i_response], self.game.board.points[loc_r_response_2][loc_i_response_2], is_starting=True)
                player.has_completed_initial_placement = True

        # Building
        if(action_type == 13):
                loc_r_response = args[1]
                loc_i_response = args[2]
                status = player.build_settlement(self.game.board.points[loc_r_response][loc_i_response], is_starting=True)
                player.has_placed_initial_settlement = True
                player.initial_settlement = self.game.board.points[loc_r_response][loc_i_response]


        return Statuses.ALL_GOOD


    # def promptInitialPlacement(self):
    #     full_action = []
    #     print('Settlement')
    #     print('Tile Location X:')
    #     loc_x_response = int(input())
    #     full_action.append(loc_x_response)
    #     print('Tile Location Y:')
    #     loc_y_response = int(input())
    #     full_action.append(loc_y_response)

    #     print('Location road endpoint')
    #     print('Road Location X:')
    #     road_loc_x_response = int(input())
    #     full_action.append(road_loc_x_response)
    #     print('Road Location Y:')
    #     road_loc_y_response = int(input())
    #     full_action.append(road_loc_y_response)

    #     return full_action


    # def doInitialPlacement(self, player, args):
    #     loc_x = args[0]
    #     loc_y = args[1]

    #     loc_x_2 = args[2]
    #     loc_y_2 = args[3]
    #     status = player.build_settlement(self.game.board.points[loc_x][loc_y], True)
    #     if(status != Statuses.ALL_GOOD):
    #             return status
    #     status = player.build_road(self.game.board.points[loc_x][loc_y], self.game.board.points[loc_x_2][loc_y_2], True)
    #     return status

    
    def displayBoard(self):
            self.boardRenderer.render()

    def displayPlayerGameInfo(self, player):
        print('Player ' + str(player.num) + '(' + colors[player.num] + ')'  ':')
        print('VP: ' + str(player.get_VP(True)))
        print('Knight Cards Played: ' + str(player.knight_cards))
        print('Longest Road Length: ' + str(player.longest_road_length))
        print('Forfeited cards left: ' + str(player.forfeited_cards_left))
        print('Number of attempted trades this turn: ' + str(player.num_trades_in_turn))
        print('Accessible Ports:')
        harbors = player.get_connected_harbor_types()
        print(harbors)
        print('Robber Location:')
        print(self.game.board.robber)
        # TODO
        # Find connected ports

        print('Dev Cards:')
        player.print_cards(player.dev_cards)

        print('Cards:')
        player.print_cards(player.cards)
        
        # Pending trades
        if(player.pending_trade):
                print('Pending Trade from player ' + str(player.trading_player.num) + '(' + colors[player.trading_player.num] + ')')
                print('Forfeit: ' + ResCard(player.trade_forfeit_card).name)
                print('Receive: ' + ResCard(player.trade_receive_card).name)

    # Used for pitboss mode
    def displayLimitedPlayerGameInfo(self, player):
        print('Player ' + str(player.num) + '(' + colors[player.num] + ')'  ':')
        print('Knight Cards Played: ' + str(player.knight_cards))
        print('Longest Road Length: ' + str(player.longest_road_length))
        print('Forfeited cards left: ' + str(player.forfeited_cards_left))
        print('Number of attempted trades this turn: ' + str(player.num_trades_in_turn))
        print('Accessible Ports:')
        harbors = player.get_connected_harbor_types()
        print(harbors)
        print('Robber Location:')
        print(self.game.board.robber)
        
        # Pending trades
        if(player.pending_trade):
                print('Pending Trade from player ' + str(player.trading_player.num) + '(' + colors[player.trading_player.num] + ')')
                print('Forfeit: ' + ResCard(player.trade_forfeit_card).name)
                print('Receive: ' + ResCard(player.trade_receive_card).name)

    def displayNonHumanGameInfo(self, player):
        pass
    


    def displayFullGameInfo(self):
        self.displayBoard()
        for player in self.game.players:
                print('Player ' + str(player.num) + ':')
                print('Cards:')
                player.print_cards(player.cards) 
                print()


CatanGame = GameWrapper()
CatanGame.setup()