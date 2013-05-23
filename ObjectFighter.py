#-------------------------------------------------------------------------------
# Name:        Objects and Fighters
# Purpose:
#
# Author:      Piccool
#
# Created:     09/05/2013
# Copyright:   (c) Piccool 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame, pyganim, ast, math

import GameGlobals
from Item import *
from GameConstants import *

class Object:
    #this is a generic object: the GameGlobals.player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, name, resources, blocks=False, fighter=None, ai=None, item=None, always_visible=False, equipment=None):
        self.x = x
        self.y = y
        self.name = name
        self.blocks = blocks
        self.resources = resources
        self.always_visible = always_visible

        self.fighter = fighter
        if self.fighter:  #let the fighter component know who owns it
            self.fighter.owner = self

        self.ai = ai
        if self.ai:  #let the AI component know who owns it
            self.ai.owner = self

        self.item = item
        if self.item:  #let the Item component know who owns it
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:  #let the Equipment component know who owns it
            self.equipment.owner = self

            #there must be an Item component for the Equipment component to work properly
            self.item = Item()
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
        (xtop, ytop) = ast.literal_eval(self.resources['image_top'])
        # Now split the image
        if self.resources['image_animated'] == 'yes':
            self.animObj_UP = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(xtop,ytop,self.spriteWidth,self.spriteHeight)), 0.3),
                           (spriteSurface.subsurface(pygame.Rect(xtop+self.spriteWidth,ytop,self.spriteWidth,self.spriteHeight)), 0.3),
                           (spriteSurface.subsurface(pygame.Rect(xtop+self.spriteWidth*2,ytop,self.spriteWidth,self.spriteHeight)), 0.3)])
            self.animObj_RIGHT = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(xtop,ytop+self.spriteHeight,self.spriteWidth,self.spriteHeight)), 0.3),
                           (spriteSurface.subsurface(pygame.Rect(xtop+self.spriteWidth,ytop+self.spriteHeight,self.spriteWidth,self.spriteHeight)), 0.3),
                           (spriteSurface.subsurface(pygame.Rect(xtop+self.spriteWidth*2,ytop+self.spriteHeight,self.spriteWidth,self.spriteHeight)), 0.3)])
            self.animObj_DOWN = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(xtop,ytop+self.spriteHeight*2,self.spriteWidth,self.spriteHeight)), 0.3),
                           (spriteSurface.subsurface(pygame.Rect(xtop+self.spriteWidth,ytop+self.spriteHeight*2,self.spriteWidth,self.spriteHeight)), 0.3),
                           (spriteSurface.subsurface(pygame.Rect(xtop+self.spriteWidth*2,ytop+self.spriteHeight*2,self.spriteWidth,self.spriteHeight)), 0.3)])
            self.animObj_LEFT = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect(xtop,ytop+self.spriteHeight*3,self.spriteWidth,self.spriteHeight)), 0.3),
                           (spriteSurface.subsurface(pygame.Rect(xtop+self.spriteWidth,ytop+self.spriteHeight*3,self.spriteWidth,self.spriteHeight)), 0.3),
                           (spriteSurface.subsurface(pygame.Rect(xtop+self.spriteWidth*2,ytop+self.spriteHeight*3,self.spriteWidth,self.spriteHeight)), 0.3)])
            self.spriteImage = self.animObj_RIGHT #arbitrary start

        else:
            self.spriteImage = self.animObj_DOWN = self.animObj_LEFT = self.animObj_RIGHT = self.animObj_UP = pyganim.PygAnimation([(spriteSurface.subsurface(pygame.Rect((xtop, ytop),(self.spriteWidth, self.spriteHeight))),1)])

        conductor_object = pyganim.PygConductor([self.animObj_UP, self.animObj_RIGHT, self.animObj_DOWN, self.animObj_LEFT])
        conductor_object.play() # starts all three animations at the same time.
        self.needRewrite = True # we need to rewrite after Move

    def setLocation(self, location):
        self.x = location[0]
        self.y = location[1]

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
            if self != GameGlobals.player:
                if GameGlobals.levelmap.getTileAt(self.x, self.y).isExplored():
                    self.spriteImage.blit(GameGlobals.entireWindowSurface, (self.x*IMG_SIZE_TILE_X, self.y*IMG_SIZE_TILE_Y))
            else:
                self.spriteImage.blit(GameGlobals.entireWindowSurface, (self.x*IMG_SIZE_TILE_X, self.y*IMG_SIZE_TILE_Y))
            self.needRewrite = False


    def clear(self):
        #erase the character that represents this object
        GameGlobals.levelmap.drawTile(self.x, self.y, True)
        self.needRewrite = True

    def is_blocked(self, new_x, new_y):
        #first test the map tile
        if GameGlobals.levelmap.getTileAt(new_x,new_y).blocked:
            return True

        #now check for any blocking objects
        for object in GameGlobals.levelobjects:
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

    def distance(self, x, y):
        #return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

class Fighter:

    #combat-related properties and methods (monster, GameGlobals.player, NPC).
    def __init__(self, hp, defense, power, xp = 0, wealth = 0, death_function=None):
        self.max_hp = hp
        self.hp = hp # vital energy
        self.defense = defense # defense, important!
        self.power = power # attack, important!
        if wealth > 0:
            self.wealth = random.randrange(wealth)
        else: self.wealth = 0
        self.xp=xp
        self.death_function = death_function

        # Naheulbleuk rules - Player setting!
        self.courage = 0 # courage
        self.dexterity = 0 #adresse
        self.strength = 0 #force
        self.wisdom = 0
        self.charisma = 0
        self.origin = ''
        self.work = ''
        self.mp = 0 # current astral energy
        self.max_mp = 0 # astral energy
        self.destiny_point = 3 # Number of lifes
        self.competencies = []


    def _player_roll(self):
        self.courage = random.randrange(7,13)
        self.wisdom = random.randrange(7,13)
        self.charisma = random.randrange(7,13)
        self.dexterity = random.randrange(7,13)
        self.strength = random.randrange(7,13)
        self.xp = 0

    def _rollOrigin(self):
        origins = []
        if self.courage >= 12 and self.strength>=13:
            origins.append(ORIGIN_LIST[1])
        if self.courage >= 11 and self.strength>=12:
            origins.append(ORIGIN_LIST[2])
        if self.wisdom >= 11 and self.charisma>=12 and self.dexterity >=12 and self.strength<=12:
            origins.append(ORIGIN_LIST[3])
        if self.charisma >= 10 and self.dexterity >=11:
            origins.append(ORIGIN_LIST[4])
        if self.charisma >= 12 and self.dexterity >=10 and self.strength <= 11:
            origins.append(ORIGIN_LIST[5])
        if self.wisdom >= 12 and self.dexterity >=13:
            origins.append(ORIGIN_LIST[6])
        if self.wisdom <= 8 and self.charisma<=10 and self.strength>=12:
            origins.append(ORIGIN_LIST[7])
        if self.wisdom <= 10 and self.dexterity<=11 and self.strength>=12:
            origins.append(ORIGIN_LIST[8])
        if self.courage <= 10 and self.wisdom<=10 and self.charisma<=8 and self.strength<=9:
            origins.append(ORIGIN_LIST[9])
        if self.wisdom<=9 and self.charisma<=10 and self.dexterity<=11 and self.strength>=13:
            origins.append(ORIGIN_LIST[10])
        if self.courage>=12 and self.wisdom>=10 and self.strength<=10:
            origins.append(ORIGIN_LIST[11])
        if self.wisdom>=10 and self.dexterity>=13 and self.strength<=8:
            origins.append(ORIGIN_LIST[12])
        if len(origins) == 0:
            self.origin = ORIGIN_LIST[0]
        else:
            self.origin = random.choice(origins)

    def _rollWork(self):
        works = []
        if self.courage>=12 and self.strength>= 12:
            works.append(WORK_LIST[0])
        if self.dexterity>=13:
            works.append(WORK_LIST[1])
        if self.dexterity>=12:
            works.append(WORK_LIST[2])
        if self.charisma>=12:
            works.append(WORK_LIST[3])
        if self.wisdom>=12:
            works.append(WORK_LIST[4])
        if self.courage>=12 and self.wisdom>= 10 and self.charisma>=11 and self.strength>=9:
            works.append(WORK_LIST[5])
        if self.charisma>=10 and self.dexterity>= 10:
            works.append(WORK_LIST[6])
        if self.charisma>=12 and self.dexterity>= 11:
            works.append(WORK_LIST[7])
        if self.wisdom>=12 and self.charisma>=11:
            works.append(WORK_LIST[8])
        if self.dexterity >= 11:
            works.append(WORK_LIST[9])
        if self.courage>=11 and self.dexterity >= 11:
            works.append(WORK_LIST[10])
        if self.wisdom>=10 and self.charisma >= 11:
            works.append(WORK_LIST[11])
        if len(works) == 0:
            self.work = 'unemployed'
        else:
            self.work = random.choice(works)

    def _modifyOriginalCharacteristics(self):
        if self.origin in (ORIGIN_LIST[1], ORIGIN_LIST[7]): # Barbare, Orc
            self.max_hp = 35
            self.power += 1
            self.defense -= 1
        if self.origin in (ORIGIN_LIST[2], ORIGIN_LIST[8]): # Dwarf, half orc
            self.max_hp = 35
        if self.origin in (ORIGIN_LIST[3], ORIGIN_LIST[5], ORIGIN_LIST[6], ORIGIN_LIST[11]) : # High elf or Sylvan, Dark, hobbit
            self.max_hp = 25
        if self.origin == ORIGIN_LIST[4]: # Half elf
            self.max_hp = 28
        if self.origin == ORIGIN_LIST[9]: # Goblin
            self.max_hp = 20
        if self.origin == ORIGIN_LIST[10]: # Ogre
            self.max_hp = 20
            self.power += 1
            self.defense -= 1
        if self.origin == ORIGIN_LIST[11]: # Gnome
            self.max_hp = 15
            self.power += 2
            self.defense -= 2

        # Now for Work...
        if self.work in (WORK_LIST[0]):
            if self.origin in (ORIGIN_LIST[0], ORIGIN_LIST[1]):
                self.max_hp = 35
            else:
                self.max_hp += 5
        # TODO!!!

    def _addCompetencies(self):
        pass

    def playerBirth(self):
        self.power = 8
        self.defense = 10
        self.hp = 30
        while (self.work== '' or self.work == 'unemployed'):
            self._player_roll()
            self._rollOrigin()
            self._rollWork()
        self._modifyOriginalCharacteristics()
        self._addCompetencies()
        self.wealth = random.randrange(2,12) * 10

    @property
    def equipmentProtection(self):
        if self.owner == GameGlobals.player:
            return 0 + sum(equipment.power_bonus for equipment in get_all_equipped(self.owner))

    @property
    def magical_resistance(self):
        return int((self.courage + self.wisdom + self.strength)/3)

    def print_stat(self):
        string = "Courage: "+str(self.courage)+"-" +"Wisdom: "+str(self.wisdom)+"-" +"Charisma: "+str(self.charisma)+"-" +"Dexterity: "+str(self.dexterity)+"-" +"Strength: "+str(self.strength)
        string = string + "-" + "Origin: "+ str(self.origin) + "-" + "Work: "+str(self.work)
        string = string + "-" + "Magical Resistance " + str(self.magical_resistance)
        string = string + "-" + "Wealth " + str(self.wealth)
        print(string)
        return(string)

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
        '''
        #a simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            #make the target take some damage
            GameGlobals.messageBox.print(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
            target.fighter.take_damage(damage)
        else:
            GameGlobals.messageBox.print(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')
        '''
        # Each round is a combination of an attack by A, and an attack by B
        # Biggest courage start
        fighterA = self
        fighterB = target.fighter
        if (fighterB.courage > fighterA.courage):
            fighterA = target.fighter
            fighterB = self

        # fighter A turn
        Fighter._combatTurn(fighterA,fighterB)

        if (fighterB.hp>0):
        # fighter B turn if not dead!
            Fighter._combatTurn(fighterB, fighterA)

    @staticmethod
    def _combatTurn(fighterA, fighterB):
        '''
        Fighter A is attacking fighter B.
        '''
        attackScore = random.randrange(1,20)
        if (attackScore <= fighterA.power):
            # success
            GameGlobals.messageBox.print(fighterA.owner.name.capitalize() + ' attacks ' + fighterB.owner.name + ' with success [SCORE:' + str(attackScore) + '/POWER:'+str(fighterA.power)+']', COLOR_ORANGE)
            defenseScore = random.randrange(1,20)
            if (defenseScore <= fighterB.defense):
                GameGlobals.messageBox.print(fighterB.owner.name.capitalize() + ' successfully avoid ' + fighterA.owner.name + ' blow [SCORE:' + str(defenseScore) + '/DEFENSE:'+str(fighterB.defense)+']', COLOR_ORANGE)
            else:
                GameGlobals.messageBox.print(fighterB.owner.name.capitalize() + ' cannot avoid ' + fighterA.owner.name + ' blow [SCORE:' + str(defenseScore) + '/DEFENSE:'+str(fighterB.defense)+']', COLOR_ORANGE)
                damage = random.randrange(1,10) # to update
                GameGlobals.messageBox.print(fighterB.owner.name.capitalize() + ' takes from ' + fighterA.owner.name + ' ' + str(damage) + ' damage', COLOR_ORANGE)
                fighterB.take_damage(damage)
        else:
            # attack failure
            GameGlobals.messageBox.print(fighterA.owner.name.capitalize() + ' attacks ' + fighterB.owner.name + ' but fails [SCORE:' + str(attackScore) + '/POWER:'+str(fighterA.power)+']', COLOR_ORANGE)


    def heal(self, amount):
        #heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp


class BasicMonster:
    #AI for a basic monster.
    def take_turn(self):
        monster = self.owner
        #move towards GameGlobals.player if far away (but not too far
        distance = monster.distance_to(GameGlobals.player)
        if  distance >= 2 and distance <=6:
            monster.move_towards(GameGlobals.player.x, GameGlobals.player.y)
        #close enough, attack! (if the GameGlobals.player is still alive.)
        elif distance < 2 and GameGlobals.player.fighter.hp > 0:
            monster.fighter.attack(GameGlobals.player)

class ConfusedMonster:
    #AI for a temporarily confused monster (reverts to previous AI after a while).
    def __init__(self, old_ai, num_turns=10):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:  #still confused...
            #move in a random direction, and decrease the number of turns confused
            self.owner.move(randint(-1, 1), randint(-1, 1))
            self.num_turns -= 1

        else:  #restore the previous AI (this one will be deleted because it's not referenced anymore)
            self.owner.ai = self.old_ai
            messageBox.print('The ' + self.owner.name + ' is no longer confused!', color=COLOR_RED)


def player_move_or_attack(dx, dy):

    #the coordinates the GameGlobals.player is moving to/attacking
    oldRoomName = GameGlobals.levelmap.getRoomOfTile(GameGlobals.player.x, GameGlobals.player.y).name
    x = GameGlobals.player.x + dx
    y = GameGlobals.player.y + dy

    #try to find an attackable object there
    target = None
    for anobject in GameGlobals.levelobjects:
        if anobject.fighter and anobject.x == x and anobject.y == y:
            target = anobject
            break

    #attack if target found, move otherwise
    if target is not None:
        GameGlobals.player.fighter.attack(target)
    else:
        GameGlobals.player.move(dx, dy)
        newRoomName = GameGlobals.levelmap.getRoomOfTile(GameGlobals.player.x, GameGlobals.player.y).name
        if newRoomName != oldRoomName:
            GameGlobals.messageBox.print("You enter the " + str(newRoomName))
            GameGlobals.player.fighter.heal(random.randrange(0,3))
        #recomputeFog(GameGlobals.player.x, GameGlobals.player.y)

    # Test if a trap has been triggered
    GameGlobals.levelmap.testTrap()


def player_death(self):
    #the game ended!
    global game_state
    GameGlobals.messageBox.print('You died!')
    GameGlobals.gameState = 'dead'

    #for added effect, transform the GameGlobals.player into a corpse!
    GameGlobals.player.spriteImage = pyganim.PygAnimation([('resources/images/tumb.png',1)])
    GameGlobals.player.needRewrite = True

def monster_death(monster):
    GameGlobals.messageBox.print(monster.name.capitalize() + ' is dead! - You win '+str(monster.fighter.xp)+' xp points and '+str(monster.fighter.wealth)+ ' wealth')
    GameGlobals.player.fighter.xp += monster.fighter.xp
    GameGlobals.player.fighter.wealth += monster.fighter.wealth
    #transform it into a nasty corpse! it doesn't block, can't be
    #attacked and doesn't move
    monster.conductor_object = None
    monster.spriteImage = pyganim.PygAnimation([('resources/images/tumb.png',1)])
    monster.spriteImage.play()
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.needRewrite = True
    monster.name = 'remains of ' + monster.name

def closest_monster(max_range):
    #find closest enemy, up to a maximum range, and in the GameGlobals.player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  #start with (slightly more than) maximum range

    for object in GameGlobals.levelobjects:
        if object.fighter and not object == GameGlobals.player and GameGlobals.levelmap.getTileAt(object.x, object.y).isVisible():
            #calculate distance between this object and the GameGlobals.player
            dist = GameGlobals.player.distance_to(object)
            if dist < closest_dist:  #it's closer, so remember it
                closest_enemy = object
                closest_dist = dist
    return closest_enemy

def main():
    pass

if __name__ == '__main__':
    main()
