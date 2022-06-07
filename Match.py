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

        self.game = Game(game_number=self.game_number, 
            num_of_players=self.num_of_players, agent_type_arr=self.agent_type_arr)
        # self.game.add_settlement(0, self.game.board.points[3][0], is_starting=True)
        # self.game.add_settlement(0, (0,1))
        # self.game.add_settlement(0, (0,2))
        if(display):
            self.display.new_game(self.game)
        self.winner = 0
        print('new game')




    def begin(self):
        # num_inputs = 4
        # num_actions = 2
        # num_hidden = 128

        # inputs = layers.Input(shape=(num_inputs,))
        # common = layers.Dense(num_hidden, activation="relu")(inputs)
        # action = layers.Dense(num_actions, activation="softmax")(common)
        # critic = layers.Dense(1)(common)

        # model = keras.Model(inputs=inputs, outputs=[action, critic])

        # optimizer = keras.optimizers.Adam(learning_rate=0.01)
        # huber_loss = keras.losses.Huber()
        # action_probs_history = []
        # critic_value_history = []
        # rewards_history = []
        # running_reward = 0
        # episode_count = 0

        # print(self.game.board.tiles)
        # return

        while(not self.game.has_ended):
            # Prompts action from player and updates game state

            # Tick display
            if(self.display):
                print('curr ', self.currrent_step)
                print('largest ', self.largest_step)
                # if(self.game_states): print(self.game_states[self.currrent_step - 1].step_count)
                if(self.display.control_display.play_button.toggled or self.display.control_display.step_forward_button_toggled):
                    self.currrent_step += 1
                    if(self.currrent_step > self.largest_step):
                        self.step_game()
                        self.display.set_game(self.game)                        
                    else:
                        self.display.set_game(self.game_states[self.currrent_step - 1])



                    self.display.control_display.step_forward_button_toggled = False

                if(self.display.control_display.step_back_button_toggled):
                    self.currrent_step -= 1
                    if(self.currrent_step >= 0):
                        self.display.set_game(self.game_states[self.currrent_step - 1])

                    self.display.control_display.step_back_button_toggled = False

                

            else:
                self.step_game()
            # print(self.game.board.roads)

            self.display.tick()


        # Save game states to disk
        self.serialize()
        # self.winner = self.game_states[len(self.game_states)-1].curr_player_index

        # cPickle_off = open("data.txt", "rb")
        # file = cPickle.load(cPickle_off)

    def step_game(self):
        self.game.step()
        self.game_states.append(copy.deepcopy(self.game))
        self.largest_step += 1
        # Save game state
        # self.serialize()

    def serialize(self):
        self.game_states.append(cPickle.dumps(self.game))

        # self.game.players[0].cards.append(ResCard(0))
        # self.game.players[0].cards.append(ResCard(1))

    #     with tf.GradientTape() as tape:
    #         for timestep in range(1, max_steps_per_episode):
    #             # env.render(); Adding this line would show the attempts
    #             # of the agent in a pop up window.

    #             state = tf.convert_to_tensor(state)
    #             state = tf.expand_dims(state, 0)

    #             # Predict action probabilities and estimated future rewards
    #             # from environment state
    #             action_probs, critic_value = model(state)
    #             critic_value_history.append(critic_value[0, 0])

    #             # Sample action from action probability distribution
    #             action = np.random.choice(num_actions, p=np.squeeze(action_probs))
    #             action_probs_history.append(tf.math.log(action_probs[0, action]))

    #             # Apply the sampled action in our environment
    #             state, reward, done, _ = env.step(action)
    #             rewards_history.append(reward)
    #             episode_reward += reward

    #             if done:
    #                 break

    #         # Update running reward to check condition for solving
    #         running_reward = 0.05 * episode_reward + (1 - 0.05) * running_reward

    #         # Calculate expected value from rewards
    #         # - At each timestep what was the total reward received after that timestep
    #         # - Rewards in the past are discounted by multiplying them with gamma
    #         # - These are the labels for our critic
    #         returns = []
    #         discounted_sum = 0
    #         for r in rewards_history[::-1]:
    #             discounted_sum = r + gamma * discounted_sum
    #             returns.insert(0, discounted_sum)

    #         # Normalize
    #         returns = np.array(returns)
    #         returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
    #         returns = returns.tolist()

    #         # Calculating loss values to update our network
    #         history = zip(action_probs_history, critic_value_history, returns)
    #         actor_losses = []
    #         critic_losses = []
    #         for log_prob, value, ret in history:
    #             # At this point in history, the critic estimated that we would get a
    #             # total reward = `value` in the future. We took an action with log probability
    #             # of `log_prob` and ended up recieving a total reward = `ret`.
    #             # The actor must be updated so that it predicts an action that leads to
    #             # high rewards (compared to critic's estimate) with high probability.
    #             diff = ret - value
    #             actor_losses.append(-log_prob * diff)  # actor loss

    #             # The critic must be updated so that it predicts a better estimate of
    #             # the future rewards.
    #             critic_losses.append(
    #                 huber_loss(tf.expand_dims(value, 0), tf.expand_dims(ret, 0))
    #             )

    #         # Backpropagation
    #         loss_value = sum(actor_losses) + sum(critic_losses)
    #         grads = tape.gradient(loss_value, model.trainable_variables)
    #         optimizer.apply_gradients(zip(grads, model.trainable_variables))

    #         # Clear the loss and reward history
    #         action_probs_history.clear()
    #         critic_value_history.clear()
    #         rewards_history.clear()

    # # Log details
    # episode_count += 1
    # if episode_count % 10 == 0:
    #     template = "running reward: {:.2f} at episode {}"
    #     print(template.format(running_reward, episode_count))

    # if running_reward > 195:  # Condition to consider the task solved
    #     print("Solved at episode {}!".format(episode_count))
    #     break
        



        # self.game.run()

    # Handle piping to files and general housekeeping
