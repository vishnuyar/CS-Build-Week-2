import requests
import json
from datetime import datetime
from util import Stack
import csv
import time
from util import Queue


TOKEN = "46b1a83c354572a2b13401760d72e76bf5143cc2"
HOST = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"

GAME_INIT_get = HOST+'init/'
MOVEMENT = HOST+'move/'

visit_list = []
room_dict = {}

opposites = {'n':'s','s':'n','w':'e','e':'w'}

headers = {"Authorization":f"Token {TOKEN}"}
r = requests.get(GAME_INIT_get, headers=headers)
start_time = datetime.now()
print(r.status_code)
response = json.loads(r.text)
print('init',response)
cooldown = response['cooldown']



def get_room_details(direction,cooldown):
    time.sleep(cooldown+1)
    data_direction = {}
    data_direction['direction'] = direction
    data = json.dumps(data_direction)
    #print("data",data)
    r = requests.post(MOVEMENT, data=data, headers=headers)
    print('get room',r.text)
    room_details = json.loads(r.text)
    return room_details

def move_known_room(direction,room_no,cooldown):
    time.sleep(cooldown+1)
    data_direction = {}
    data_direction['direction'] = direction
    data_direction['next_room_id'] = str(room_no)
    data = json.dumps(data_direction)
    print('move room data',data)
    r = requests.post(MOVEMENT,data=data, headers=headers)
    #print('move room',r.text)
    room_details = json.loads(r.text)
    return room_details['room_id'],room_details['cooldown']


def visit_current_room(rooms,directions,cooldown):
    for i in range(1,len(directions)):
        room_no, cooldown = move_known_room(directions[i],rooms[i],cooldown)
        print(f'In room:{room_no}')


def add_directions_dict(room):
    for direction in room['exits']:
        room[direction] = None
    return room

def assign_direction(room_a,room_b,direction):
    room_dict[room_a][direction] = room_b
    room_dict[room_b][opposites[direction]] = room_a

def path_to_current_room(oldroom,newroom):
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
                    path_copy = vertex_path.copy()
                    direction_copy = direction_path.copy()
                    room_no = room_dict[vertex][direction]
                    path_copy.append(room_no)
                    direction_copy.append(direction)
                    direction_queue.enqueue(direction_copy)
                    bft_queue.enqueue(path_copy)

#Doing a breadth first traversal
visited = []
room_dict = {}
room_queue = Queue()
room_no = response['room_id']
previous_room = None
#create directions for response received
room = add_directions_dict(response)
#Add the response to the room dictionary
room_dict[room_no] = room
room_queue.enqueue(room_no)
while room_queue.size() > 0:
    room_no = room_queue.dequeue()
    if room_no not in visited:
        visited.append(room_no)
        print('Room in visited',room_no)
        if previous_room:
            #get direction to move from previous room to current room
            rooms_list,direction_list = path_to_current_room(previous_room,room_no)
            print(f'rooms list:{rooms_list}')
            print(f'directions list:{direction_list}')
            visit_current_room(rooms_list,direction_list,cooldown)

        #check if all the directions have been visited
        for direction in room_dict[room_no]['exits']:
            if direction in room_dict[room_no].keys():
                if room_dict[room_no][direction] is None:
                    #go to the direction get the room details
                    room_details = get_room_details(direction,cooldown)
                    #add directions to room details
                    room = add_directions_dict(room_details)
                    new_room_no = room['room_id']
                    #add this room to the room dict
                    room_dict[new_room_no] = room
                    #assign directions to rooms
                    assign_direction(room_no,new_room_no,direction)
                    #add the room to the queue
                    room_queue.enqueue(new_room_no)
                    #go back to previous room
                    previous_room,cooldown = move_known_room(opposites[direction],room_no,room['cooldown'])
        #write to file
        with open('room_graphs.txt','a+') as room_file:
            room_file.write(str(room_dict[room_no]))
            room_file.write("\n")