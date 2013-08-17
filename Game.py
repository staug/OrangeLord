#-------------------------------------------------------------------------------
# Name:        Game
# Purpose:      Main Aspect of the game, all main variables.
#
# Author:      Piccool
#
# Created:     09/05/2013
# Copyright:   (c) Piccool 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame, shelve, configparser, GameGlobals, sys
import pygame._view

from pygame.locals import *
from GameConstants import *

from DungeonTile import *
from ObjectFighter import *
from Item import *
from Equipment import *

import __main__


class MessageBox:
    '''
    The part of teh screen taht is responsible for writing status messages
    '''
    def __init__(self):
        self.font = pygame.font.Font(GAME_FONT, 14)
        self.messages=[]
        self.nbMessages = 10
        self.textRect = pygame.Rect(20, DISP_PLAYABLE_HEIGHT + 70, DISP_MESSAGE_WIDTH, DISP_MESSAGE_HEIGHT)
        self.textSurface = gameSurface.subsurface(self.textRect)
        # create a copy of the background
        self.saveSurface = self.textSurface.copy()

    def print(self, aMessage, color=(255,255,255)):
        #Erase previous
        self.textSurface.blit(self.saveSurface, (0,0))

        if (len(aMessage) < 100):
            self.messages.append({'txt':aMessage,'color':color})
        else:
            self.messages.append({'txt':aMessage[:125],'color':color})
            self.messages.append({'txt':aMessage[125:],'color':color})
            if len(self.messages) > self.nbMessages:
                self.messages = self.messages[1:]
        if len(self.messages) > self.nbMessages:
            self.messages = self.messages[1:]

        fontHeight = self.font.get_height()
        surfaces = [self.font.render(ln['txt'], True, ln['color'], (80,22,22)) for ln in self.messages]

        for i in range(len(self.messages)):
            self.textSurface.blit(surfaces[i], (0,i*fontHeight))
        pygame.display.update(self.textSurface.get_rect())


def target_objects(maxDistanceFromPlayer=None, rangeRadius=1, limitToOne=True, includesPlayer=False):
    '''
    Returns an array of objects containing objects:
        - that are located at the click position +/- the range radius
        - that are at a distance less or equal to the maxDistanceFromPlayer
        - if limitToOne is set to true, the first object is returned
        - if includesPlayer is set to true, returns also the player
    The objects needs to be in a visible tile.
    '''
    #returns a clicked monster inside FOV up to a range, or None if right-clicked
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return None

            if event.type == MOUSEBUTTONDOWN:
                (clickx,clicky) = event.pos
                playableleft = max(GameGlobals.player.x*IMG_SIZE_TILE_X - (DISP_PLAYABLE_WIDTH)/2,0)
                playabletop = max(GameGlobals.player.y*IMG_SIZE_TILE_Y - (DISP_PLAYABLE_HEIGHT)/2,0)
                if GameGlobals.player.y*IMG_SIZE_TILE_Y + (DISP_PLAYABLE_HEIGHT)/2 > GAME_NB_TILE_Y*IMG_SIZE_TILE_Y:
                    playabletop = GAME_NB_TILE_Y*IMG_SIZE_TILE_Y - DISP_PLAYABLE_HEIGHT
                if GameGlobals.player.x*IMG_SIZE_TILE_X + (DISP_PLAYABLE_WIDTH)/2 > GAME_NB_TILE_X*IMG_SIZE_TILE_X:
                    playableleft = GAME_NB_TILE_X*IMG_SIZE_TILE_X - DISP_PLAYABLE_WIDTH
                tilex = int((clickx -10 + playableleft)/IMG_SIZE_TILE_X)
                tiley = int((clicky -10 + playabletop)/IMG_SIZE_TILE_Y)

                monsterList = []
                for obj in GameGlobals.levelobjects:
                    if (obj.x in range(tilex-rangeRadius, tilex+rangeRadius) and obj.y in range(tiley-rangeRadius, tiley+rangeRadius) and obj.fighter!= None) and  GameGlobals.levelmap.getRoomOfTile(obj.x, obj.y).name ==  GameGlobals.levelmap.getRoomOfTile(GameGlobals.player.x, GameGlobals.player.y).name:
                        # print( GameGlobals.levelmap.getRoomOfTile(obj.x, obj.y).name +'-'+GameGlobals.levelmap.getRoomOfTile(GameGlobals.player.x, GameGlobals.player.y).name)
                        if (maxDistanceFromPlayer == None or GameGlobals.player.distance(obj.x, obj.y) <= maxDistanceFromPlayer):
                            if (includesPlayer == True or obj != GameGlobals.player):
                                # We have an object that is eligible...
                                if (limitToOne == True):
                                    return obj
                                monsterList.append(obj)
                return monsterList



def menu(header, options, width, colorBar=COLOR_RED):
    ''' Shows a nice menu on top of the screen
    '''
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    #but before that make a copy of the original!
    copySurface = gameSurface.copy()

    font = pygame.font.Font(GAME_FONT, GAME_FONT_SIZE)
    fontHeight = font.get_height()+5
    #calculate total height for the header (after auto-wrap) and one line per option
    height = (len(options)+2)*fontHeight


    #create an off-screen console that represents the menu's window
    window = pygame.Surface((width, height))
    window.fill(COLOR_BLACK)
    #rect2 = AAfilledRoundedRect(gameSurface, pygame.Rect(DISP_GAME_WIDTH/2 - width/2 -10 , DISP_GAME_HEIGHT/2 - height/2 - 10, width +20, height+20), COLOR_GREEN)
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

    rect = gameSurface.blit(window, (x, y))

    #present the root console to the player and wait for a key-press
    #pygame.display.update(rect)
    pygame.display.update()
    pygame.event.set_allowed([pygame.KEYDOWN])
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Now we copy back the old content
                gameSurface.blit(copySurface, (x, y), rect)
                pygame.display.update(rect)
                #convert the ASCII code to an index; if it corresponds to an option, return it
                index = -1
                if(event.unicode != ''):
                    index = ord(event.unicode) - ord('a')
                if index >= 0 and index < len(options):
                    return index
                return None

def inventory_menu(header):
    #show a menu with each item of the inventory as an option
    if len(GameGlobals.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in GameGlobals.inventory]

    index = menu(header, options, DISP_INVENTORY_WIDTH)

    #if an item was chosen, return it
    if index is None or len(GameGlobals.inventory) == 0: return None
    return GameGlobals.inventory[index].item

def getPlayableRect(screensizex, screensizey):
    playableleft = playabletop = 0
    playerY = GameGlobals.player.y * IMG_SIZE_TILE_Y
    playerX = GameGlobals.player.x * IMG_SIZE_TILE_X

    playableleft = max(playerX - (screensizex)/2,0)
    playabletop = max(playerY - (screensizey)/2,0)
    if playerY + (screensizey)/2 > GAME_NB_TILE_Y*IMG_SIZE_TILE_Y:
        playabletop = GameGlobals.levelmap.grid_size[1]*IMG_SIZE_TILE_Y - screensizey
    if playerX + (screensizex)/2 > GAME_NB_TILE_X*IMG_SIZE_TILE_X:
        playableleft = GameGlobals.levelmap.grid_size[0]*IMG_SIZE_TILE_X - screensizex
    playableRect = pygame.Rect(playableleft,playabletop,screensizex,screensizey)
    return playableRect

def render_bar(x, y, total_width, total_height, name, value, maximum, bar_color, back_color=(0,0,0)):
    ''' The bar is located at x,y part of the screen
    '''
    #render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = 1
    if maximum>0:
        bar_width = max(1, int(float(value) / maximum * total_width))

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

def print_player_char():
    font = pygame.font.Font(GAME_FONT, 15)
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.name),1,(255,255,255)), (890, 34))
    gameSurface.blit(font.render("Of " + str(GameGlobals.player.fighter.country),1,(255,255,255)), (890, 34+font.get_height()))
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.origin),1,(255,255,255)), (890, 34+font.get_height()*2))
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.work),1,(255,255,255)), (890, 34+font.get_height()*3))
    #display text with the values
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.courage),1,(255,255,255)), (RECT_CHAR_CO.x, RECT_CHAR_CO.y))
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.charisma),1,(255,255,255)), (RECT_CHAR_CH.x, RECT_CHAR_CH.y))
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.wisdom),1,(255,255,255)), (RECT_CHAR_WI.x, RECT_CHAR_WI.y))
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.attack),1,(255,255,255)), (RECT_CHAR_AT.x, RECT_CHAR_AT.y))
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.strength),1,(255,255,255)), (RECT_CHAR_ST.x, RECT_CHAR_ST.y))
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.agility),1,(255,255,255)), (RECT_CHAR_AG.x, RECT_CHAR_AG.y))
    gameSurface.blit(font.render(str(GameGlobals.player.fighter.parry),1,(255,255,255)), (RECT_CHAR_PA.x, RECT_CHAR_PA.y))


def system_init():
##    global messageBox, allButtons # UI ZONES
    global gameSurface # Spritable zones
    global mainClock

    # System Init
    pygame.init()
    mainClock = pygame.time.Clock()
    gameSurface = pygame.display.set_mode((DISP_GAME_WIDTH,DISP_GAME_HEIGHT))
    pygame.display.set_caption('Orange Lord Game v0.8')

def main_menu():
    mainMenuImage = pygame.image.load('resources/images/the_orange_knight_by_jouste.jpg').convert_alpha()

    while True:
        #show the background image, at twice the regular console resolution
        gameSurface.blit(mainMenuImage, (0, 0), (0,0,1024,768))
        pygame.display.update()

        pygame.mixer.music.load('resources/donjon_crom.ogg')
        pygame.mixer.music.play(-1,0.0)

        #show options and wait for the player's choice
        choice = menu('  Orange Dungeon  ', ['Play a new game', 'Continue last game', 'Quit'], 500, colorBar= COLOR_ORANGE)

        if choice == 0:  #new game
            pygame.mixer.music.stop()
            new_game(1)
            play()
        if choice == 1:  #load last game
            pygame.mixer.music.stop()
            try:
                load_game()
                play()
            except:
                print('No saved game to load')
                continue
        elif choice == 2:  #quit
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

def new_game(level, reroll_player=True):
    config = configparser.RawConfigParser()
    config.read('resources/definitions.ini')

    if reroll_player: GameGlobals.inventory = []
    GameGlobals.levelobjects = []


    # INIT OBJECTS
    # ------------------------------------------------
    # Read the config file

    itemQty = monsterQty = 0

    levelName = 'Level ' + str(level)

    # How many items in Level 1?
    globalItemQty = globalMonsterQty = 0
    itemList = (config.get(levelName, 'items')).split('#')
    for item in itemList:
        itemName = (item.split(','))[0]
        itemQty = int((item.split(','))[1])


        for i in range(itemQty):
            equipment = None
            listing = config._sections[itemName]
            if config.has_option(itemName, 'equipment'):
                equipment = Equipment(config.get(itemName, 'equipment'), config._sections[itemName])
                item = Object(0, 0, itemName, config._sections[itemName], equipment = equipment)
                GameGlobals.levelobjects.append(item)
            else:
                item_component = Item(use_function=getattr(__main__,config.get(itemName, 'use_function')))
                item = Object(0, 0, itemName, config._sections[itemName], item=item_component)
                GameGlobals.levelobjects.append(item)
            globalItemQty += 1


    monsterList = (config.get(levelName, 'monsters')).split('#')
    for monster in monsterList:
        monsterName = (monster.split(','))[0]
        monsterQty = int((monster.split(','))[1])

        for i in range(monsterQty):
            fighter_component = Fighter(config._sections[monsterName])
            ai_component = BasicMonster()
            monster = Object(0,0, monsterName, config._sections[monsterName], blocks=True, fighter=fighter_component, ai=ai_component)
            GameGlobals.levelobjects.append(monster)
            globalMonsterQty += 1

    # Generate Map
    GameGlobals.levelmap = Dungeon((GAME_NB_TILE_X,GAME_NB_TILE_Y),level,50,(4,4),(10,12),globalItemQty,globalMonsterQty)
    GameGlobals.levelmap.generate_dungeon()

    totalplace = GameGlobals.levelmap.item_locs + GameGlobals.levelmap.monster_locs
    index = 0
    for object in GameGlobals.levelobjects:
        object.setLocation(totalplace[index])
        index += 1

    # Stairs
    GameGlobals.levelobjects.append(ObjectFighter.Object(GameGlobals.levelmap.pos_stairup[0], GameGlobals.levelmap.pos_stairup[1], 'Stair going up', {'image_file':'resources/images/abigaba_nethack_bis.png','image_animated':'none','image_size_x':'32','image_size_y':'32','image_top':'(415,670)'}))
    GameGlobals.levelobjects.append(ObjectFighter.Object(GameGlobals.levelmap.pos_stairdown[0], GameGlobals.levelmap.pos_stairdown[1], 'Stair going down', {'image_file':'resources/images/abigaba_nethack_bis.png','image_animated':'none','image_size_x':'32','image_size_y':'32','image_top':'(447,670)'}))

    # PLAYER
    if reroll_player:
        fighter_component = Fighter(config._sections['player'])
        fighter_component.playerBirth()
        GameGlobals.player = Object(0,0, 'player', config._sections['player'], blocks=True, fighter = fighter_component)
        GameGlobals.player.setLocation(GameGlobals.levelmap.pos_stairup)
        GameGlobals.levelobjects.append(GameGlobals.player)



def play():
    global game_state
##    global entireWindowSurface

    game_state = "playing"

    # Totally erase the surface
    #gameSurface.fill(COLOR_BLACK)
    backgroundImage = pygame.image.load('resources/images/backgroundImage.png').convert()
    gameSurface.blit(backgroundImage, (0,0))

    # Prepare the message bar
    GameGlobals.messageBox = MessageBox()

    # Prepare drawing
    GameGlobals.entireWindowSurface = pygame.Surface((GAME_NB_TILE_X*IMG_SIZE_TILE_X, GAME_NB_TILE_Y*IMG_SIZE_TILE_Y))
    GameGlobals.messageBox.print("Welcome in the Orange Lord Domain....", color=COLOR_RED)

    # Draw the world
    GameGlobals.levelmap.draw()
#    for button in GameGlobals.allButtons:
#        button.draw(gameSurface)

    # STATE VARIABLE
    player_action = None
    GameGlobals.levelmap.computeFogOfWar(GameGlobals.player.x, GameGlobals.player.y)

    # run the game loop
    while True:
        for object in GameGlobals.levelobjects:
            object.clear()
        GameGlobals.levelmap.reinitFogOfWar(GameGlobals.player.x, GameGlobals.player.y)

        #handle keys and exit game if needed
        player_action = handle_key()
        if player_action == 'exit':
            #save_game()
            pygame.quit()
            sys.exit()

        GameGlobals.levelmap.computeFogOfWar(GameGlobals.player.x, GameGlobals.player.y)

        #let monsters take their turn
        if game_state == 'playing' and player_action != 'didnt-take-turn':
            for object in GameGlobals.levelobjects:
                if object.ai:
                    object.ai.take_turn()

        #draw all objects (including player) in the list if required
        for object in GameGlobals.levelobjects:
            if object != GameGlobals.player:
                object.draw()
        GameGlobals.player.draw()

        playableSurface = GameGlobals.entireWindowSurface.subsurface(getPlayableRect(DISP_PLAYABLE_WIDTH, DISP_PLAYABLE_HEIGHT))
        gameSurface.blit(playableSurface,(10,10))

        #draw health & magic bar
        render_bar(RECT_HP.x, RECT_HP.y, RECT_HP.w, RECT_HP.h, 'HP', GameGlobals.player.fighter.hp, GameGlobals.player.fighter.max_hp, (170,0,0), back_color=(222,135,135))
        render_bar(RECT_MP.x, RECT_MP.y, RECT_MP.w, RECT_MP.h, 'MP', GameGlobals.player.fighter.mp, GameGlobals.player.fighter.max_mp, (0,102,128), back_color=(175,198,233))
        print_player_char()

        pygame.display.update()
        mainClock.tick(40)


def handle_key():
    dx = dy = 0
    eventHandledByButton = False
    if game_state == 'playing':
        for event in pygame.event.get():
            # handle button
            if event.type == MOUSEBUTTONDOWN:
                if RECT_QUIT.collidepoint(event.pos):
                    return 'exit'
                else:
                    (clickx,clicky) = event.pos
                    playableleft = max(GameGlobals.player.x*IMG_SIZE_TILE_X - (DISP_PLAYABLE_WIDTH)/2,0)
                    playabletop = max(GameGlobals.player.y*IMG_SIZE_TILE_Y - (DISP_PLAYABLE_HEIGHT)/2,0)
                    if GameGlobals.player.y*IMG_SIZE_TILE_Y + (DISP_PLAYABLE_HEIGHT)/2 > GAME_NB_TILE_Y*IMG_SIZE_TILE_Y:
                        playabletop = GAME_NB_TILE_Y*IMG_SIZE_TILE_Y - DISP_PLAYABLE_HEIGHT
                    if GameGlobals.player.x*IMG_SIZE_TILE_X + (DISP_PLAYABLE_WIDTH)/2 > GAME_NB_TILE_X*IMG_SIZE_TILE_X:
                        playableleft = GAME_NB_TILE_X*IMG_SIZE_TILE_X - DISP_PLAYABLE_WIDTH
                    tilex = int((clickx-10 + playableleft)/IMG_SIZE_TILE_X)
                    tiley = int((clicky-10 + playabletop)/IMG_SIZE_TILE_Y)

                    names = [obj.name for obj in GameGlobals.levelobjects if (obj.x in (tilex, tilex-1, tilex+1) and obj.y in (tiley, tiley-1, tiley+1))]
                    names = ', '.join(names)
                    if names!=None and names != '':
                        if GameGlobals.levelmap.getRoomOfTile(tilex, tiley) != None:
                            names = names + ' in the ' + GameGlobals.levelmap.getRoomOfTile(tilex, tiley).name
                        GameGlobals.messageBox.print("Around, " + names.capitalize())

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
                    for object in GameGlobals.levelobjects:  #look for an item in the player's tile
                        if object.x == GameGlobals.player.x and object.y == GameGlobals.player.y and object.item:
                            object.item.pick_up()
                            break
                if event.key == K_i:
                    #inventory
                    #show the inventory; if an item is selected, use it
                    chosen_item = inventory_menu('Use one of:')
                    if chosen_item is not None:
                        chosen_item.use()

                if event.key == K_d:
                #show the inventory; if an item is selected, drop it
                    chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                    if chosen_item is not None:
                        chosen_item.drop()

                if event.key == K_c:
                #Display the player characteristics
                    GameGlobals.messageBox.print(GameGlobals.player.fighter.print_stat(), COLOR_GREEN)
                return 'didnt-take-turn'
    if dx!=0 or dy != 0:
        player_move_or_attack(dx, dy)
    else:
        return 'didnt-take-turn'


if __name__ == '__main__':
    system_init()
    main_menu()
