#-------------------------------------------------------------------------------
# Name:        Items
# Purpose:
#
# Author:      Piccool
#
# Created:     09/05/2013
# Copyright:   (c) Piccool 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import GameGlobals, Game, GameConstants
import ObjectFighter
import Equipment
import random


class Item:
    #an item that can be picked up and used.
    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        #add to the player's inventory and remove from the map
        if len(GameGlobals.inventory) >= 26:
            GameGlobals.messageBox.print('Your inventory is full, cannot pick up ' + self.owner.name + '.')
        else:
            GameGlobals.inventory.append(self.owner)
            GameGlobals.levelobjects.remove(self.owner)
            GameGlobals.messageBox.print('You picked up a ' + self.owner.name + '!')

            #special case: automatically equip, if the corresponding equipment slot is unused
            equipment = self.owner.equipment
            if equipment and Equipment.get_equipped_in_slot(equipment.slot) is None:
                equipment.equip()

    def use(self):
        #special case: if the object has the Equipment component, the "use" action is to equip/dequip
        if self.owner.equipment:
            GameGlobals.messageBox.print('You equiped a ' + self.owner.name + '.')
            self.owner.equipment.toggle_equip()
            return

        #just call the "use_function" if it is defined
        if self.use_function is None:
            GameGlobals.messageBox.print('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                GameGlobals.inventory.remove(self.owner)  #destroy after use, unless it was cancelled for some reason

    def drop(self):
        #special case: if the object has the Equipment component, dequip it before dropping
        if self.owner.equipment:
            self.owner.equipment.dequip()

        #add to the map and remove from the player's inventory. also, place it at the player's coordinates
        GameGlobals.levelobjects.append(self.owner)
        GameGlobals.inventory.remove(self.owner)
        self.owner.x = GameGlobals.player.x
        self.owner.y = GameGlobals.player.y
        GameGlobals.messageBox.print('You dropped a ' + self.owner.name + '.')

##
## OBJECTS FUNCTIONS...
##

def cast_heal():
    #heal the player
    if GameGlobals.player.fighter.hp == GameGlobals.player.fighter.max_hp:
        GameGlobals.messageBox.print('You are already at full health.')
        return 'cancelled'

    GameGlobals.messageBox.print('Your wounds start to feel better!')
    GameGlobals.player.fighter.heal(random.randrange(10))

def fire_bolt():
    #trigger an explosion

    #find closest enemy (inside a maximum range) and damage it
    monster = closest_monster(5)
    if monster is None:  #no enemy found within maximum range
        GameGlobals.messageBox.print('No enemy is close enough to strike.', color=GameConstants.COLOR_RED)
        return 'cancelled'
    damage = random.randrange(10)
    #zap it!
    GameGlobals.messageBox.print('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is '
        + str(damage) + ' hit points.', color=GameConstants.COLOR_ORANGE)
    monster.fighter.take_damage(damage)

def closest_monster(max_range):
    #find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  #start with (slightly more than) maximum range

    for object in GameGlobals.levelobjects:
        if object.fighter and not object == GameGlobals.player: #and libtcod.map_is_in_fov(fov_map, object.x, object.y):
            #calculate distance between this object and the player
            dist = GameGlobals.player.distance_to(object)
            if dist < closest_dist:  #it's closer, so remember it
                closest_enemy = object
                closest_dist = dist
    return closest_enemy


def cast_fireball():
    fireball_radius = 3
    fireball_damage = 5
    #ask the player for a target tile to throw a fireball at
    GameGlobals.messageBox.print('Click a mosnter for the fireball (damage around!), or escape to cancel.')
    targets = Game.target_objects(maxDistanceFromPlayer=None, rangeRadius=fireball_radius, limitToOne=False, includesPlayer=True)
    if targets is None or len(targets) == 0: return 'cancelled'
    GameGlobals.messageBox.print('The fireball explodes, burning everything within ' + str(fireball_radius) + ' tiles!')

    for obj in GameGlobals.levelobjects:  #damage every fighter in range, including the player
        if obj in targets:
            damage = random.randrange(fireball_damage)
            GameGlobals.messageBox.print('The ' + obj.name + ' gets burned for ' + str(damage) + ' hit points.')
            obj.fighter.take_damage(damage)

def cast_confuse():
    confuse_range=3
    #ask the player for a target to confuse
    GameGlobals.messageBox.print('Click an enemy to confuse it, or escape to cancel.')
    monster = Game.target_objects(maxDistanceFromPlayer=confuse_range, rangeRadius=1, limitToOne=True, includesPlayer=False)
    if monster is None: return 'cancelled'

    #replace the monster's AI with a "confused" one; after some turns it will restore the old AI
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster  #tell the new component who owns it
    GameGlobals.messageBox.print('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!')




def main():
    pass

if __name__ == '__main__':
    main()
