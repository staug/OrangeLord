#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Piccool
#
# Created:     10/05/2013
# Copyright:   (c) Piccool 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import GameGlobals, ast

class Equipment:
    #an object that can be equipped, yielding bonuses. automatically adds the Item component.
    def __init__(self, slot, characteristics):
        self.slot = slot
        self.is_equipped = False
        self.attack_bonus = (0,0)
        self.protection_bonus = 0
        self.range_attack = 0
        if "attack_bonus" in characteristics:
            self.attack_bonus = ast.literal_eval(characteristics["attack_bonus"])
        if "protection_bonus" in characteristics:
            self.protection_bonus = int(characteristics["protection_bonus"])
        if "range_attack" in characteristics:
            self.range_attack = int(characteristics["range_attack"])

    def toggle_equip(self):  #toggle equip/dequip status
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def equip(self):
        #if the slot is already being used, dequip whatever is there first
        old_equipment = get_equipped_in_slot(self.slot)
        if old_equipment is not None:
            old_equipment.dequip()

        #equip object and show a message about it
        self.is_equipped = True
        GameGlobals.messageBox.print('Equipped ' + self.owner.name + ' on ' + self.slot + '.')

    def dequip(self):
        #dequip object and show a message about it
        if not self.is_equipped: return
        self.is_equipped = False
        GameGlobals.messageBox.print('Dequipped ' + self.owner.name + ' from ' + self.slot + '.')

def get_max_range_attack_equiped():
    max_range = 0
    for obj in GameGlobals.inventory:
        if obj.equipment and obj.equipment.is_equipped:
            if max_range < obj.equipment.range_attack:
                max_range = obj.equipment.range_attack
    return max_range


def get_equipped_in_slot(slot):  #returns the equipment in a slot, or None if it's empty
    for obj in GameGlobals.inventory:
        if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
            return obj.equipment
    return None

def get_all_equipped(obj):  #returns a list of equipped items
    if obj == GameGlobals.player:
        equipped_list = []
        for item in GameGlobals.inventory:
            if item.equipment and item.equipment.is_equipped:
                equipped_list.append(item.equipment)
        return equipped_list
    else:
        return []  #other objects have no equipment

def main():
    pass

if __name__ == '__main__':
    main()
