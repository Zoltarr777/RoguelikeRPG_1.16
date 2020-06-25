import libtcodpy as libtcod

from enum import Enum

from game_states import GameStates

from menus import character_screen, inventory_menu, level_up_menu, bag_menu, help_menu, equipment_inventory_menu, quit_menu, drop_menu, sell_menu, buy_menu, shop_menu, buy_equipment_menu, sell_equipment_menu

from components.inventory import Inventory

class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER, "{0}: {1}/{2}".format(name, value, maximum))

def render_line(panel, x, y, width, color):
    libtcod.console_set_default_background(panel, color)
    libtcod.console_rect(panel, x, y, width, 1, False, libtcod.BKGND_SCREEN)

def render_vert(panel, x, y, width, height, color):
    libtcod.console_set_default_background(panel, color)
    libtcod.console_rect(panel, x, y, width, height, False, libtcod.BKGND_SCREEN)

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, kill_count, game_state, wall_tile, floor_tile, grass_tile):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if game_map.dungeon_level == 0:
                    if visible:
                        if wall:
                            libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.white, libtcod.black)
                        else:
                            libtcod.console_put_char_ex(con, x, y, grass_tile, libtcod.white, libtcod.black)

                        game_map.tiles[x][y].explored = True

                    elif game_map.tiles[x][y].explored:
                        if wall:
                            libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.grey, libtcod.black)
                        else:
                            libtcod.console_put_char_ex(con, x, y, grass_tile, libtcod.grey, libtcod.black)

                else:
                    if visible:
                        if wall:
                            libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.white, libtcod.black)
                        else:
                            libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.white, libtcod.black)

                        game_map.tiles[x][y].explored = True

                    elif game_map.tiles[x][y].explored:
                        if wall:
                            libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.grey, libtcod.black)
                        else:
                            libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.grey, libtcod.black)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map, floor_tile)

    libtcod.console_set_default_foreground(con, libtcod.black)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE,libtcod.LEFT, message.text)
        y += 1

# 0 - Description names under mouse
# 1 - HP
# 2 - Talisman Health
# 3 - Mana
# 4 - EXP
# 5 - Status
# 6 - Gold
# 7 - Dungeon Level

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))
    
    # BORDERS
    #render_line(panel, 0, 1, screen_width, libtcod.darkest_sky)
    #render_vert(panel, 20, 2, 1, 7, libtcod.darkest_sky)

    render_bar(panel, 0, 1, bar_width, "HP", player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)

    if player.inventory.search("Health Talisman") is not None:
        render_bar(panel, 0, 2, bar_width, "Talisman HP", player.fighter.talismanhp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
        render_bar(panel, 0, 3, bar_width, "MANA", player.fighter.mana, player.fighter.max_mana, libtcod.dark_purple, libtcod.darker_purple)
        render_bar(panel, 0, 4, bar_width, "EXP", player.level.current_xp, player.level.experience_to_next_level, libtcod.light_blue, libtcod.darker_blue)
    else:
        render_bar(panel, 0, 2, bar_width, "MANA", player.fighter.mana, player.fighter.max_mana, libtcod.dark_purple, libtcod.darker_purple)
        render_bar(panel, 0, 3, bar_width, "EXP", player.level.current_xp, player.level.experience_to_next_level, libtcod.light_blue, libtcod.darker_blue)    


    if player.fighter.status is not None:
        status = player.fighter.status.name
        libtcod.console_print_ex(panel, 0, 6, libtcod.BKGND_NONE, libtcod.LEFT, "Status: {0}".format(status))


    libtcod.console_print_ex(panel, 0, 7, libtcod.BKGND_NONE, libtcod.LEFT, "Gold: {0}".format(player.fighter.gold))
    
    if game_map.dungeon_level == 0:
        libtcod.console_print_ex(panel, 0, 8, libtcod.BKGND_NONE, libtcod.LEFT, "Village")
    else:
        libtcod.console_print_ex(panel, 0, 8, libtcod.BKGND_NONE, libtcod.LEFT, "Dungeon Level: {0}".format(game_map.dungeon_level))


    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = "Press the key next to an item to use it, or ESC to cancel.\n"
        elif game_state == GameStates.DROP_INVENTORY:
            inventory_title = "Press the key next to an item to drop it, or ESC to cancel.\n"

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state in (GameStates.SHOW_EQUIPMENT_INVENTORY, GameStates.DROP_EQUIPMENT):
        if game_state == GameStates.SHOW_EQUIPMENT_INVENTORY:
            inventory_title = "Press the key next to an item to equip it, or ESC to cancel.\n"
        else:
            inventory_title = "Press the key next to the equipment to drop it, or ESC to cancel.\n"

        equipment_inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, "Level up! Choose a stat to raise:\n", player, 46, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height, kill_count)

    elif game_state == GameStates.SHOW_BAG:
        bag_title = "Press the key next to the option to open the bag.\n"

        bag_menu(con, bag_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.HELP_MENU:
        help_menu(player, 30, 10, screen_width, screen_height)

    elif game_state == GameStates.QUIT_MENU:
        quit_title = "ARE YOU SURE YOU WANT\n  TO QUIT THE GAME?\n"

        quit_menu(con, quit_title, player, 21, screen_width, screen_height)

    elif game_state == GameStates.DROP_MENU:
        drop_title = "Which inventory would you like to drop items from?"

        drop_menu(con, drop_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.SELL_MENU:
        shop_title = "Welcome to the Shop!\nWhat would you like to sell?\n"

        sell_menu(con, shop_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.BUY_MENU:
        shop_title = "Welcome to the Shop!\nWhat would you like to buy?\n"

        buy_menu(con, shop_title, player, 50, screen_width, screen_height, game_map.shop_items)

    elif game_state == GameStates.SELL_EQUIPMENT_MENU:
        shop_title = "Welcome to the Shop!\nWhat would you like to sell?\n"

        sell_equipment_menu(con, shop_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.BUY_EQUIPMENT_MENU:
        shop_title = "Welcome to the Shop!\nWhat would you like to buy?\n"

        buy_equipment_menu(con, shop_title, player, 50, screen_width, screen_height, game_map.shop_equipment_items)

    elif game_state == GameStates.SHOP_MENU:
        shop_title = "Welcome to the Shop!\nWhat would you like to do?\n"

        shop_menu(con, shop_title, player, 50, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map, game_map, floor_tile):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

    if not libtcod.map_is_in_fov(fov_map, entity.x, entity.y) and not entity.stairs and game_map.tiles[entity.x][entity.y].explored:
    	libtcod.console_set_default_foreground(con, entity.color)
    	libtcod.console_put_char_ex(con, entity.x, entity.y, floor_tile, libtcod.grey, libtcod.black)


def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)


