import math
import numpy as np

def log_scale(L, k, x0, x):
    x = max(L, x)
    return math.max(0, (1/k) * math.ln(-y/(y- L)) + x0)




class NNState:
    # Basically serialize game object
    def __init__(self, game, agent):
        self.game = game
        self.agent = agent
        self.player = agent.player



    def preprocess_scalars(self):
        game = self.game
        # Game info


        #TODO, maybe normalize these as games get shorter?
        # logarithmically transformed with max 400
        # x_0 = 0.5, k = 10, L = 400
        turn_counter = np.array([math.min(1, log_scale(400, 10, 0.5, game.turn_counter))])
        
        # logarithmically transformed with max 4000
        # x_0 = 0.5, k = 10, L = 4000
        step_counter = np.array([math.min(1, log_scale(4000, 10, 0.5, game.step_counter))])

        # one hot with maximum of 1
        initial_placement_mode = np.array([1 if game.initial_placement_mode else 0])

        # one hot with maximum of 1
        give_initial_yield_flag = np.array([1 if game.give_initial_yield_flag else 0])
        
        # one hot with maximum of 4
        longest_road_owner = np.array([int(i == game.longest_road_owner.num) for i in range(4)])

        # one hot with maximum of 4
        largest_army_owner = np.array([int(i == game.largest_army_owner.num) for i in range(4)])
        
        # one hot with maximum of 4
        player_with_turn = np.array([int(i == game.player_with_turn_index) for i in range(4)])
        
        # one hot with maximum of 4
        current_player = np.array([int(i == game.curr_player_index) for i in range(4)])

        # one hot with maximum of 1
        can_roll = np.array([1 if game.can_roll else 0])
        
        # one hot with maximum of 12    
        last_roll = np.array([int(i == game.last_roll) for i in range(12)])

        # one hot with maximum of 1
        rolled_seven = np.array([1 if game.rolled_seven else 0])
        
        # one hot with maximum of 1
        robber_moved = np.array([1 if game.robber_moved else 0])

        # one hot with maximum of 4
        player_num = np.array([int(i == self.player.num) for i in range(4)])


        # one hot with maximum of 14
        available_actions = np.array([int(i == game.available_actions) for i in range(14)])


        preprocessed_scalars = np.concatenate((
            turn_counter, 
            step_counter, 
            initial_placement_mode, 
            give_initial_yield_flag, 
            longest_road_owner,
            largest_army_owner,
            player_with_turn,
            current_player,
            can_roll,
            last_roll,
            rolled_seven,
            robber_moved,
            player_num
            ), axis=None)

        return preprocessed_scalars



    # Preproccesing for entities (players)
    def preprocess_entities(self):
        # self.game_ended = np.array([int(i == 5) for i in range(1)])
        preprocessed_entities = np.array()
        # For all four players (max 4)
        for i in range(0, 3):
            player = self.game.players[i]
            # Player info

            # one hot with maximum of 4
            player_num = np.array([int(i==player.num) for i in range(4)])

            # one hot with maximum of 1
            has_placed_initial_settlement = np.array([1 if player.has_placed_initial_settlement else 0])
            
            # one hot with maximum of 1
            has_placed_initial_road = np.array([1 if player.has_placed_initial_road else 0])

            # one hot with maximum of 5
            knight_cards_played = np.array([int(i == player.knight_cards) for i in range(5)])

            # one hot with maximum of 10
            victory_points = np.array([int(i==player.victory_points) for i in range(10)])

            # one hot with maximum of 1
            turn_to_play = np.array([0 if player.turn_over else 1])
            
            # one hot with maximum of 1
            pending_trade = np.array([1 if player.pending_trade else 0])

            # one hot with maximum of 4
            num_trades_in_turn = np.array([int(i == player.num_trades_in_turn) for i in range(4)])

            # one hot with maximum of 4
            trading_player = np.array([int(i == player.trading_player.num) for i in range(4)])
            
            # one hot with maximum of 5
            trade_forfeit_card = np.array([int(i == player.trade_forfeit_card.value) for i in range(5)])

            # one hot with maximum of 5
            trade_receive_card = np.array([int(i == player.trade_forfeit_card.value) for i in range(5)])

            # one hot with maximum of 10
            forfeited_cards_left = np.array([int(i == player.forfeited_cards_left) for i in range(10)])

            # one hot with maximum of 1
            played_road_building = np.array([1 if player.played_road_building else 0])

            # Resource Cards
            # one hot with maximum of 8
            num_wood_cards = np.array([int (i == [player.cards.count(ResCard.Wood)]) for i in range(12)])
            # one hot with maximum of 8
            num_brick_cards = np.array([int (i == [player.cards.count(ResCard.Brick)]) for i in range(12)])
            # one hot with maximum of 8
            num_ore_cards = np.array([int (i == [player.cards.count(ResCard.Ore)]) for i in range(12)])
            # one hot with maximum of 8
            num_sheep_cards = np.array([int (i == [player.cards.count(ResCard.Sheep)]) for i in range(12)])
            # one hot with maximum of 8
            num_wheat_cards = np.array([int (i == [player.cards.count(ResCard.Wheat)]) for i in range(12)])

            # Dev Cards
            # one hot with maximum of 5
            num_victory_point_cards = np.array([int (i == [player.dev_cards.count(DevCard.VictoryPoint)]) for i in range(5)])
            # one hot with maximum of 14
            num_knight_cards = np.array([int (i == [player.dev_cards.count(DevCard.Knight)]) for i in range(14)])
            # one hot with maximum of 2
            num_monopoly_cards = np.array([int (i == [player.dev_cards.count(ResCard.Monopoly)]) for i in range(2)])
            # one hot with maximum of 2
            num_year_of_plenty_cards = np.array([int (i == [player.dev_cards.count(ResCard.Wheat)]) for i in range(2)])
            # one hot with maximum of 2
            num_road_cards = np.array([int (i == [player.dev_cards.count(DevCard.Road)]) for i in range(2)])


            preprocessed_entities = np.concatenate((preprocessed_entities, 
                player_num,
                has_placed_initial_settlement,
                has_placed_initial_road,
                knight_cards_played,
                victory_points,
                turn_to_play,
                pending_trade,
                num_trades_in_turn,
                trading_player,
                trade_forfeit_card,
                trade_receive_card,
                forfeited_cards_left,
                played_road_building,
                num_wood_cards,
                num_brick_cards,
                num_ore_cards,
                num_sheep_cards,
                num_wheat_cards,
                num_road_cards,
                num_victory_point_cards,
                num_knight_cards,
                num_monopoly_cards,
                num_year_of_plenty_cards
                ))

        return preprocessed_entities



    def preprocess_board(self):
        game = self.game
        # Points
        for row in game.board.points:
            for point in row:
                # (Re_0, Rs_0, Re_1, Rs_1, Re_2, Rs_2, port, robber, Building, player #, buildable)
                if(point.tiles[0]):
                    # one hot with maximum of 5
                    resource_type_one = np.array([int (i == [point.tiles[0].type.value]) for i in range(5)])
                
                if(point.tiles[1]):
                    # one hot with maximum of 5
                    resource_type_two = np.array([int (i == [point.tiles[1].type.value]) for i in range(5)])

                if(point.tiles[2]):
                    # one hot with maximum of 5
                    resource_type_two = np.array([int (i == [point.tiles[2].type.value]) for i in range(5)])



        pass

    # def unpack_game_state():
    #     pass

    # def get_game_state():
    #     return game


# Game Object State



# def one_hot_encode(length, conditionFunc):
# 	return np.array([int(i == ?) for i in range(0, length)])

# Neural Network state

# 1-D Tensor (Input)
# ------------Categorical:------------------ 
# Game:
# assigned player num
# self.assigned_player_num = np.array([int(i == )])

# curent player playing [0, 3]

# Player's cards (P_0):
# 	resource cards [0,4]
# 	-># of each [0, 9]

# 	dev cards [0,2]
# 	-># of each [0, 9]
# 	buildings [0,2]
# 	-># of each [0, 1]

# Other player's (P_1, P_2, P_3) cards:
# 	resource cards [0,4]
# 	-># of each [0, 9]
# 	dev cards [0,20]
# 	-># of each [0, 9]
# 	buildings [0,2]
# 	-># of each [0, 1]

# ------------Numerical:------------------
# int victoryPoints [0,10]
# victory_points = []
# int currTurn [0,?]
# int currStep [0,?]

# ------------Spacial:------------------
# 48 action points * 
# (Re_0, Rs_0, Re_1, Rs_1, Re_2, Rs_2, port, robber, Building, player #, buildable)


# Re_0 (OHE) [5]
# Rs_0 (norm[0, 12]) [1]
# Re_1 (OHE) [5]
# Rs_1 (norm[0, 12]) [1]
# Re_2 (OHE) [5]
# Rs_2 (norm[0, 12]) [1]

