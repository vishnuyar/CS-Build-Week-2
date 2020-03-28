import requests
import json
from datetime import datetime
from util import Stack
import csv
import time


TOKEN = "46b1a83c354572a2b13401760d72e76bf5143cc2"
HOST = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"

GAME_INIT_get = HOST+'init/'
MOVEMENT = HOST+'move/'
TAKE_TREASURE = HOST + 'take/'
DROP_TREASURE = HOST + 'drop/'
SELL_TREASURE = HOST + 'sell/'
BUY_ITEMS = HOST + 'buy/'
STATUS_INVENTORY = HOST + 'status/'
EXAMINE = HOST + 'examine/'
WEAR = HOST + 'wear/'
UNDRESS = HOST + 'undress/'
CHANGE_NAME = HOST + 'change_name/'
PRAY = HOST + 'pray/'
FLY = HOST + 'fly/'
DASH = HOST + 'dash/'
CARRY_ITEM = HOST + 'carry/'
RECEIVE_ITEM = HOST + 'receive/'
RECALL_post = HOST +'recall/'
WARP = HOST + 'warp/'
TRANMORGIGY = HOST + 'transmogrify/'
MINE_COINS = "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/"
PROOF_get = "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/"
COINS_BALANCE_get = "https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/"


TOTAL_ROOMS = 500
opposites = {'n':'s','s':'n','w':'e','e':'w'}

#Initialize the player first
headers = {"Authorization":f"Token {TOKEN}"}
r = requests.get(GAME_INIT_get, headers=headers)
start_time = datetime.now()
print(r.status_code)
response = json.loads(r.text)

#Start preparation for moving to all rooms
visit_list = []
room_dict = {}
previous_room = None
rooms_stack = Stack()
print('init response',response)
rooms_stack.push(response)
cool_period = response['cooldown']
time.sleep(cool_period)

while rooms_stack.size() > 0:
    current_room = rooms_stack.pop()
    room_no = current_room['room_id']
    if room_no not in visit_list:
        visit_list.append(room_no)
        room_dict[room_no] = current_room
        print('add to list',current_room)
        if previous_room:
            #move from previous room get it's direction to here
            directions = room_dict[previous_room]['exits']
            for direction in directions:
                if room_dict[previous_room][direction] == room_no:
                    data_direction[direction] = direction
                    data_direction['next_room_id'] = room_no
                    data = json.dumps(data_direction)
                    r = requests.post(MOVEMENT,data=data, headers=headers)
                    response = json.loads(r.text)
                    cool_period = response['cooldown']+1
                    time.sleep(cool_period+1)

        for direction in current_room['exits']:
            data_direction = {}
            data_direction['direction'] = direction
            data = json.dumps(data_direction)
            #print("data",data)
            r = requests.post(MOVEMENT, data=data, headers=headers)
            #print(r.text)
            response = json.loads(r.text)
            print('response for ',response['room_id'])
            cool_period = response['cooldown']
            print(f'cool down:{cool_period}')
            if response['room_id']:
                room_dict[room_no].update({direction:response['room_id']})
                rooms_stack.push(response)
                time.sleep(cool_period+1)
                #go back for other directions
                data_direction[direction] = opposites[direction]
                data_direction['next_room_id'] = room_no
                data = json.dumps(data_direction)
                r = requests.post(MOVEMENT,data=data, headers=headers)
                response = json.loads(r.text)
                print(response)
                cool_period = response['cooldown']+1
                time.sleep(cool_period+1)
        previous_room = room_no
        with open('room_graphs.txt','w+') as room_file:
            room_file.write(str(room_dict[room_no]))
            room_file.write("\n")
            



            




with open("room_graph.txt","w+") as roomfile:
    roomfile.write(str(room_dict))




