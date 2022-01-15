import cProfile
import pstats
from pstats import SortKey

from pycatan import Player
from pycatan import Game
from pycatan import Statuses
from pycatan import Building
from pycatan.card import ResCard, DevCard
from agent import Agent
from random_agent import RandomAgent
from match import Match
import random

from display.visual_display import VisualDisplay

import time

def main():

    # GLOBAL SETTINGS

    print_mode = False
    user_mode = False

    display_mode = True
    display = None
    if(display_mode):
        display = VisualDisplay()

    number_of_players = 4

    number_of_matches = 500
    matches_played = 0
    turns_played = 0

    for i in range(0, number_of_matches):
        match = Match(game_number=i, num_of_players=number_of_players, agent_type_arr=['R', 'R', 'R', 'R'], display=display)
        match.begin()

        matches_played += 1
        turns_played += match.game.turn_counter
        print('Match #', matches_played)




    print('Total turns played', turns_played)
    print('Average time / turn')

def profile():
    pass

if __name__ == "__main__":

    # Profiling
    cProfile.runctx('main()', globals(), locals(), 'restats')
    p = pstats.Stats('restats')
    p.strip_dirs().sort_stats(SortKey.TIME).print_stats(10)
    p.print_stats()
    # main()
