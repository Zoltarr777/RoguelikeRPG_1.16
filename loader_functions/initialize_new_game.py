import tcod as libtcod

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from equipment_slots import EquipmentSlots
from game_messages import MessageLog, Message
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder
from item_functions import cast_confusion, cast_fireball, cast_lightning, heal, cast_sleep, cast_sleep_aura, health_talisman_sacrifice, cast_mind_control, necromancy, recover_mana, cast_magic, shoot_arrow, poison, freeze, antidote, haste, regeneration, disease
from components.item import Item
from random import randint
import random

def get_constants():
	window_title = "Roguelike RPG Version 1.16"

	screen_width = 80
	screen_height = 50

	bar_width = 20
	panel_height = 9
	panel_y = screen_height - panel_height

	message_x = bar_width + 1
	message_width = screen_width - bar_width - 1
	message_height = panel_height - 1

	map_width = screen_width
	map_height = screen_height - panel_height

	room_max_size = 10
	room_min_size = 6
	max_rooms = 30

	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10

	max_monsters_per_room = 3
	max_items_per_room = 2

	kill_count = 0

	wall_tile = 256
	floor_tile = 257
	stairs_tile = 258
	player_tile = 259
	goblin_tile = 260
	orc_tile = 261
	troll_tile = 262
	ghost_tile = 263
	slime_tile = 264
	baby_slime_tile = 265
	skeleton_tile = 266
	corpse_tile = 267
	slime_corpse_tile = 268
	baby_slime_corpse_tile = 269
	skeleton_corpse_tile = 270
	scroll_tile = 271
	healing_potion_tile = 272
	greater_healing_potion_tile = 273
	mana_potion_tile = 274
	sword_tile = 275
	dagger_tile = 276
	magic_wand_tile = 277
	wizard_staff_tile = 278
	shield_tile = 279
	health_talisman_tile = 280
	basilisk_tile = 281
	treasure_tile = 282
	chestplate_tile = 283
	leg_armor_tile = 284
	helmet_tile = 285
	amulet_tile = 286
	long_bow_tile = 287
	arrow_tile = 288
	grass_tile = 289
	path_tile = 290
	roof_tile = 291
	brick_tile = 292
	player_overworld_tile = 293
	forest_tile = 294
	door_tile = 295
	sign_tile = 296
	
	
	colors = {
			'dark_wall': libtcod.Color(36, 36, 36),
			'dark_ground': libtcod.Color(40, 51, 35),
			'light_wall': libtcod.Color(130, 110, 50),
			'light_ground': libtcod.Color(200, 180, 50)
	}

	constants = {
		'window_title': window_title,
		'screen_width': screen_width,
		'screen_height': screen_height,
		'bar_width': bar_width,
		'panel_height': panel_height,
		'panel_y': panel_y,
		'message_x': message_x,
		'message_width': message_width,
		'message_height': message_height,
		'map_width': map_width,
		'map_height': map_height,
		'room_max_size': room_max_size,
		'room_min_size': room_min_size,
		'max_rooms': max_rooms,
		'fov_algorithm': fov_algorithm,
		'fov_light_walls': fov_light_walls,
		'fov_radius': fov_radius,
		'max_monsters_per_room': max_monsters_per_room,
		'max_items_per_room': max_items_per_room,
		'colors': colors,
		'kill_count': kill_count,
		'wall_tile': wall_tile,
		'floor_tile': floor_tile,
		'player_tile': player_tile,
		'orc_tile': orc_tile,
		'troll_tile': troll_tile,
		'scroll_tile': scroll_tile,
		'healing_potion_tile': healing_potion_tile,
		'sword_tile': sword_tile,
		'shield_tile': shield_tile,
		'stairs_tile': stairs_tile,
		'dagger_tile': dagger_tile,
		'magic_wand_tile': magic_wand_tile,
		'greater_healing_potion_tile': greater_healing_potion_tile,
		'mana_potion_tile': mana_potion_tile,
		'ghost_tile': ghost_tile,
		'slime_tile': slime_tile,
		'corpse_tile': corpse_tile,
		'goblin_tile': goblin_tile,
		'baby_slime_tile': baby_slime_tile,
		'skeleton_tile': skeleton_tile,
		'slime_corpse_tile': slime_corpse_tile,
		'baby_slime_corpse_tile': baby_slime_corpse_tile,
		'skeleton_corpse_tile': skeleton_corpse_tile,
		'wizard_staff_tile': wizard_staff_tile,
		'health_talisman_tile': health_talisman_tile,
		'basilisk_tile': basilisk_tile,
		'treasure_tile': treasure_tile,
		'chestplate_tile': chestplate_tile,
		'leg_armor_tile': leg_armor_tile,
		'helmet_tile': helmet_tile,
		'amulet_tile': amulet_tile,
		'long_bow_tile': long_bow_tile,
		'arrow_tile': arrow_tile,
		'grass_tile': grass_tile,
		'path_tile': path_tile,
		'roof_tile': roof_tile,
		'brick_tile': brick_tile,
		'player_overworld_tile': player_overworld_tile,
		'forest_tile': forest_tile,
		'door_tile': door_tile,
		'sign_tile': sign_tile
	}

	return constants

def get_game_variables(constants):
	fighter_component = Fighter(hp=100, defense=1, power=2, magic=0, magic_defense=1, talismanhp=0, gold=0, status=None, mana=100)
	inventory_component = Inventory(26)
	equipment_inventory_component = Inventory(26)
	level_component = Level()
	equipment_component = Equipment()
	player = Entity(0, 0, constants['player_overworld_tile'], libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, 
		inventory=inventory_component, level=level_component, equipment=equipment_component, equipment_inventory=equipment_inventory_component)
	entities = [player]

	equipment_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=1, gold=1)
	dagger = Entity(0, 0, constants['dagger_tile'], libtcod.white, "Terrium Dagger (+1 atk)", equippable=equipment_component)
	player.equipment_inventory.add_item(dagger)
	player.equipment.toggle_equip(dagger)

	item_component = Item(use_function=cast_magic, damage=2, maximum_range=3, gold=2)
	magic_wand = Entity(0, 0, constants['magic_wand_tile'], libtcod.white, "Magic Wand", item=item_component)
	player.inventory.add_item(magic_wand)

	game_map = GameMap(constants['map_width'], constants['map_height'])
	game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], 
		constants['map_height'], player, entities, constants['orc_tile'], constants['healing_potion_tile'], constants['scroll_tile'], 
		constants['troll_tile'], constants['stairs_tile'], constants['sword_tile'], constants['shield_tile'], constants['dagger_tile'], 
		constants['magic_wand_tile'], constants['greater_healing_potion_tile'], constants['ghost_tile'], constants['slime_tile'], 
		constants['corpse_tile'], constants['goblin_tile'], constants['baby_slime_tile'], constants['skeleton_tile'], 
		constants['slime_corpse_tile'], constants['baby_slime_corpse_tile'], constants['skeleton_corpse_tile'], constants['mana_potion_tile'],
		constants['wizard_staff_tile'], constants['health_talisman_tile'], constants['basilisk_tile'], constants['treasure_tile'], 
		constants['chestplate_tile'], constants['leg_armor_tile'], constants['helmet_tile'], constants['amulet_tile'], constants['floor_tile'], 
		constants['long_bow_tile'], constants['arrow_tile'], constants['wall_tile'], constants['grass_tile'], constants['path_tile'],
		constants['roof_tile'], constants['brick_tile'], constants['player_overworld_tile'], constants['player_tile'], constants['forest_tile'], 
		constants['door_tile'], constants['sign_tile'])

	item_descriptors = [
			'Valor', 'Power', 'Ingenuity', 'Glory', 'Strength', 'Speed', 'Wealth', 'Divinity', 'Energy', 'Honor', 'Resistance', 'Greatness',
			'Courage', 'Intelligence'
		]

	all_shop_items = []

	item_component = Item(use_function=heal, amount=20, gold=20)
	item = Entity(0, 0, constants['healing_potion_tile'], libtcod.white, "Health Potion (+20 HP)", render_order=RenderOrder.ITEM, item=item_component)
	all_shop_items.append(item)

	item_component = Item(use_function=recover_mana, amount=20, gold=10)
	item = Entity(0, 0, constants['mana_potion_tile'], libtcod.white, "Mana Potion (+20 MANA)", render_order=RenderOrder.ITEM, item=item_component)
	all_shop_items.append(item)


	all_shop_equipment = []

	sword_amount = randint(2, 4)
	equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=sword_amount, gold=10)
	item = Entity(0, 0, constants['sword_tile'], libtcod.white, "Terrium Sword of " + random.choice(item_descriptors) + " (+" + str(sword_amount) + " atk)", equippable=equippable_component)
	all_shop_equipment.append(item)

	shield_amount = randint(1, 2)
	equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=shield_amount, gold=7)
	item = Entity(0, 0, constants['shield_tile'], libtcod.white, "Terrium Shield of " + random.choice(item_descriptors) + " (+" + str(shield_amount) + " def)", equippable=equippable_component)
	all_shop_equipment.append(item)

	chestplate_amount = randint(2, 3)
	equippable_component = Equippable(EquipmentSlots.CHEST, defense_bonus=chestplate_amount, gold=20)
	item = Entity(0, 0, constants['chestplate_tile'], libtcod.darker_grey, "Terrium Chestplate of " + random.choice(item_descriptors) + " (+" + str(chestplate_amount) + " def)", equippable=equippable_component)
	all_shop_equipment.append(item)

	leg_amount = randint(1, 3)
	equippable_component = Equippable(EquipmentSlots.LEGS, defense_bonus=leg_amount, gold=15)
	item = Entity(0, 0, constants['leg_armor_tile'], libtcod.darker_grey, "Terrium Leg Armor of " + random.choice(item_descriptors) + " (+" + str(leg_amount) + " def)", equippable=equippable_component)
	all_shop_equipment.append(item)

	helmet_amount = randint(1, 2)
	equippable_component = Equippable(EquipmentSlots.HEAD, defense_bonus=helmet_amount, gold=5)
	item = Entity(0, 0, constants['helmet_tile'], libtcod.darker_grey, "Terrium Helmet of " + random.choice(item_descriptors) + " (+" + str(helmet_amount) + " def)", equippable=equippable_component)
	all_shop_equipment.append(item)

	amulet_amount = randint(1, 4)
	equippable_component = Equippable(EquipmentSlots.AMULET, magic_bonus=amulet_amount, gold=6)
	item = Entity(0, 0, constants['amulet_tile'], libtcod.darker_grey, "Terrium Amulet of " + random.choice(item_descriptors) + " (+" + str(amulet_amount) + " mgk)", equippable=equippable_component)
	all_shop_equipment.append(item)


	number_of_shop_items = randint(1, 3)
	for i in range(number_of_shop_items):
		random_item = randint(0, len(all_shop_items) - 1)
		game_map.shop_items.append(all_shop_items[random_item])

	number_of_shop_equipment = randint(1, 2)
	for i in range(number_of_shop_equipment):
		random_equipment = randint(0, len(all_shop_equipment) - 1)
		game_map.shop_equipment_items.append(all_shop_equipment[random_equipment])


	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

	game_state = GameStates.PLAYERS_TURN

	return player, entities, game_map, message_log, game_state





