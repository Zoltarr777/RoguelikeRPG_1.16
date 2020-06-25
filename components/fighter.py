import tcod as libtcod

from game_messages import Message
from random import randint
from entity import Entity
from components.ai import BasicMonster, AsleepMonster
from render_functions import RenderOrder
from components.status import Burn, Poison, Diseased


class Fighter:
	def __init__(self, hp, defense, power, magic, magic_defense, mana, talismanhp, gold, status=None, xp=0):
		self.base_max_hp = hp
		self.hp = hp
		self.base_defense = defense
		self.base_power = power
		self.base_magic = magic
		self.base_magic_defense = magic_defense
		self.xp = xp
		self.talismanhp = talismanhp
		self.gold = gold
		self.base_max_mana = mana
		self.mana = mana
		self.status = status

	@property
	def max_hp(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_hp_bonus
		else:
			bonus = 0

		return self.base_max_hp + bonus

	@property
	def power(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.power_bonus
		else:
			bonus = 0

		return self.base_power + bonus

	@property
	def defense(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.defense_bonus
		else:
			bonus = 0

		return self.base_defense + bonus

	@property
	def magic_defense(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.magic_defense_bonus
		else:
			bonus = 0

		return self.base_magic_defense + bonus

	@property
	def magic(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.magic_bonus
		else:
			bonus = 0

		return self.base_magic + bonus

	@property
	def max_mana(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_mana_bonus
		else:
			bonus = 0

		return self.base_max_mana + bonus

	def take_damage(self, amount):
		results = []

		if self.talismanhp >= amount:
			self.talismanhp -= amount
		else:
			hpdamage = amount - self.talismanhp
			self.talismanhp -= self.talismanhp
			self.hp -= hpdamage

		if self.hp <= 0:
			self.hp = 0

		if self.hp <= 0:
			results.append({'dead': self.owner, 'xp': self.xp})

		return results

	def heal(self, amount):
		results = []

		self.hp += amount

		if self.hp > self.max_hp:
			self.hp = self.max_hp

		return results

	def recover_mana(self, amount):
		self.mana += amount

		if self.mana > self.max_mana:
			self.mana = self.max_mana

	def use_mana(self, mana_cost):
		results = []

		self.mana -= mana_cost

		if self.mana <= 0:
			results.append({'message': Message("You've run out of mana!", libtcod.orange)})

		return results

	def sacrifice(self, amount):
		results = []

		self.hp -= amount
		self.talismanhp += amount

		if self.hp <= 0:
			results.append({'dead': self.owner, 'xp': self.xp})

		return results

	def attack(self, target, constants, **kwargs):
		results = []

		if target.name == "Ghost":
			results.append({'message': Message("{0} attacks {1} but phases through it!".format(self.owner.name.capitalize(), target.name), libtcod.orange)})

		elif self.owner.name == "Floor Trap":
			damage = round(self.power * (10 / (10 + target.fighter.defense)))
			results.append({'message': Message("The {0} explodes and deals {1} hit points!".format(self.owner.name.capitalize(), str(damage)), libtcod.red)})
			results.extend(target.fighter.take_damage(damage))
			results.append({'dead': self.owner, 'xp': self.xp})

		elif target.name == "Building":
			pass

		elif target.name == "Forest":
			pass

		elif target.name == "Door":
			results.append({'message': Message("The door is locked.", libtcod.orange)})

		elif target.name == "Sign":
			results.append({'message': Message("The sign says the shop is closed.", libtcod.orange)})

		else:
			attack_chance = randint(1, 20)

			if self.owner.name == "Ghost":
				damage = round(self.magic * (10 / (10 + target.fighter.magic_defense)))
			else:
				damage = round(self.power * (10 / (10 + target.fighter.defense)))

			if 2 <= attack_chance <= 19:

				results.append({'message': Message("{0} attacks {1} for {2} hit points.".format(self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
				results.extend(target.fighter.take_damage(damage))

				if self.owner.name == "Basilisk" and target.fighter.status == None:
					poison_chance = randint(1, 5)
					if poison_chance == 5:
						results.append({'message': Message("The Basilisk poisons you!", libtcod.orange)})
						target.fighter.status = Poison(5, 3, target)

				elif self.owner.name == "Wraith" and target.fighter.status == None:
					disease_chance = randint(1, 5)
					if disease_chance == 5:
						results.append({'message': Message("The Wriath gives you a disease!", libtcod.orange)})
						target.fighter.status = Diseased("hp", 10, target)

				if target.name == "Slime" and target.fighter.hp <= (0.4 * target.fighter.base_max_hp):
					entities = kwargs.get('entities')
					number_of_slimes = randint(1, 2)

					for i in range(number_of_slimes):
						x = randint(target.x - 1, target.x + 1)
						y = randint(target.y - 1, target.y + 1)

						if not any([entity for entity in entities if entity.x == x and entity.y == y]):
							fighter_component = Fighter(hp=5, defense=0, power=1, magic=0, magic_defense=2, xp=20, talismanhp=0, gold=randint(1, 2))
							ai_component = BasicMonster()
							monster = Entity(x, y, constants['baby_slime_tile'], libtcod.white, 'Baby Slime', blocks=True, 
								render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

							entities.append(monster)

					results.append({'consumed': True, 'message': Message("The slime split into {0}!".format(number_of_slimes), libtcod.light_green)})

			elif attack_chance == 1:
				dodgemiss = randint(1, 2)

				if dodgemiss == 1:
					results.append({'message': Message("{0} attacks {1} but {1} dodges!".format(self.owner.name.capitalize(), target.name), libtcod.white)})
				else:
					results.append({'message': Message("{0} attacks {1} but misses!".format(self.owner.name.capitalize(), target.name), libtcod.white)})

			elif attack_chance == 20:

				damage *= 2

				results.append({'message': Message("{0} attacks {1} and critical hits for {2} hit points!".format(self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
				results.extend(target.fighter.take_damage(damage))

				if target.name == "Slime" and target.fighter.hp <= (0.4 * target.fighter.base_max_hp):
					entities = kwargs.get('entities')
					number_of_slimes = randint(1, 2)

					for i in range(number_of_slimes):
						x = randint(target.x - 1, target.x + 1)
						y = randint(target.y - 1, target.y + 1)

						if not any([entity for entity in entities if entity.x == x and entity.y == y]):
							fighter_component = Fighter(hp=5, defense=0, power=1, magic=0, magic_defense=2, xp=20, talismanhp=0, gold=randint(1, 2))
							ai_component = BasicMonster()
							monster = Entity(x, y, constants['baby_slime_tile'], libtcod.white, 'Baby Slime', blocks=True, 
								render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

							entities.append(monster)

					results.append({'consumed': True, 'message': Message("The slime split into {0}!".format(number_of_slimes), libtcod.light_green)})

		return results

