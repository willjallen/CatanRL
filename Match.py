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
import random
import copy


import pickle as cPickle

# import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers

class Match():
    def __init__(self, game_number, num_of_players, agent_type_arr, display):

        # threading.Thread.__init__(self)
        self.game_number = game_number
        self.num_of_players = num_of_players
        self.agent_type_arr = agent_type_arr
        self.display = display

        # Record statistics
        self.game_states = []
        self.match_id = 0

        self.currrent_step = 0
        self.largest_step = 0

        self.bind_game_obj = False

        self.game = Game(game_number=self.game_number, 
            num_of_players=self.num_of_players, agent_type_arr=self.agent_type_arr)
        # self.game.add_settlement(0, self.game.board.points[3][0], is_starting=True)
        # self.game.add_settlement(0, (0,1))
        # self.game.add_settlement(0, (0,2))
        if(display):
            self.display.new_game(self.game)
        self.winner = 0
        print('new game')




    def step(self):



        # Tick display
        if(self.display):

            # if(self.game_states): print(self.game_states[self.currrent_step - 1].step_count)
            if(self.display.control_display.play_button.toggled or self.display.control_display.step_forward_button_toggled):
                self.currrent_step += 1
                if(self.currrent_step > self.largest_step):
                    if self.bind_game_obj:
                        self.display.set_game(self.game)
                        self.bind_game_obj = False
                    self.step_game()
                    # self.display.set_game(self.game)                        
                else:
                    self.display.set_game(self.game_states[self.currrent_step-1])
                    self.bind_game_obj = True



                self.display.control_display.step_forward_button_toggled = False

            if(self.display.control_display.rewind_button.toggled or self.display.control_display.step_back_button_toggled):
                self.currrent_step -= 1
                self.bind_game_obj = True
                if(self.currrent_step >= 1):
                    self.display.set_game(self.game_states[self.currrent_step-1])
                else:
                    self.currrent_step = 0

                self.display.control_display.step_back_button_toggled = False

            self.display.tick()
            # print('curr ', self.currrent_step)
            # print('largest ', self.largest_step)
        else:
            self.step_game()


        # Save game states to disk
        # self.serialize()

        # cPickle_off = open("data.txt", "rb")
        # file = cPickle.load(cPickle_off)

    def step_game(self):
        self.game.step()
        if( self.display):
            self.game_states.append(copy.deepcopy(self.game))
        self.largest_step += 1
        # Save game state
        # self.serialize()

    def serialize(self):
        self.game_states.append(cPickle.dumps(self.game))
