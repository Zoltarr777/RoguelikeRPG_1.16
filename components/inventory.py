import tcod as libtcod

from game_messages import Message
from game_states import GameStates

class Inventory:
	def __init__(self, capacity):
		self.capacity = capacity
		self.items = []

	def add_item(self, item):
		results = []

		if len(self.items) >= self.capacity:
			results.append({'item_added': None, 'message': Message("You can't carry any more, your inventory is full!", libtcod.yellow)})
		else:
			results.append({'item_added': item, 'message': Message("You pick up the {0}!".format(item.name), libtcod.light_cyan)})

			self.items.append(item)

		return results

	def use(self, item_entity, **kwargs):
		results = []

		item_component = item_entity.item

		if item_component.use_function is None:
			equippable_component = item_entity.equippable

			if equippable_component:
				results.append({'equip': item_entity})
			else:
				results.append({'message': Message("The {0} can't be used.".format(item_entity.name), libtcod.yellow)})
		else:
			if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
				results.append({'targeting': item_entity})
			else:
				kwargs = {**item_component.function_kwargs, **kwargs}
				item_use_results = item_component.use_function(self.owner, **kwargs)

				for item_use_result in item_use_results:
					if item_use_result.get('consumed'):
						self.remove_item(item_entity)

				results.extend(item_use_results)

		return results

	def remove_item(self, item):
		self.items.remove(item)

	def drop_item(self, item):
		results = []

		if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item or self.owner.equipment.chest == item or self.owner.equipment.legs == item or self.owner.equipment.head == item or self.owner.equipment.amulet == item:
			self.owner.equipment.toggle_equip(item)

		item.x = self.owner.x
		item.y = self.owner.y

		self.remove_item(item)
		results.append({'item_dropped': item, 'message': Message("You dropped the {0}".format(item.name), libtcod.yellow)})

		return results

	def loot_item(self, item):
		item.x = self.owner.x
		item.y = self.owner.y

		self.remove_item(item)

	def sell(self, item, game_state):
		results = []

		if game_state == GameStates.SELL_MENU:
			item_gold_value = item.item.function_kwargs['gold']
		else:
			item_gold_value = item.equippable.function_kwargs['gold']

		self.owner.fighter.gold += item_gold_value

		self.remove_item(item)
		results.append({'consumed': item, 'message': Message("You sold the {0} for {1} gold!".format(item.name, item_gold_value), libtcod.light_cyan)})

		return results

	def buy(self, item, game_state):
		results = []

		if game_state == GameStates.BUY_MENU:
			item_gold_value = item.item.function_kwargs['gold']
		else:
			item_gold_value = item.equippable.function_kwargs['gold']

		if self.owner.fighter.gold < item_gold_value:
			results.append({'item_consumed': False, 'message': Message("You don't have enough gold to buy that item!", libtcod.yellow)})

		else:
			if len(self.items) >= self.capacity:
				results.append({'item_consumed': False, 'message': Message("You can't buy any more, your inventory is full!", libtcod.yellow)})
			else:
				if game_state == GameStates.BUY_MENU:
					results.append({'item_bought': item, 'message': Message("You buy the {0} for {1} gold!".format(item.name, item_gold_value), libtcod.light_cyan)})
					self.owner.fighter.gold -= item_gold_value
					self.items.append(item)
				else:
					results.append({'equipment_bought': item, 'message': Message("You buy the {0} for {1} gold!".format(item.name, item_gold_value), libtcod.light_cyan)})
					self.owner.fighter.gold -= item_gold_value
					self.items.append(item)

		return results

	def search(self, target_name):
	    result = None
	    for item in self.items:
	        if item.name == target_name:
	            result = item
	            break
	    return result