from room import Room
from player import Player
from world import World
import random
from ast import literal_eval


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

    def tail(self):
        return self.stack[-1]


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = []

# {
#   0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}],
#   1: [(3, 6), {'s': 0, 'n': 2, 'e': 12, 'w': 15}],
#   2: [(3, 7), {'s': 1}],
#   3: [(4, 5), {'w': 0, 'e': 4}],
#   4: [(5, 5), {'w': 3}],
#   5: [(3, 4), {'n': 0, 's': 6}],
#   6: [(3, 3), {'n': 5, 'w': 11}],
#   7: [(2, 5), {'w': 8, 'e': 0}],
#   8: [(1, 5), {'e': 7}],
#   9: [(1, 4), {'n': 8, 's': 10}],
#   10: [(1, 3), {'n': 9, 'e': 11}],
#   11: [(2, 3), {'w': 10, 'e': 6}],
#   12: [(4, 6), {'w': 1, 'e': 13}],
#   13: [(5, 6), {'w': 12, 'n': 14}],
#   14: [(5, 7), {'s': 13}],
#   15: [(2, 6), {'e': 1, 'w': 16}],
#   16: [(1, 6), {'n': 17, 'e': 15}],
#   17: [(1, 7), {'s': 16}]
# }
# Fill this out with directions to walk
# traversal_path = ['n', 'n', 's', 's', 'w']
traversal_path = []
path_direction = []
path_room_number = []
reverse_path = []
s = Stack()
visited = set()
visited.add(0)
reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
s.push((0,))


def check_if_neighbors_in_visited(room_dict):
    count = 0
    for direction, room_id in room_dict.items():
        if room_id in visited:
            count += 1
    if len(room_dict) == count:
        return True
    else:
        return False


while len(room_graph) != len(visited):
    current_room = s.pop()
    visited.add(current_room[0])
    if len(current_room) == 2:
        path_direction.append(current_room[1])
        path_room_number.append(current_room[0])
    neighbors = room_graph[current_room[0]][1]
    count = 0
    for direction, room_id in neighbors.items():
        if room_id not in visited:
            s.push((room_id, direction))
        else:
            count += 1
    if count == len(neighbors):
        result = True
        count = len(path_direction) - 1
        while result:
            neighbors = room_graph[path_room_number[count]][1]
            result = check_if_neighbors_in_visited(neighbors)
            if count < 0:
                result = False
            elif result is True:
                reverse_path.append(reverse[path_direction[count]])
                count -= 1
        traversal_path = traversal_path + path_direction + reverse_path
        path_direction = []
        reverse_path = []
        path_room_number = []
        # for direction in path_direction:
        #     temp = reverse[direction]
        #     reverse_path.insert(0, temp)
        # traversal_path = traversal_path + path_direction + reverse_path
        # path_direction = []
        # reverse_path = []

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
