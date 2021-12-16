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
from match import Match
import random

def main():
    
    # GLOBAL SETTINGS
    
    print_mode = False
    user_mode = False

    number_of_players = 4

    number_of_matches = 1000
    matches_played = 0

    for i in range(0, number_of_matches):
        match = Match(number_of_players, print_mode, user_mode, ['R', 'R', 'R', 'R'])
        match.begin()

        matches_played += 1
        print('Match #', matches_played)



if __name__ == "__main__":

    # Profiling
    cProfile.runctx('main()', globals(), locals(), 'restats')
    p = pstats.Stats('restats')
    p.strip_dirs().sort_stats(SortKey.TIME).print_stats(10)
    p.print_stats()
    # main()
