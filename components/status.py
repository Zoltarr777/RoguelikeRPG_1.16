import tcod as libtcod
import random
from random import randint

from game_messages import Message
from entity import Entity
from game_states import GameStates

class Burn:
	def __init__(self, damage, turns, owner):
		self.damage = damage
		self.turns = turns
		self.owner = owner
		self.name = "Burned"

	def update(self):
		results = []

		if self.turns == 0:
			self.owner.fighter.status = None
			results.append({'message': Message("The {0} is no longer burned!".format(self.owner.name.capitalize()), libtcod.green)})
		else:
			results.append({'message': Message("The {0} takes {1} burn damage!".format(self.owner.name.capitalize(), str(self.damage)), libtcod.orange)})
			results.extend(self.owner.fighter.take_damage(self.damage))
			self.turns -= 1

		return results

class Poison:
	def __init__(self, damage, turns, owner):
		self.damage = damage
		self.turns = turns
		self.owner = owner
		self.name = "Poisoned"
		self.frequency = randint(0, 3)

	def update(self):
		results = []

		if self.frequency == 0:
			if self.turns == 0:
				self.owner.fighter.status = None
				results.append({'message': Message("The {0} is no longer poisoned!".format(self.owner.name.capitalize()), libtcod.green)})
			else:
				results.append({'message': Message("The {0} takes {1} poison damage!".format(self.owner.name.capitalize(), str(self.damage)), libtcod.orange)})
				results.extend(self.owner.fighter.take_damage(self.damage))
				self.turns -= 1
			self.frequency = randint(1, 3)

		else:
			self.frequency -= 1

		return results

class Frozen:
	def __init__(self, turns, owner):
		self.turns = turns
		self.owner = owner
		self.name = "Frozen"

	def update(self):
		results = []

		if self.turns == 0:
			self.owner.fighter.status = None
			results.append({'message': Message("The {0} is no longer frozen!".format(self.owner.name.capitalize()), libtcod.green)})
		else:
			results.append({'message': Message("The {0} is frozen and can't move!".format(self.owner.name.capitalize()), libtcod.orange)})
			self.turns -= 1

		return results

class Haste:
	def __init__(self, turns, owner):
		self.turns = turns
		self.owner = owner
		self.name = "Haste"

	def update(self):
		results = []

		if self.turns == 0:
			self.owner.fighter.status = None
			results.append({'message': Message("The {0} no longer has haste!".format(self.owner.name.capitalize()), libtcod.orange)})
		else:
			self.turns -= 1

		return results


class Regenerate:
	def __init__(self, amount, turns, owner):
		self.amount = amount
		self.turns = turns
		self.owner = owner
		self.name = "Regenerating"

	def update(self):
		results = []

		if self.turns == 0:
			self.owner.fighter.status = None
			results.append({'message': Message("The {0} no longer is regenerating!".format(self.owner.name.capitalize()), libtcod.orange)})
		else:
			results.append({'message': Message("The {0} regenerates {1} HP!".format(self.owner.name.capitalize(), str(self.amount)), libtcod.green)})
			results.extend(self.owner.fighter.heal(self.amount))
			self.turns -= 1

		return results


class Diseased:
	def __init__(self, stat, amount, owner):
		self.stat = stat
		self.amount = amount
		self.owner = owner
		self.name = "Diseased"
		self.stat_decreased = False
		self.amount_more_than_stat = False
		self.old_stat = 0

	def reset_stat(self):
		results = []

		if self.amount_more_than_stat == True:
			if self.stat == 'hp':
				self.owner.fighter.base_max_hp = self.old_stat
			elif self.stat == 'defense':
				self.owner.fighter.base_defense = self.old_stat
			elif self.stat == 'power':
				self.owner.fighter.base_power = self.old_stat
			elif self.stat == 'magic':
				self.owner.fighter.base_magic = self.old_stat
			elif self.stat == 'magic_defense':
				self.owner.fighter.base_magic_defense = self.old_stat
			elif self.stat == 'mana':
				self.owner.fighter.base_max_mana = self.old_stat

		else:
			if self.stat == 'hp':
				self.owner.fighter.base_max_hp += self.amount
			elif self.stat == 'defense':
				self.owner.fighter.base_defense += self.amount
			elif self.stat == 'power':
				self.owner.fighter.base_power += self.amount
			elif self.stat == 'magic':
				self.owner.fighter.base_magic += self.amount
			elif self.stat == 'magic_defense':
				self.owner.fighter.base_magic_defense += self.amount
			elif self.stat == 'mana':
				self.owner.fighter.base_max_mana += self.amount

		self.owner.fighter.status = None

		results.append({'message': Message("The {0}'s {1} was returned to normal!".format(self.owner.name.capitalize(), self.stat), libtcod.green)})		

		return results

	def update(self):
		results = []

		if self.stat == 'hp':
			stat = self.owner.fighter.base_max_hp
		elif self.stat == 'defense':
			stat = self.owner.fighter.base_defense
		elif self.stat == 'power':
			stat = self.owner.fighter.base_power
		elif self.stat == 'magic':
			stat = self.owner.fighter.base_magic
		elif self.stat == 'magic_defense':
			stat = self.owner.fighter.base_magic_defense
		elif self.stat == 'mana':
			stat = self.owner.fighter.base_max_mana


		if self.stat_decreased == False:
			self.old_stat = stat
			stat -= self.amount
			if stat <= 0:
				stat = 0
				self.amount_more_than_stat = True

			if self.stat == 'hp':
				self.owner.fighter.base_max_hp = stat
				if self.owner.fighter.hp > stat:
					self.owner.fighter.hp = stat
			elif self.stat == 'defense':
				self.owner.fighter.base_defense = stat
			elif self.stat == 'power':
				self.owner.fighter.base_power = stat
			elif self.stat == 'magic':
				self.owner.fighter.base_magic = stat
			elif self.stat == 'magic_defense':
				self.owner.fighter.base_magic_defense = stat
			elif self.stat == 'mana':
				self.owner.fighter.base_max_mana = stat
				if self.owner.fighter.mana > stat:
					self.owner.fighter.mana = stat
			results.append({'message': Message("The {0}'s {1} was lowered by {2}! You better find a cure!".format(self.owner.name.capitalize(), self.stat, str(self.amount)), libtcod.orange)})
			self.stat_decreased = True

		return results








