import tcod as libtcod

from random import randint
from game_messages import Message

class BasicMonster:
	def take_turn(self, target, fov_map, game_map, entities, constants):
		results = []
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if monster.distance_to(target) >= 2:
				monster.move_astar(target, entities, game_map)

			elif target.fighter.hp > 0:
				attack_results = monster.fighter.attack(target, constants)
				results.extend(attack_results)

		return results

class MindControlled:
	def __init__(self, previous_ai, number_of_turns=10):
		self.previous_ai = previous_ai
		self.number_of_turns = number_of_turns

	def take_turn(self, target, fov_map, game_map, entities, constants):
		results = []

		if self.number_of_turns > 0:
			monster = self.owner
			target = None
			for entity in entities:
				if entity.fighter and entity != self.owner and entity.char is not "@" and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
					target = entity

			if libtcod.map_is_in_fov(fov_map, monster.x, monster.y) and target is not None:
				if monster.distance_to(target) >= 2:
					monster.move_astar(target, entities, game_map)

				elif target.fighter.hp > 0:
					attack_results = monster.fighter.attack(target, constants)
					results.extend(attack_results)

			self.number_of_turns -= 1
		else:
			self.owner.ai = self.previous_ai
			results.append({'message': Message("The {0} is no longer controlled!".format(self.owner.name), libtcod.orange)})

		return results

class NecromancyAI:
	def take_turn(self, target, fov_map, game_map, entities, constants):
		results = []

		monster = self.owner
		target = None
		for entity in entities:
			if entity.fighter and entity != self.owner and entity.char is not "@" and entity.name != 'Goblin Corpse' and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
				target = entity

		for entity in entities:
			if entity.fighter and entity.char == "@":
				entity = player

		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y) and target is not None:
			if monster.distance_to(target) >= 2:
				monster.move_astar(target, entities, game_map)

			elif target.fighter.hp > 0:
				attack_results = monster.fighter.attack(target, constants)
				results.extend(attack_results)

		elif target is None:
			if monster.distance_to(player) >=2:
				monster.move_astar(player, entities, game_map)

		return results

class ConfusedMonster:
	def __init__(self, previous_ai, number_of_turns=10):
		self.previous_ai = previous_ai
		self.number_of_turns = number_of_turns

	def take_turn(self, target, fov_map, game_map, entities, constants):
		results = []

		if self.number_of_turns > 0:
			random_x = self.owner.x + randint(0, 2) - 1
			random_y = self.owner.y + randint(0, 2) - 1

			if random_x != self.owner.x and random_y != self.owner.y:
				self.owner.move_towards(random_x, random_y, game_map, entities)

			self.number_of_turns -= 1
		else:
			self.owner.ai = self.previous_ai
			results.append({'message': Message("The {0} is no longer confused!".format(self.owner.name), libtcod.orange)})

		return results

class AsleepMonster:
	def __init__(self, previous_ai, number_of_turns=10):
		self.previous_ai = previous_ai
		self.number_of_turns = number_of_turns

	def take_turn(self, target, fov_map, game_map, entities, constants):
		results = []

		if self.number_of_turns > 0:
			self.number_of_turns -= 1
		else:
			self.owner.ai = self.previous_ai
			results.append({'message': Message("The {0} woke up!".format(self.owner.name), libtcod.orange)})

		return results

class Trap:
	def take_turn(self, target, fov_map, game_map, entities, constants):
		results = []
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if monster.distance_to(target) < 1 and target.fighter.hp > 0:
				attack_results = monster.fighter.attack(target, constants)
				results.extend(attack_results)

		return results



