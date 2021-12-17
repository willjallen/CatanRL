from board_renderer import BoardRenderer
from pycatan.card import ResCard, DevCard
from pycatan.building import Building
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


class Display:
    def __init__(self, game):
        self.game = game
        self.board_renderer = BoardRenderer(self.game.board, [50, 10])


    def printBlankLines(self, num):
        for i in range(0, num):
            print()


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
        if(response == ROLL):
            pass
        # Prompt No op
        if(response == NO_OP):
            print(1)
        # Prompt Purchase Resource
        if(response == PURCHASE_RESOURCE):
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
        if(response == PURCHASE_AND_PLAY_BUILDING):
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
        if(response == PURCHASE_DEV_CARD):
            pass
        # Prompt Play dev card
        if(response == PLAY_DEV_CARD):
            for allowed_card in allowed_actions['allowed_dev_cards']:
                print(str(allowed_card.value) + ': ' + allowed_card.name + ' | ', end='')
            print()

            dev_card_response = int(input())
            full_action.append(dev_card_response)


            if(dev_card_response == 0):
                pass

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
        if(response == PLAY_ROBBER):
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
        if(response == START_TRADE):

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
        if(response == ACCEPT_TRADE):
            pass
        # Deny trade
        if(response == DENY_TRADE):
            pass
        # Forfeit card
        if(response == FORFEIT_CARDS):
            print('Forfeit(' + str(player.forfeited_cards_left) + ' left): ') 

            for allowed_card in allowed_actions['allowed_forfeit_cards']:
                print(str(allowed_card.value) + ': ' + allowed_card.name + ' | ', end='')
            print()

            player_response = int(input())
            full_action.append(player_response)

        if(response == 11):
            pass

        # Prompt initial road placement
        if(response == INITIAL_PLACE_ROAD):
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
        if(response == INITIAL_PLACE_BUILDING):
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

        if(response == PLACE_ROAD):

            print('Place road:')
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

        return full_action        


    def displayBoard(self):
        self.board_renderer.render()

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


    def displayGameInfo(self):
        print('Turn: ' + str(self.game.turn_counter))
        print('Player with turn: ' + colors[self.game.player_with_turn_index])
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

    def displayFullGameInfo(self):
        self.displayBoard()
        for player in self.game.players:
            print('Player ' + str(player.num) + ':')
            print('Cards:')
            player.print_cards(player.cards) 
            print()
