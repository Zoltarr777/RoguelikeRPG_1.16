import libtcodpy as libtcod

from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys( key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)
    elif game_state == GameStates.SHOW_EQUIPMENT_INVENTORY:
        return handle_equipment_inventory_keys(key)
    elif game_state == GameStates.SHOW_BAG:
        return handle_bag_keys(key)
    elif game_state == GameStates.HELP_MENU:
        return handle_help_menu(key)
    elif game_state == GameStates.QUIT_MENU:
        return handle_quit_menu(key)
    elif game_state == GameStates.DROP_MENU:
        return handle_drop_menu(key)
    elif game_state == GameStates.DROP_EQUIPMENT:
        return handle_drop_equipment_keys(key)
    elif game_state == GameStates.SELL_MENU:
        return handle_sell_menu(key)
    elif game_state == GameStates.BUY_MENU:
        return handle_buy_menu(key)
    elif game_state == GameStates.SELL_EQUIPMENT_MENU:
        return handle_sell_equipment_menu(key)
    elif game_state == GameStates.BUY_EQUIPMENT_MENU:
        return handle_buy_equipment_menu(key)
    elif game_state == GameStates.SHOP_MENU:
        return handle_shop_menu(key)


    return {}

def handle_player_turn_keys(key):

    # A - LEFT
    # B - BOW
    # C - CHARACTER SCREEN
    # D - RIGHT
    # E - UP RIGHT
    # F -
    # G - GET
    # H - HELP
    # I - INVENTORY
    # J -
    # K -
    # L -
    # M - MAGIC
    # N -
    # O - SHOP
    # P - PASS
    # Q - UP LEFT
    # R -
    # S - DOWN
    # T -
    # U - DROP ITEMS
    # V -
    # W - UP
    # X - DOWN RIGHT
    # Y - 
    # Z - DOWN LEFT

    key_char = chr(key.c)

    if key.vk == libtcod.KEY_UP or key_char == 'w':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 's':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'a':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'd':
        return {'move': (1, 0)}
    elif key_char == 'q':
        return {'move': (-1, -1)}
    elif key_char == 'e':
        return {'move': (1, -1)}
    elif key_char == 'z':
        return {'move': (-1, 1)}
    elif key_char == 'x':
        return {'move': (1, 1)}
    elif key_char == 'p':
        return {'wait': True}

    if key_char == 'g':
        return {'pickup': True}

    elif key_char == 'i':
        return {'show_bag': True}

    elif key_char == 'u':
        return {'drop_menu': True}

    elif key.vk == libtcod.KEY_ENTER:
    	return {'take_stairs': True}

    elif key_char == 'm':
        return  {'cast_magic_wand': True}

    elif key_char == 'b':
        return {'shoot_bow': True}

    elif key_char == 'c':
        return {'show_character_screen': True}

    elif key_char == 'h':
        return {'show_help_menu': True}

    elif key_char == "o":
        return {'shop_menu': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_player_dead_keys(key):
	key_char = chr(key.c)

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}

	return {}

def handle_inventory_keys(key):
	index = key.c - ord('a')

	if index >= 0:
		return {'inventory_index': index}

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}

	return {}

def handle_equipment_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'equipment_inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_drop_equipment_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'equipment_inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_bag_keys(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'show_inventory': True}
    elif key_char == 'b':
        return {'show_equipment_inventory': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_shop_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'sell_menu': True}
    elif key_char == 'b':
        return {'buy_menu': True}
    if key_char == 'c':
        return {'sell_equipment_menu': True}
    elif key_char == 'd':
        return {'buy_equipment_menu': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_sell_menu(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_buy_menu(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'shop_menu_index': index}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_sell_equipment_menu(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'equipment_inventory_index': index}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_buy_equipment_menu(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'shop_equipment_menu_index': index}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key_char == 'h':
        return {'main_help_menu': True}
    elif key_char == 'd' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_level_up_menu(key):
    if key:
        key_char = chr(key.c)

        if key_char == '1':
            return {'level_up': 'hp'}
        elif key_char == '2':
            return {'level_up': 'str'}
        elif key_char == '3':
            return {'level_up': 'def'}
        elif key_char == '4':
            return {'level_up': 'mgk'}
        elif key_char == '5':
            return {'level_up': 'mgk_def'}

    return {}

def handle_character_screen(key):
    key_char = chr(key.c)
    
    if key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_help_menu(key):
    key_char = chr(key.c)
    
    if key_char == 'h' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_quit_menu(key):
    key_char = chr(key.c)

    if key_char == '1' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    elif key_char == '2':
        return {'exit_quit_menu': True}

    return {}

def handle_drop_menu(key):
    key_char = chr(key.c)

    if key_char == '1':
        return {'drop_inventory': True}
    elif key_char == '2':
        return {'drop_equipment': True}
    elif key_char == '3' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}