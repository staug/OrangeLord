# TEST
import pygame, sys, time, random
from pygame.locals import *
import dMapModule
import Object, Tile, Utilities

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()


gameSurface = pygame.display.set_mode((Utilities.NBSPRITX_DISP*Utilities.SPRITEWIDTH, Utilities.NBSPRITY_DISP*Utilities.SPRITEHEIGHT), 0, 32)
pygame.display.set_caption('Sprites and Sound')
entireWindowSurface = pygame.Surface((Utilities.NBTILEX*Utilities.SPRITEWIDTH, Utilities.NBTILEY*Utilities.SPRITEHEIGHT))


tileSet = Tile.TileSet(Utilities.NBTILEX, Utilities.NBTILEY)
tileSet.paint(entireWindowSurface)
player = Object.Object(tileSet.getPlayerBeginPlace()[0], tileSet.getPlayerBeginPlace()[1] ,'resources/images/player.png')
player.paint(entireWindowSurface)
# run the game loop

gameSurface.blit(entireWindowSurface, pygame.Rect(0,0,Utilities.NBSPRITX_DISP*Utilities.SPRITEWIDTH, Utilities.NBSPRITY_DISP*Utilities.SPRITEHEIGHT))

goUp = goDown = goRight = goLeft = False
dx = dy = 0
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                dy -= 2
            if event.key == K_DOWN:
                dy += 2
            if event.key == K_LEFT:
                dx -= 2
            if event.key == K_RIGHT:
                dx += 2
        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_DOWN:
                dy = 0
            if event.key == K_LEFT or K_RIGHT:
                dx = 0

    if dx != 0 or dy != 0:
        player.clear(tileSet, gameSurface)
        player.move(dx,dy,tileSet)
        player.paint(gameSurface)
        # dx = dy = 0

    pygame.display.update()
    mainClock.tick(10)
