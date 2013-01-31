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

import pygame, pyganim, sys, math
from random import *
from math import *
from pygame.locals import *

class dMap:
    def __init__(self, tilemapx, tilemapy):
        self.roomList=[]
        self.cList=[]
        self.tileMap = []
        self.possibleBeginPlace=[]
        self.sizeTileX = 31
        self.sizeTileY = 31

        self.nbTileX = tilemapx
        self.nbTileY = tilemapy

        FLOOR = 0
        WALL = 2

        self.makeMap(tilemapx,tilemapy,30,0,80)
        for y in range(tilemapy):
            self.tileMap.append([])
            for x in range(tilemapx):
                if self.mapArr[y][x] == FLOOR:
                        self.possibleBeginPlace.append((x,y))
                        self.tileMap[y].append(Tile(x,y,'Floor'))
#                if somename.mapArr[y][x]==1:
#                        line += " "
                elif self.mapArr[y][x] == WALL:
                        # By default all is a floor around
                        up = down = right = left = None
                        if x == 0 or self.mapArr[y][x-1] == WALL:
                            left = '2'
                        if x == tilemapx-1 or self.mapArr[y][x+1] == WALL:
                            right = '2'
                        #Now we have to do the top - easy part first
                        if y == 0:
                            up = '222'
                        else:
                            up='000'
                            #we were not at the top, we need to build it slowlier
                            if x == 0 or self.mapArr[y-1][x-1] == WALL:
                                up = '2'+up[1:]
                            if self.mapArr[y-1][x] == WALL:
                                up = up[0:1]+'2'+up[2:]
                            if x+1 == 0 or self.mapArr[y-1][x+1] == WALL:
                                up = up[0:2]+'2'

                        if y == tilemapy-1 or self.mapArr[y+1][x] == WALL:
                            down = WALL

                        self.tileMap[y].append(Tile(x,y,'Wall', topTile = up, bottomTile = down, leftTile = left, rightTile = right))

                else:
                        self.tileMap[y].append(Tile(x,y,'Other'))

#                if somename.mapArr[y][x]==3 or somename.mapArr[y][x]==4 or somename.mapArr[y][x]==5:
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

    def drawTileAt(self, x,y,surface):
        self.getTileAt(x,y).draw(surface, self)

    def drawMap(self, surface):
        #go through all tiles, and set their background color
        for y in range(self.nbTileY):
            for x in range(self.nbTileX):
                self.getTileAt(x,y).draw(surface, self)

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
        print("Init")
        Tile.IMG_Floor = pygame.image.load('resources/images/Floor.png')
        Tile.IMG_WallYYYY0 = pygame.image.load('resources/images/Center001.png') # Used when 4 corners are full (top=Y,right=Y,bottom=Y,left=Y)
        Tile.IMG_WallNYYY0 = pygame.image.load('resources/images/Side001.png') # Used when Top is None, all other full
        Tile.IMG_WallNYYY1 = pygame.image.load('resources/images/Side002.png') # Used when Top is None, all other full
        Tile.IMG_WallNYYY2 = pygame.image.load('resources/images/Side003.png') # Used when Top is None, all other full
        Tile.IMG_WallNYYY3 = pygame.image.load('resources/images/Side004.png') # Used when Top is None, all other full


    #a tile of the map and its properties
    def __init__(self, x=0, y=0, type=None, block_sight = None, topTile = None, bottomTile = None, leftTile = None, rightTile = None):
        if not Tile.graphicInitialized:
            Tile.initializeGraphics()
            Tile.graphicInitialized = True
        self.x = x
        self.y = y
        self.type = type
        self.blocked = False
        self.spriteImage= None
        self.explored = False
        if type == 'Wall':
            self.spriteImage = Tile.IMG_Floor.copy()
            self.spriteImage.blit(pygame.image.load('resources/images/Ang004.png'),(0,0))
            self.blocked = True
        elif type == 'Floor':
            #self.spriteImage = pygame.image.load('resources/images/Floor.png')
            self.spriteImage = Tile.IMG_Floor.copy()
        else:
            self.spriteImage = pygame.Surface((31,31))
            self.spriteImage.fill((64,25,12))
#            self.spriteImage = pygame.image.load('resources/images/Floor.png')
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = self.blocked
        self.block_sight = block_sight


    def draw(self, surface, map):
        if self.spriteImage != None:
            surface.blit(self.spriteImage, map.getTileTop(self.x, self.y))



class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, name, resourceFile, blocks=False, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.name = name
        self.blocks = blocks

        self.fighter = fighter
        if self.fighter:  #let the fighter component know who owns it
            self.fighter.owner = self

        self.ai = ai
        if self.ai:  #let the AI component know who owns it
            self.ai.owner = self


        # GRAPHICAL PART...
        spriteSurface = pygame.image.load(resourceFile)
        self.spriteWidth = 24
        self.spriteHeight = 32
        # In the future the resource file will contain a ref to the image...
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
        conductor_object = pyganim.PygConductor([self.animObj_UP, self.animObj_RIGHT, self.animObj_DOWN, self.animObj_LEFT])
        conductor_object.play() # starts all three animations at the same time.
        self.spriteImage = self.animObj_RIGHT
        self.needRewrite = True # we need to rewrite after Move

    def move(self, dx, dy, worldmap, worldobjects):
        #move by the given amount, if the destination is not blocked
        if not self.is_blocked(self.x+dx, self.y+dy, worldmap, worldobjects) and (dx != 0 or dy != 0):
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

    def draw(self, surface, worldmap):
        #set the color and then draw the character that represents this object at its position
        if self.needRewrite:
            self.spriteImage.blit(surface, worldmap.getTileTop(self.x, self.y))
            self.needRewrite = False

    def clear(self, surface, worldmap):
        #erase the character that represents this object
        #libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
        worldmap.drawTileAt(self.x, self.y, surface)
        self.needRewrite = True

    def is_blocked(self, new_x, new_y, worldmap, worldobjects):
        #first test the map tile
        if worldmap.getTileAt(new_x,new_y).blocked:
            return True

        #now check for any blocking objects
        for object in worldobjects:
            if object.blocks and object.x == new_x and object.y == new_y:
                return True

        return False


    def move_towards(self, target_x, target_y, worldmap, worldobject):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy, worldmap, worldobject)

    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


class Fighter:
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage

    def attack(self, target):
        #a simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            #make the target take some damage
            print(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
            target.fighter.take_damage(damage)
        else:
            print(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')


class BasicMonster:
    #AI for a basic monster.
    def take_turn(self, player, worldmap, worldobject):
        monster = self.owner
        #move towards player if far away (but not too far
        distance = monster.distance_to(player)
        if  distance >= 2 and distance <=6:
            monster.move_towards(player.x, player.y, worldmap, worldobject)

        #close enough, attack! (if the player is still alive.)
        elif distance < 2 and player.fighter.hp > 0:
            monster.fighter.attack(player)



def render_all(surface, worldmap):
    #draw all objects in the list
    for object in objects:
        object.draw(surface, worldmap)

    #blit the contents of "con" to the root console
    #libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

'''def handle_keys():
    #key = libtcod.console_check_for_keypress()  #real-time
    key = libtcod.console_wait_for_keypress(True)  #turn-based

    if key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game

    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)
'''
def getPlayableRect(player, screensizex, screensizey, worldmap):
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

def player_move_or_attack(dx, dy, player, worldmap, worldobject):

    #the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy

    #try to find an attackable object there
    target = None
    for anobject in worldobject:
        if anobject.x == x and anobject.y == y:
            target = anobject
            break

    #attack if target found, move otherwise
    if target is not None:
        player.fighter.attack(target)
    else:
        player.move(dx, dy, worldmap, worldobject)
        fov_recompute = True


def handle_key(player, worldmap, worldobject):
    dx = dy = 0
    global game_state

    if game_state == 'playing':
        for event in pygame.event.get():
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
            else:
                return 'didnt-take-turn'
    if dx!=0 or dy != 0:
        player_move_or_attack(dx, dy, player, worldmap, worldobject)
    else:
        return 'didnt-take-turn'

def main():
    # INIT MAP
    nbMapTileX = 120
    nbMapTileY = 90
    worldmap = dMap(nbMapTileX, nbMapTileY)

    # INIT OBJECTSx
    worldobject = []
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Object(worldmap.possibleBeginPlace[0][0], worldmap.possibleBeginPlace[0][1], 'player', 'resources/images/player.png', blocks=True, fighter = fighter_component)
    for i in range(1,20):
        fighter_component = Fighter(hp=10, defense=0, power=3)
        ai_component = BasicMonster()
        monster = Object(worldmap.possibleBeginPlace[i][0], worldmap.possibleBeginPlace[i][1], 'monster', 'resources/images/monster.png', blocks=True, fighter=fighter_component, ai=ai_component)
        worldobject.append(monster)
    worldobject.append(player)

    # STATE VARIABLE
    global game_state
    player_action = None

    # INIT DRAWINGS
    pygame.init()
    mainClock = pygame.time.Clock()
    gameSurface = pygame.display.set_mode((1024,768))
    pygame.display.set_caption('OrangeLord Game v0.1')
    entireWindowSurface = pygame.Surface(worldmap.getMapDimensionPixel())

    worldmap.drawMap(entireWindowSurface)
#    player.draw(entireWindowSurface, worldmap)


    # run the game loop
    while True:
        for object in worldobject:
            object.clear(entireWindowSurface, worldmap)

        #handle keys and exit game if needed
        player_action = handle_key(player, worldmap, worldobject)
        if player_action == 'exit':
            pygame.quit()
            sys.exit()

        #let monsters take their turn
        if game_state == 'playing' and player_action != 'didnt-take-turn':
            for object in worldobject:
                if object.ai:
                    object.ai.take_turn(player, worldmap, worldobject)
                    #print('The monster growls!')

        #player.clear(entireWindowSurface, worldmap)
        #(dx, dy) = handle_key()
        #player.move(dx, dy, worldmap, worldobject)


        #draw all objects (including player) in the list if required
        for object in worldobject:
            object.draw(entireWindowSurface, worldmap)

        playableSurface = entireWindowSurface.subsurface(getPlayableRect(player, 1024,768, worldmap))
        gameSurface.blit(playableSurface,(0,0))

        pygame.display.update()
        mainClock.tick(40)


if __name__ == '__main__':
    game_state = "playing"
    main()
