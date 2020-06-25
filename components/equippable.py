class Equippable:
	def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0, magic_bonus=0, magic_defense_bonus=0, max_mana_bonus=0, **kwargs):
		self.slot = slot
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus
		self.max_hp_bonus = max_hp_bonus
		self.magic_bonus = magic_bonus
		self.magic_defense_bonus = magic_defense_bonus
		self.max_mana_bonus = max_mana_bonus
		self.function_kwargs = kwargs