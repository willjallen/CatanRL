


class NNState:
    # Basically serialize game object
    def __init__(self, game):
        pass

    # 
    def def_build_NN_state(self):
        # Game info
        self.initial_placement_mode = np.array([int(i == 5) for i in range(6)])
        self.give_initial_yield_flag = np.array([int(i == 5) for i in range(1)])
        self.longest_road_owner = np.array([int(i == 5) for i in range(1)])
        self.largest_army_owner_label = np.array([int(i == 5) for i in range(1)])
        # self.game_ended = np.array([int(i == 5) for i in range(1)])
        self.turn_counter = np.array([int(i == 5) for i in range(1)])
        self.step_counter = np.array([int(i == 5) for i in range(1)])

        # Turn info
        self.player_with_turn = np.array([int(i == 5) for i in range(1)])
        self.current_player = np.array([int(i == 5) for i in range(1)])

        self.can_roll = np.array([int(i == 5) for i in range(1)])
        self.last_roll = np.array([int(i == 5) for i in range(1)])
        self.rolled_seven = np.array([int(i == 5) for i in range(1)])
        self.robber_moved = np.array([int(i == 5) for i in range(1)])

        # Player info
        self.player_num = np.array([int(i == 5) for i in range(1)])
        self.placed_initial_settlement = np.array([int(i == 5) for i in range(1)])
        self.placed_initial_road = np.array([int(i == 5) for i in range(1)])
        self.knight_cards_played = np.array([int(i == 5) for i in range(1)])
        self.longest_road = np.array([int(i == 5) for i in range(1)])
        # self.dev_cards = 
        # self.

        self.current_player_playing = np.array([int(i == self.game.player_with_turn_index) for i in range(4)])
        # Trade:
        # player's trading partner [0,2] (OHE)
        self.trading_player = np.array([int(i == self.game.) for i in range(2)])
        # Offered resource cards [0, 4] (OHE)
        self.offered_resource_cards = np.array([int(i == 5) for i in range(4)])
        # Expected resource cards [0, 4] (OHE)
        self.expected_resource_cards = np.array([int(i == 5) for i in range(4)])

        # Player:
        # turn to play [0,1] (OHE)
        self.turn_to_play = np.array([int(i == 5) for i in range(1)])
        # pending trade [0,1] (OHE)
        self.pending_trade = np.array([int(i == 5) for i in range(1)])
        # available actions [0, 14] (OHE)
        self.available_actions = np.array([int(i == self.) for i in range(14)])

        player_0_num_wheat_cards = np.array([])

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
victory_points = []
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

