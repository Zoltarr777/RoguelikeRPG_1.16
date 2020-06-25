from equipment_slots import EquipmentSlots

class Equipment:
	def __init__(self, main_hand=None, off_hand=None, chest=None, legs=None, head=None, amulet=None):
		self.main_hand = main_hand
		self.off_hand = off_hand
		self.chest = chest
		self.legs = legs
		self.head = head
		self.amulet = amulet

	@property
	def max_hp_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.max_hp_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.max_hp_bonus

		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.max_hp_bonus

		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.max_hp_bonus

		if self.head and self.head.equippable:
			bonus += self.head.equippable.max_hp_bonus

		if self.amulet and self.amulet.equippable:
			bonus += self.amulet.equippable.max_hp_bonus

		return bonus

	@property
	def power_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.power_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.power_bonus

		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.power_bonus

		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.power_bonus

		if self.head and self.head.equippable:
			bonus += self.head.equippable.power_bonus

		if self.amulet and self.amulet.equippable:
			bonus += self.amulet.equippable.power_bonus

		return bonus

	@property
	def defense_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.defense_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.defense_bonus

		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.defense_bonus

		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.defense_bonus

		if self.head and self.head.equippable:
			bonus += self.head.equippable.defense_bonus

		if self.amulet and self.amulet.equippable:
			bonus += self.amulet.equippable.defense_bonus

		return bonus

	@property
	def magic_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.magic_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.magic_bonus

		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.magic_bonus

		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.magic_bonus

		if self.head and self.head.equippable:
			bonus += self.head.equippable.magic_bonus

		if self.amulet and self.amulet.equippable:
			bonus += self.amulet.equippable.magic_bonus

		return bonus

	@property
	def magic_defense_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.magic_defense_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.magic_defense_bonus

		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.magic_defense_bonus

		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.magic_defense_bonus

		if self.head and self.head.equippable:
			bonus += self.head.equippable.magic_defense_bonus

		if self.amulet and self.amulet.equippable:
			bonus += self.amulet.equippable.magic_defense_bonus

		return bonus

	@property
	def max_mana_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.max_mana_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.max_mana_bonus

		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.max_mana_bonus

		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.max_mana_bonus

		if self.head and self.head.equippable:
			bonus += self.head.equippable.max_mana_bonus

		if self.amulet and self.amulet.equippable:
			bonus += self.amulet.equippable.max_mana_bonus

		return bonus

	def toggle_equip(self, equippable_entity):
		results = []

		slot = equippable_entity.equippable.slot

		if slot == EquipmentSlots.MAIN_HAND:
			if self.main_hand == equippable_entity:
				self.main_hand = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.main_hand:
					results.append({'dequipped': self.main_hand})

				self.main_hand = equippable_entity
				results.append({'equipped': equippable_entity})

		elif slot == EquipmentSlots.OFF_HAND:
			if self.off_hand == equippable_entity:
				self.off_hand = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.off_hand:
					results.append({'dequipped': self.off_hand})

				self.off_hand = equippable_entity
				results.append({'equipped': equippable_entity})

		elif slot == EquipmentSlots.CHEST:
			if self.chest == equippable_entity:
				self.chest = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.chest:
					results.append({'dequipped': self.chest})

				self.chest = equippable_entity
				results.append({'equipped': equippable_entity})

		elif slot == EquipmentSlots.LEGS:
			if self.legs == equippable_entity:
				self.legs = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.legs:
					results.append({'dequipped': self.legs})

				self.legs = equippable_entity
				results.append({'equipped': equippable_entity})

		elif slot == EquipmentSlots.HEAD:
			if self.head == equippable_entity:
				self.head = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.head:
					results.append({'dequipped': self.head})

				self.head = equippable_entity
				results.append({'equipped': equippable_entity})

		elif slot == EquipmentSlots.AMULET:
			if self.amulet == equippable_entity:
				self.amulet = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.amulet:
					results.append({'dequipped': self.amulet})

				self.amulet = equippable_entity
				results.append({'equipped': equippable_entity})

		return results







	