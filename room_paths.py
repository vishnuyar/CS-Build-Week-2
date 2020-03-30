import ast
import json
from util import Stack,Queue

def path_to_current_room(oldroom,newroom,room_dict):
    paths = []
    visited = set()
    bft_queue = Queue()
    direction_queue = Queue()
    direction_queue.enqueue([None])
    bft_queue.enqueue([oldroom])
    while bft_queue.size() > 0:
        vertex_path = bft_queue.dequeue()
        direction_path = direction_queue.dequeue()
        vertex = vertex_path[-1]
        if vertex not in visited:
            visited.add(vertex)
            if vertex == newroom:
                return vertex_path,direction_path
            if vertex in room_dict.keys():
                for direction in room_dict[vertex]['exits']:
                    if room_dict[vertex][direction] is not None:
                        path_copy = vertex_path.copy()
                        direction_copy = direction_path.copy()
                        room_no = room_dict[vertex][direction]
                        path_copy.append(room_no)
                        direction_copy.append(direction)
                        direction_queue.enqueue(direction_copy)
                        bft_queue.enqueue(path_copy) 


with open('room_dict (copy).txt') as room_data:
    for line in room_data:
       room_dict = ast.literal_eval(line)
    #print(room_dict)

#print(room_dict[28])

#print(room_dict[397])


room_from,room_to = input("From room -  To room with one space ").split()
print(f'path from {room_from} to {room_to} {path_to_current_room(int(room_from),int(room_to),room_dict)}')
