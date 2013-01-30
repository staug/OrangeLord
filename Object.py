import pygame, pyganim
from Utilities import *

class Object():
    '''this is an animated object, which is able to be moved (player, monster, fireballs)...
    '''
    def __init__(self, tilex, tiley, resourceFileName):
        self.Rect = getTileRect(tilex, tiley)
        #self.Rect = getTileRect(tilex, tiley)
        # need later a way to differentiate between static and non static files...
        spriteImage = pygame.image.load(resourceFileName)
        self.spriteUP = pyganim.PygAnimation([(spriteImage.subsurface(pygame.Rect(0,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH*2,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)]).getCopy()
        self.spriteRIGHT = pyganim.PygAnimation([(spriteImage.subsurface(pygame.Rect(0,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)]).getCopy()
        self.spriteDOWN = pyganim.PygAnimation([(spriteImage.subsurface(pygame.Rect(0,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)]).getCopy()
        self.spriteLEFT = pyganim.PygAnimation([(spriteImage.subsurface(pygame.Rect(0,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)]).getCopy()
        self.spriteUP.play()
        self.spriteDOWN.play()
        self.spriteLEFT.play()
        self.spriteRIGHT.play()
        self.anim = self.spriteRIGHT

    def move(self, dx, dy, tileMap):
        '''move by the given amount (pixel coordinates), if the destination is not blocked. Also setup the correct anim.
        '''
        possibleRect =self.Rect.move(dx, dy)
        blocked = tileMap.getTileAtScreenPos(possibleRect.top, possibleRect.left).isBlocked() and tileMap.getTileAtScreenPos(possibleRect.top, possibleRect.right).isBlocked() and tileMap.getTileAtScreenPos(possibleRect.bottom, possibleRect.right).isBlocked() and tileMap.getTileAtScreenPos(possibleRect.bottom, possibleRect.left).isBlocked()
##        x = y = 0
##        if (dx>=0):
##            x=self.Rect.right + dx -1
##        else:
##            x=self.Rect.left + dx + 1
##        if (dy>=0):
##            y=self.Rect.bottom + dy - 1
##        else:
##            y=self.Rect.top + dy + 1
##
##
##        (tilex, tiley) = convertScreenPosToTilePos(x + dx, y + dy)
##        if not tileMap.getTileAt(tilex, tiley).isBlocked():
        if not blocked:
            self.Rect=self.Rect.move(dx, dy)
            if abs(dy) >= abs(dx):
                if dy >= 0:
                    self.anim = self.spriteDOWN
                else:
                    self.anim = self.spriteUP
            else:
                if dx >= 0:
                    self.anim = self.spriteRIGHT
                else:
                    self.anim = self.spriteLEFT
        else:
            print("Blocked")

    def paint(self, overlay):
        #set the color and then draw the character that represents this object at its position
        self.anim.blit(overlay, self.Rect)

    def clear(self, tileMap, overlay):
        '''erase the character that represents this object: get the tile for this background
call the paint method
optional: call the paint method on its neighbor
'''
        (tilex, tiley) = convertScreenPosToTilePos(self.Rect.centerx, self.Rect.centery)
        tileMap.getTileAt(tilex, tiley).isVisited()
        tileMap.getTileAt(tilex-1, tiley).isVisited()
        tileMap.getTileAt(tilex+1, tiley).isVisited()
        tileMap.getTileAt(tilex, tiley+1).isVisited()
        tileMap.getTileAt(tilex, tiley-1).isVisited()
        tileMap.getTileAt(tilex-1, tiley-1).isVisited()
        tileMap.getTileAt(tilex+1, tiley-1).isVisited()
        tileMap.getTileAt(tilex+1, tiley+1).isVisited()
        tileMap.getTileAt(tilex-1, tiley+1).isVisited()

        tileMap.getTileAt(tilex, tiley).paint(overlay)
        tileMap.getTileAt(tilex-1, tiley).paint(overlay)
        tileMap.getTileAt(tilex+1, tiley).paint(overlay)
        tileMap.getTileAt(tilex, tiley+1).paint(overlay)
        tileMap.getTileAt(tilex, tiley-1).paint(overlay)
        tileMap.getTileAt(tilex-1, tiley-1).paint(overlay)
        tileMap.getTileAt(tilex+1, tiley-1).paint(overlay)
        tileMap.getTileAt(tilex+1, tiley+1).paint(overlay)
        tileMap.getTileAt(tilex-1, tiley+1).paint(overlay)


