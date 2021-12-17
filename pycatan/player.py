from pycatan.building import Building
from pycatan.statuses import Statuses
from pycatan.card import ResCard, DevCard

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

# The player class for
class Player:

    def __init__ (self, game, num, agent_type):
        self.agent_type = agent_type
        # the game the player belongs to
        self.game = game
        # the player number for this player
        self.num = num
        # used to track which initial placements the player has made        
        self.num_initial_settlements = 2
        self.num_initial_roads = 2
        self.has_placed_initial_settlement = False
        self.has_completed_initial_placement = False
        self.initial_settlement = None
        # used to determine the longest road
        self.starting_roads = []
        # the number of victory points
        self.victory_points = 0
        # the cards the player has
        # each will be a number corresponding with the static variables CARD_<type>
        self.cards = []
        # the development cards this player has
        self.dev_cards = []
        # the number of knight cards the player has played
        self.knight_cards = 0
        # the longest road segment this player has
        self.longest_road_length = 0
        # whether the player has ended their turn
        self.turn_over = True
        # whether the player has a pending trade
        self.pending_trade = False
        # how many trades this player has requested in a turn
        self.num_trades_in_turn = 0
        # trading player
        self.trading_player = None
        # which card the trading player wants in trade
        self.trade_forfeit_card = None
        # which card the player will receive in trade
        self.trade_receive_card = None
        # number of cards the player must discard (from a 7 roll)
        self.forfeited_cards_left = 0
        # whether the player has played a road building dev card
        self.played_road_building = False
        # how many roads the player has left to place
        self.roads_remaining = 0
        # store the last bought dev card and the turn it was bought on 
        self.last_bought_dev_card = 0
        self.last_bought_dev_card_turn = 0
    # builds a settlement belonging to this player
    def build_settlement(self, point, is_starting=False):

        if not is_starting:
            # makes sure the player has the cards to build a settlements
            cards_needed = [
                ResCard.Wood,
                ResCard.Brick,
                ResCard.Sheep,
                ResCard.Wheat
            ]

            # checks the player has the cards
            if not self.has_cards(cards_needed):
                return Statuses.ERR_CARDS

            # checks it is connected to a road owned by the player
            connected_by_road = False
            # gets the roads
            roads = self.game.board.roads

            for r in roads:
                # checks if the road is connected
                if r.point_one is point or r.point_two is point:
                    # checks this player owns the road
                    if r.owner == self.num:
                        connected_by_road = True

            if not connected_by_road:
                return Statuses.ERR_ISOLATED

        # checks that a building does not already exist there
        if point.building != None:
            return Statuses.ERR_BLOCKED

        # checks all other settlements are at least 2 away
        # gets the connecting point's coords
        points = point.connected_points
        for p in points:

            # checks if the point is occupied
            if p.building != None:
                return Statuses.ERR_BLOCKED

        if not is_starting:
            # removes the cards
            self.remove_cards(cards_needed)

        # adds the settlement
        self.game.board.add_building(Building(
            owner = self.num,
            type = Building.BUILDING_SETTLEMENT,
            point_one = point),
            point = point)
        # adds a victory point
        self.victory_points += 1

        return Statuses.ALL_GOOD

    def can_build_dev(self):
        # makes sure there is still at least one development card left
        if len(self.game.dev_deck) < 1:
            return Statuses.ERR_DECK
        # makes sure the player has the right cards
        needed_cards = [
            ResCard.Wheat,
            ResCard.Ore,
            ResCard.Sheep
        ]
        if not self.has_cards(needed_cards):
            return Statuses.ERR_CARDS
        return Statuses.ALL_GOOD

        # checks if the player has all of the cards given in an array
    def has_cards(self, cards):

        # needs to duplicate the cards, and then delete them once found
        # otherwise checking if the player has multiple of the same card
        # will return true with only one card

        # cards_dup stands for cards duplicate
        cards_dup = self.cards[:]
        for c in cards:
            if cards_dup.count(c) == 0:
                return False
            else:
                index = cards_dup.index(c)
                del cards_dup[index]

        return True

    def get_types_of_cards_possessed(self):
        card_types = []
        for c in self.cards:
            if not(c in card_types):
                card_types.append(c)
        return card_types

    def get_available_buildings(self):
        available_buildings = []

        road_cards = [
            ResCard.Wood,
            ResCard.Brick
        ]

        settlement_cards = [
            ResCard.Wood,
            ResCard.Brick,
            ResCard.Sheep,
            ResCard.Wheat
        ]

        city_cards = [
            ResCard.Wheat,
            ResCard.Wheat,
            ResCard.Ore,
            ResCard.Ore,
            ResCard.Ore
        ]

        if(self.has_cards(settlement_cards)):
            available_buildings.append(Building.BUILDING_SETTLEMENT)

        if(self.has_cards(road_cards)):
            available_buildings.append(Building.BUILDING_ROAD)

        if(self.has_cards(city_cards)):
            available_buildings.append(Building.BUILDING_CITY)

        return available_buildings

    def get_available_robber_placement_tiles_and_victims(self):

        robber_actions = []

        curr_robber = self.game.board.robber
        # checks the victim has a settlement on the tile
        for r in self.game.board.tiles:
            for tile in r:
                # Check this is a different tile than the current robber tile
                if(curr_robber):
                    if(curr_robber.position[0] == tile.position[0] and curr_robber.position[1] == tile.position[1]):
                        # If not, skip this tile
                        continue

                # Iterate over points and check if there is a settlement/city on any of them
                points = tile.points
                for p in points:
                    if p != None and p.building != None:
                        # Check the victim owns the settlement/city and has > 0 cards
                        for player in self.game.players:
                            if(p.building.owner == player.num) and (player.num != self.num) and (len(player.cards) > 0):
                                robber_actions.append((tile, player))
        return robber_actions

    def get_available_road_point_pairs(self):

        road_point_pairs = []



        for r in self.game.board.points:
            for point in r:
                if(point.building):
                    if(point.building.owner == self.num):
                        for local_point in point.connected_points:
                            location_status = self.road_location_is_valid(start=point, end=local_point)
                            if(location_status == Statuses.ALL_GOOD):
                                road_point_pairs.append((point, local_point))


        for road in self.game.board.roads:
            if(road.owner == self.num):
                positions = [road.point_one, road.point_two]
                for point in positions:
                    for local_point in point.connected_points:
                        location_status = self.road_location_is_valid(start=point, end=local_point)
                        if(location_status == Statuses.ALL_GOOD):
                            road_point_pairs.append((point, local_point)) 


        unique_road_point_pairs = []
        [unique_road_point_pairs.append(pair) for pair in road_point_pairs if pair not in unique_road_point_pairs]
        return unique_road_point_pairs


    def get_available_initial_settlement_points(self):
        available_points = []

        for r in self.game.board.points:
            for point in r:

                # Check if there is already a building here
                if(point.building == None):
                    # Get all adjacent points and check for buildings there
                    adj_points_clear = True
                    points = point.connected_points
                    for p in points:
                        if(p.building != None):
                            if(p.building.type == Building.BUILDING_SETTLEMENT or p.building.type == Building.BUILDING_CITY):
                                adj_points_clear = False

                    if(adj_points_clear):
                        available_points.append(point) 

        return available_points


    def get_available_initial_road_point_pairs(self):
        available_points = []

        connected_points = self.initial_settlement.connected_points

        adj_point_clear = True
        for p in connected_points:
            if(p.building != None):
                if(point.building.type == Building.BUILDING_SETTLEMENT or point.building.type == Building.BUILDING_CITY):
                    adj_points_clear = False
            if(adj_point_clear):
                available_points.append((self.initial_settlement, p))

        return available_points

    def get_available_settlement_points(self):

        available_points = []

        for r in self.game.board.points:
            for point in r:
                # checks it is connected to a road owned by the player
                connected_by_road = False
                # gets the roads
                roads = self.game.board.roads

                # checks that a settlement or city does not already exist there
                if(point.building != None):
                    if(point.building.type == Building.BUILDING_SETTLEMENT or point.building.type == Building.BUILDING_CITY):
                        continue

                for r in roads:
                    # checks if the road is connected
                    if r.point_one is point or r.point_two is point:
                        # checks this player owns the road
                        if r.owner == self.num:
                            connected_by_road = True

                if not connected_by_road:
                    continue


                # checks all other settlements are at least 2 away
                # gets the connecting point's coords
                distance_violation = False

                points = point.connected_points

                for p in points:
                    # checks if the point is occupied
                    if(p.building != None):
                        if(p.building.type == Building.BUILDING_SETTLEMENT or p.building.type == Building.BUILDING_CITY):
                            distance_violation = True
                            break

                if(distance_violation):
                    continue

                available_points.append(point)

        return available_points

    def get_available_city_points(self):
        pass

    def has_at_least_num_cards(self, card_type, num):
        return self.cards.count(card_type) >= num



    # adds some cards to a player's hand
    def add_cards(self, cards):
        for c in cards:
            self.cards.append(c)

    # removes cards from a player's hand
    def remove_cards(self, cards):
        # makes sure it has all the cards before deleting any
        if not self.has_cards(cards):
            return Statuses.ERR_CARDS

        else:
            # removes the cards
            for c in cards:
                index = self.cards.index(c)
                del self.cards[index]

    #adds a development card
    def add_dev_card(self, dev_card):
        self.dev_cards.append(dev_card)

    # removes a dev card
    def remove_dev_card(self, card):
        # finds the card
        for i in range(len(self.dev_cards)):
            if self.dev_cards[i] == card:

                # deletes the card
                del self.dev_cards[i]
                return Statuses.ALL_GOOD

        # error if the player does not have the cards
        return Statuses.ERR_CARDS




    # checks a road location is valid
    def road_location_is_valid(self, start, end):
        has_city_owned_point = False
        # checks if this player owns the settlement/city
        # At most one point can be owned by a different player
        if start.building != None:
            if start.building.owner == self.num:
                has_city_owned_point = True

        # does the same for the other point
        if end.building != None:
            if end.building.owner == self.num:
                has_city_owned_point = True

        # # checks the two points are connected
        # connected = False
        # # gets the points connected to start
        # points = start.connected_points

        # for p in points:
        #     if end == p:
        #         connected = True
        #         break

        # if not connected:
        #     return Statuses.ERR_NOT_CON

        # checks the road does not already exists with these points
        for road in self.game.board.roads:
            if (road.point_one == start or road.point_two == start):
                if road.point_one == end or road.point_two == end:
                    return Statuses.ERR_BLOCKED


        # then checks if there is a road connecting them
        has_road_owned_point = False

        roads = self.game.board.roads
        # points = [start, end]

        for r in roads:
            if(r.owner == self.num):
                if (r.point_one == start or r.point_one == end) or (r.point_two == start or r.point_two == end):
                    has_road_owned_point = True
                # checks that there is not another player's settlement here, so that it's not going through it
                # if(p.building == None):
                #     is_connected = True

        if(has_road_owned_point or has_city_owned_point):
            return Statuses.ALL_GOOD
        else:
            return Statuses.ERR_BLOCKED

    def get_available_upgrade_points(self):
        points = []

        for r in self.game.board.points:
            for point in r:
                # Get building at point
                building = point.building

                # checks there is a settlement at r, i
                if building == None:
                    continue

                # checks the settlement is controlled by the correct player
                # if no player is specified, uses the current controlling player
                if building.owner != self.num:
                    continue

                # checks it is a settlement and not a city
                if building.type != Building.BUILDING_SETTLEMENT:
                    continue
                points.append(point)

        return points

    # builds a road
    def build_road(self, start, end, is_starting=False):

        # checks the location is valid
        location_status = self.road_location_is_valid(start=start, end=end)

        if not location_status == Statuses.ALL_GOOD:
            return location_status

        # if the road is being created on the starting turn, the player does not needed
        # to have the cards
        if not is_starting:

            # checks that it has the proper cards
            cards_needed = [
                ResCard.Wood,
                ResCard.Brick
            ]
            if not self.has_cards(cards_needed):
                return Statuses.ERR_CARDS

            # removes the cards
            self.remove_cards(cards_needed)

        # adds the road
        road = Building(owner=self.num, type=Building.BUILDING_ROAD, point_one=start, point_two=end)
        (self.game).board.add_road(road)

        self.get_longest_road(new_road=road)

        return Statuses.ALL_GOOD

    # returns an array of all the harbors the player has access to
    def get_connected_harbor_types(self):

        # gets the settlements/cities belonging to this player
        harbors = []
        all_harbors = self.game.board.harbors
        buildings = self.game.board.get_buildings()

        for b in buildings:
            # checks the building belongs to this player
            if b.owner == self.num:
                # checks if the building is connected to any harbors
                for h in all_harbors:
                    # print(h)
                    # print(b.point)
                    if h.point_one is b.point or h.point_two is b.point:
                        # print("A")
                        # adds the type
                        if harbors.count(h.type) == 0:
                            harbors.append(h.type)

        return harbors

    # gets the longest road segment this player has which includes the road given
    # should be called whenever a new road is build
    # since this player's longest road will only change if a new road is build
    def get_longest_road(self, new_road):

        # gets the roads that belong to this player
        roads = self.get_roads()

        roads_c = roads[:];
        for road in roads_c:
            # remove the new road from all player roads
            del roads_c[roads_c.index(road)]
            # checks for longest road
            self.check_connected_roads(road=road, all_roads=roads_c, length=1)
            roads_c = roads[:];

    # checks the roads for connected roads, and then checks those roads until there are no more
    def check_connected_roads(self, road, all_roads, length):
        # print()
        # print('---------------')
        # print('Current Road: ')
        # print(road)
        # print()

        # print('All available roads: ')
        # print(all_roads)
        # print()

        # print('Current length: ')
        # print(length)
        # print()

        # do both point one and two
        points = [
            road.point_one,
            road.point_two
        ]

        for p in points:
            # gets the connected roads
            connected = self.get_connected_roads(point=p, roads=all_roads)
            # print('Connected roads at point: ', p)
            # print(connected)
            # print()
            # print('---------------')
            # if there are no new connected roads
            if len(connected) == 0:
                # if this is the longest road so far
                if length > self.longest_road_length:
                    # records the length
                    self.longest_road_length = length
                    # print('longest_road_length: ', self.longest_road_length)
                    # if(length == 7):
                    #     quit()
                    # self.begin_celebration()

            # if there are connected roads
            else:
                c_roads = all_roads[:]

                # check each of them for connections if they have not been used
                for c in connected:

                    # print('road ' + str(c) + ' in connected');
                    # checks it hasn't used this road before
                    del c_roads[c_roads.index(c)]

                for c in connected:    
                    self.check_connected_roads(c, c_roads, length + 1)

    # returns which roads in the roads array are connected to the point
    def get_connected_roads(self, point, roads):
        con_roads = []
        for r in roads:
            if r.point_one == point or r.point_two == point:
                con_roads.append(r)

        return con_roads

    # returns an array of all the roads belonging to this player
    def get_roads(self):
        # gets all the roads on the board
        all_roads = (self.game).board.roads
        # filters out roads that do not belong to this player
        roads = []
        for r in all_roads:
            if r.owner == self.num:
                roads.append(r)

        return roads

    # checks if the player has some development cards
    def has_dev_cards(self, cards):
        card_duplicate = self.dev_cards[:]
        for c in cards:
            if not card_duplicate.count(c) > 0:
                return False
            else:
                del card_duplicate[card_duplicate.index(c)]

        return True

    # returns the number of VP
    # if include_dev is False, it will not include points from developement cards
    # because other players aren't able to see them
    def get_VP(self, include_dev=False):

        # gets the victory points from settlements and cities
        points = self.victory_points

        # adds VPs from longest road
        if self.game.longest_road_owner == self.num:
            points += 2

        # adds VPs from largest army
        if self.game.largest_army == self.num:
            points += 2

        # adds VPs from developement cards
        if include_dev:
            for d in self.dev_cards:
                if d == DevCard.VictoryPoint:
                    points += 1

        return points

    # prints the cards given
    @staticmethod
    def print_cards(cards):
        print("[")
        for c in cards:

            card_name = ""

            if c == ResCard.Wood:
                card_name = "Wood"

            elif c == ResCard.Sheep:
                card_name = "Sheep"

            elif c == ResCard.Brick:
                card_name = "Brick"

            elif c == ResCard.Wheat:
                card_name = "Wheat"

            elif c == ResCard.Ore:
                card_name = "Ore"

            elif c == DevCard.Road:
                card_name = "Road"

            elif c == DevCard.VictoryPoint:
                card_name = "VP"

            elif c == DevCard.Knight:
                card_name = "Knight"

            elif c == DevCard.Monopoly:
                card_name = "Monopoly"

            elif c == DevCard.YearOfPlenty:
                card_name = "YOP"

            else:
                print("INVALID CARD %s" % c)
                continue

            if cards.index(c) < len(cards) - 1:
                card_name += ","

            print("    %s" % card_name)

        print("]")
