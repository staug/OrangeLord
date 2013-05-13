class Node:


    def __init__(self, pos, parent, walkable):

        self.f_score = 0
        self.g_score = 0
        self.h_score = 0

        self.position = pos
        self.parent = parent
        self.walkable = walkable


    def calc_f_score(self):

        self.f_score = self.g_score + self.h_score


    def calc_g_score(self, diagonal=False):

        if not diagonal:
            self.g_score = self.parent.g_score + 10
        else:
            self.g_score = self.parent.g_score + 14


    def calc_h_score(self, end_node):

        a = self.position[0] - end_node.position[0]
        if a < 0:
            a *= -1

        b = self.position[1] - end_node.position[1]
        if b < 0:
            b *= -1

        self.h_score = (a + b) * 10





class Pathfinder:


    def __init__(self):

        self.nodes = []
        self.open_list = set()
        self.closed_list = set()
        self.path = []

        self.start_node = None
        self.end_node = None


    def setup(self, map, unwalkable_tile_ids):

        for y in range(0, len(map)):
            row = []
            for x in range(0, len(map[0])):
                if map[y][x] in unwalkable_tile_ids:
                    row.append(Node((x, y), None, False))
                else:
                    row.append(Node((x, y), None, True))
            self.nodes.append(row)


    def update_node_scores(self, node, end_node, diagonal=False):

        node.calc_g_score(diagonal)
        node.calc_h_score(end_node)
        node.calc_f_score()


    def check_around_node(self, current_node):

        #check right
        check = (current_node.position[0]+1, current_node.position[1])
        if check[0] >= 0 and check[0] < len(self.nodes[0]) and check[1] >= 0 and check[1] < len(self.nodes):
            if check == self.end_node.position:
                return 0
            elif check == self.start_node.position:
                pass
            elif self.nodes[check[1]][check[0]] in self.open_list:
                if current_node.g_score + 10 < self.nodes[check[1]][check[0]].g_score:
                    self.nodes[check[1]][check[0]].parent = current_node
                    self.update_node_scores(self.nodes[check[1]][check[0]],
                                            self.end_node, False)
            elif self.nodes[check[1]][check[0]] in self.closed_list:
                pass
            elif self.nodes[check[1]][check[0]].walkable:
                self.open_list.add(self.nodes[check[1]][check[0]])
                self.nodes[check[1]][check[0]].parent = current_node
                self.update_node_scores(self.nodes[check[1]][check[0]],
                                        self.end_node, False)

        #check left
        check = (current_node.position[0]-1, current_node.position[1])
        if check[0] >= 0 and check[0] < len(self.nodes[0]) and check[1] >= 0 and check[1] < len(self.nodes):
            if check == self.end_node.position:
                return 0
            elif check == self.start_node.position:
                pass
            elif self.nodes[check[1]][check[0]] in self.open_list:
                if current_node.g_score + 10 < self.nodes[check[1]][check[0]].g_score:
                    self.nodes[check[1]][check[0]].parent = current_node
                    self.update_node_scores(self.nodes[check[1]][check[0]],
                                            self.end_node, False)
            elif self.nodes[check[1]][check[0]] in self.closed_list:
                pass
            elif self.nodes[check[1]][check[0]].walkable:
                self.open_list.add(self.nodes[check[1]][check[0]])
                self.nodes[check[1]][check[0]].parent = current_node
                self.update_node_scores(self.nodes[check[1]][check[0]],
                                        self.end_node, False)

        #check south
        check = (current_node.position[0], current_node.position[1]+1)
        if check[0] >= 0 and check[0] < len(self.nodes[0]) and check[1] >= 0 and check[1] < len(self.nodes):
            if check == self.end_node.position:
                return 0
            elif check == self.start_node.position:
                pass
            elif self.nodes[check[1]][check[0]] in self.open_list:
                if current_node.g_score + 10 < self.nodes[check[1]][check[0]].g_score:
                    self.nodes[check[1]][check[0]].parent = current_node
                    self.update_node_scores(self.nodes[check[1]][check[0]],
                                            self.end_node, False)
            elif self.nodes[check[1]][check[0]] in self.closed_list:
                pass
            elif self.nodes[check[1]][check[0]].walkable:
                self.open_list.add(self.nodes[check[1]][check[0]])
                self.nodes[check[1]][check[0]].parent = current_node
                self.update_node_scores(self.nodes[check[1]][check[0]],
                                        self.end_node, False)

        #check north
        check = (current_node.position[0], current_node.position[1]-1)
        if check[0] >= 0 and check[0] < len(self.nodes[0]) and check[1] >= 0 and check[1] < len(self.nodes):
            if check == self.end_node.position:
                return 0
            elif check == self.start_node.position:
                pass
            elif self.nodes[check[1]][check[0]] in self.open_list:
                if current_node.g_score + 10 < self.nodes[check[1]][check[0]].g_score:
                    self.nodes[check[1]][check[0]].parent = current_node
                    self.update_node_scores(self.nodes[check[1]][check[0]],
                                            self.end_node, False)
            elif self.nodes[check[1]][check[0]] in self.closed_list:
                pass
            elif self.nodes[check[1]][check[0]].walkable:
                self.open_list.add(self.nodes[check[1]][check[0]])
                self.nodes[check[1]][check[0]].parent = current_node
                self.update_node_scores(self.nodes[check[1]][check[0]],
                                        self.end_node, False)

        #check topright
        check = (current_node.position[0]+1, current_node.position[1]-1)
        if check[0] >= 0 and check[0] < len(self.nodes[0]) and check[1] >= 0 and check[1] < len(self.nodes):
            if check == self.end_node.position:
                return 0
            elif check == self.start_node.position:
                pass
            elif self.nodes[check[1]][check[0]] in self.open_list:
                if current_node.g_score + 14 < self.nodes[check[1]][check[0]].g_score:
                    self.nodes[check[1]][check[0]].parent = current_node
                    self.update_node_scores(self.nodes[check[1]][check[0]],
                                            self.end_node, False)
            elif self.nodes[check[1]][check[0]] in self.closed_list:
                pass
            elif self.nodes[check[1]][check[0]].walkable:
                self.open_list.add(self.nodes[check[1]][check[0]])
                self.nodes[check[1]][check[0]].parent = current_node
                self.update_node_scores(self.nodes[check[1]][check[0]],
                                        self.end_node, True)

        #check topleft
        check = (current_node.position[0]-1, current_node.position[1]-1)
        if check[0] >= 0 and check[0] < len(self.nodes[0]) and check[1] >= 0 and check[1] < len(self.nodes):
            if check == self.end_node.position:
                return 0
            elif check == self.start_node.position:
                pass
            elif self.nodes[check[1]][check[0]] in self.open_list:
                if current_node.g_score + 14 < self.nodes[check[1]][check[0]].g_score:
                    self.nodes[check[1]][check[0]].parent = current_node
                    self.update_node_scores(self.nodes[check[1]][check[0]],
                                            self.end_node, False)
            elif self.nodes[check[1]][check[0]] in self.closed_list:
                pass
            elif self.nodes[check[1]][check[0]].walkable:
                self.open_list.add(self.nodes[check[1]][check[0]])
                self.nodes[check[1]][check[0]].parent = current_node
                self.update_node_scores(self.nodes[check[1]][check[0]],
                                        self.end_node, True)

        #check bottomright
        check = (current_node.position[0]+1, current_node.position[1]+1)
        if check[0] >= 0 and check[0] < len(self.nodes[0]) and check[1] >= 0 and check[1] < len(self.nodes):
            if check == self.end_node.position:
                return 0
            elif check == self.start_node.position:
                pass
            elif self.nodes[check[1]][check[0]] in self.open_list:
                if current_node.g_score + 14 < self.nodes[check[1]][check[0]].g_score:
                    self.nodes[check[1]][check[0]].parent = current_node
                    self.update_node_scores(self.nodes[check[1]][check[0]],
                                            self.end_node, False)
            elif self.nodes[check[1]][check[0]] in self.closed_list:
                pass
            elif self.nodes[check[1]][check[0]].walkable:
                self.open_list.add(self.nodes[check[1]][check[0]])
                self.nodes[check[1]][check[0]].parent = current_node
                self.update_node_scores(self.nodes[check[1]][check[0]],
                                        self.end_node, True)

        #check bottomleft
        check = (current_node.position[0]-1, current_node.position[1]+1)
        if check[0] >= 0 and check[0] < len(self.nodes[0]) and check[1] >= 0 and check[1] < len(self.nodes):
            if check == self.end_node.position:
                return 0
            elif check == self.start_node.position:
                pass
            elif self.nodes[check[1]][check[0]] in self.open_list:
                if current_node.g_score + 14 < self.nodes[check[1]][check[0]].g_score:
                    self.nodes[check[1]][check[0]].parent = current_node
                    self.update_node_scores(self.nodes[check[1]][check[0]],
                                            self.end_node, False)
            elif self.nodes[check[1]][check[0]] in self.closed_list:
                pass
            elif self.nodes[check[1]][check[0]].walkable:
                self.open_list.add(self.nodes[check[1]][check[0]])
                self.nodes[check[1]][check[0]].parent = current_node
                self.update_node_scores(self.nodes[check[1]][check[0]],
                                        self.end_node, True)


    def find_path(self, map, start_pos, end_pos, unwalkable_tile_ids):

        self.nodes = []
        self.open_list = set()
        self.closed_list = set()
        self.path = []

        if start_pos == None or end_pos == None:
            print("\n***Start/End node error***\n")
            return []

        self.setup(map, unwalkable_tile_ids)
        self.start_node = self.nodes[start_pos[1]][start_pos[0]]
        self.end_node = self.nodes[end_pos[1]][end_pos[0]]

        self.open_list.add(self.start_node)

        while self.open_list:

            current_node = sorted(self.open_list, key=lambda x:x.f_score)[0]

            if self.check_around_node(current_node) == 0:
                self.open_list.remove(current_node)
                self.closed_list.add(current_node)
                break

            else:
                self.open_list.remove(current_node)
                self.closed_list.add(current_node)

        if len(self.open_list) > 0:
            self.end_node.parent = current_node
            self.closed_list.add(self.end_node)
            current_node = self.end_node

            while 1:
                if current_node.parent != None:
                    self.path.append(current_node.position)
                    current_node = current_node.parent
                else:
                    break

            self.path.reverse()

        return self.path



    def dump_nodes_info(self):

        nodes = []

        for i in self.open_list:
            info = []
            info.append(i.position)
            info.append(i.f_score)
            info.append(i.g_score)
            info.append(i.h_score)
            nodes.append(info)

        for i in self.closed_list:
            info = []
            info.append(i.position)
            info.append(i.f_score)
            info.append(i.g_score)
            info.append(i.h_score)
            nodes.append(info)

        return nodes
