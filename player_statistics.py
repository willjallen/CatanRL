from pycatan import Player
from pycatan import Game
from pycatan import Statuses
from pycatan import Building
from pycatan.card import ResCard, DevCard
from board_renderer import BoardRenderer
from display import Display
from agent import Agent
from random_agent import RandomAgent
from match import Match
import random

class PlayerStatistics:
	def __init__(self):
		# Record statistics
		self.wood_collected = 0
		self.brick_collected = 0
		self.ore_collected = 0
		self.sheep_collected = 0
		self.wheat_collected = 0
    
    	

    # Wood = 0
    # Brick = 1
    # Ore = 2
    # Sheep = 3
    # Wheat = 4


