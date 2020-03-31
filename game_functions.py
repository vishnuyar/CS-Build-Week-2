#Functions to help playing the game.
import hashlib
import requests
import json
import time
from datetime import datetime
import random
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
                    path_copy = vertex_path.copy()
                    direction_copy = direction_path.copy()
                    room_no = room_dict[vertex][direction]
                    path_copy.append(room_no)
                    direction_copy.append(direction)
                    direction_queue.enqueue(direction_copy)
                    bft_queue.enqueue(path_copy)

def move_known_room(direction,room_no,cooldown,headers,visit_url):
    time.sleep(cooldown+1)
    data_direction = {}
    data_direction['direction'] = direction
    data_direction['next_room_id'] = str(room_no)
    data = json.dumps(data_direction)
    r = requests.post(visit_url,data=data, headers=headers)
    room_details = json.loads(r.text)
    print(f'moved {direction} to room {room_details["room_id"]}')
    print('normal move',room_details)
    return room_details,room_details['cooldown']

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

def move_dash_rooms(direction,no_rooms,rooms_list,cooldown,headers,visit_url):
    time.sleep(cooldown+1)
    rs = str(rooms_list).replace('[','').replace(']','').replace(' ','')
    data_direction = {"direction":direction, "num_rooms":str(no_rooms), "next_room_ids":rs}
    data = json.dumps(data_direction)
    #print(f'dash data:{data}')
    r = requests.post(visit_url,data=data, headers=headers)
    room_details = json.loads(r.text)
    print(f'dash moved {direction} to room {room_details["room_id"]}')
    print('dash move',room_details)
    return room_details,room_details['cooldown']        
        


def dash_current_room(rooms,directions,cooldown,headers,list_urls):
    dash_results = get_dash_results(directions)
    print(f'dash_results:{dash_results}')
    i=0
    for result in dash_results:
        direction, number = result
        if number == 1:
            room_no,cooldown = move_known_room(direction,rooms[i],cooldown,headers,list_urls[0])
            i += 1
        else:
            room_no,cooldown = move_dash_rooms(direction,number,rooms[i:i+number],cooldown,headers,list_urls[1])
            i += number
    return room_no, cooldown

def visit_current_room(rooms,directions,cooldown,headers,visit_url):
    for i in range(len(directions)):
        room_no, cooldown = move_known_room(directions[i],rooms[i],cooldown,headers,visit_url)
        print(f'In room:{room_no}')
    return room_no, cooldown


def visit_using_dash(oldroom,newroom,room_dict,cooldown,headers,list_urls):
    room_path,direction_path  = path_to_current_room(oldroom,newroom,room_dict)
    room_path.pop(0)
    direction_path.pop(0)
    # print(len(direction_path))
    # print(room_path)
    # print(direction_path)
    response,cooldown = dash_current_room(room_path,direction_path,cooldown,headers,list_urls)
    return response,cooldown


def visit_using_normal(oldroom,newroom,room_dict,cooldown,headers,visit_url):
    room_path,direction_path  = path_to_current_room(oldroom,newroom,room_dict)
    room_path.pop(0)
    direction_path.pop(0)
    response,cooldown = visit_current_room(room_path,direction_path,cooldown,headers,visit_url)
    return response,cooldown



def get_new_proof(block,difficulty):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    proof = random.randint(1,100)
    json_block = json.dumps(block,sort_keys=True)
    pattern = None
    for i in range(difficulty):
        if i == 0:
            pattern = '0'
        else:
            pattern += '0'
    print(pattern)
    while valid_proof(json_block,proof,difficulty,pattern) is False:
        proof +=1
    return proof


def valid_proof(block_string, proof,difficulty,pattern):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    block_string_proof = f'{block_string}{proof}'.encode()
    hash_block = hashlib.sha256(block_string_proof).hexdigest()
    #print("hasbloc",hash_block)


    if hash_block[:difficulty]==pattern:
        print("hasbloc",hash_block)
        return True
    else:
        return False

