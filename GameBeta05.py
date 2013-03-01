#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Piccool
#
# Created:     27/01/2013
# Copyright:   (c) Piccool 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

'''
TODO:

Main:
    Levels, with specific monsters
    New Walls
    Fog of War
    Stats and rules
    Experience
    Movement by pixel and not by side (?)

Side:
    (*) Door opened
    Exploration: change floor color
    Inventory button
    Stat button
    On a reload, erase previous monster and keep doors opened

'''

import pygame, pygbutton, pyganim, sys, math, ast
import shelve
import configparser

from random import *
from pygame.locals import *

from GameConstants import *

import __main__

class dMap:
    def __init__(self, tilemapx, tilemapy):
        self.roomList=[]
        self.cList=[]
        self.tileMap = []
        self.possibleBeginPlace=[]
        self.sizeTileX = IMG_SIZE_TILE_X
        self.sizeTileY = IMG_SIZE_TILE_Y

        self.nbTileX = tilemapx
        self.nbTileY = tilemapy

        FLOOR = 0
        WALL = 2

        self.makeMap(tilemapx,tilemapy,30,0,80)
        for y in range(tilemapy):
            self.tileMap.append([])
            for x in range(tilemapx):
                if self.mapArr[y][x] == FLOOR :
                        self.possibleBeginPlace.append((x,y))
                        self.tileMap[y].append(Tile(x,y,'Floor'))
#                if somename.mapArr[y][x]==1:
#                        line += " "
                elif self.mapArr[y][x] == WALL or self.mapArr[y][x] == 1:
                        # Using the http://www.angryfishstudios.com/2011/04/adventures-in-bitmasking/ method
                        # By default all is a floor around
                        up = down = right = left = 0
                        if x == 0 or self.mapArr[y][x-1] != FLOOR or self.mapArr[y][x-1] == 1:
                            left = 1
                        if x == tilemapx-1 or self.mapArr[y][x+1] != FLOOR or self.mapArr[y][x+1] == 1:
                            right = 1
                        #Now we have to do the top - easy part first
                        if y == 0 or self.mapArr[y-1][x] != FLOOR or self.mapArr[y-1][x] == 1:
                            up = 1
                        if y == tilemapy-1 or self.mapArr[y+1][x] != FLOOR or self.mapArr[y+1][x] == 1:
                            down = 1
                        self.tileMap[y].append(Tile(x,y,'Wall', tileIndex=left * 8 + down * 4 + right * 2 + up))
                else:
                        up = down = right = left = 0
                        if x == 0 or self.mapArr[y][x-1] != FLOOR or self.mapArr[y][x-1] == 1:
                            left = 1
                        if x == tilemapx-1 or self.mapArr[y][x+1] != FLOOR or self.mapArr[y][x+1] == 1:
                            right = 1
                        #Now we have to do the top - easy part first
                        if y == 0 or self.mapArr[y-1][x] != FLOOR or self.mapArr[y-1][x] == 1:
                            up = 1
                        if y == tilemapy-1 or self.mapArr[y+1][x] != FLOOR or self.mapArr[y+1][x] == 1:
                            down = 1
                        self.tileMap[y].append(Tile(x,y,'Other', tileIndex=left * 8 + down * 4 + right * 2 + up))
        shuffle(self.possibleBeginPlace)

    def getTileAt(self, x, y):
        return self.tileMap[y][x]

    def getTileCenter(self, x,y):
        tilecenterx = x * self.sizeTileX + self.sizeTileX / 2
        tilecentery = y * self.sizeTileY + self.sizeTileY / 2
        return(tilecenterx,tilecentery)

    def getTileTop(self, x,y):
        tiletopx = x * self.sizeTileX
        tiletopy = y * self.sizeTileY
        return(tiletopx,tiletopy)

    def drawTileAt(self, x,y):
        self.getTileAt(x,y).draw()

    def drawMap(self):
        #go through all tiles, and set their background color
        for y in range(self.nbTileY):
            for x in range(self.nbTileX):
                self.getTileAt(x,y).draw()

    def initGraphics(self):
        #go through all tiles, and reset their graphics
        for y in range(self.nbTileY):
            for x in range(self.nbTileX):
                self.getTileAt(x,y).initGraphics()


    def getMapDimensionPixel(self):
        return(self.sizeTileX*self.nbTileX, self.sizeTileY*self.nbTileY)

    def makeMap(self,xsize,ysize,fail,b1,mrooms):
        """Generate random layout of rooms, corridors and other features"""
	    #makeMap can be modified to accept arguments for values of failed, and percentile of features.
	    #Create first room
        self.mapArr=[]
        for y in range(ysize):
            self.mapArr.insert(y,[])
            for x in range(xsize):
                (self.mapArr[y]).insert(x,1.0)

        w,l,t=self.makeRoom()
        while len(self.roomList)==0:
            y=randrange(ysize-1-l)+1
            x=randrange(xsize-1-w)+1
            p=self.placeRoom(l,w,x,y,xsize,ysize,6,0)
        failed=0
        while failed<fail: #The lower the value that failed< , the smaller the dungeon
            chooseRoom=randrange(len(self.roomList))
            ex,ey,ex2,ey2,et=self.makeExit(chooseRoom)
            feature=randrange(100)
            if feature<b1: #Begin feature choosing (more features to be added here)
                w,l,t=self.makeCorridor()
            else:
                w,l,t=self.makeRoom()
            roomDone=self.placeRoom(l,w,ex2,ey2,xsize,ysize,t,et)
            if roomDone==0: #If placement failed increase possibility map is full
                failed+=1
            elif roomDone==2: #Possiblilty of linking rooms
                if self.mapArr[ey2][ex2]==0:
                    if randrange(100)<7:
                        self.makePortal(ex,ey)
                    failed+=1
            else: #Otherwise, link up the 2 rooms
                self.makePortal(ex,ey)
                failed=0
                if t<5:
                    tc=[len(self.roomList)-1,ex2,ey2,t]
                    self.cList.append(tc)
                    self.joinCorridor(len(self.roomList)-1,ex2,ey2,t,50)
            if len(self.roomList)==mrooms:
                failed=fail
        self.finalJoins()

    def makeRoom(self):
        """Randomly produce room size"""
        rtype=5
        rwide=randrange(8)+3
        rlong=randrange(8)+3
        return rwide,rlong,rtype

    def makeCorridor(self):
        """Randomly produce corridor length and heading"""
        clength=randrange(18)+3
        heading=randrange(4)
        if heading==0: #North
            wd=1
            lg=-clength
        elif heading==1: #East
            wd=clength
            lg=1
        elif heading==2: #South
            wd=1
            lg=clength
        elif heading==3: #West
            wd=-clength
            lg=1
        return wd,lg,heading

    def placeRoom(self,ll,ww,xposs,yposs,xsize,ysize,rty,ext):
        """Place feature if enough space and return canPlace as true or false"""
        #Arrange for heading
        xpos=xposs
        ypos=yposs
        if ll<0:
            ypos+=ll+1
            ll=abs(ll)
        if ww<0:
            xpos+=ww+1
            ww=abs(ww)
        #Make offset if type is room
        if rty==5:
            if ext==0 or ext==2:
                offset=randrange(ww)
                xpos-=offset
            else:
                offset=randrange(ll)
                ypos-=offset
        #Then check if there is space
        canPlace=1
        if ww+xpos+1>xsize-1 or ll+ypos+1>ysize:
            canPlace=0
            return canPlace
        elif xpos<1 or ypos<1:
            canPlace=0
            return canPlace
        else:
            for j in range(ll):
                for k in range(ww):
                    if self.mapArr[(ypos)+j][(xpos)+k]!=1:
                        canPlace=2
        #If there is space, add to list of rooms
        if canPlace==1:
            temp=[ll,ww,xpos,ypos]
            self.roomList.append(temp)
            for j in range(ll+2): #Then build walls
                for k in range(ww+2):
                    self.mapArr[(ypos-1)+j][(xpos-1)+k]=2
            for j in range(ll): #Then build floor
                for k in range(ww):
                    self.mapArr[ypos+j][xpos+k]=0
        return canPlace #Return whether placed is true/false

    def makeExit(self,rn):
        """Pick random wall and random point along that wall"""
        room=self.roomList[rn]
        while True:
            rw=randrange(4)
            if rw==0: #North wall
                rx=randrange(room[1])+room[2]
                ry=room[3]-1
                rx2=rx
                ry2=ry-1
            elif rw==1: #East wall
                ry=randrange(room[0])+room[3]
                rx=room[2]+room[1]
                rx2=rx+1
                ry2=ry
            elif rw==2: #South wall
                rx=randrange(room[1])+room[2]
                ry=room[3]+room[0]
                rx2=rx
                ry2=ry+1
            elif rw==3: #West wall
                ry=randrange(room[0])+room[3]
                rx=room[2]-1
                rx2=rx-1
                ry2=ry
            if self.mapArr[ry][rx]==2: #If space is a wall, exit
                break
        return rx,ry,rx2,ry2,rw

    def makePortal(self,px,py):
        """Create doors in walls"""
        ptype=randrange(100)
        if ptype>90: #Secret door
            self.mapArr[py][px]=5
            return
        elif ptype>75: #Closed door
            self.mapArr[py][px]=4
            return
        elif ptype>40: #Open door
            self.mapArr[py][px]=3
            return
        else: #Hole in the wall
            self.mapArr[py][px]=0

    def joinCorridor(self,cno,xp,yp,ed,psb):
        """Check corridor endpoint and make an exit if it links to another room"""
        cArea=self.roomList[cno]
        if xp!=cArea[2] or yp!=cArea[3]: #Find the corridor endpoint
            endx=xp-(cArea[1]-1)
            endy=yp-(cArea[0]-1)
        else:
            endx=xp+(cArea[1]-1)
            endy=yp+(cArea[0]-1)
        checkExit=[]
        if ed==0: #North corridor
            if endx>1:
                coords=[endx-2,endy,endx-1,endy]
                checkExit.append(coords)
            if endy>1:
                coords=[endx,endy-2,endx,endy-1]
                checkExit.append(coords)
            if endx<78:
                coords=[endx+2,endy,endx+1,endy]
                checkExit.append(coords)
        elif ed==1: #East corridor
            if endy>1:
                coords=[endx,endy-2,endx,endy-1]
                checkExit.append(coords)
            if endx<78:
                coords=[endx+2,endy,endx+1,endy]
                checkExit.append(coords)
            if endy<38:
                coords=[endx,endy+2,endx,endy+1]
                checkExit.append(coords)
        elif ed==2: #South corridor
            if endx<78:
                coords=[endx+2,endy,endx+1,endy]
                checkExit.append(coords)
            if endy<38:
                coords=[endx,endy+2,endx,endy+1]
                checkExit.append(coords)
            if endx>1:
                coords=[endx-2,endy,endx-1,endy]
                checkExit.append(coords)
        elif ed==3: #West corridor
            if endx>1:
                coords=[endx-2,endy,endx-1,endy]
                checkExit.append(coords)
            if endy>1:
                coords=[endx,endy-2,endx,endy-1]
                checkExit.append(coords)
            if endy<38:
                coords=[endx,endy+2,endx,endy+1]
                checkExit.append(coords)
        for xxx,yyy,xxx1,yyy1 in checkExit: #Loop through possible exits
            if self.mapArr[yyy][xxx]==0: #If joins to a room
                if randrange(100)<psb: #Possibility of linking rooms
                    self.makePortal(xxx1,yyy1)

    def finalJoins(self):
        """Final stage, loops through all the corridors to see if any can be joined to other rooms"""
        for x in self.cList:
            self.joinCorridor(x[0],x[1],x[2],x[3],10)

class Tile:

    graphicInitialized = False

    @staticmethod
    def initializeGraphics():
        '''
        Notes about the picture: each tile is 32x32
        Walls are located in picture at (160,288). They follow teh same representation as the numerical pad
        '''
        # Load the main surface

        goodImage = pygame.image.load('resources/images/TileA5.png').convert()
        Tile.IMG_Floor = goodImage.subsurface((0,192,32,32)).copy()

        mainImage1 = pygame.image.load('resources/images/testownwall.png')
        Tile.IMG_WALL1 = {
        0 :mainImage1.subsurface((0,0,32,32)).copy(),
        1 :mainImage1.subsurface((64,0,32,32)).copy(),
        2 :mainImage1.subsurface((128,0,32,32)).copy(),
        3 :mainImage1.subsurface((192,0,32,32)).copy(),
        4 :mainImage1.subsurface((0,64,32,32)).copy(),
        5 :mainImage1.subsurface((64,64,32,32)).copy(),
        6 :mainImage1.subsurface((128,64,32,32)).copy(),
        7 :mainImage1.subsurface((192,64,32,32)).copy(),
        8 :mainImage1.subsurface((0,128,32,32)).copy(),
        9 :mainImage1.subsurface((64,128,32,32)).copy(),
        10:mainImage1.subsurface((128,128,32,32)).copy(),
        11:mainImage1.subsurface((192,128,32,32)).copy(),
        12:mainImage1.subsurface((0,192,32,32)).copy(),
        13:mainImage1.subsurface((64,192,32,32)).copy(),
        14:mainImage1.subsurface((128,192,32,32)).copy(),
        15:mainImage1.subsurface((192,192,32,32)).copy(),
        }
        mainImage2 = pygame.image.load('resources/images/testownwall2.png')
        Tile.IMG_WALL2 = {
        0 :mainImage2.subsurface((0,0,32,32)).copy(),
        1 :mainImage2.subsurface((64,0,32,32)).copy(),
        2 :mainImage2.subsurface((128,0,32,32)).copy(),
        3 :mainImage2.subsurface((192,0,32,32)).copy(),
        4 :mainImage2.subsurface((0,64,32,32)).copy(),
        5 :mainImage2.subsurface((64,64,32,32)).copy(),
        6 :mainImage2.subsurface((128,64,32,32)).copy(),
        7 :mainImage2.subsurface((192,64,32,32)).copy(),
        8 :mainImage2.subsurface((0,128,32,32)).copy(),
        9 :mainImage2.subsurface((64,128,32,32)).copy(),
        10:mainImage2.subsurface((128,128,32,32)).copy(),
        11:mainImage2.subsurface((192,128,32,32)).copy(),
        12:mainImage2.subsurface((0,192,32,32)).copy(),
        13:mainImage2.subsurface((64,192,32,32)).copy(),
        14:mainImage2.subsurface((128,192,32,32)).copy(),
        15:mainImage2.subsurface((192,192,32,32)).copy(),
        }

        doorsImage = pygame.image.load('resources/images/doors.png')
        Tile.IMG_DOOR = {
        0 :doorsImage.subsurface((0,0,32,32)).copy(),
        1 :doorsImage.subsurface((64,0,32,32)).copy(),
        2 :doorsImage.subsurface((0,64,32,32)).copy(),
        3 :doorsImage.subsurface((64,64,32,32)).copy()
        }

    #a tile of the map and its properties
    def __init__(self, x=0, y=0, type=None, block_sight = None, tileIndex = -1):
        self.x = x
        self.y = y
        self.type = type
        self.blocked = False
        if type == 'Wall':
            self.blocked = True
        self.spriteImage= None
        self.explored = False
        self.tileIndex = tileIndex
        if block_sight is None: block_sight = self.blocked
        self.block_sight = block_sight
        self.initGraphics()

    def initGraphics(self):
        if not Tile.graphicInitialized:
            Tile.initializeGraphics()
            Tile.graphicInitialized = True

        if self.type == 'Wall' and self.tileIndex >= 0:
            self.spriteImage = Tile.IMG_Floor.copy()
            rw=randrange(2)
            if rw == 0:
                self.spriteImage.blit(Tile.IMG_WALL1[self.tileIndex], (0,0))
            else:
                self.spriteImage.blit(Tile.IMG_WALL2[self.tileIndex], (0,0))
        elif self.type == 'Wall':
            print("WARNING" + type + "index="+str(self.tileIndex))
            self.spriteImage = pygame.Surface((32,32))
            self.spriteImage.fill((12,80,102))
        elif self.type == 'Floor':
            self.spriteImage = Tile.IMG_Floor.copy()
        else:
            self.spriteImage = Tile.IMG_Floor.copy()
            if self.tileIndex == 1 or self.tileIndex == 4 or self.tileIndex == 5:
                self.spriteImage.blit(Tile.IMG_DOOR[0], (0,0))
            else:
                self.spriteImage.blit(Tile.IMG_DOOR[1], (0,0))

    def draw(self):
        if self.spriteImage != None:
            entireWindowSurface.blit(self.spriteImage, worldmap.getTileTop(self.x, self.y))

    def setExplored(self):
        self.explored = True
        if(self.type != 'Wall' and self.type!='Floor'):
            self.spriteImage = Tile.IMG_Floor.copy()
            if self.tileIndex == 1 or self.tileIndex == 4 or self.tileIndex == 5:
                self.spriteImage.blit(Tile.IMG_DOOR[2], (0,0))
            else:
                self.spriteImage.blit(Tile.IMG_DOOR[3], (0,0))



class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, name, resources, blocks=False, fighter=None, ai=None, item=None):
        self.x = x
        self.y = y
        self.name = name
        self.blocks = blocks
        self.resources = resources

        self.fighter = fighter
        if self.fighter:  #let the fighter component know who owns it
            self.fighter.owner = self

        self.ai = ai
        if self.ai:  #let the AI component know who owns it
            self.ai.owner = self

        self.item = item
        if self.item:  #let the Item component know who owns it
            self.item.owner = self

        # Empty Graphical init
        self.spriteImage = self.animObj_DOWN = self.animObj_LEFT = self.animObj_RIGHT = self.animObj_UP = None
        self.spriteWidth = self.spriteHeight = None
        self.needRewrite = True
        self.initGraphics()

    def initGraphics(self):
        # GRAPHICAL PART...
        # first, load the image and setup the sprite dimensions
        spriteSurface = pygame.image.load(self.resources['image_file'])
        self.spriteWidth = int(self.resources['image_size_x'])
        self.spriteHeight = int(self.resources['image_size_y'])
        # Now split the image
        if self.resources['image_animated'] == 'yes':
            self.animObj_UP = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(0,0,self.spriteWidth,self.spriteHeight)), 0.1),
                           (spriteSurface.subsurface(pygame.Rect(self.spriteWidth,0,self.spriteWidth,self.spriteHeight)), 0.1),
                           (spriteSurface.subsurface(pygame.Rect(self.spriteWidth*2,0,self.spriteWidth,self.spriteHeight)), 0.1)])
            self.animObj_RIGHT = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(0,self.spriteHeight,self.spriteWidth,self.spriteHeight)), 0.1),
                           (spriteSurface.subsurface(pygame.Rect(self.spriteWidth,self.spriteHeight,self.spriteWidth,self.spriteHeight)), 0.1),
                           (spriteSurface.subsurface(pygame.Rect(self.spriteWidth*2,self.spriteHeight,self.spriteWidth,self.spriteHeight)), 0.1)])
            self.animObj_DOWN = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(0,self.spriteHeight*2,self.spriteWidth,self.spriteHeight)), 0.1),
                           (spriteSurface.subsurface(pygame.Rect(self.spriteWidth,self.spriteHeight*2,self.spriteWidth,self.spriteHeight)), 0.1),
                           (spriteSurface.subsurface(pygame.Rect(self.spriteWidth*2,self.spriteHeight*2,self.spriteWidth,self.spriteHeight)), 0.1)])
            self.animObj_LEFT = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(0,self.spriteHeight*3,self.spriteWidth,self.spriteHeight)), 0.1),
                           (spriteSurface.subsurface(pygame.Rect(self.spriteWidth,self.spriteHeight*3,self.spriteWidth,self.spriteHeight)), 0.1),
                           (spriteSurface.subsurface(pygame.Rect(self.spriteWidth*2,self.spriteHeight*3,self.spriteWidth,self.spriteHeight)), 0.1)])
            self.spriteImage = self.animObj_RIGHT #arbitrary

        else:
            self.spriteImage = self.animObj_DOWN = self.animObj_LEFT = self.animObj_RIGHT = self.animObj_UP = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(ast.literal_eval(self.resources['image_single']),(self.spriteWidth, self.spriteHeight))),1)])

        conductor_object = pyganim.PygConductor([self.animObj_UP, self.animObj_RIGHT, self.animObj_DOWN, self.animObj_LEFT])
        conductor_object.play() # starts all three animations at the same time.
        self.needRewrite = True # we need to rewrite after Move

    def move(self, dx, dy):
        #move by the given amount, if the destination is not blocked
        if not self.is_blocked(self.x+dx, self.y+dy) and (dx != 0 or dy != 0):
            self.needRewrite = True
            self.x += dx
            self.y += dy
            if abs(dx)>abs(dy):
                if dx > 0:
                    self.spriteImage = self.animObj_RIGHT
                else:
                    self.spriteImage = self.animObj_LEFT
            else:
                if dy > 0:
                    self.spriteImage = self.animObj_DOWN
                else:
                    self.spriteImage = self.animObj_UP

    def draw(self):
        #set the color and then draw the character that represents this object at its position
        if self.needRewrite:
            if self == player:
                worldmap.getTileAt(self.x, self.y).setExplored()
            self.spriteImage.blit(entireWindowSurface, worldmap.getTileTop(self.x, self.y))
            self.needRewrite = False


    def clear(self):
        #erase the character that represents this object
        #libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
        worldmap.drawTileAt(self.x, self.y)
        self.needRewrite = True

    def is_blocked(self, new_x, new_y):
        #first test the map tile
        if worldmap.getTileAt(new_x,new_y).blocked:
            return True

        #now check for any blocking objects
        for object in worldobjects:
            if object.blocks and object.x == new_x and object.y == new_y:
                return True

        return False


    def move_towards(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


class Fighter:
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power, death_function=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
            #check for death. if there's a death function, call it
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner)

    def attack(self, target):
        #a simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            #make the target take some damage
            messageBox.print(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
            target.fighter.take_damage(damage)
        else:
            messageBox.print(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

    def heal(self, amount):
        #heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp


class BasicMonster:
    #AI for a basic monster.
    def take_turn(self):
        monster = self.owner
        #move towards player if far away (but not too far
        distance = monster.distance_to(player)
        if  distance >= 2 and distance <=6:
            monster.move_towards(player.x, player.y)
        #close enough, attack! (if the player is still alive.)
        elif distance < 2 and player.fighter.hp > 0:
            monster.fighter.attack(player)

class Item:
    #an item that can be picked up and used.
    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        #add to the player's inventory and remove from the map
        if len(inventory) >= 26:
            messageBox.print('Your inventory is full, cannot pick up ' + self.owner.name + '.')
        else:
            inventory.append(self.owner)
            worldobjects.remove(self.owner)
            messageBox.print('You picked up a ' + self.owner.name + '!')

    def use(self):
        #just call the "use_function" if it is defined
        if self.use_function is None:
            messageBox.print('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self.owner)  #destroy after use, unless it was cancelled for some reason

def render_all():
    #draw all objects in the list
    for object in worldobjects:
        object.draw(gameSurface, worldmap)

def getPlayableRect(screensizex, screensizey):
    playableleft = playabletop = 0
    playerY = player.y * worldmap.sizeTileY
    playerX = player.x * worldmap.sizeTileX
    playableleft = max(playerX - (screensizex)/2,0)
    playabletop = max(playerY - (screensizey)/2,0)
    if playerY + (screensizey)/2 > worldmap.getMapDimensionPixel()[1]:
        playabletop = worldmap.getMapDimensionPixel()[1] - screensizey
    if playerX + (screensizex)/2 > worldmap.getMapDimensionPixel()[0]:
        playableleft = worldmap.getMapDimensionPixel()[0] - screensizex
    playableRect = pygame.Rect(playableleft,playabletop,screensizex,screensizey)
    return playableRect

def player_move_or_attack(dx, dy):

    #the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy

    #try to find an attackable object there
    target = None
    for anobject in worldobjects:
        if anobject.fighter and anobject.x == x and anobject.y == y:
            target = anobject
            break

    #attack if target found, move otherwise
    if target is not None:
        player.fighter.attack(target)
    else:
        player.move(dx, dy)
        fov_recompute = True


def player_death(player):
    #the game ended!
    global game_state
    messageBox.print('You died!')
    game_state = 'dead'

    #for added effect, transform the player into a corpse!
    player.spriteImage = pygame.image.load('resources/images/Close.png')
    player.needRewrite = True

def monster_death(monster):
    #transform it into a nasty corpse! it doesn't block, can't be
    #attacked and doesn't move
    messageBox.print(monster.name.capitalize() + ' is dead!')
    monster.conductor_object = None
    monster.spriteImage = pyganim.PygAnimation([('resources/images/Mushroom003.png',1)])
    monster.spriteImage.play()
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.needRewrite = True
    monster.name = 'remains of ' + monster.name

def cast_heal():
    #heal the player
    if player.fighter.hp == player.fighter.max_hp:
        messageBox.print('You are already at full health.')
        return 'cancelled'

    messageBox.print('Your wounds start to feel better!')
    player.fighter.heal(randrange(4))

def handle_key():
    dx = dy = 0
    eventHandledByButton = False
    if game_state == 'playing':
        for event in pygame.event.get():
            # handle button
            for button in allButtons:
                events = button.handleEvent(event)
                if 'click' in events:
                    if button.caption == 'Quit':
                        return 'exit'
                    if button.caption == 'Quit':
                        eventHandledByButton = True
                    if button.caption == 'Quit':
                        eventHandledByButton = True
            if event.type == MOUSEBUTTONDOWN and not eventHandledByButton:
                # player is suppposed at 466,365.. Small hack there
                (clickx,clicky) = event.pos
                tilex = player.x + int(float(clickx - 466) / IMG_SIZE_TILE_X)
                tiley = player.y + int(float(clicky - 365) / IMG_SIZE_TILE_Y)
                names = [obj.name for obj in worldobjects if obj.x == tilex and obj.y == tiley]
                names = ', '.join(names)
                if names!=None and names != '':
                    messageBox.print(names.capitalize())

            # handle key
            if event.type == QUIT:
                return 'exit'
            if event.type == KEYUP:
                if event.key == K_UP:
                    dy -= 1
                if event.key == K_DOWN:
                    dy += 1
                if event.key == K_LEFT:
                    dx -= 1
                if event.key == K_RIGHT:
                    dx += 1
            if event.type == KEYDOWN:
                if event.key == K_g:
                    #pick up an item
                    for object in worldobjects:  #look for an item in the player's tile
                        if object.x == player.x and object.y == player.y and object.item:
                            object.item.pick_up()
                            break
                if event.key == K_i:
                    #inventory
                    #show the inventory; if an item is selected, use it
                    chosen_item = inventory_menu('Use one of:')
                    print(str(chosen_item))
                    if chosen_item is not None:
                        chosen_item.use()
                return 'didnt-take-turn'
    if dx!=0 or dy != 0:
        player_move_or_attack(dx, dy)
    else:
        return 'didnt-take-turn'

class MessageBox:
    def __init__(self, surface, background):
        self.surface = surface
        self.background = background
        self.font = pygame.font.Font(GAME_FONT, 14)
        self.messages=[]
        #self.colors=[]
        self.nbMessages = 5
        self.textRect = pygame.Rect(DISP_SEP_WIDTH, DISP_SEP_HEIGHT*2+DISP_PLAYABLE_HEIGHT, DISP_MESSAGE_WIDTH, DISP_MESSAGE_HEIGHT)

    def print(self, aMessage, color=(255,255,255)):
        #Erase previous
        self.surface.fill(self.background, self.textRect)

        self.messages.append({'txt':aMessage,'color':color})
        #self.colors.append(color)

        if len(self.messages) > self.nbMessages:
            self.messages = self.messages[1:]
        fontHeight = self.font.get_height()

        surfaces = [self.font.render(ln['txt'], 1, ln['color']) for ln in self.messages]
        # can't pass background to font.render, because it doesn't respect the alpha

        maxwidth = max([s.get_width() for s in surfaces])
        result = pygame.Surface((maxwidth, len(self.messages)*fontHeight), pygame.SRCALPHA)

        for i in range(len(self.messages)):
            result.blit(surfaces[i], (0,i*fontHeight))
        self.surface.blit(result,self.textRect)

def menu(header, options, width, colorBar=COLOR_RED):
    ''' Shows a nice menu on top of the screen
    '''
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    font = pygame.font.Font(GAME_FONT, GAME_FONT_SIZE)
    fontHeight = font.get_height()+5
    #calculate total height for the header (after auto-wrap) and one line per option
    height = (len(options)+2)*fontHeight

    #create an off-screen console that represents the menu's window
    window = pygame.Surface((width, height))
    window.fill(COLOR_BLACK)
    pygame.draw.rect(window, colorBar, window.get_rect().copy(), font.size(header)[1])

    #print the header - with a black background...
    window.blit(font.render(header,1,COLOR_WHITE, COLOR_BLACK), (fontHeight,0))

    #print all the options
    y = 1
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.blit(font.render(text,1,COLOR_WHITE), (2*fontHeight+15,y*fontHeight))
        y += 1
        letter_index += 1

    #blit the contents of "window" to the root console
    x = DISP_GAME_WIDTH/2 - width/2
    y = DISP_GAME_HEIGHT/2 - height/2

    #but before that make a copy of the original!
    copySurface = gameSurface.copy()
    rect = gameSurface.blit(window, (x, y))

    #present the root console to the player and wait for a key-press
    pygame.display.update(rect)
    pygame.event.set_allowed([pygame.KEYDOWN])
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Now we copy back the old content
                gameSurface.blit(copySurface, (x, y), rect)
                pygame.display.update(rect)
                #convert the ASCII code to an index; if it corresponds to an option, return it

                index = ord(event.unicode) - ord('a')
                if index >= 0 and index < len(options):
                    return index
                return None

def inventory_menu(header):
    #show a menu with each item of the inventory as an option
    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory]

    index = menu(header, options, DISP_INVENTORY_WIDTH)

    #if an item was chosen, return it
    if index is None or len(inventory) == 0: return None
    return inventory[index].item


def render_bar(x, y, total_width, total_height, name, value, maximum, bar_color, back_color=(0,0,0)):
    ''' The bar is located at x,y part of the screen
    '''
    #render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    #render the background first
    totalBar = pygame.Surface((total_width, total_height))
    totalBar.fill((back_color))
    gameSurface.blit(totalBar, (x,y))

    # render the bar now
    bar = pygame.Surface((bar_width, total_height))
    bar.fill((bar_color))
    gameSurface.blit(bar, (x,y))

    #finally, some centered text with the values
    font = pygame.font.Font(GAME_FONT, 14)
    fontSurface = font.render(name + ': ' + str(value) + '/' + str(maximum),1,(255,255,255))
    gameSurface.blit(fontSurface, (x+10,y+int(float(total_height-font.get_height())/2)))

def save_game():
    #open a new empty shelve (possibly overwriting an old one) to write the game data
    file = shelve.open('savegame', 'n')
    file['map'] = worldmap
    file['objects'] = worldobjects
    file['player_index'] = worldobjects.index(player)  #index of player in objects list
    file['inventory'] = inventory
    file['game_state'] = game_state
    file.close()

def load_game():
    #open the previously saved shelve and load the game data
    global worldmap, worldobjects, player, inventory, game_state

    file = shelve.open('savegame', 'r')
    worldmap = file['map']
    worldobjects = file['objects']
    inventory = file['inventory']
    game_state = file['game_state']
    player = worldobjects[file['player_index']]  #get index of player in objects list and access it
    file.close()
    # we need to reinit all the graphics...
    worldmap.initGraphics()
    for object in worldobjects:
        object.initGraphics()


def new_game():
    global worldmap, worldobjects, gameState, player, inventory

    config = configparser.RawConfigParser()
    config.read('resources/definitions.ini')
    # Generate Map
    worldmap = dMap(GAME_NB_TILE_X, GAME_NB_TILE_Y)
    while len(worldmap.possibleBeginPlace) < GAME_MINIMUM_START_PLACE:
        worldmap = dMap(GAME_NB_TILE_X, GAME_NB_TILE_Y)

    inventory=[]
    worldobjects = []

    # INIT OBJECTS
    # ------------------------------------------------
    # Read the config file
    # PLAYER
    fighter_component = Fighter(hp=30, defense=2, power=5, death_function=player_death)
    player = Object(worldmap.possibleBeginPlace[0][0], worldmap.possibleBeginPlace[0][1], 'player', config._sections['player'], blocks=True, fighter = fighter_component)

    for i in range(1,GAME_NB_MONSTER+1):
        monster_name='orc'
        fighter_component = Fighter(hp=config.getint(monster_name, 'hp'), defense=config.getint(monster_name, 'defense'), power=config.getint(monster_name, 'power'), death_function = getattr(__main__,config.get(monster_name, 'death_function')))
        ai_component = BasicMonster()
        monster = Object(worldmap.possibleBeginPlace[i][0], worldmap.possibleBeginPlace[i][1], monster_name, config._sections[monster_name], blocks=True, fighter=fighter_component, ai=ai_component)
        worldobjects.append(monster)
    worldobjects.append(player)

    for i in range(GAME_NB_MONSTER+1, 2*(GAME_NB_MONSTER+1)):
        item_name='healing potion'
        listing = config._sections[item_name]
        item_component = Item(use_function=getattr(__main__,config.get(item_name, 'use_function')))
        item = Object(worldmap.possibleBeginPlace[i][0], worldmap.possibleBeginPlace[i][1], item_name, config._sections[item_name], item=item_component)
        worldobjects.append(item)


def system_init():
    global messageBox, allButtons # UI ZONES
    global gameSurface # Spritable zones
    global mainClock

    # System Init
    pygame.init()
    mainClock = pygame.time.Clock()
    gameSurface = pygame.display.set_mode((DISP_GAME_WIDTH,DISP_GAME_HEIGHT))
    pygame.display.set_caption('Orange Lord Game v0.4')

    # Prepare the message bar
    messageBox = MessageBox(gameSurface,(0,0,0))

    # Prepare the buttons
    buttonQuit = pygbutton.PygButton((DISP_GAME_WIDTH-DISP_SEP_WIDTH-DISP_BUTTON_WIDTH, DISP_SEP_HEIGHT, DISP_BUTTON_WIDTH, DISP_BUTTON_HEIGHT), 'Quit', font=pygame.font.Font(GAME_FONT, 14))
    buttonInv = pygbutton.PygButton((DISP_GAME_WIDTH-DISP_SEP_WIDTH-DISP_BUTTON_WIDTH, DISP_SEP_HEIGHT*2+DISP_BUTTON_HEIGHT, DISP_BUTTON_WIDTH, DISP_BUTTON_HEIGHT), 'Inv', font=pygame.font.Font(GAME_FONT, 14))
    buttonStat = pygbutton.PygButton((DISP_GAME_WIDTH-DISP_SEP_WIDTH-DISP_BUTTON_WIDTH, DISP_SEP_HEIGHT*3+DISP_BUTTON_HEIGHT*2, DISP_BUTTON_WIDTH, DISP_BUTTON_HEIGHT), 'Stat', font=pygame.font.Font(GAME_FONT, 14))
    allButtons = (buttonInv, buttonQuit, buttonStat)

def main_menu():
    mainMenuImage = pygame.image.load('resources/images/the_orange_knight_by_jouste.jpg')

    while True:
        #show the background image, at twice the regular console resolution
        gameSurface.blit(mainMenuImage, (0, 0), (0,0,1024,768))
        pygame.display.update()
        #show options and wait for the player's choice
        choice = menu('  Orange Dungeon  ', ['Play a new game', 'Continue last game', 'Quit'], 500, colorBar= COLOR_ORANGE)

        if choice == 0:  #new game
            new_game()
            play()
        if choice == 1:  #load last game
            try:
                load_game()
                play()
            except:
                print('No saved game to load')
                continue
        elif choice == 2:  #quit
            pygame.quit()
            sys.exit()

def play():
    global game_state
    global entireWindowSurface
    game_state = "playing"

    # Totally erase the surface
    gameSurface.fill(COLOR_BLACK)

    # Prepare drawing
    entireWindowSurface = pygame.Surface(worldmap.getMapDimensionPixel())
    messageBox.print("Welcome to Orange Lord Domain....", color=COLOR_RED)

    # Draw the world
    worldmap.drawMap()
    for button in allButtons:
        button.draw(gameSurface)

    # STATE VARIABLE
    player_action = None

    # run the game loop
    while True:
        for object in worldobjects:
            object.clear()

        #handle keys and exit game if needed
        player_action = handle_key()
        if player_action == 'exit':
            save_game()
            pygame.quit()
            sys.exit()

        #let monsters take their turn
        if game_state == 'playing' and player_action != 'didnt-take-turn':
            for object in worldobjects:
                if object.ai:
                    object.ai.take_turn()

        #draw all objects (including player) in the list if required
        for object in worldobjects:
            if object != player:
                object.draw()
        player.draw()

        playableSurface = entireWindowSurface.subsurface(getPlayableRect(DISP_PLAYABLE_WIDTH, DISP_PLAYABLE_HEIGHT))
        gameSurface.blit(playableSurface,(DISP_SEP_WIDTH,DISP_SEP_HEIGHT))

        #draw health bar
        render_bar(DISP_GAME_WIDTH-DISP_SEP_WIDTH-DISP_BUTTON_WIDTH, DISP_SEP_HEIGHT*4+DISP_BUTTON_HEIGHT*3, DISP_BUTTON_WIDTH, DISP_BUTTON_HEIGHT, 'HP', player.fighter.hp, player.fighter.max_hp, (5,50,78))

        pygame.display.update()
        mainClock.tick(40)


if __name__ == '__main__':
    system_init()
    main_menu()
