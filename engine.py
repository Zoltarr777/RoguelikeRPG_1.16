import sys
import warnings

if not sys.warnoptions:
	warnings.simplefilter("ignore")

import libtcodpy as libtcod
from playsound import playsound

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box, main_menu_help_menu, buy_menu, buy_equipment_menu
from render_functions import clear_all, render_all
from item_functions import cast_magic
from components.item import Item
from components.inventory import Inventory

def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
	fov_recompute = True

	fov_map = initialize_fov(game_map)

	key = libtcod.Key()
	mouse = libtcod.Mouse()

	if not game_state == GameStates.PLAYER_DEAD:
		game_state = GameStates.PLAYERS_TURN

	begin_player_turn = True

	previous_game_state = game_state

	targeting_item = None

	if not game_state == GameStates.PLAYER_DEAD:
		PLAYERDEADSTATE = False
	else:
		PLAYERDEADSTATE = True

	while not libtcod.console_is_window_closed():
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

		if fov_recompute:
			if game_map.dungeon_level != 0:
				recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])
			else:
				recompute_fov(fov_map, player.x, player.y, 100, constants['fov_light_walls'], constants['fov_algorithm'])

		render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, 
			constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], 
			constants['panel_y'], mouse, constants['colors'], constants['kill_count'], game_state, constants['wall_tile'], constants['floor_tile'], constants['grass_tile'])

		fov_recompute = False

		libtcod.console_flush()

		clear_all(con, entities)

		action = handle_keys(key, game_state)
		mouse_action = handle_mouse(mouse)

		move = action.get('move')
		wait = action.get('wait')
		pickup = action.get('pickup')
		show_inventory = action.get('show_inventory')
		drop_inventory = action.get('drop_inventory')
		drop_equipment = action.get('drop_equipment')
		show_equipment_inventory = action.get('show_equipment_inventory')
		show_bag = action.get('show_bag')
		inventory_index = action.get('inventory_index')
		equipment_inventory_index = action.get('equipment_inventory_index')
		take_stairs = action.get('take_stairs')
		level_up = action.get('level_up')
		show_character_screen = action.get('show_character_screen')
		show_help_menu = action.get('show_help_menu')
		exit = action.get('exit')
		exit_quit_menu = action.get('exit_quit_menu')
		fullscreen = action.get('fullscreen')
		cast_magic_wand = action.get('cast_magic_wand')
		shoot_bow = action.get('shoot_bow')
		drop_menu = action.get('drop_menu')
		sell_menu = action.get('sell_menu')
		sell_equipment_menu = action.get('sell_equipment_menu')
		buy_menu = action.get('buy_menu')
		buy_equipment_menu = action.get('buy_equipment_menu')
		shop_menu = action.get('shop_menu')
		shop_menu_index = action.get('shop_menu_index')
		shop_equipment_menu_index = action.get('shop_equipment_menu_index')

		left_click = mouse_action.get('left_click')
		right_click = mouse_action.get('right_click')

		player_turn_results = []

		if begin_player_turn and game_state == GameStates.PLAYERS_TURN:
			begin_player_turn = False

			if player.fighter.status:
				player_turn_results.extend(player.fighter.status.update())

		if move and game_state == GameStates.PLAYERS_TURN:
			if player.fighter.status:
				if player.fighter.status.name == "Frozen":
					dx = 0
					dy = 0
					destination_x = player.x + dx
					destination_y = player.y + dy
				elif player.fighter.status.name == "Haste":
					dx, dy = move
					dx *= 2
					dy *= 2
					destination_x = player.x + dx
					destination_y = player.y + dy
				else:
					dx, dy = move
					destination_x = player.x + dx
					destination_y = player.y + dy
			else:
				dx, dy = move
				destination_x = player.x + dx
				destination_y = player.y + dy

			if not game_map.is_blocked(destination_x, destination_y):
				if player.fighter.status:
					if player.fighter.status.name == "Frozen":
						target = None
					else:
						target = get_blocking_entities_at_location(entities, destination_x, destination_y)
				else:
					target = get_blocking_entities_at_location(entities, destination_x, destination_y)

				if target:
					attack_results = player.fighter.attack(target, constants, entities=entities)
					#playsound('sounds/attack.mp3', block=False)
					player_turn_results.extend(attack_results)
				else:
					player.move(dx, dy)

					fov_recompute = True

				game_state = GameStates.ENEMY_TURN

		elif wait:
			game_state = GameStates.ENEMY_TURN

		elif pickup and game_state == GameStates.PLAYERS_TURN:
			for entity in entities:
				if entity.item and (not entity.equippable) and entity.x == player.x and entity.y == player.y:
					pickup_results = player.inventory.add_item(entity)
					player_turn_results.extend(pickup_results)

					break

				elif entity.item and entity.x == player.x and entity.y == player.y:
					pickup_results = player.equipment_inventory.add_item(entity)
					player_turn_results.extend(pickup_results)

					break
			else:
				message_log.add_message(Message("There is nothing here to pick up...", libtcod.yellow))

		if show_inventory:
			previous_game_state = game_state
			game_state = GameStates.SHOW_INVENTORY

		if show_equipment_inventory:
			previous_game_state = game_state
			game_state = GameStates.SHOW_EQUIPMENT_INVENTORY

		if drop_inventory:
			previous_game_state = game_state
			game_state = GameStates.DROP_INVENTORY

		if drop_equipment:
			previous_game_state = game_state
			game_state = GameStates.DROP_EQUIPMENT

		if show_bag:
			previous_game_state = game_state
			game_state = GameStates.SHOW_BAG

		if drop_menu:
			previous_game_state = game_state
			game_state = GameStates.DROP_MENU

		if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
			item = player.inventory.items[inventory_index]

			if game_state == GameStates.SHOW_INVENTORY:
				player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
			elif game_state == GameStates.DROP_INVENTORY:
				player_turn_results.extend(player.inventory.drop_item(item))
			elif game_state == GameStates.SELL_MENU:
				player_turn_results.extend(player.inventory.sell(item, game_state))

		if equipment_inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and equipment_inventory_index < len(player.equipment_inventory.items):
			equip_item = player.equipment_inventory.items[equipment_inventory_index]

			if game_state == GameStates.SHOW_EQUIPMENT_INVENTORY:
				player_turn_results.extend(player.equipment_inventory.use(equip_item))
			elif game_state == GameStates.DROP_EQUIPMENT:
				player_turn_results.extend(player.equipment_inventory.drop_item(equip_item))
			elif game_state == GameStates.SELL_EQUIPMENT_MENU:
				player_turn_results.extend(player.equipment_inventory.sell(equip_item, game_state))

		if shop_menu_index is not None and previous_game_state != GameStates.PLAYER_DEAD:
			item = game_map.shop_items[shop_menu_index]

			if game_state == GameStates.BUY_MENU:
				player_turn_results.extend(player.inventory.buy(item, game_state))

		if shop_equipment_menu_index is not None and previous_game_state != GameStates.PLAYER_DEAD:
			item = game_map.shop_equipment_items[shop_equipment_menu_index]

			if game_state == GameStates.BUY_EQUIPMENT_MENU:
				player_turn_results.extend(player.equipment_inventory.buy(item, game_state))

		if take_stairs and game_state == GameStates.PLAYERS_TURN:
			for entity in entities:
				if entity.name == "Up Stairs" and entity.x == player.x and entity.y == player.y:
					entities = game_map.go_to_village(player, message_log, constants)
					fov_map = initialize_fov(game_map)
					fov_recompute = True
					libtcod.console_clear(con)

					break

				elif entity.stairs and entity.x == player.x and entity.y == player.y:
					entities = game_map.next_floor(player, message_log, constants)
					fov_map = initialize_fov(game_map)
					fov_recompute = True
					libtcod.console_clear(con)

					break
			else:
				message_log.add_message(Message("There are no stairs here...", libtcod.yellow))

		if cast_magic_wand and game_state == GameStates.PLAYERS_TURN:
			wand = player.inventory.search("Magic Wand")
			staff = player.inventory.search("Wizard Staff")
			if wand is None and staff is None:
			    message_log.add_message(Message("You cannot cast magic without a magic item!", libtcod.orange))
			else:
				if player.fighter.status:
					if player.fighter.status.name == "Frozen":
						game_state = GameStates.ENEMY_TURN
					else:
						player_turn_results.extend(player.inventory.use(wand, entities=entities, fov_map=fov_map))
				else:
					player_turn_results.extend(player.inventory.use(wand, entities=entities, fov_map=fov_map))

				game_state = GameStates.ENEMY_TURN

		if shoot_bow and game_state == GameStates.PLAYERS_TURN:
			bow = player.inventory.search("Long Bow")
			arrow = player.inventory.search("Arrow")
			fire_arrow = player.inventory.search("Fire Arrow")
			if bow is None and arrow is None and fire_arrow is None:
			    message_log.add_message(Message("You don't have anything to shoot with at this time!", libtcod.orange))
			elif bow is None and (arrow is not None or fire_arrow is not None):
				message_log.add_message(Message("You cannot shoot an arrow without a bow!", libtcod.orange))
			elif bow is not None and (arrow is None and fire_arrow is None):
				message_log.add_message(Message("You need arrows to use your bow", libtcod.orange))
			else:
				if player.fighter.status:
					if player.fighter.status.name == "Frozen":
						game_state = GameStates.ENEMY_TURN
					else:
						player_turn_results.extend(player.inventory.use(bow, entities=entities, fov_map=fov_map))
				else:
					player_turn_results.extend(player.inventory.use(bow, entities=entities, fov_map=fov_map))

				game_state = GameStates.ENEMY_TURN

		if level_up:
			if level_up == 'hp':
				player.fighter.base_max_hp += 20
				player.fighter.hp += 20
				message_log.add_message(Message("You leveled up your HP!", libtcod.light_cyan))
			elif level_up == 'str':
				player.fighter.base_power += 1
				message_log.add_message(Message("You leveled up your ATTACK!", libtcod.light_cyan))
			elif level_up == 'def':
				player.fighter.base_defense += 1
				message_log.add_message(Message("You leveled up your DEFENSE!", libtcod.light_cyan))
			elif level_up == 'mgk':
				player.fighter.base_magic += 1
				message_log.add_message(Message("You leveled up your MAGIC!", libtcod.light_cyan))
			elif level_up == 'mgk_def':
				player.fighter.base_magic_defense += 1
				message_log.add_message(Message("You leveled up your MAGIC RESISTANCE!", libtcod.light_cyan))

			game_state = previous_game_state

		if show_character_screen:
			previous_game_state = game_state
			game_state = GameStates.CHARACTER_SCREEN

		if show_help_menu:
			previous_game_state = game_state
			game_state = GameStates.HELP_MENU

		if sell_menu:
			previous_game_state = game_state
			game_state = GameStates.SELL_MENU

		if sell_equipment_menu:
			previous_game_state = game_state
			game_state = GameStates.SELL_EQUIPMENT_MENU

		if buy_menu:
			previous_game_state = game_state
			game_state = GameStates.BUY_MENU

		if buy_equipment_menu:
			previous_game_state = game_state
			game_state = GameStates.BUY_EQUIPMENT_MENU

		if shop_menu:
			previous_game_state = game_state
			game_state = GameStates.SHOP_MENU

		if game_state == GameStates.TARGETING:
			if left_click:
				target_x, target_y = left_click

				item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(item_use_results)
			elif right_click:
				player_turn_results.append({'targeting_cancelled': True})

		if exit:
			if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.DROP_EQUIPMENT, GameStates.CHARACTER_SCREEN, GameStates.HELP_MENU, GameStates.SHOW_EQUIPMENT_INVENTORY, GameStates.SELL_MENU, GameStates.BUY_MENU, GameStates.SELL_EQUIPMENT_MENU, GameStates.BUY_EQUIPMENT_MENU):
				game_state = previous_game_state
			elif game_state == GameStates.TARGETING:
				player_turn_results.append({'targeting_cancelled': True})
			elif game_state == GameStates.SHOW_BAG:
				if PLAYERDEADSTATE == True:
					game_state = GameStates.PLAYER_DEAD
				else:
					game_state = GameStates.PLAYERS_TURN
			elif game_state == GameStates.SHOP_MENU:
				if PLAYERDEADSTATE == True:
					game_state = GameStates.PLAYER_DEAD
				else:
					game_state = GameStates.PLAYERS_TURN
			elif game_state == GameStates.PLAYERS_TURN:
				game_state = GameStates.QUIT_MENU
			elif game_state == GameStates.DROP_MENU:
				game_state = GameStates.PLAYERS_TURN
			else:
				save_game(player, entities, game_map, message_log, game_state)
				
				return True

		if exit_quit_menu:
			if game_state == GameStates.QUIT_MENU:
				game_state = previous_game_state

		if fullscreen:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

		for player_turn_result in player_turn_results:
			message = player_turn_result.get('message')
			dead_entity = player_turn_result.get('dead')
			item_added = player_turn_result.get('item_added')
			equipment_item_added = player_turn_result.get('equipment_item_added')
			item_consumed = player_turn_result.get('consumed')
			equipment_consumed = player_turn_result.get('equipment_consumed')
			item_dropped = player_turn_result.get('item_dropped')
			loot_dropped = player_turn_result.get('loot_dropped')
			staff_used = player_turn_result.get('staff_used')
			equip = player_turn_result.get('equip')
			targeting = player_turn_result.get('targeting')
			targeting_cancelled = player_turn_result.get('targeting_cancelled')
			xp = player_turn_result.get('xp')
			item_bought = player_turn_result.get('item_bought')
			equipment_bought = player_turn_result.get('equipment_bought')
			end_turn = player_turn_result.get('end_turn')

			if message:
				message_log.add_message(message)

			if targeting_cancelled:
				game_state = previous_game_state

				message_log.add_message(Message('Targeting cancelled'))

			if xp:
				leveled_up = player.level.add_xp(xp)
				message_log.add_message(Message("You gain {0} experience points.".format(xp)))

				if leveled_up:
					message_log.add_message(Message("Your battle prowess grows stronger! You reached level {0}!".format(player.level.current_level), libtcod.yellow))
					previous_game_state =  game_state
					game_state = GameStates.LEVEL_UP

			if dead_entity:
				if dead_entity == player:
					PLAYERDEADSTATE = True
					message, game_state = kill_player(dead_entity, constants)
					message_log.add_message(message)
				else:
					monster_name = ''
					monster_name = dead_entity.name
					message = kill_monster(dead_entity, player, constants)
					constants['kill_count'] += 1
					message_log.add_message(message)

					while dead_entity.equipment_inventory.items:
						item = dead_entity.equipment_inventory.items[0]
						dead_entity.equipment_inventory.loot_item(item)
						entities.append(item)
						message_log.add_message(Message("The {0} dropped the {1}.".format(monster_name, item.name), libtcod.yellow))

					while dead_entity.inventory.items:
						item = dead_entity.inventory.items[0]
						dead_entity.inventory.loot_item(item)
						entities.append(item)
						message_log.add_message(Message("The {0} dropped the {1}.".format(monster_name, item.name), libtcod.yellow))

			if item_added:
				entities.remove(item_added)

				game_state = GameStates.ENEMY_TURN

			if equipment_item_added:
				entities.remove(equipment_item_added)

				game_state = GameStates.ENEMY_TURN

			if item_consumed:
				game_state = GameStates.ENEMY_TURN

			if item_bought:
				game_map.shop_items.remove(item_bought)

				game_state = GameStates.ENEMY_TURN

			if equipment_bought:
				game_map.shop_equipment_items.remove(equipment_bought)

				game_state = GameStates.ENEMY_TURN

			if equipment_consumed:
				game_state = GameStates.ENEMY_TURN

			if staff_used:
				game_state = GameStates.ENEMY_TURN

			if end_turn:
				game_state = GameStates.ENEMY_TURN

			if targeting:
				previous_game_state = GameStates.PLAYERS_TURN
				game_state = GameStates.TARGETING

				targeting_item = targeting

				message_log.add_message(targeting_item.item.targeting_message)

			if item_dropped:
				entities.append(item_dropped)

				game_state = GameStates.ENEMY_TURN

			if loot_dropped:
				entities.append(loot_dropped)

				game_state = GameStates.ENEMY_TURN

			if equip:
				equip_results = player.equipment.toggle_equip(equip)

				for equip_result in equip_results:
					equipped = equip_result.get('equipped')
					dequipped = equip_result.get('dequipped')

					if equipped:
						message_log.add_message(Message("You equipped the {0}".format(equipped.name)))

					if dequipped:
						message_log.add_message(Message("You dequipped the {0}".format(dequipped.name)))

				game_state = GameStates.ENEMY_TURN

		if game_state == GameStates.ENEMY_TURN:
			fov_recompute = True
			for entity in entities:
				if entity.ai:

					enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities, constants)

					if entity.fighter.status:
						enemy_turn_results.extend(entity.fighter.status.update())

					for enemy_turn_result in enemy_turn_results:
						message = enemy_turn_result.get('message')
						dead_entity = enemy_turn_result.get('dead')

						if message:
							message_log.add_message(message)

						if dead_entity:
							if dead_entity == player:
								PLAYERDEADSTATE = True
								message, game_state = kill_player(dead_entity, constants)
								message_log.add_message(message)
							else:
								monster_name = ''
								monster_name = dead_entity.name
								message = kill_monster(dead_entity, player, constants)
								constants['kill_count'] += 1
								message_log.add_message(message)

								while dead_entity.equipment_inventory.items:
									item = dead_entity.equipment_inventory.items[0]
									dead_entity.equipment_inventory.loot_item(item)
									entities.append(item)
									message_log.add_message(Message("The {0} dropped the {1}.".format(monster_name, item.name), libtcod.yellow))

								while dead_entity.inventory.items:
									item = dead_entity.inventory.items[0]
									dead_entity.inventory.loot_item(item)
									entities.append(item)
									message_log.add_message(Message("The {0} dropped the {1}.".format(monster_name, item.name), libtcod.yellow))

							if game_state == GameStates.PLAYER_DEAD:
								break
					if game_state == GameStates.PLAYER_DEAD:
						break
			else:
				game_state = GameStates.PLAYERS_TURN
				begin_player_turn = True

def main():
	constants = get_constants()

	libtcod.console_set_custom_font('TiledFont.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD, 32, 10)

	load_customfont()

	libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

	con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
	panel = libtcod.console_new(constants['screen_width'],constants['panel_height'])

	player = None
	entities = []
	game_map = None
	message_log = None
	game_state = None

	show_main_menu = True
	show_load_error_message = False
	show_main_help_menu = False

	main_menu_background_image = libtcod.image_load('menu_background.png')

	key = libtcod.Key()
	mouse = libtcod.Mouse()

	while not libtcod.console_is_window_closed():
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

		if show_main_menu:
			main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])

			if show_load_error_message:
				message_box(con, "No save game to load", 50, constants['screen_width'], constants['screen_height'])

			if show_main_help_menu:
				main_menu_help_menu(con, 30, 13, constants['screen_width'], constants['screen_height'])

			libtcod.console_flush()

			action = handle_main_menu(key)

			new_game = action.get('new_game')
			load_saved_game = action.get('load_game')
			exit_game = action.get('exit')
			main_help_menu = action.get('main_help_menu')

			if show_load_error_message and (new_game or load_saved_game or exit_game or main_help_menu):
				show_load_error_message = False
			elif show_main_help_menu and (new_game or load_saved_game or exit_game or main_help_menu):
				show_main_help_menu = False
			elif new_game:
				player, entities, game_map, message_log, game_state = get_game_variables(constants)
				game_state = GameStates.PLAYERS_TURN

				show_main_menu = False
			elif load_saved_game:
				try:
					player, entities, game_map, message_log, game_state = load_game()
					show_main_menu = False
				except FileNotFoundError:
					show_load_error_message = True

			elif main_help_menu:
				show_main_help_menu = True

			elif exit_game:
				break

		else:
			libtcod.console_clear(con)
			play_game(player, entities, game_map, message_log, game_state, con, panel, constants)

			show_main_menu = True

def load_customfont():
	#the index of the first custom tile in the file
	a = 256

	#the y is the row index, this is loading the 6th row in the font file. Increase the 6 to load any new rows from the file (added the 7)
	for y in range(5, 7):
		libtcod.console_map_ascii_codes_to_font(a, 32, 0, y)
		a += 32

if __name__ == '__main__':
	main()