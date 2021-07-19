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
					loc = random.choice(allowed_actions['allowed_city_points'])
					full_action.append(loc.position[0])
					full_action.append(loc.position[1])

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
			other_player = random.choice(allowed_actions['allowed_trade_partners'])
			full_action.append(other_player)
			print('Target player: ' + str(other_player.num))
			
			allowed_cards = allowed_actions['allowed_trade_pairs']
			print(allowed_cards)
			print()
			allowed_cards = [(x,y) for x, y in allowed_cards if x == other_player.num][0][1]
			print(allowed_cards)
			print()
			allowed_cards = [x[0] for x in allowed_cards]
			print(allowed_cards)
			print()
			forfeit_card = random.choice(allowed_cards)

			print('Forfeit Card ' + forfeit_card.name)
			other_player_allowed_cards = allowed_actions['allowed_trade_pairs']
			print(other_player_allowed_cards)
			print()
			other_player_allowed_cards = [(x,y) for x, y in other_player_allowed_cards if x == other_player.num][0][1]
			print(other_player_allowed_cards)
			print()
			other_player_allowed_cards = [(x,y) for x, y in other_player_allowed_cards if x.value == forfeit_card.value][0]
			print(other_player_allowed_cards[1])
			print()
			print('----------')

			receive_card = random.choice(other_player_allowed_cards[1])
			print(forfeit_card)
			print(receive_card)
			full_action.append(forfeit_card)
			full_action.append(receive_card)
		# Accept Trade
		if(action == 8):
				pass
		# Deny trade
		if(action == 9):
				pass
		
		# Forfeit cards
		if(action == 10):
				choice = random.choice(allowed_actions['allowed_forfeit_cards'])
				full_action.append(choice)
		# if(response == 11):
		# 		pass

		return full_action


