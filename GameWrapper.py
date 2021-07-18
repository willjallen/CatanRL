from pycatan import Game
from pycatan import Statuses
from pycatan import Building
from pycatan.card import ResCard, DevCard
from board_renderer import BoardRenderer
from agent import Agent
from random_agent import RandomAgent
import random

action_types = ["no_op", "roll", "purchase_resource", "purchase_and_play_building", "purchase_dev_card", "play_dev_card", "play_robber", "start_trade", "accept_trade", "deny_trade", "forfeit_cards", "end_turn"]
NO_OP = 0
ROLL = 1
PURCHASE_RESOURCE = 2
PURCHASE_AND_PLAY_BUILDING = 3
PURCHASE_DEV_CARD = 4
PLAY_DEV_CARD = 5
PLAY_ROBBER = 6
START_TRADE = 7
ACCEPTED_TRADE = 8
DENY_TRADE = 9
FORFEIT_CARDS = 10
END_TURN = 11

def printBlankLines(num):
        for i in range(0, num):
                print()


class GameWrapper:
        def __init__(self):
                num_of_players = 4

                game = Game(num_of_players)

                self.game = game
                self.boardRenderer = BoardRenderer(game.board, [50, 10])


        # An interface for human players to interact with the game
        


        # Get allowed actions
        def getAllowedActions(self, player, player_with_turn):
                actions = {
                'allowed_actions': [],
                'allowed_forfeit_cards': [],
                'allowed_bank_trade_cards': [],
                'allowed_dev_cards': [],
                'allowed_buildings': [],
                'allowed_robber_tiles': [],
                'allowed_road_point_one_x': [],
                'allowed_road_point_pairs': [],
                'allowed_settlement_points': [], 
                'allowed_city_points': [],
                'allowed_victim_players': []
                }

                is_players_turn = (player.num == player_with_turn.num)


                ## FORFEIT_CARDS (Priority action, others ignored)
                # - A 7 is active and player has >= 8 cards
                if(self.game.rolled_seven and len(player.cards) >= 8):
                        actions['allowed_actions'].append(FORFEIT_CARDS)
                        allowed_actions.append(FORFEIT_CARDS)
                        actions['allowed_forfeit_cards'] = player.get_type_of_cards_possessed()
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

                ## ROLL
                # - It is the players turn
                # - The dice has not been rolled
                if(is_players_turn and self.game.can_roll):
                        actions['allowed_actions'].append(ROLL)

                # TODO    
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
                        available_cities = []
                        available_road_pairs = player.get_available_road_point_pairs()
                        if(len(available_buildings) != 0):
                                actions['allowed_settlement_points'] = player.get_available_settlement_points()
                                if(actions['allowed_settlement_points']):
                                        actions['allowed_actions'].append(PURCHASE_AND_PLAY_BUILDING)
                                        actions['allowed_buildings'].append(Building.BUILDING_SETTLEMENT)

                                # if(Building.BUILDING_CITY in available_buildings):
                                #         actions['allowed_city_points']
                        if(Building.BUILDING_ROAD in available_buildings):
                                if(len(available_road_pairs) != 0):
                                        actions['allowed_road_point_pairs'] = available_road_pairs
                                        if not(PURCHASE_AND_PLAY_BUILDING in actions['allowed_actions']):
                                                actions['allowed_actions'].append(PURCHASE_AND_PLAY_BUILDING)
                                                actions['allowed_buildings'].append(Building.BUILDING_ROAD)


                        if(Building.BUILDING_CITY in available_buildings):
                                pass                                


                ## PURCHASE_DEV_CARD
                # - It is the players turn
                # - The dice has been rolled                
                # - Player has relevant cards
                if(is_players_turn and player.can_build_dev()==Statuses.ALL_GOOD and not self.game.can_roll):
                        actions['allowed_actions'].append(PURCHASE_DEV_CARD)

                ## PLAY_DEV_CARD
                # - It is the players turn
                # - Player has at least one development card
                if(is_players_turn and len(player.dev_cards) >= 1):
                        actions['allowed_actions'].append(PLAY_DEV_CARD)
                        for card in DevCard:
                                if(card in player.dev_cards):
                                        actions['allowed_dev_cards'].append(card)
                                        
                                        if(card == DevCard.Knight):
                                                possible_robber_tiles_and_victims = player.get_available_robber_placement_tiles_and_victims()
                                                actions['allowed_robber_tiles'] = possible_robber_tiles_and_victims[0]
                                                actions['allowed_victim_players'] = possible_robber_tiles_and_victims[1]


                ## PLAY_ROBBER
                # - It is the players turn
                # - A 7 is active and robber has not been moved
                if(self.game.rolled_seven and not self.robber_moved):
                        actions['allowed_actions'].append(PLAY_ROBBER)

                ## START_TRADE
                # - It is the players turn
                # - Player actually has the card they are forfeiting
                # - Receiving player actually has the card they are forfeiting 
                if(is_players_turn):
                    pass

                ## END_TURN
                # - It is the players turn
                # - The dice has been rolled                
                if(is_players_turn and not self.game.can_roll):
                    actions['allowed_actions'].append(END_TURN)

                return actions

        def promptActions(self, player, possible_actions):
                print('Possible Actions')
                
                # print('0: No Op | 1: Roll | 2: Purchase Resource (From Bank/Port) | 3: Purchase Building | 4: Purchase Dev Card | 5: Play Dev Card |\n6: Play Robber | 7: Do Trade | 8: Accept Trade | 9: Reject Trade | 10: Forfeit Cards | 11: End Turn')
                for action in possible_actions['allowed_actions']:
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
                        for allowed_card in possible_actions['allowed_bank_trade_cards']:
                                print(str(allowed_card[0].value) + ': ' + allowed_card[0].name + '(' + str(allowed_card[1])  + ')' + ' | ', end='')
                        print()
                        forfeited_resource = int(input())
                        full_action.append(forfeited_resource)
                # Prompt Purchase & play building
                if(response == 3):
                        for allowed_building in possible_actions['allowed_buildings']:
                                print(str(allowed_building) + ': ' + Building.BUILDINGS[allowed_building] + ' | ', end='')
                        print()
   
                        building_response = int(input())
                        full_action.append(building_response)

                        
                        # Settlement
                        if(building_response == 0):
                                print('Allowed Locations: (r, i)')
                                print(possible_actions['allowed_settlement_points'])

                                print('r:')
                                loc_r_response = int(input())
                                full_action.append(loc_r_response)
                                print('i:')
                                loc_i_response = int(input())
                                full_action.append(loc_i_response)

                        # Road
                        if(building_response == 1):
                                print('Allowed Locations: (r, i)->(r2, i2)')
                                print(possible_actions['allowed_road_point_pairs'])
                                
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
                                print(possible_actions['allowed_city_points'])

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
                        for allowed_card in possible_actions['allowed_dev_cards']:
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
                                print('Location X:')
                                loc_x_response = int(input())
                                full_action.append(loc_x_response)
                                print('Location Y:')
                                loc_y_response = int(input())
                                full_action.append(loc_y_response)
                                print('Player:')
                                print('0: Red | 1: Cyan | 2: Green | 3: Yellow')
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
                        print('Location X:')
                        loc_x_response = int(input())
                        full_action.append(loc_x_response)
                        print('Location Y:')
                        loc_y_response = int(input())
                        full_action.append(loc_y_response)
                        print('Player:')
                        print('0: Red | 1: Cyan | 2: Green | 3: Yellow')
                        player_response = int(input())
                        full_action.append(player_response)
                # Prompt Do trade
                if(response == 7):
                        print('0: Player 0 | 1: Player 1 | 2: Player 2 | 3: Player 3')
                        which_player_response = int(input())
                        full_action.append(which_player_response)
                        
                        print('You offer:') 
                        print('0: Wood | 1: Brick | 2: Ore | 3: Sheep | 4: Wheat')
                        offered_resource_response = int(input())
                        full_action.append(offered_resource_response)

                        print('You receive:')
                        print('0: Wood | 1: Brick | 2: Ore | 3: Sheep | 4: Wheat')
                        received_resource_response = int(input())
                        full_action.append(received_resource_response)
                # Accept Trade
                if(response == 8):
                        pass
                # Deny trade
                if(response == 9):
                        pass
                if(response == 10):
                        pass
                if(response == 11):
                        pass

                return full_action        

        def doAction(self, player, args):
                action_type = args[0]



                # No op
                if(action_type == 0):
                        return Statuses.ALL_GOOD
                # Roll
                if(action_type == 1):
                        if(self.game.can_roll):
                                self.game.board.add_yield(self.game.get_roll())
                                self.game.can_roll = False
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
                        loc_x_response = args[2]
                        loc_y_response = args[3]
                        victim_player_response = args[4]

                        status = self.game.move_robber(self.game.board.tiles[loc_x_response][loc_y_response], player.num, victim_player_response)
                        return status
        
                # Do trade
                if(action_type == 7):
                        pass
                        # TODO
                        # this

                        # print('0: Player 0 | 1: Player 1 | 2: Player 2 | 3: Player 3')
                        # which_player_response = int(input())
                        # full_action.append(which_player_response)
                        
                        # print('You offer:') 
                        # print('1: Wood | 2: Wheat | 3: Ore | 4: Sheep | 5: Brick')
                        # offered_resource_response = int(input())
                        # full_action.append(offered_resource_response)

                        # print('You receive:')
                        # print('1: Wood | 2: Wheat | 3: Ore | 4: Sheep | 5: Brick')
                        # received_resource_response = int(input())
                        # full_action.append(received_resource_response)
                # Accept Trade
                if(action_type == 8):
                        pass
                # Deny trade
                if(action_type == 9):
                        pass
                if(action_type == 10):
                        pass
                if(action_type == 11):
                        player.turn_over = True
                        return Statuses.ALL_GOOD
                return Statuses.ALL_GOOD


        def promptInitialPlacement(self):
                full_action = []
                print('Settlement')
                print('Tile Location X:')
                loc_x_response = int(input())
                full_action.append(loc_x_response)
                print('Tile Location Y:')
                loc_y_response = int(input())
                full_action.append(loc_y_response)

                print('Location road endpoint')
                print('Road Location X:')
                road_loc_x_response = int(input())
                full_action.append(road_loc_x_response)
                print('Road Location Y:')
                road_loc_y_response = int(input())
                full_action.append(road_loc_y_response)

                return full_action


        def doInitialPlacement(self, player, args):
                loc_x = args[0]
                loc_y = args[1]

                loc_x_2 = args[2]
                loc_y_2 = args[3]
                status = player.build_settlement(self.game.board.points[loc_x][loc_y], True)
                if(status != Statuses.ALL_GOOD):
                        return status
                status = player.build_road(self.game.board.points[loc_x][loc_y], self.game.board.points[loc_x_2][loc_y_2], True)
                return status

        def displayBoard(self):
                self.boardRenderer.render()

        def displayPlayerGameInfo(self, player):
                self.displayBoard()
                printBlankLines(10)
                colors = ['Red', 'Cyan', 'Green', 'Yellow']
                print('Player ' + str(player.num) + '(' + colors[player.num] + ')'  ':')
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


        def displayFullGameInfo(self):
                self.displayBoard()
                for player in self.game.players:
                        print('Player ' + str(player.num) + ':')
                        print('Cards:')
                        player.print_cards(player.cards) 
                        print()




def main():

        # Game Set-up questions
        print('Manual Mode (y/n)')
        #manual_mode = input()
        
        #print('Number of players (2-4)')
        # Might just cap this at 4 for training
        # num_players = int(input())
        
        num_players = 4
        
        # Other stuff here
        # Maybe a manual board input, but thats sounds lame rn

        # Init
        CatanGame = GameWrapper()

        debug = True

        if debug:
                CatanGame.game.players[0].add_dev_card(DevCard.Knight)
                CatanGame.game.players[0].add_dev_card(DevCard.YearOfPlenty)
                CatanGame.game.players[0].add_dev_card(DevCard.Monopoly)
                CatanGame.game.players[0].add_dev_card(DevCard.Road)   

                CatanGame.game.add_settlement(player=0, point=CatanGame.game.board.points[0][0], is_starting=True)                
                CatanGame.game.add_settlement(player=0, point=CatanGame.game.board.points[1][2], is_starting=True)
                CatanGame.game.add_settlement(player=1, point=CatanGame.game.board.points[3][3], is_starting=True)
                CatanGame.game.add_settlement(player=1, point=CatanGame.game.board.points[2][6], is_starting=True)
                CatanGame.game.add_settlement(player=2, point=CatanGame.game.board.points[4][3], is_starting=True)
                CatanGame.game.add_settlement(player=2, point=CatanGame.game.board.points[3][8], is_starting=True)
                CatanGame.game.add_settlement(player=3, point=CatanGame.game.board.points[4][6], is_starting=True)
                CatanGame.game.add_settlement(player=3, point=CatanGame.game.board.points[1][6], is_starting=True)
                

                # Add some roads
                CatanGame.game.add_road(player=0, start=CatanGame.game.board.points[0][0], end=CatanGame.game.board.points[0][1], is_starting=True)
                CatanGame.game.add_road(player=0, start=CatanGame.game.board.points[1][2], end=CatanGame.game.board.points[1][3], is_starting=True)
                CatanGame.game.add_road(player=0, start=CatanGame.game.board.points[1][3], end=CatanGame.game.board.points[1][4], is_starting=True)
                CatanGame.game.add_road(player=1, start=CatanGame.game.board.points[3][3], end=CatanGame.game.board.points[3][2], is_starting=True)
                CatanGame.game.add_road(player=1, start=CatanGame.game.board.points[2][6], end=CatanGame.game.board.points[2][5], is_starting=True)
                CatanGame.game.add_road(player=2, start=CatanGame.game.board.points[4][3], end=CatanGame.game.board.points[4][4], is_starting=True)
                CatanGame.game.add_road(player=2, start=CatanGame.game.board.points[3][8], end=CatanGame.game.board.points[3][7], is_starting=True)
                CatanGame.game.add_road(player=3, start=CatanGame.game.board.points[4][6], end=CatanGame.game.board.points[4][5], is_starting=True)
                CatanGame.game.add_road(player=3, start=CatanGame.game.board.points[1][6], end=CatanGame.game.board.points[1][7], is_starting=True)
                
                CatanGame.game.players[0].add_cards([ResCard.Wheat, ResCard.Ore, ResCard.Wood, ResCard.Brick, ResCard.Sheep])

                CatanGame.game.players[0].add_cards([ResCard.Ore, ResCard.Ore, ResCard.Wheat, ResCard.Wheat, ResCard.Wheat])   
                CatanGame.game.board.upgrade_settlement(0, CatanGame.game.board.points[1][2])

        # Make players into agents
        agents = []
        for player in CatanGame.game.players:
                if debug:
                        print('Player ' + str(player.num) + ' human? (y/n)')
                        is_human = input()
                        if(is_human == 'y'):
                                agents.append(Agent(player, True, []))
                        else:
                                agents.append(RandomAgent(player))
                else:
                        agents.append(Agent(player, True, []))

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

        print(starting_play_order)
        placement_okay = False

        if not debug:
                for player_index in starting_play_order:
                        
                        curr_agent = agents[player_index]
                        if(curr_agent.is_human):
                                while(not placement_okay):
                                        CatanGame.displayBoard()
                                        print('Player ' + str(curr_agent.player.num))
                                        printBlankLines(10)
                                        
                                        full_action = CatanGame.promptInitialPlacement()
                                        status = CatanGame.doInitialPlacement(curr_agent.player, full_action)
                                        
                                        if(status == Statuses.ALL_GOOD):
                                                placement_okay = True
                                        else:
                                                print(Statuses.status_list[status])
                                        print()

                                placement_okay = False
                        else:
                                # AI stuff
                                pass

        # Add initial placement yield
        # (This might be the wrong way to do it)
        for i in range(2, 13):
                if i != 7:
                        CatanGame.game.board.add_yield(i)

        player_index = chosen_player

        # Game Loop
        # Cycle over all players per turn steps to allow for responses to trades
        turn_counter = 0
        game_over = False
        turn_over = False
        cycle_complete = False        
        while(not game_over):
                CatanGame.game.can_roll = True
                curr_agent = agents[player_index]
                player_with_turn = curr_player = curr_agent.player
                player_with_turn_index = player_index
                player_with_turn.turn_over = turn_over = False

                # Cycle, starting with the player playing their turn, through all other players
                while(not turn_over):
                        curr_player = CatanGame.game.players[player_index] 
                        print('Turn: ' + str(turn_counter))
                        CatanGame.displayPlayerGameInfo(curr_player)

                        # allowed_actions = CatanGame.getAllowedActions(player, player_with_turn)
                        possible_actions = CatanGame.getAllowedActions(curr_player, player_with_turn)
                        
                        action_okay = False
                        while(not action_okay):
                               
                                # Debug
                                if(len(possible_actions['allowed_actions']) == 1 and (NO_OP in possible_actions['allowed_actions'])):
                                        action_okay = True
                                else:
                                        if(curr_agent.human):
                                                full_action = CatanGame.promptActions(curr_player, possible_actions)
                                        else:
                                                full_action = curr_agent.doTurn(possible_actions)
                                        
                                        status = CatanGame.doAction(curr_player, full_action)
                                        
                                        if status == Statuses.ALL_GOOD:
                                                action_okay = True
                                        else:
                                                print('Error: ')
                                                print(Statuses.status_list[int(status)])

                        turn_over = player_with_turn.turn_over 

                        if(not turn_over):
                                # 2 -> 3 -> 0 -> 1 -> 2
                                if(player_index == 3):
                                        player_index = 0
                                else:
                                        player_index += 1

                turn_counter += 1

                # Turn has ended
                player_index = player_with_turn_index
                
                # 2 -> 3 -> 0 -> 1 -> 2
                if(player_index == 3):
                        player_index = 0
                else:
                        player_index += 1


if __name__ == "__main__":
        main()