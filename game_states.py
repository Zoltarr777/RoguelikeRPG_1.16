from enum import Enum


class GameStates(Enum):
	PLAYERS_TURN = 1
	ENEMY_TURN = 2
	PLAYER_DEAD = 3
	SHOW_INVENTORY = 4
	DROP_INVENTORY = 5
	TARGETING = 6
	LEVEL_UP = 7
	CHARACTER_SCREEN = 8
	SHOW_EQUIPMENT = 9
	SHOW_BAG = 10
	HELP_MENU = 11
	SHOW_EQUIPMENT_INVENTORY = 12
	QUIT_MENU = 13
	DROP_MENU = 14
	DROP_EQUIPMENT = 15
	SHOP_MENU = 16
	BUY_MENU = 17
	BUY_EQUIPMENT_MENU = 18
	SELL_MENU = 19
	SELL_EQUIPMENT_MENU = 20