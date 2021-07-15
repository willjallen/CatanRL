from pycatan import Game
from pycatan import Statuses
from board_renderer import BoardRenderer
import random

action_types = ["no_op", "purchase_resource", "purchase_and_play_building", "purchase_dev_card", "play_dev_card", "play_robber", "start_trade", "accept_trade", "deny_trade", "forfeit_cards", "end_turn"]


class GameWrapper:
        def __init__(self):
                num_of_players = 4

                game = Game(num_of_players)
                # game.add_settlement(player=0, point=game.board.points[0][0], is_starting=True)
                # game.add_settlement(player=1, point=game.board.points[2][3], is_starting=True)
                # game.add_settlement(player=1, point=game.board.points[6][0], is_starting=True)
                # game.add_settlement(player=1, point=game.board.points[2][3], is_starting=True)
                
                # game.add_settlement(player=2, point=game.board.points[4][1], is_starting=True)
                # Add some roads
                # game.add_road(player=0, start=game.board.points[0][0], end=game.board.points[0][1], is_starting=True)
                # game.add_road(player=1, start=game.board.points[2][3], end=game.board.points[2][2], is_starting=True)
                # game.add_road(player=2, start=game.board.points[4][1], end=game.board.points[4][0], is_starting=True)
                self.game = game
                self.boardRenderer = BoardRenderer(game.board, [50, 10])

        def promptActions(self, player):
                print('1: No Op | 2: Purchase Resource (From Bank/Port) | 3: Purchase Building | 4: Purchase Dev Card | 5: Play Dev Card |\n6: Play Robber | 7: Do Trade | 8: Accept Trade | 9: Reject Trade | 10: Forfeit Cards | 11: End Turn')
                full_action = [] 

                response = int(input())

                full_action.append(response)
                
                print(action_types[response-1])
                # Prompt No op
                if(response == 1):
                        print(1)
                # Prompt Purchase Resource
                if(response == 2):
                        print('Request Resource:')
                        print('1: Wood | 2: Brick | 3: Ore | 4: Sheep | 5: Wheat')
                        requested_resource = int(input())
                        full_action.append(resource_response)
                        print('Forfeited Resource:')
                        print('1: Wood | 2: Brick | 3: Ore | 4: Sheep | 5: Wheat')
                        forfeited_resource = int(input())
                        full_action.append(forfeited_resource)
                # Prompt Purchase & play building
                if(response == 3):
                        print('1: Road | 2: Settlement | 3: City')
                        building_response = int(input())
                        full_action.append(building_response)

                        print('Location X:')
                        loc_x_response = int(input())
                        full_action.append(loc_x_response)
                        print('Location Y:')
                        loc_y_response = int(input())
                        full_action.append(loc_y_response)

                        # Need second point for road
                        if(building_response == 1):
                                print('Location X 2:')
                                loc_x_response_2 = int(input())
                                full_action.append(loc_x_response_2)
                                print('Location Y 2:')
                                loc_y_response_2 = int(input())
                                full_action.append(loc_y_response_2)

                # Prompt Purchase dev card
                if(response == 4):
                        pass
                # Prompt Play dev card
                if(response == 5):
                        print('1: Knight | 2: YOP | 3: Monopoly | 4: Road Building')
                        dev_card_response = int(input())
                        full_action.append(dev_card_response)

                        if(dev_card_response == 1):
                                print('Location X:')
                                loc_x_response = int(input())
                                full_action.append(loc_x_response)
                                print('Location Y:')
                                loc_y_response = int(input())
                                full_action.append(loc_y_response)

                        if(dev_card_response == 2):
                                print('First resource:')
                                print('1: Wood | 2: Brick | 3: Ore | 4: Sheep | 5: Wheat')
                                first_resource_response = int(input())
                                full_action.append(first_resource_response)

                                print('Second resource:')
                                print('1: Wood | 2: Brick | 3: Ore | 4: Sheep | 5: Wheat')
                                second_resource_response = int(input())
                                full_action.append(second_resource_response)

                        if(dev_card_response == 3):
                                print('1: Wood | 2: Brick | 3: Ore | 4: Sheep | 5: Wheat')
                                resource_response = int(input())
                                full_action.append(resource_response)

                        if(dev_card_response == 4):
                                print('Location X:')
                                loc_x_response = int(input())
                                full_action.append(loc_x_response)
                                print('Location Y:')
                                loc_y_response = int(input())
                                full_action.append(loc_y_response)

                # Prompt Play robber
                if(response == 6):
                        print('Location X:')
                        loc_x_response = int(input())
                        full_action.append(loc_x_response)
                        print('Location Y:')
                        loc_y_response = int(input())
                        full_action.append(loc_y_response)
                # Prompt Do trade
                if(response == 7):
                        print('1: Player 1 | 2: Player 2 | 3: Player 3 | 4: Player 4')
                        which_player_response = int(input())
                        full_action.append(which_player_response)
                        
                        print('You offer:') 
                        print('1: Wood | 2: Brick | 3: Ore | 4: Sheep | 5: Wheat')
                        offered_resource_response = int(input())
                        full_action.append(offered_resource_response)

                        print('You receive:')
                        print('1: Wood | 2: Brick | 3: Ore | 4: Sheep | 5: Wheat')
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

        def doAction(self, player, args):
                action_type = args[0]

                  # No op
                if(response == 1):
                        pass
                # Purchase Resource
                if(response == 2):
                        requested_resource = args[1]
                        forfeited_resource = args[2]
                        # TODO
                        # Forfeited resource needs to be sent as [card, card, card, card]
                        # And check to occur if player has a port to send instead as [card, card, card] or otherwise
                        # self.game.trade_to_bank(player, forfeited_resource, requested_resource)
                # Purchase & play building
                if(response == 3):
                        building_response = args[1]
                        loc_x_response = args[2]
                        loc_y_response = args[3]
                        if(building_response == 1):
                                loc_x_response_2 = args[4]
                                loc_y_response_2 = args[5]     
                                status = player.build_road(self.game.board.points[loc_x_response][loc_y_response], self.game.board.points[loc_x_response_2][loc_y_response_2])
                        if(building_response == 2):
                                status = player.build_settlement(self.game.board.points[loc_x_response][loc_y_response])
                        if(building_response == 3):
                                status = self.game.add_city(self.game.board.points[loc_x_response][loc_y_response], player)

                # Purchase dev card
                if(response == 4):
                        status = self.game.build_dev(player)

                # Play Item
                if(response == 5):
                        dev_card_response = args[1]
                        """
                            # the developement cards
                            Road = 0
                            VictoryPoint = 1
                            Knight = 2
                            Monopoly = 3
                            YearOfPlenty = 4

                        """
                        # Knight
                        if(dev_card_response == 1):
                                loc_x_response = args[2]
                                loc_y_response = args[3]
                                # TODO
                                # Tile at r,c index within the array
                                # status = self.game.move_robber()
                        # YOP
                        if(dev_card_response == 2):
                                first_resource_response = args[2]
                                second_resource_response = args[3]
                                status = self.game.use_dev_card(player, DevCard.YearOfPlenty, [('card_one', first_resource_response), ('card_two', second_resource_response)])
                        # Monopoly
                        if(dev_card_response == 3):
                                resource_response = args[2]
                                status = self.game.use_dev_card(player, DevCard.Monopoly, [('card_types', resource_response)])

                # Play robber
                if(response == 6):
                        loc_x_response = args[2]
                        loc_y_response = args[3]
                        # TODO
                        # Tile at r,c index within the array
                        # status = self.game.move_robber()

                # Do trade
                if(response == 7):
                        pass
                        # TODO
                        # this

                        # print('1: Player 1 | 2: Player 2 | 3: Player 3 | 4: Player 4')
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
                if(response == 8):
                        pass
                # Deny trade
                if(response == 9):
                        pass
                if(response == 10):
                        pass
                if(response == 11):
                        pass

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

        def displayPlayerGameInfo(self, player):
                self.displayBoard()
                # Pending trades


        def displayBoard(self):
                self.boardRenderer.render()

        def displayFullGameInfo(self):
                self.displayBoard()
                for player in self.game.players:
                        print('Player ' + str(player.num) + ':')
                        print('Cards:')
                        player.print_cards(player.cards) 
                        print()






class Match:
        def __init__():
                pass


class Agent:
        """
        Demonstrates agent interface.

        In practice, this needs to be instantiated with the right neural network
        architecture.
        """
        def __init__(self, player, is_human, initial_weights):
                self.player = player
                self.is_human = is_human
                self.steps = 0
                self.weights = initial_weights
                self.turnStep = 0;
                self.availableActions = []

        """
        Return actions that can not be played on this turn step
        """
        def getAvailableActions():
                availableActions = []


                """
                Forfeit cards
                - A 7 is rolled and player has > 8 cards so player must select cards to forfeit
                """


                """
                No Op
                - Not playing turn &&
                - No pending trades
                """     

                """
                Purchase
                - Have any permutation of cards that allows purhcasing any items
                """

                """
                Build
                - Have any available buildings
                """

                """
                Play Dev Card
                - Have any available dev cards
                """

                """
                Play Robber
                - Robber flag is active
                """
                pass

        # def initial_state(self):
        #       """Returns the hidden state of the agent for the start of an episode."""
        #       # Network details elided.
        #       return initial_state

        # def set_weights(self, weights):
        #       self.weights = weights

        # def get_steps(self):
        #       """How many agent steps the agent has been trained for."""
        #       return self.steps

        # def step(self, observation, last_state):
        #       """Performs inference on the observation, given hidden state last_state."""
        #       # We are omitting the details of network inference here.
        #       # ...
        #       return action, policy_logits, new_state

        # def unroll(self, trajectory):
        #       """Unrolls the network over the trajectory.

        #       The actions taken by the agent and the initial state of the unroll are
        #       dictated by trajectory.
        #       """
        #       # We omit the details of network inference here.
        #       return policy_logits, baselines



def printBlankLines(num):
        for i in range(0, num):
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


        # Make players into agents
        agents = []
        for player in CatanGame.game.players:
                print('Player ' + str(player.num) + ' human? (y/n)')
                is_human = input()
                if(is_human == 'y'):
                        agents.append(Agent(player, True, []))
                else:
                        agents.append(Agent(player, False, []))


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


        # Game Loop        
        # while(!gameOver):
                # 

        CatanGame.displayFullGameInfo()
        CatanGame.promptActions(CatanGame.game.players[0])

if __name__ == "__main__":
        main()
