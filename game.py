from pycatan import Game
from board_renderer import BoardRenderer

action_types = ["no_op", "purchase", "build", "play_dev_card", "play_robber", "forfeit_cards", "bank_trade", "start_trade", "accept_trade", "deny_trade", "end_turn"]


def main():

	num_of_players = 4

	game = Game()
	#print(game.board.tiles)

	# game.add_settlement(player=0, point=game.board.points[0][0], is_starting=True)
	# game.add_settlement(player=1, point=game.board.points[2][3], is_starting=True)
	# game.add_settlement(player=2, point=game.board.points[4][1], is_starting=True)
	# Add some roads
	game.add_road(player=0, start=game.board.points[0][0], end=game.board.points[0][1], is_starting=True)
	game.add_road(player=1, start=game.board.points[2][3], end=game.board.points[2][2], is_starting=True)
	game.add_road(player=2, start=game.board.points[4][1], end=game.board.points[4][0], is_starting=True)




	boardRenderer = BoardRenderer(game.board, [50, 10])
	boardRenderer.render()

if __name__ == "__main__":
	main()

class Match:
	def __init__():
		pass


class Agent:
	"""
	Demonstrates agent interface.

	In practice, this needs to be instantiated with the right neural network
	architecture.
	"""
	def __init__(player, initial_weights):
		self.steps = 0
		self.weights = initial_weights
		self.turnStep = 0;
		self.availableActions = []

	"""
	Return actions that can not be played on this turn step
	"""
	def getAvailableActions():
		availableActions = []


		"""
		Forfeit cards
		- A 7 is rolled and player has > 8 cards so player must select cards to forfeit
		"""


		"""
		No Op
		- Not playing turn &&
		- No pending trades
		"""	

		"""
		Purchase
		- Have any permutation of cards that allows purhcasing any items
		"""

		"""
		Build
		- Have any available buildings
		"""

		"""
		Play Dev Card
		- Have any available dev cards
		"""

		"""
		Play Robber
		- Robber flag is active
		"""
		pass

	# def initial_state(self):
	# 	"""Returns the hidden state of the agent for the start of an episode."""
	# 	# Network details elided.
	# 	return initial_state

	# def set_weights(self, weights):
	# 	self.weights = weights

	# def get_steps(self):
	# 	"""How many agent steps the agent has been trained for."""
	# 	return self.steps

	# def step(self, observation, last_state):
	# 	"""Performs inference on the observation, given hidden state last_state."""
	# 	# We are omitting the details of network inference here.
	# 	# ...
	# 	return action, policy_logits, new_state

	# def unroll(self, trajectory):
	# 	"""Unrolls the network over the trajectory.

	# 	The actions taken by the agent and the initial state of the unroll are
	# 	dictated by trajectory.
	# 	"""
	# 	# We omit the details of network inference here.
	# 	return policy_logits, baselines


