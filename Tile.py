import dMapModule
from Utilities import *

import random

# Tile Representation
class Tile:
    ''' A tile of the map and its properties
    '''

    def __init__(self, tilex, tiley, blocked, block_sight = None):
        self.blocked = blocked
        self.tilex = tilex
        self.tiley = tiley
        self.visited = False

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

    def setBlocked(self, blockingState):
        self.blocked = blockingState
    def isBlocked(self):
        return self.blocked

    def isVisited(self):
        self.visited = True

    def isColidingWith(self, aRect):
        return aRect.collideRect(getTileRect(self.tilex, self.tiley))

    def paint(self, overlay):
        if self.visited:
            if self.blocked:
                overlay.fill((125, 125, 255), getTileRect(self.tilex, self.tiley))
            else:
                overlay.fill((10, 10, 10), getTileRect(self.tilex, self.tiley))

class TileSet:
    ''' The worldGame :-)
    '''
    def __init__(self, nbTileX , nbTileY):
        self.nbTileX = nbTileX
        self.nbTileY = nbTileY
        somename= dMapModule.dMap()
        somename.makeMap(nbTileX,nbTileY,30,0,80)
        self.possibleBeginPlace=[]
        self.tileArray=[[ Tile(x,y,False)
        for y in range(nbTileY) ]
            for x in range(nbTileX) ]

        for y in range(nbTileY):
            for x in range(nbTileX):
                if somename.mapArr[y][x]==0:
                    self.possibleBeginPlace.append((x,y))
                if somename.mapArr[y][x]==2:
                    self.tileArray[x][y].setBlocked(True)
        random.shuffle(self.possibleBeginPlace)

    def getTileAt(self,x,y):
        return self.tileArray[x][y]

    def getTileAtScreenPos(self, posx, posy):
        (x,y) =  convertScreenPosToTilePos(posx, posy)
        return self.tileArray[x][y]

    def paint(self,overlay):
        for y in range(self.nbTileY):
            for x in range(self.nbTileX):
                self.getTileAt(x,y).paint(overlay)

    def getPlayerBeginPlace(self):
        return (self.possibleBeginPlace[0][0], self.possibleBeginPlace[0][1])



