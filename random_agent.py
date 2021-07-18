from pycatan.card import ResCard, DevCard
from agent import Agent
import random


class RandomAgent():
	def __init__(self, player):
		self.player = player
		self.human = False

	def doTurn(self, allowed_actions):
		action = random.choice(allowed_actions['allowed_actions'])
		full_action = []

		full_action.append(action)
		# Roll
		if(action == 0):
			pass
		# Prompt No op
		if(action == 1):
				print(1)
		# Prompt Purchase Resource
		if(action == 2):
			requested_resource = random.choice(list(ResCard)).value
			full_action.append(requested_resource)
			forfeited_resource = random.choice(allowed_actions['allowed_bank_trade_cards'][0])
			full_action.append(forfeited_resource)
		# Prompt Purchase & play building
		if(action == 3):
				building_response = random.choice(allowed_actions['allowed_buildings'])
				full_action.append(building_response)

				
				# Settlement
				if(building_response == 0):
						loc = random.choice(allowed_actions['allowed_settlement_points'])
						full_action.append(loc.position[0])
						full_action.append(loc.position[1])


				# Road
				if(building_response == 1):
						loc = random.choice(allowed_actions['allowed_road_point_pairs'])
						print(loc)
						full_action.append(loc[0].position[0])
						full_action.append(loc[0].position[1])
						full_action.append(loc[1].position[0])
						full_action.append(loc[1].position[1])

				# City
				if(building_response == 2):
					pass
						# print('Allowed Locations: (r, i)')
						# print(possible_actions['allowed_city_points'])

						# print('r:')
						# loc_r_response = int(input())
						# full_action.append(loc_r_response)
						# print('i:')
						# loc_i_response = int(input())
						# full_action.append(loc_i_response)

		# Prompt Purchase dev card
		if(action == 4):
				pass
		# Prompt Play dev card
		if(action == 5):
				dev_card = random.choice(allowed_actions['allowed_dev_cards'])
				full_action.append(dev_card)

				# Knight
				if(dev_card == 2):
						choice = random.choice(allowed_actions['allowed_robber_tiles'])
						loc = choice[0]

						full_action.append(loc[0][0])
						full_action.append(loc[0][1])
					
						victim = choice[1]
						full_action.append(victim)
				# Monopoly
				if(dev_card == 3):
						resource = random.choice(list(ResCard)).value
						full_action.append(resource)
				# YOP
				if(dev_card == 4):
						resource = random.choice(list(ResCard)).value
						full_action.append(resource)
						resource = random.choice(list(ResCard)).value
						full_action.append(resource)



		# Prompt Play robber
		if(action == 6):
			choice = random.choice(allowed_actions['allowed_robber_tiles'])
			loc = choice[0]

			full_action.append(loc[0][0])
			full_action.append(loc[0][1])
		
			victim = choice[1]
			full_action.append(victim)
		
			victim = random.choice(allowed_actions['allowed_victim_players'])
			full_action.append(victim)
		# Prompt Do trade
		if(action == 7):
			pass
				# print('0: Player 0 | 1: Player 1 | 2: Player 2 | 3: Player 3')
				# which_player_response = int(input())
				# full_action.append(which_player_response)
				
				# print('You offer:') 
				# print('0: Wood | 1: Brick | 2: Ore | 3: Sheep | 4: Wheat')
				# offered_resource_response = int(input())
				# full_action.append(offered_resource_response)

				# print('You receive:')
				# print('0: Wood | 1: Brick | 2: Ore | 3: Sheep | 4: Wheat')
				# received_resource_response = int(input())
				# full_action.append(received_resource_response)
		# # Accept Trade
		# if(response == 8):
		# 		pass
		# # Deny trade
		# if(response == 9):
		# 		pass
		# if(response == 10):
		# 		pass
		# if(response == 11):
		# 		pass

		return full_action


