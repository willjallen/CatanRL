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

        ## This stuff can be done after multi-threading and proper piping to files for better analysis)

        # Board Exposure
        # self.

        # Resources
        self.wood_collected = 0
        self.brick_collected = 0
        self.ore_collected = 0
        self.sheep_collected = 0
        self.wheat_collected = 0

    # Dev Cards
    self.knights_collected = 0
    self.YOP_collected = 0
    self.road_building_collected = 0
    self.VP_collected = 0

        # Buyables
    self.settlements_placed = 0
    self.cities_placed = 0
    self.roads_built = 0
    self.dev_cards_bought = 0

    # Trades to bank / port (Do averages for this section like 0.45 wood per 1 stone to account for 3:1 point and stuff)
    # self.


    # Trades
    self.trades_conducted = 0
    self.wood_traded_received = 0

    # 


# Wood = 0
# Brick = 1
# Ore = 2
# Sheep = 3
# Wheat = 4


