#-------------------------------------------------------------------------------
# Name: GameConstants
# Purpose: Set of Constants for the Game
#
# Author:      Piccool
#
# Created:     03/02/2013
# Copyright:   (c) Piccool 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame

# GRAPHICAL CONSTANTS
DISP_GAME_WIDTH = 1024
DISP_GAME_HEIGHT = 768

DISP_PLAYABLE_WIDTH = 900
DISP_PLAYABLE_HEIGHT = 600

DISP_BUTTON_WIDTH = 100
DISP_BUTTON_HEIGHT = 30

DISP_MESSAGE_HEIGHT = 140

DISP_SEP_WIDTH = (DISP_GAME_WIDTH - (DISP_BUTTON_WIDTH+DISP_PLAYABLE_WIDTH)) / 5
DISP_SEP_HEIGHT = (DISP_GAME_HEIGHT - (DISP_BUTTON_HEIGHT+DISP_PLAYABLE_HEIGHT)) / 3

DISP_MESSAGE_WIDTH = DISP_GAME_WIDTH - 2*DISP_SEP_WIDTH

DISP_INVENTORY_WIDTH=500

# CONSTANTS FOR IMAGES
# Tiles
IMG_SIZE_TILE_X = 32
IMG_SIZE_TILE_Y = 32

# CONSTANTS FOR GAMES
GAME_NB_MONSTER = 15
GAME_NB_TILE_X = 120
GAME_NB_TILE_Y = 90

# Font
GAME_FONT='resources/segoepr.ttf'
GAME_FONT_SIZE=14

# Constants For Color
COLOR_WHITE=(255,255,255)
COLOR_BLACK=(0,0,0)
COLOR_RED=(240,0,0)
COLOR_GREEN=(0,240,0)