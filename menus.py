import tcod as libtcod

from random import randint
import random

def menu(con, header, options, width, screen_width, screen_height):
	if len(options) > 26: raise ValueError("Cannot have a menu with more than 26 options.")

	header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
	height = len(options) + header_height

	window = libtcod.console_new(width, height)

	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ') ' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1

	x = int(screen_width / 2 - width / 2)
	y = int(screen_height / 2 - height / 2)
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def number_menu(con, header, options, width, screen_width, screen_height):
	if len(options) > 9: raise ValueError("Cannot have a number menu with more than 9 options.")

	header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
	height = len(options) + header_height

	window = libtcod.console_new(width, height)

	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	y = header_height
	number_index = ord('1')
	for option_text in options:
		text = '(' + chr(number_index) + ') ' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		number_index += 1

	x = int(screen_width / 2 - width / 2)
	y = int(screen_height / 2 - height / 2)
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def quit_menu(con, header, player, menu_width, screen_width, screen_height):
	options = ["YES", "NO"]

	number_menu(con, header, options, menu_width, screen_width, screen_height)

def drop_menu(con, header, player, menu_width, screen_width, screen_height):
	options = ["ITEMS", "EQUIPMENT", "CANCEL"]
	number_menu(con, header, options, menu_width, screen_width, screen_height)

def bag_menu(con, header, player, menu_width, screen_width, screen_height):
	options = ["Items", "Equipment"]
	menu(con, header, options, menu_width, screen_width, screen_height)

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
	if len(player.inventory.items) == 0:
		options = ["Your inventory is empty."]
	else:
		options = []

		for item in player.inventory.items:
			if player.equipment.main_hand == item:
				options.append("{0} (in main hand)".format(item.name))
			elif player.equipment.off_hand == item:
				options.append("{0} (in off hand)".format(item.name))
			elif player.equipment.chest == item:
				options.append("{0} (on chest)".format(item.name))
			elif player.equipment.legs == item:
				options.append("{0} (on legs)".format(item.name))
			elif player.equipment.head == item:
				options.append("{0} (on head)".format(item.name))
			elif player.equipment.amulet == item:
				options.append("{0} (in amulet)".format(item.name))
			else:
				options.append(item.name)

	menu(con, header, options, inventory_width, screen_width, screen_height)

def equipment_inventory_menu(con, header, player, equipment_inventory_width, screen_width, screen_height):
	if len(player.equipment_inventory.items) == 0:
		options = ["You don't have any equipment."]
	else:
		options = []

		for item in player.equipment_inventory.items:
			if player.equipment.main_hand == item:
				options.append("{0} (in main hand)".format(item.name))
			elif player.equipment.off_hand == item:
				options.append("{0} (in off hand)".format(item.name))
			elif player.equipment.chest == item:
				options.append("{0} (on chest)".format(item.name))
			elif player.equipment.legs == item:
				options.append("{0} (on legs)".format(item.name))
			elif player.equipment.head == item:
				options.append("{0} (on head)".format(item.name))
			elif player.equipment.amulet == item:
				options.append("{0} (in amulet)".format(item.name))
			else:
				options.append(item.name)

	menu(con, header, options, equipment_inventory_width, screen_width, screen_height)

def shop_menu(con, header, player, menu_width, screen_width, screen_height):
	options = ["SELL ITEMS", "BUY ITEMS",  "SELL EQUIPMENT", "BUY EQUIPMENT"]
	menu(con, header, options, menu_width, screen_width, screen_height)

def sell_menu(con, header, player, inventory_width, screen_width, screen_height, **kwargs):
	if len(player.inventory.items) == 0:
		options = ["You have nothing to sell..."]
	else:
		options = []

		for item in player.inventory.items:
			gold_value = kwargs.get('gold')
			options.append("{0} . . . {1} G".format(item.name, item.item.function_kwargs['gold']))

	menu(con, header, options, inventory_width, screen_width, screen_height)

def sell_equipment_menu(con, header, player, inventory_width, screen_width, screen_height, **kwargs):
	if len(player.equipment_inventory.items) == 0:
		options = ["You have nothing to sell..."]
	else:
		options = []

		for item in player.equipment_inventory.items:
			gold_value = kwargs.get('gold')
			options.append("{0} . . . {1} G".format(item.name, item.equippable.function_kwargs['gold']))

	menu(con, header, options, inventory_width, screen_width, screen_height)

def buy_menu(con, header, player, menu_width, screen_width, screen_height, shop_items):
	if len(shop_items) == 0:
		options = ["There is nothing to buy today."]
	else:
		options = []

		for item in shop_items:
			options.append("{0} . . . {1} G".format(item.name, item.item.function_kwargs['gold']))

	menu(con, header, options, menu_width, screen_width, screen_height)

def buy_equipment_menu(con, header, player, menu_width, screen_width, screen_height, shop_equipment_items):
	if len(shop_equipment_items) == 0:
		options = ["There is nothing to buy today."]
	else:
		options = []

		for item in shop_equipment_items:
			options.append("{0} . . . {1} G".format(item.name, item.equippable.function_kwargs['gold']))

	menu(con, header, options, menu_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):
	libtcod.image_blit_2x(background_image, 0, 0, 0)

	libtcod.console_set_default_foreground(0, libtcod.light_yellow)
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, "ROGUELIKE RPG")
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 4), libtcod.BKGND_NONE, libtcod.CENTER, "By Zoltarr777, 2020")
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER, "Version Alpha 1.16")
	menu(con, '', ["Play a new game", "Continue last game", "Help", "Quit"], 24, screen_width, screen_height)

def main_menu_help_menu(con, help_menu_width, help_menu_height, screen_width, screen_height):
	help_menu_width = 38
	help_menu_height = 14
	window = libtcod.console_new(help_menu_width, help_menu_height)
	menu_title = help_menu_width // 2 - 4

	libtcod.console_set_default_foreground(window, libtcod.white)

	libtcod.console_print_rect_ex(window, menu_title, 1, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "HELP MENU")
	libtcod.console_print_rect_ex(window, 0, 3, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> WASD: Cardinal movement")
	libtcod.console_print_rect_ex(window, 0, 4, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> QEZX: Diagonal movement")
	libtcod.console_print_rect_ex(window, 0, 5, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> ENTER: Descend stairs")
	libtcod.console_print_rect_ex(window, 0, 6, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> ESC: Exit and save the game")
	libtcod.console_print_rect_ex(window, 0, 7, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> MOUSE over objects for descriptions")
	libtcod.console_print_rect_ex(window, 0, 8, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> G: Pick up objects")
	libtcod.console_print_rect_ex(window, 0, 9, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> M: Attack with magic wand")
	libtcod.console_print_rect_ex(window, 0, 10, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> I: Open the INVENTORY")
	libtcod.console_print_rect_ex(window, 0, 11, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> C: Open the CHARACTER SCREEN")
	libtcod.console_print_rect_ex(window, 0, 12, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> U: Drop items")
	libtcod.console_print_rect_ex(window, 0, 13, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> P: Wait (Skip a turn)")
	libtcod.console_print_rect_ex(window, 0, 14, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> H: Open the HELP MENU")

	x = screen_width // 2 - help_menu_width // 2
	y = screen_height // 2 - help_menu_height // 2
	libtcod.console_blit(window, 0, 0, help_menu_width, help_menu_height, 0, x, y, 1.0, 1.0)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
	options = ["Constitution (+20 HP, from {0})".format(player.fighter.max_hp),
				"Strength (+1 attack, from {0})".format(player.fighter.power),
				"Resistance (+1 defense, from {0})".format(player.fighter.defense),
				"Magic (+1 magic, from {0})".format(player.fighter.magic),
				"Magic Resistance (+1 magic resist, from {0})".format(player.fighter.magic_defense)]

	number_menu(con, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height, kill_count):
	character_screen_width = 50
	character_screen_height = 21

	if player.equipment.head is None:
		helmet_name = "NONE"
	else:
		helmet_name = player.equipment.head.name

	if player.equipment.main_hand is None:
		main_name = "NONE"
	else:
		main_name = player.equipment.main_hand.name

	if player.equipment.off_hand is None:
		off_name = "NONE"
	else:
		off_name = player.equipment.off_hand.name

	if player.equipment.chest is None:
		chest_name = "NONE"
	else:
		chest_name = player.equipment.chest.name

	if player.equipment.legs is None:
		legs_name = "NONE"
	else:
		legs_name = player.equipment.legs.name

	if player.equipment.amulet is None:
		amulet_name = "NONE"
	else:
		amulet_name = player.equipment.amulet.name


	window = libtcod.console_new(character_screen_width, character_screen_height)

	libtcod.console_set_default_foreground(window, libtcod.white)

	libtcod.console_print_rect_ex(window, 3, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "CHARACTER INFORMATION")

	libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Level: {0}".format(player.level.current_level))
	libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Experience: {0}".format(player.level.current_xp))
	libtcod.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Experience to level up: {0}".format(player.level.experience_to_next_level))

	libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Max HP:    {0}".format(player.fighter.max_hp))
	libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Attack:    {0}".format(player.fighter.power))
	libtcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Defense:   {0}".format(player.fighter.defense))
	libtcod.console_print_rect_ex(window, 0, 10, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Magic:     {0}".format(player.fighter.magic))
	libtcod.console_print_rect_ex(window, 0, 11, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Magic Def: {0}".format(player.fighter.magic_defense))
	libtcod.console_print_rect_ex(window, 0, 12, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "Gold:      {0}".format(player.fighter.gold))
	libtcod.console_print_rect_ex(window, 0, 13, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "KILL COUNT:{0}".format(kill_count))

	libtcod.console_print_rect_ex(window, 0, 15, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "HELMET:    {0}".format(helmet_name))
	libtcod.console_print_rect_ex(window, 0, 16, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "MAIN HAND: {0}".format(main_name))
	libtcod.console_print_rect_ex(window, 0, 17, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "OFF HAND:  {0}".format(off_name))
	libtcod.console_print_rect_ex(window, 0, 18, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "CHEST:     {0}".format(chest_name))
	libtcod.console_print_rect_ex(window, 0, 19, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "LEGS:      {0}".format(legs_name))
	libtcod.console_print_rect_ex(window, 0, 20, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, "AMULET:    {0}".format(amulet_name))


	x = screen_width // 2 - character_screen_width // 2
	y = screen_height // 2 - character_screen_height // 2
	libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def help_menu(player, help_menu_width, help_menu_height, screen_width, screen_height):
	help_menu_width = 38
	help_menu_height = 14
	window = libtcod.console_new(help_menu_width, help_menu_height)
	menu_title = help_menu_width // 2 - 4

	libtcod.console_set_default_foreground(window, libtcod.white)

	libtcod.console_print_rect_ex(window, menu_title, 1, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "HELP MENU")
	libtcod.console_print_rect_ex(window, 0, 3, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> WASD: Cardinal movement")
	libtcod.console_print_rect_ex(window, 0, 4, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> QEZX: Diagonal movement")
	libtcod.console_print_rect_ex(window, 0, 5, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> ENTER: Descend stairs")
	libtcod.console_print_rect_ex(window, 0, 6, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> ESC: Exit and save the game")
	libtcod.console_print_rect_ex(window, 0, 7, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> MOUSE over objects for descriptions")
	libtcod.console_print_rect_ex(window, 0, 8, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> G: Pick up objects")
	libtcod.console_print_rect_ex(window, 0, 9, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> M: Attack with magic wand")
	libtcod.console_print_rect_ex(window, 0, 10, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> I: Open the INVENTORY")
	libtcod.console_print_rect_ex(window, 0, 11, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> C: Open the CHARACTER SCREEN")
	libtcod.console_print_rect_ex(window, 0, 12, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> U: Drop items")
	libtcod.console_print_rect_ex(window, 0, 13, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> P: Wait (Skip a turn)")
	libtcod.console_print_rect_ex(window, 0, 14, help_menu_width, help_menu_height, libtcod.BKGND_NONE, libtcod.LEFT, "> H: Open the HELP MENU")

	x = screen_width // 2 - help_menu_width // 2
	y = screen_height // 2 - help_menu_height // 2
	libtcod.console_blit(window, 0, 0, help_menu_width, help_menu_height, 0, x, y, 1.0, 0.7)

def message_box(con, header, width, screen_width, screen_height):
	menu(con, header, [], width, screen_width, screen_height)