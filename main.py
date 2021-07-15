from pycatan import Game
from board_renderer import BoardRenderer

action_types = ["no_op", "purchase_resource", "purchase_and_play_building", "purchase_dev_card", "play_dev_card", "play_robber", "start_trade", "accept_trade", "deny_trade", "forfeit_cards", "end_turn"]


class GameWrapper:
        def __init__(self):
                num_of_players = 4

                game = Game(num_of_players)
                game.add_settlement(player=0, point=game.board.points[0][0], is_starting=True)
                game.add_settlement(player=1, point=game.board.points[2][3], is_starting=True)
                game.add_settlement(player=2, point=game.board.points[4][1], is_starting=True)
                # Add some roads
                game.add_road(player=0, start=game.board.points[0][0], end=game.board.points[0][1], is_starting=True)
                game.add_road(player=1, start=game.board.points[2][3], end=game.board.points[2][2], is_starting=True)
                game.add_road(player=2, start=game.board.points[4][1], end=game.board.points[4][0], is_starting=True)
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

        def doAction(self, player, full_action):
                action_type = full_action[0]

                  # No op
                if(response == 1):
                        pass
                # Purchase Resource
                if(response == 2):
                        requested_resource = full_action[1]
                        forfeited_resource = full_action[2]
                        # TODO
                        # Forfeited resource needs to be sent as [card, card, card, card]
                        # And check to occur if player has a port to send instead as [card, card, card] or otherwise
                        # self.game.trade_to_bank(player, forfeited_resource, requested_resource)
                # Purchase & play building
                if(response == 3):
                        building_response = full_action[1]
                        loc_x_response = full_action[2]
                        loc_y_response = full_action[3]
                        if(building_response == 1):
                                loc_x_response_2 = full_action[4]
                                loc_y_response_2 = full_action[5]     
                                status = player.build_road(point(loc_x_response, loc_y_response), point(loc_x_response_2, loc_y_response_2))
                        if(building_response == 2):
                                status = player.build_settlement(point(loc_x_response, loc_y_response))
                        if(building_response == 3):
                                status = self.game.add_city(point(loc_x_response, loc_y_response), player)

                # Purchase dev card
                if(response == 4):
                        status = self.game.build_dev(player)

                # Play Item
                if(response == 5):
                        dev_card_response = full_action[1]
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
                                loc_x_response = full_action[2]
                                loc_y_response = full_action[3]
                                # TODO
                                # Tile at r,c index within the array
                                # status = self.game.move_robber()
                        # YOP
                        if(dev_card_response == 2):
                                first_resource_response = full_action[2]
                                second_resource_response = full_action[3]
                                status = self.game.use_dev_card(player, DevCard.YearOfPlenty, [('card_one', first_resource_response), ('card_two', second_resource_response)])
                        # Monopoly
                        if(dev_card_response == 3):
                                resource_response = full_action[2]
                                status = self.game.use_dev_card(player, DevCard.Monopoly, [('card_types', resource_response)])

                # Play robber
                if(response == 6):
                        loc_x_response = full_action[2]
                        loc_y_response = full_action[3]
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
        def __init__(self, player, initial_weights):
                self.player = player
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




def main():

        # Init
        CatanGame = GameWrapper()

        # Make players into agents
        agents = []
        for player in CatanGame.game.players:
                agents.append(Agent(player, []))

        # while(!gameOver):


        CatanGame.displayFullGameInfo()
        CatanGame.promptActions(CatanGame.game.players[0])

if __name__ == "__main__":
        main()
