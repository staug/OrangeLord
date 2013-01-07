# CONSTANT and UTILITIES FILES
import pygame

# set up the window
SPRITEWIDTH = 24 # Ref for the default sprite size
SPRITEHEIGHT = 32 # Ref for the default sprite size
SPRITEDELAY = 0.1 # Ref for the default sprite delay
NBTILTEX = 300 # Define the world game max size (unit: a sprite width) 
NBTITLEY = 200 # Define the world game max size (unit: a sprite height)
NBSPRITX_DISP = 30 # Define how many sprites should be displayed on screen (unit: sprite)
NBSPRITY_DISP = 20 # Define how many sprites should be displayed on screen (unit: sprite)



# Utilities

def convertTilePosToScreenPos(tilex, tiley):
    """ this function converts a tile index couple (x,y) to a screen index.
        The screen index returned in the top left corner position """
    return (tilex * SPRITEWIDTH, tiley * SPRITEHEIGHT)

def convertScreenPosToTilePos(pox, poy):
    """ returns the x,y coordinates of the tile[x][y] to which the screen point belongs
returns -1,-1 if the pos is out of the screen coordinate
    """
    if posx > SPRITEWIDTH * NBTILTEX or posy > SPRITEHEIGHT * NBTILTEY:
        print("convertScreenPosToTilePos error: posx or posy out of bound")
        return (-1,-1)
    return (int(posx/SPRITEWIDTH), int(posy/SPRITEHEIGHT))

    
def getTileRect(tilex, tiley):
    """ create a PyGame.Rect struct associated to the tile
    """
    return pygame.Rect(tilex * SPRITEWIDTH, tiley * SPRITEHEIGHT, SPRITEWIDTH, SPRITEHEIGHT)

def getTileCenter(tilex, tiley):
    """ Return the centerx, centery of the tile
    """
    tileRec = getTileRect(tilex,tiley)
    return (tileRec.centerx, tileRec.centery)
