import cProfile
import pstats
from pstats import SortKey

from pycatan import Player
from pycatan import Game
from pycatan import Statuses
from pycatan import Building
from pycatan.card import ResCard, DevCard
from board_renderer import BoardRenderer
from display import Display
from agent import Agent
from random_agent import RandomAgent
import random

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


class GameWrapper:
    def __init__(self, headless=False):

        self.num_of_players = 0
        self.game = Game(4)
        self.agents = []




        self.game.run()

    def run(self, player_index):
        self.game.run(player_index)




CatanGame = GameWrapper()
CatanGame.run()
