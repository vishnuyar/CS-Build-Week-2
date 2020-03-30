import json
import ast
import requests
import json
from datetime import datetime
from util import Stack
import csv
import time
from util import Queue


room_dict = {}
visited = []
with open('room_graphs (copy).txt') as room_data:
    for line in room_data:
       room_data = ast.literal_eval(line)
       room_no = room_data['room_id']
       visited.append(room_no)
print(f'Number of Visited Rooms:{len(visited)}')


with open('room_dict (copy).txt') as room_data:
    for line in room_data:
       room_dict = ast.literal_eval(line)
    #print(room_dict)

with open('room_queue (copy).txt') as room_data:
    for line in room_data:
       room_queue = ast.literal_eval(line)
print(f'Rooms in queue:{len(room_queue)}')


TOKEN = "46b1a83c354572a2b13401760d72e76bf5143cc2"
HOST = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"

GAME_INIT_get = HOST+'init/'
MOVEMENT = HOST+'move/'
DASH = HOST + 'dash/'

opposites = {'n':'s','s':'n','w':'e','e':'w'}

headers = {"Authorization":f"Token {TOKEN}"}
# r = requests.get(GAME_INIT_get, headers=headers)
# start_time = datetime.now()
# print(r.status_code)
# response = json.loads(r.text)
# print('init',response)
# cooldown = response['cooldown']



def get_room_details(direction,cooldown):
    time.sleep(cooldown+1)
    data_direction = {}
    data_direction['direction'] = direction
    data = json.dumps(data_direction)
    r = requests.post(MOVEMENT, data=data, headers=headers)
    room_details = json.loads(r.text)
    print(room_details)
    print(f'moving {direction} got {room_details["room_id"]}')
    return room_details

def move_known_room(direction,room_no,cooldown):
    time.sleep(cooldown+1)
    data_direction = {}
    data_direction['direction'] = direction
    data_direction['next_room_id'] = str(room_no)
    data = json.dumps(data_direction)
    r = requests.post(MOVEMENT,data=data, headers=headers)
    room_details = json.loads(r.text)
    
    print(f'moved {direction} to room {room_details["room_id"]}')
    return room_details['room_id'],room_details['cooldown']

def get_dash_results(moving_list):
    result_list = []
    current = moving_list[0]
    count = 0
    for value in moving_list:
        if value == current:
            count += 1
        else:
            result_list.append((current, count))
            current = value
            count = 1
    result_list.append((current, count))
    return result_list

def move_dash_rooms(direction,no_rooms,rooms_list,cooldown):
    time.sleep(cooldown+1)
    data_direction = {"direction":direction, "num_rooms":str(no_rooms), "next_room_ids":str(rooms_list)}
    data = json.dumps(data_direction)
    r = requests.post(DASH,data=data, headers=headers)
    room_details = json.loads(r.text)
    print(f'dash moved {direction} to room {room_details["room_id"]}')
    return room_details['room_id'],room_details['cooldown']        


def dash_current_room(rooms,directions,cooldown):
    dash_results = get_dash_results(directions)
    i=0
    for result in dash_results:
        direction, number = result
        if number == 1:
            room_no,cooldown = move_known_room(direction,rooms[i],cooldown)
            i += 1
        else:
            room_no,cooldown = move_dash_rooms(direction,number,rooms[i:i+number],cooldown)
            i += number
    return room_no, cooldown

def visit_current_room(rooms,directions,cooldown):
    for i in range(len(directions)):
        room_no, cooldown = move_known_room(directions[i],rooms[i],cooldown)
        print(f'In room:{room_no}')
    return room_no, cooldown

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

#Start traversal from where it was left off

# room_no = response['room_id']

#Always change based on where it stopped
previous_room = 37
#create directions for response received
#room = add_directions_dict(response)
#Add the response to the room dictionary
# room_dict[room_no] = room
# room_queue.append(room_no)
cooldown = 10
while len(room_queue) > 0:
    room_no = room_queue.pop()
    if room_no not in visited:
        visited.append(room_no)
        print('Room in visited',room_no)
        if previous_room:
            if previous_room != room_no:
                #get direction to move from previous room to current room
                rooms_list,direction_list = path_to_current_room(previous_room,room_no)
                
                #removing the first items from both
                rooms_list.pop(0)
                direction_list.pop(0)
                print(f'rooms list:{rooms_list}')
                print(f'directions list:{direction_list}')
                #Move to the current room
                previous_room,cooldown = visit_current_room(rooms_list,direction_list,cooldown)

        #Get only the directions to be visited
        visit_directions = []
        for direction in room_dict[room_no]['exits']:
            if room_dict[room_no][direction] is None:
                visit_directions.append(direction)
        total_d = len(visit_directions)
        for i,direction in enumerate(visit_directions):
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
            room_queue.append(new_room_no)
            #go back to previous room only if it is not the last room
            if i <  (total_d - 1):
                previous_room,cooldown = move_known_room(opposites[direction],room_no,room['cooldown'])
            else:
                previous_room = new_room_no
                cooldown = 15
        #write to file
        with open('room_graphs.txt','a+') as room_file:
            room_file.write(str(room_dict[room_no]))
            room_file.write("\n")
        with open('room_dict.txt','w') as room_file:
            room_file.write(str(room_dict))
        with open('room_queue.txt','w') as room_file:
            
            room_q = []
            for room in room_queue:
                room_q.append(room)
            room_file.write(str(room_q))