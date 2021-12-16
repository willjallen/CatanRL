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

class Match:
    def __init__(self, num_of_players, print_mode, user_mode, agent_type_arr):
        self.print_mode = print_mode
        self.user_mode = user_mode
        self.num_of_players = num_of_players

        self.agent_type_arr = agent_type_arr
        
        # Record statistics


        pass

    def begin(self):
        game = Game(num_of_players=self.num_of_players, print_mode=self.print_mode, user_mode=self.user_mode, agent_type_arr=self.agent_type_arr)
        game.run()

