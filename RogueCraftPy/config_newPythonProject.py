"""Configuration file: variables named here can be tweaked to adjust game balance"""
import libtcodpy as libtcod

PROJECT_NAME = 'newPythonProject'

#sets screen width and height
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
#camera params
CAMERA_WIDTH = 80
CAMERA_HEIGHT = 43
#FOV Settings
FOV_ALGO = 0 #default algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 12
#GUI params
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
INVENTORY_WIDTH = 50
LEVEL_SCREEN_WIDTH = 40
CHARACTER_SCREEN_WIDTH = 30
#message log params
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
#sets fps
LIMIT_FPS = 20

#tile colors
color_dark_wall = libtcod.Color(30,30,30)
color_nolight_wall = libtcod.Color(10,10,10)
color_not_in_view_wall = libtcod.Color(8,8,16)
color_light_wall = libtcod.Color(133,133,42)
color_dark_ground = libtcod.Color(60,60,60)
color_nolight_ground = libtcod.Color(20,20,20)
color_not_in_view_ground = libtcod.Color(10,10,20)
color_light_ground = libtcod.Color(210,210,67)

