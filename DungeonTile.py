#-------------------------------------------------------------------------------
# Name:        Dungeon and map related objects
# Purpose:     Manage the overall maps, and print the tile
#
# Author:       Piccool
#               Reuse the algorithm from Breiny Games
# ##########################################
# # Dungeon Generator -- map_generator.py ##
# ##########################################
# ###### Breiny Games (c) 2011 #############
#               https://code.google.com/p/pygame-dungeon-gen/
#
# Created:     08/05/2013
# Copyright:   (c) Piccool 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import random, math
import time
import pygame
import GameGlobals

from astar import *
from distance_map import *

from GameConstants import *

class Room:


    """
    The class for all of the rooms in a dungeon.


    Room((size_x, size_y), tiles)


    (size_x, size_y)
        -an ordered pair representing the size of the room.

    tiles
        -a 2D list containing numbers that represent tiles inside the room.
            0 = blank space (non-useable)
            1 = floor tile (walkable)
            2 = corner tile (non-useable)
            3 = wall tile facing NORTH.
            4 = wall tile facing EAST.
            5 = wall tile facing SOUTH.
            6 = wall tile facing WEST.
            7 = door tile.
            8 = stairs leading to a higher lever in the dungeon.
            9 = stairs leading to a lower level in the dungeon.
            10 = chest
            11 = path from up to down staircases (floor tile)
    """
    def __init__(self, size, tiles):

        self.size = size
        self.tiles = tiles
        self.position = None
        self.name = Room.nameGenerator()

    def getConnectionPoints(self):
        '''
        build a list of location to rooms that are connected
        '''


        connectionList = []
        for xvar in range(0, self.size[0]-1):
            if self.tiles[0][xvar] in (1,7):
                connectionList.append((self.position[0]+xvar, self.position[1]+2))
            if self.tiles[self.size[1]-1][xvar] in (1,7):
                connectionList.append((self.position[0]+xvar, self.position[1]+self.size[1]-2))

        for yvar in range(0, self.size[1]-1):
            if self.tiles[yvar][0] in (1,7):
                connectionList.append((self.position[0]+2, self.position[1]+yvar))
            if self.tiles[yvar][self.size[0]-1] in (1,7):
                connectionList.append((self.position[0]+self.size[0]-2, self.position[1]+yvar))

        return connectionList

    @staticmethod
    def nameGenerator():
        roomNamePart1 = ('Accursed', 'Ancient', 'Baneful', 'Batrachian', 'Black', 'Bloodstained', 'Cold', 'Dark', 'Devouring', 'Diabolical', 'Ebon', 'Eldritch', 'Forbidden', 'Forgotten', 'Haunted', 'Hidden', 'Lonely', 'Lost', 'Malevolent', 'Misplaced', 'Nameless', 'Ophidian', 'Scarlet', 'Secret', 'Shrouded', 'Squamous', 'Strange', 'Tenebrous', 'Uncanny', 'Unspeakable', 'Unvanquishable', 'Unwholesome', 'Vanishing', 'Weird')
        roomNamePart2 = ('room', 'hall', 'place', 'pit', 'shamble', 'crossing', 'location', 'center', 'cavity','cell', 'hollow', 'alcove', 'antechamber', 'wherabouts')
        roomNamePart3 = ('the Axolotl', 'Blood', 'Bones', 'Chaos', 'Curses', 'the Dead', 'Death', 'Demons', 'Despair', 'Deviltry', 'Doom', 'Evil', 'Fire', 'Frost', 'the 8 Geases', 'Gloom', 'Hells', 'Horrors', 'Ichor', 'Ice', 'Id Insinuation', 'the Idol', 'Iron', 'Madness', 'Mirrors', 'Mists', 'Monsters', 'Mystery', 'Necromancy', 'Oblivion', 'Peril', 'Phantasms', 'Random Harlots', 'Secrets', 'Shadows', 'Sigils', 'Skulls', 'Slaughter', 'Sorcery', 'Syzygy', 'Terror', 'Torment', 'Treasure', 'the Undercity', 'the Underworld', 'the Unknown', 'Whispers')
        return random.choice(roomNamePart1) + ' ' + random.choice(roomNamePart2) + ' of ' + random.choice(roomNamePart3)

class Dungeon:


    """
    The Dungeon class.


    Dungeon((grid_size_x, grid_size_y),
             name,
             max_num_rooms,
             min_room_size,
             max_room_size)

    (grid_size_x, grid_size_y)
        - the total size/area of the map in tiles.
            e.g. (25, 20) would set the map to be 25 tiles wide and 20 tall.

    name
        - the name of the dungeon

    max_num_rooms
        - the maximum number of rooms for the dungeon to contain.

    min_room_size
        - the minimum size for each room.
            e.g. (3, 3) would set the minimum room size to 3 tiles by 3 tiles.

    max_room_size
        - the maximum size for each room.
            e.g. (7, 7) would set the maximum room size to 7 tiles by 7 tiles.



    Misc Information:

        -self.grid is the most important variable in this whole file. It is a 2
        dimensional list that stores the entire map and layout of the dungeon.
        Each number in the list represents a tile in the dungeon.
            0 = blank space (non-useable)
            1 = floor tile (walkable)
            2 = corner tile (non-useable)
            3 = wall tile facing NORTH.
            4 = wall tile facing EAST.
            5 = wall tile facing SOUTH.
            6 = wall tile facing WEST.
            7 = door tile.
            8 = stairs leading to a higher lever in the dungeon.
            9 = stairs leading to a lower level in the dungeon.
            10 = chest
            11 = path from up to down staircases (floor tile)

        -self.rooms stores the Room object from the Room class, which stores
         what tiles are room holds, the size of the room, and the coordinate
         of the top-left tile (number) of the room. The position and size
         variables are especially important because they are used together to
         calculate the section of the dungeon grid we look at to pick a random
         wall (number) to branch from in the get_branching_position() function.



    Functions:


        print_info(grid=True)
            - prints the name, size, number of rooms, and if passed 'True' for
              the grid argument, prints the actual layout of the dungeon, all
              to the python shell.


        generate_room((min_size_x, min_size_y), (max_size_x, max_size_y))
            - enerates a randomly sized list of numbers to represent a room.
              (see the Room class for more details on what the numbers mean.)

            (min_size_x, min_size_y)
                - the minimum size of each room to be generated.

            (max_size_x, max_size_y)
                - the maximum size of each room to be generated.


        get_branching_position()
            - picks a random room that has been placed, then picks a random
              (valid) wall tile (number) from the room, and returns the
              position in the dungeon grid that it is located at. Valid walls
              (numbers) include 3, 4, 5, 6. See the Room class for more info
              on what the numbers actually represent.


        get_branching_direction(branching_position)
            - returns the direction the passed 'wall tile' (numbers 3, 4, 5, 6
              in the grid list) is facing.

            branching_position
                - the coordinates of the 'wall tile' in the grid list we want
                  to find out which way is facing.


        space_for_new_room((new_room_size_x, new_room_size_y),
                            new_room_position)
            - checks to see if there is space to add a given room to the
              dungeon. Returns True if there is, False if otherwise.

            (new_room_size_x, new_room_size_y)
                - the size of the room to be checked.

            new_room_position
                - the coordinates of where the room would be. We start here,
                  then check the entire area of the grid the room covers
                  to see if it overlaps with any other rooms. If it doesn't
                  overlap with anything, return True. Otherwise return False.


        place_room(room, (grid_x, grid_y))
            - changes the grid list to add the given room to it.

            room
                - the room we want to add to the grid.

            (grid_x, grid_y)
                - the location inside the grid we want to change to add the
                  room to.


        connect_rooms(branching_pos, direction)
            - slightly changes the grid list to connect 2 rooms. Changes the
              wall tile, and the tile next to it in the direction it's
              facing, both to floor tiles (1's in the grid list).

            branching_pos
                - the location of the tile we just added a room to.

            direction
                - the direction the wall was facing before we added the room.

            *- think of it like this. We pick a random wall tile of a random
               room. This is the spot we want to add another room to. After we
               add the room to that spot, we now turn that spot from a wall tile
               into a floor tile (e.g. a 3 into a 1), then whichever way the
               tile was facing, we take the tile in that direction next to it
               and also turn it into a floor tile.


        set_staircases()
            - picks a random room, then a random floor tile (a 1 in the grid
              list) and turn it into a staircase going up (8 in the grid list).
              Then does the same thing again, but changes the next floor tile
              into a staircase going dowm (9 in the grid list).


        generate_dungeon()
            - uses all of the above functions, to generate a dungeon.
    """


    def __init__(self, grid_size, name,
                 max_num_rooms, min_room_size, max_room_size, number_items, number_monsters):

        self.grid_size = grid_size
        self.name = name
        self.max_num_rooms = max_num_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size

        self.number_items = number_items
        self.number_monsters = number_monsters

        self.rooms = []
        self.grid = []
        self.tileset = []

        # intersting positions
        self.pos_stairdown = (0,0)
        self.pos_stairup = (0,0)
        self.item_locs = []
        self.monster_locs = []


    def print_info(self, grid=False):

        print("Printing Dungeon Info...\n\n")
        print("NAME:  " + str(self.name))
        print("SIZE:  " + str(self.grid_size[0]) + "x" + str(self.grid_size[1]))
        print("ROOMS:  " + str(len(self.rooms)) + "\n\n")
        print("ROOM NAMES: ")
        for room in self.rooms:
            print(room.name)
        print("Player Location: " + str(self.pos_stairup))
        print("Monster Location: " + str(self.monster_locs))
        print("Item Location: " + str(self.item_locs))
        if grid:
            for row in self.grid:
                print(row)


    def generate_room(self, min_size, max_size):

        size_x = random.randint(min_size[0], max_size[0])
        size_y = random.randint(min_size[1], max_size[1])
        tiles = []

        for y in range(0, size_y):
            row = []
            for x in range(0, size_x):
                if x == 0 and y == 0:
                    row.append(2)
                elif x == size_x-1 and y == 0:
                    row.append(2)
                elif x == 0 and y == size_y-1:
                    row.append(2)
                elif x == size_x-1 and y == size_y-1:
                    row.append(2)
                elif y == 0:
                    row.append(3)
                elif x == size_x-1:
                    row.append(4)
                elif y == size_y-1:
                    row.append(5)
                elif x == 0:
                    row.append(6)
                else:
                    row.append(1)
            tiles.append(row)

        return Room((size_x, size_y), tiles)


    def get_branching_position(self):

        branching_room = random.choice(self.rooms)
        branching_tile_position = (0, 0)
        for i in range(0, branching_room.size[0] * branching_room.size[1]):

            x = random.randint(branching_room.position[0],
                               branching_room.position[0] + branching_room.size[0]-1)
            y = random.randint(branching_room.position[1],
                               branching_room.position[1] + branching_room.size[1]-1)

            if self.grid[y][x] > 2:
                branching_tile_position = (x, y)
                break

        return branching_tile_position


    def get_branching_direction(self, branching_position):

        direction = None
        if self.grid[branching_position[1]][branching_position[0]] == 3:
            direction = "NORTH"
        elif self.grid[branching_position[1]][branching_position[0]] == 4:
            direction = "EAST"
        elif self.grid[branching_position[1]][branching_position[0]] == 5:
            direction = "SOUTH"
        elif self.grid[branching_position[1]][branching_position[0]] == 6:
            direction = "WEST"
        else:
            return False

        return direction


    def space_for_new_room(self, new_room_size, new_room_position):

        for y in range(new_room_position[1],
                       new_room_position[1] + new_room_size[1]):
            for x in range(new_room_position[0],
                           new_room_position[0] + new_room_size[0]):
                if x < 0 or x > self.grid_size[0] - 1:
                    return False
                if y < 0 or y > self.grid_size[1] - 1:
                    return False
                if self.grid[y][x] != 0:
                    return False

        return True


    def place_room(self, room, gridposition):


        room.position = gridposition
        room_tile_x = 0
        room_tile_y = 0
        for y in range(gridposition[1], gridposition[1] + room.size[1]):
            for x in range(gridposition[0], gridposition[0] + room.size[0]):
                self.grid[y][x] = room.tiles[room_tile_y][room_tile_x]
                room_tile_x += 1
            room_tile_y += 1
            room_tile_x = 0


    def connect_rooms(self, branching_pos, direction):

        chance = random.randint(1, 5)
        # 1 chance out of 5 to get a door
        if chance == 5:
            self.grid[branching_pos[1]][branching_pos[0]] = 7
        else:
            self.grid[branching_pos[1]][branching_pos[0]] = 1

        if direction == "NORTH":
            self.grid[branching_pos[1]-1][branching_pos[0]] = 1
        elif direction == "EAST":
            self.grid[branching_pos[1]][branching_pos[0]+1] = 1
        elif direction == "SOUTH":
            self.grid[branching_pos[1]+1][branching_pos[0]] = 1
        elif direction == "WEST":
            self.grid[branching_pos[1]][branching_pos[0]-1] = 1


    def set_staircases(self):


        for i in range(0, len(self.rooms)):
            stairs_up_room = random.choice(self.rooms)
            x = int(stairs_up_room.position[0] + (stairs_up_room.size[0]/2))
            y = int(stairs_up_room.position[1] + (stairs_up_room.size[1]/2))
            if self.grid[y][x] == 1:
                self.grid[y][x] = 8
                self.pos_stairup = (x,y)
                break

        for i in range(0, len(self.rooms)):
            stairs_down_room = random.choice(self.rooms)
            x = int(stairs_down_room.position[0] + (stairs_down_room.size[0]/2))
            y = int(stairs_down_room.position[1] + (stairs_down_room.size[1]/2))
            if self.grid[y][x] == 1:
                self.grid[y][x] = 9
                self.pos_stairdown = (x,y)
                break


    def find_path_between_staircases(self):

        astar = Pathfinder()

        start = None
        end = None
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[0])):
                if self.grid[y][x] == 8:
                    start = (x, y)
                elif self.grid[y][x] == 9:
                    end = (x, y)
                if start != None and end != None:
                    break

        path = astar.find_path(self.grid, start, end, [0, 2, 3, 4, 5, 6, 7])

        if path != None:
            for i in range(0, len(path)-1):
                self.grid[path[i][1]][path[i][0]] = 11
        else:
            print("No path possible.")


    def generate_dungeon_map(self):

        self.rooms = []
        self.grid = []
        for y in range(0, self.grid_size[1]):
            row = []
            for x in range(0, self.grid_size[0]):
                row.append(0)
            self.grid.append(row)

        self.rooms.append(self.generate_room(self.min_room_size,
                                             self.max_room_size))

        self.place_room(self.rooms[-1],
                            (int(self.grid_size[0]/2 - (self.rooms[-1].size[0]/2)),
                             int(self.grid_size[1]/2 - (self.rooms[-1].size[1]/2))))

        for i in range(0, ((self.grid_size[0] * self.grid_size[1]) * 2)):

            if self.max_num_rooms != 0:
                if len(self.rooms) == self.max_num_rooms:
                    break

            branching_pos = self.get_branching_position()
            direction = self.get_branching_direction(branching_pos)
            if direction:

                new_room_pos = (0, 0)
                new_room = self.generate_room(self.min_room_size,
                                              self.max_room_size)

                if direction == "NORTH":
                    new_room_pos = (int(branching_pos[0] - (new_room.size[0]/2)),
                                    int(branching_pos[1] - new_room.size[1]))
                elif direction == "EAST":
                    new_room_pos = (int(branching_pos[0] + 1),
                                    int(branching_pos[1] - (new_room.size[1]/2)))
                elif direction == "SOUTH":
                    new_room_pos = (int(branching_pos[0] - (new_room.size[0]/2)),
                                    int(branching_pos[1] + 1))
                elif direction == "WEST":
                    new_room_pos = (int(branching_pos[0] - (new_room.size[0])),
                                    int(branching_pos[1] - (new_room.size[1]/2)))

                if self.space_for_new_room(new_room.size, new_room_pos):
                    self.place_room(new_room, new_room_pos)
                    self.rooms.append(new_room)
                    self.connect_rooms(branching_pos, direction)

                else:
                    i += 1


    def set_objects_monsters(self):

        map = distance_map(self.grid, [11], [0, 2, 3, 4, 5, 6, 7, 8, 9])
        distances = []

        for y in range(0, len(map)):
            for x in range(0, len(map[0])):
                if map[y][x] not in distances and map[y][x] != -1:
                    distances.append(map[y][x])

        average = 0
        for i in distances:
            average += i
        if len(distances) > 1:
            average /= len(distances)-1

        possible_places = []
        for y in range(0, len(map)):
            for x in range(0, len(map[0])):
                if map[y][x] >= average and (self.grid[y][x] == 1 or self.grid[y][x] > 9):
                    possible_places.append((x, y))

        for i in range(0, self.number_items):
            location = random.choice(possible_places)
            possible_places.remove(location)
            self.item_locs.append(location)

        for i in range(0, self.number_monsters):
            location = random.choice(possible_places)
            possible_places.remove(location)
            self.monster_locs.append(location)
        '''
        possible_places = []
        for y in range(0, GAME_NB_TILE_Y):
            for x in range(0, GAME_NB_TILE_X):
                if (self.grid[y][x] == 1 or self.grid[y][x] > 9):
                    possible_places.append((x, y))
        for i in range(0, self.number_items):
                location = random.choice(possible_places)
                possible_places.remove(location)
                self.item_locs.append(location)
        for i in range(0, self.number_monsters):
                location = random.choice(possible_places)
                possible_places.remove(location)
                self.monster_locs.append(location)
    '''

    def generate_dungeon(self):

        print("\n\n* Generating dungeon...")
        start = time.time()
        self.generate_dungeon_map()
        end = time.time()
        print("  DONE!   in " + str(round(end-start, 3)) + " seconds")

        print("* Setting staircases...")
        start = time.time()
        self.set_staircases()
        end = time.time()
        print ("  DONE!   in " + str(round(end-start, 3)) + " seconds")

        print("* Finding path...")
        start = time.time()
        self.find_path_between_staircases()
        end = time.time()
        print("        DONE!   in " + str(round(end-start, 3)) + " seconds")

        print("* Setting objects...")
        start = time.time()
        self.set_objects_monsters()
        end = time.time()
        print("      DONE!   in " + str(round(end-start, 3)) + " seconds")

        print("* Setting tiles...")
        start = time.time()
        self.generate_tile_representation()
        end = time.time()
        print("      DONE!   in " + str(round(end-start, 3)) + " seconds")

    def generate_tile_representation(self):
        '''
        Build in graphical tile array a representation where all walls
        are replaced with their type and numerical layout. Result is placed in tileset
        object.
        Original
            0 = blank space (non-useable)
            1 = floor tile (walkable)
            2 = corner tile (non-useable)
            3 = wall tile facing NORTH.
            4 = wall tile facing EAST.
            5 = wall tile facing SOUTH.
            6 = wall tile facing WEST.
            7 = door tile.
        TODO!

        '''
        # We start by initializing all the tileset
        for y in range(0, self.grid_size[1]):
            rowtile = []
            for x in range(0, self.grid_size[0]):
                rowtile.append(Tile(x,y))
            self.tileset.append(rowtile)

        # Now we iterate over the rooms
        indexcollection=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        index = -1
        for room in self.rooms:
            index += 1
            for y in range(room.position[1], room.position[1] + room.size[1]):
                for x in range(room.position[0], room.position[0] + room.size[0]):
                    if self.grid[y][x] == 1 or self.grid[y][x] > 7:
                        self.tileset[y][x] = Tile(x,y, index, "FLOOR")
                    else:
                        tileIndex = self.buildTileIndex(x,y)
                        indexcollection[tileIndex] += 1
                        if self.grid[y][x] == 7:
                            self.tileset[y][x] = Tile(x,y, index, "DOOR", tileIndex)
                        else:
                            self.tileset[y][x] = Tile(x,y, index, "WALL", tileIndex)

        print(indexcollection)
    def getTileAt(self, x, y):
        return self.tileset[y][x]

    def drawTile(self, x, y, forcemode = False):
        self.tileset[y][x].draw(forcemode)


    def draw(self):
        for y in range(0, len(self.tileset)):
            for x in range(0, len(self.tileset[0])):
                self.tileset[y][x].draw()

    def buildTileIndex(self, x, y):
        '''
        this uses the http://www.angryfishstudios.com/2011/04/adventures-in-bitmasking/ method
        '''
        # By default all is a floor around, check if there are walls
        up = down = right = left = 0
        if x == 0 or self.grid[y][x-1] in (0,2,3,4,5,6,7):
            left = 1
        if x == self.grid_size[0]-1 or self.grid[y][x+1] in (0,2,3,4,5,6,7):
            right = 1
        if y == 0 or self.grid[y-1][x] in (0,2,3,4,5,6,7):
            up = 1
        if y == self.grid_size[1]-1 or self.grid[y+1][x] in (0,2,3,4,5,6,7):
            down = 1
        return left * 8 + down * 4 + right * 2 + up

    def getRoomOfTile(self, x, y):
        '''
        return the room object that this tile belongs to, None if no room is referenced
        '''
        if self.tileset[y][x].roomIndex != None:
            return self.rooms[self.tileset[y][x].roomIndex]
        return None

    def computeFogOfWar(self, x, y, radius = GAME_FOG_RADIUS):
        '''
        compute the fog of war taking as a source the x,y space
        very simple to start with: illuminate the whole room :-)
        '''

        dirtytilelist = []
        # First we add teh current tile :-)
        self.getTileAt(x,y).setVisible()
        dirtytilelist.append(self.getTileAt(x,y))

        # And we go through the room
        room = self.getRoomOfTile(x,y)
        for xpos in range(room.position[0], room.position[0] + room.size[0]):
            for ypos in range(room.position[1], room.position[1] + room.size[1]):
                self.getTileAt(xpos,ypos).setVisible()
                dirtytilelist.append(self.getTileAt(xpos,ypos))

        connectionList = []
        # examine around the room
        for xvar in range(0, room.size[0]-1):
            if self.grid[room.position[1]+0][room.position[0]+xvar] in (1,7):
                # NORTH
                connectionList.append((room.position[0]+xvar, room.position[1]-2))
            if self.grid[room.position[1]+room.size[1]-1][room.position[0]+xvar] in (1,7):
                # SOUTH
                connectionList.append((room.position[0]+xvar, room.position[1]+room.size[1]+2))

        for yvar in range(0, room.size[1]-1):
            if self.grid[room.position[1]+yvar][room.position[0]+0] in (1,7):
                connectionList.append((room.position[0]-2, room.position[1]+yvar))
            if self.grid[room.position[1]+yvar][room.position[0]+room.size[0]-1] in (1,7):
                connectionList.append((room.position[0]+room.size[0]+2, room.position[1]+yvar))

        #Now we go through the nearby rooms, and we flag tehm as explored
        for neighborLoc in connectionList:
            neighborRoom = self.getRoomOfTile(neighborLoc[0], neighborLoc[1])
           # print("Evaluating room: "+neighborRoom.name)
            for xpos in range(neighborRoom.position[0], neighborRoom.position[0] + neighborRoom.size[0]):
                for ypos in range(neighborRoom.position[1], neighborRoom.position[1] + neighborRoom.size[1]):
                    if not self.getTileAt(xpos,ypos).isExplored():
                        self.getTileAt(xpos,ypos).setExplored()
                        dirtytilelist.append(self.getTileAt(xpos,ypos))

        for dirtytile in dirtytilelist:
            dirtytile.draw()


    def reinitFogOfWar(self, x, y, radius = GAME_FOG_RADIUS):
        '''
        compute the fog of war taking as a source the x,y space
        very simple to start with: illuminate the whole room :-)
        '''
        dirtytilelist = []
        # First we add teh current tile :-)
        self.getTileAt(x,y).removeVisible()
        dirtytilelist.append(self.getTileAt(x,y))

        # And we go through the room
        room = self.getRoomOfTile(x,y)
        for xpos in range(room.position[0], room.position[0] + room.size[0]):
            for ypos in range(room.position[1], room.position[1] + room.size[1]):
                self.getTileAt(xpos,ypos).removeVisible()
                dirtytilelist.append(self.getTileAt(xpos,ypos))

        for dirtytile in dirtytilelist:
            dirtytile.draw()

    def tileExist(self, x, y):
        return (y<len(self.tileset) and x<len(self.tileset[y]))


class Tile:
    '''
    A tile can either be a floor, a wall or a door.
    It is positionned at an x,y position and is part of a room (for floor).
    The tileIndex is used as an additional property to derive a graphical
    representation. RoomIndex is the room number in the global dungeon list.

    It can be visible by the player if it is in his current light of sight.
    It can be explored if teh player has already seen it. It will remain explored
    for the whole level.
    '''

    graphicInitialized = False

    @staticmethod
    def initializeGraphics():
        '''
        Notes about the picture: each tile is 32x32
        Walls are located in picture at (160,288). They follow teh same representation as the numerical pad
        '''
        # Load the main surface

        goodImage = pygame.image.load('resources/images/TileA6.png').convert()
        darkImage = pygame.image.load('resources/images/TileA5.png').convert()

        floorindex = random.randint(0,4)

        Tile.IMG_Floor = goodImage.subsurface((floorindex*32,192,32,32)).copy()
        Tile.IMG_Floor_NotVisited = goodImage.subsurface((0,0,32,32)).copy()
        Tile.IMG_Floor_Explored = darkImage.subsurface((floorindex*32,192,32,32)).copy()

        mainImage1 = pygame.image.load('resources/images/testownwall.png').convert_alpha()
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
        mainImage2 = pygame.image.load('resources/images/testownwall2.png').convert_alpha()
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
        mainImage3 = pygame.image.load('resources/images/testownwall3.png').convert_alpha()
        Tile.IMG_WALL3 = {
        0 :mainImage3.subsurface((0,0,32,32)).copy(),
        1 :mainImage3.subsurface((64,0,32,32)).copy(),
        2 :mainImage3.subsurface((128,0,32,32)).copy(),
        3 :mainImage3.subsurface((192,0,32,32)).copy(),
        4 :mainImage3.subsurface((0,64,32,32)).copy(),
        5 :mainImage3.subsurface((64,64,32,32)).copy(),
        6 :mainImage3.subsurface((128,64,32,32)).copy(),
        7 :mainImage3.subsurface((192,64,32,32)).copy(),
        8 :mainImage3.subsurface((0,128,32,32)).copy(),
        9 :mainImage3.subsurface((64,128,32,32)).copy(),
        10:mainImage3.subsurface((128,128,32,32)).copy(),
        11:mainImage3.subsurface((192,128,32,32)).copy(),
        12:mainImage3.subsurface((0,192,32,32)).copy(),
        13:mainImage3.subsurface((64,192,32,32)).copy(),
        14:mainImage3.subsurface((128,192,32,32)).copy(),
        15:mainImage3.subsurface((192,192,32,32)).copy(),
        }

        doorsImage = pygame.image.load('resources/images/doors.png').convert_alpha()
        Tile.IMG_DOOR = {
        0 :doorsImage.subsurface((0,0,32,32)).copy(),
        1 :doorsImage.subsurface((64,0,32,32)).copy(),
        2 :doorsImage.subsurface((0,64,32,32)).copy(),
        3 :doorsImage.subsurface((64,64,32,32)).copy()
        }


    #a tile of the map and its properties
    def __init__(self, x=0, y=0, roomIndex=None, tileType=None, tileIndex = -1):
        self.x = x
        self.y = y
        self.roomIndex = roomIndex
        self.tileType = tileType
        self.tileIndex = tileIndex

        self.blocked = False
        self.block_sight = False

        if self.tileType == 'WALL':
            self.blocked = True
            self.block_sight = True

        self.explored = self.currentlyVisible = False

        self.visibleImage = None # Regular image
        self.exploredImage= None # Image after exploration
        self.initGraphics()

    def initGraphics(self):
        if not Tile.graphicInitialized:
            Tile.initializeGraphics()
            Tile.graphicInitialized = True


    def isVisible(self):
        return self.currentlyVisible

    def isExplored(self):
        return self.explored

    def setExplored(self):
        self.explored = True

    def setVisible(self):
        self.currentlyVisible = True
        self.explored = True

    def removeVisible(self):
        self.currentlyVisible = False

    def draw(self, forcemode = False):
        tiletopx = self.x * IMG_SIZE_TILE_X
        tiletopy = self.y * IMG_SIZE_TILE_Y


        if self.tileType == None or not self.explored:
            GameGlobals.entireWindowSurface.fill(COLOR_BLACK, (tiletopx,tiletopy, IMG_SIZE_TILE_X, IMG_SIZE_TILE_Y))
        elif self.currentlyVisible:
            if forcemode or self.visibleImage == None:
                # initialize the image
                self.visibleImage = Tile.IMG_Floor.copy()
                if self.tileType == 'WALL' and self.tileIndex >= 0:
                    rand = random.randrange(3)
                    if rand == 0:
                        self.visibleImage.blit(Tile.IMG_WALL1[self.tileIndex], (0,0))
                    elif rand == 1:
                        self.visibleImage.blit(Tile.IMG_WALL2[self.tileIndex], (0,0))
                    else:
                        self.visibleImage.blit(Tile.IMG_WALL3[self.tileIndex], (0,0))
                elif self.tileType == 'DOOR' and (self.tileIndex == 1 or self.tileIndex == 4 or self.tileIndex == 5):
                    self.visibleImage.blit(Tile.IMG_DOOR[0], (0,0))
                elif self.tileType == 'DOOR':
                    self.visibleImage.blit(Tile.IMG_DOOR[1], (0,0))
            GameGlobals.entireWindowSurface.blit(self.visibleImage, (tiletopx,tiletopy))
        else:
            if forcemode or self.exploredImage == None:
                # initialize the image
                self.exploredImage = Tile.IMG_Floor_Explored.copy()
                if self.tileType == 'WALL' and self.tileIndex >= 0:
                    rand = random.randrange(3)
                    if rand == 0:
                        self.exploredImage.blit(Tile.IMG_WALL1[self.tileIndex], (0,0))
                    elif rand == 1:
                        self.exploredImage.blit(Tile.IMG_WALL2[self.tileIndex], (0,0))
                    else:
                        self.exploredImage.blit(Tile.IMG_WALL3[self.tileIndex], (0,0))
                elif self.tileType == 'DOOR' and (self.tileIndex == 1 or self.tileIndex == 4 or self.tileIndex == 5):
                    self.exploredImage.blit(Tile.IMG_DOOR[2], (0,0))
                elif self.tileType == 'DOOR':
                    self.exploredImage.blit(Tile.IMG_DOOR[3], (0,0))
            GameGlobals.entireWindowSurface.blit(self.exploredImage, (tiletopx,tiletopy))



def main():
    myDungeon = Dungeon((25,25),"Level -1",8,(4,4),(8,9),5,7)
    myDungeon.generate_dungeon()
    myDungeon.print_info(False)


    # System Init

    entireWindowSurface

    pygame.init()
    mainClock = pygame.time.Clock()
    GameGlobals.entireWindowSurface = pygame.display.set_mode((DISP_GAME_WIDTH,DISP_GAME_HEIGHT))
    GameGlobals.entireWindowSurface.fill(COLOR_BLACK)
    pygame.display.set_caption('Orange Lord Game v0.4')
    myDungeon.generate_tile_representation()
    myDungeon.draw()

    # run the game loop
    while True:
        # Prepare drawing

        pygame.display.update()
        mainClock.tick(40)

if __name__ == '__main__':
    main()
