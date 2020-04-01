import requests
import json
import ast
from datetime import datetime
from util import Stack
import csv
import time
from datetime import datetime
from game_functions import visit_using_dash,visit_using_normal,get_new_proof,path_to_current_room



TOKEN = "46b1a83c354572a2b13401760d72e76bf5143cc2"
HEADERS = {"Authorization":f"Token {TOKEN}"}
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
RECALL = HOST +'recall/'
WARP = HOST + 'warp/'
TRANMORGIGY = HOST + 'transmogrify/'
MINE_COINS = "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/"
PROOF_get = "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/"
COINS_BALANCE_get = "https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/"


room_dict = {}
opposites = {'n':'s','s':'n','w':'e','e':'w'}
rooms_visited = set()

def get_room_details(direction,cooldown):
    time.sleep(cooldown+1)
    data_direction = {}
    data_direction['direction'] = direction
    data = json.dumps(data_direction)
    r = requests.post(MOVEMENT, data=data, headers=HEADERS)
    #print(r)
    room_details = json.loads(r.text)
    cooldown = room_details['cooldown']
    #print(f'moving {direction} got {room_details["room_id"]}')
    return room_details,cooldown

def send_for_walk(room_no,cooldown):
    
    visit_directions = []
    for direction in room_dict[room_no]['exits']:
        if room_dict[room_no][direction] is None:
            visit_directions.append(direction)
    total_d = len(visit_directions)
    for i,direction in enumerate(visit_directions):
        #go to the direction get the room details
        room_details,cooldown = get_room_details(direction,cooldown)
        
        #add directions to room details
        if room_details['room_id'] not in room_dict.keys():
            room_dict[room_details['room_id']] = room_details
            room_details = add_directions_dict(room_details)
        new_room_no = room_details['room_id']
        player_room = new_room_no
        #rooms_visited.add(player_room)
        #add this room to the room dict
        room_dict[new_room_no].update(room_details)
        
        #assign directions to rooms
        assign_direction(room_no,new_room_no,direction)
        print(room_dict[new_room_no])
        #add the room to the queue
        #go back to previous room only if it is not the last room
        if i <  (total_d - 1):
            data_direction = {}
            data_direction['direction'] = opposites[direction]
            data_direction['next_room_id'] = str(room_no)
            data = json.dumps(data_direction)
            room_details,cooldown = do_action(cooldown,MOVEMENT,data)
            
            #player_room = room_details['room_id']
            #rooms_visited.add(player_room)
    with open('live_room_dict.txt','w') as room_file:
        room_file.write(str(room_dict))
    return new_room_no,cooldown



def add_directions_dict(room):
    for direction in room['exits']:
        room[direction] = None
    return room

def assign_direction(room_a,room_b,direction):
    room_dict[room_a][direction] = room_b
    room_dict[room_b][opposites[direction]] = room_a


def do_action(cooldown,visiturl,data,actiontype='POST'):
    time.sleep(cooldown+0.25)
    if actiontype == 'GET':
        r = requests.get(visiturl,headers=HEADERS)
    else:
        r = requests.post(visiturl,data=data,headers=HEADERS)
    response = json.loads(r.text)
    cooldown = response['cooldown']
    return response,cooldown



# Load the room dictionary
with open('live_room_dict.txt') as room_data:
    for line in room_data:
       room_dict = ast.literal_eval(line)
    #print(room_dict)

room_list = list(room_dict.keys())

print(f'No of rooms in dict is {len(room_list)}')

#Load a list of complete data rooms
visited = []
with open('room_lines.txt') as room_data:
    for line in room_data:
       room_data = ast.literal_eval(line)
       room_no = room_data['room_id']
       visited.append(room_no)
print(f'Number of Visited Rooms:{len(visited)}')

#load the rooms the player visited
with open('playervisits.txt') as room_data:
    for line in room_data:
       rooms_visited = ast.literal_eval(line)
print(f'player Visited Rooms:{len(rooms_visited)}')      
print(f'player Visited Rooms:{sorted(rooms_visited)}')


#Initialise and find the player's room

current_proof = None
previous_room = None
player_room = None
player_input = None



r = requests.get(GAME_INIT_get,headers = HEADERS)
start_time = datetime.now()
if r.status_code == 200:
    response = json.loads(r.text)
    player_room = response["room_id"]
    cooldown = response['cooldown']
    rooms_visited.add(player_room)
    print(room_dict[player_room])
    #print(f'you are in room:{player_room} \n {response}')
else:
    print('error init',r.text)

while True:
    player_input = input('What is your next move ? ')
    end_time = datetime.now()
    timediff = (end_time - start_time).total_seconds()
    if timediff > cooldown:
        cooldown = 0
    else:
        cooldown -= timediff
    if player_input in ['n','s','e','w']:
        room_name = room_dict[player_room][player_input]
        data_direction = {}
        data_direction['direction'] = player_input
        data_direction['next_room_id'] = str(room_name)
        data = json.dumps(data_direction)
        room_details,cooldown = do_action(cooldown,MOVEMENT,data)
        previous_room = player_room
        player_room = room_details['room_id']
        if player_room != room_name:
            room_dict[previous_room][player_input] = None
        rooms_visited.add(player_room)
        if player_room in visited:
            
            #replace the room dict with new details
            room_dict[player_room].update(room_details)
            print(f'The room response:{room_dict[player_room]}')
            for direction in room_dict[player_room]['exits']:
                print(f'{direction}:{room_dict[player_room][direction]}')
        else:
            room_details = add_directions_dict(room_details)
            room_dict[player_room].update(room_details)
            print(room_details)
            player_room = room_details['room_id']
            print('take a walk')
        
    
    elif player_input.startswith('fly'):
        player_input = player_input.replace('fly ','')
        room_name = room_dict[player_room][player_input]
        data_direction = {}
        data_direction['direction'] = player_input
        data_direction['next_room_id'] = str(room_name)
        data = json.dumps(data_direction)
        room_details,cooldown = do_action(cooldown,MOVEMENT,data)
        previous_room = player_room
        player_room = room_details['room_id']
        if player_room != room_name:
            room_dict[previous_room][player_input] = None
        rooms_visited.add(player_room)
        if player_room in visited:
            
            #replace the room dict with new details
            room_dict[player_room].update(room_details)
            print(f'The room response:{room_dict[player_room]}')
            for direction in room_dict[player_room]['exits']:
                print(f'{direction}:{room_dict[player_room][direction]}')
        else:
            room_dict[player_room].update(room_details)
            print(room_details)
            player_room = room_details['room_id']
            print('take a walk')
    
    elif player_input.startswith('take'):
        #get the treasure name
        treasure_name = player_input.replace('take ','')
        data = json.dumps({'name':treasure_name})
        #print(data)
        response,cooldown = do_action(cooldown,TAKE_TREASURE,data)
        print(f'Take treasure response:{response}')
    
    
    elif player_input.startswith('drop'):
        #get the treasure name
        
        treasure_name = player_input.replace('drop ','')
        data = json.dumps({'name':treasure_name})
        response,cooldown = do_action(cooldown,DROP_TREASURE,data)
        print(f'Drop treasure response:{response}')
    
    elif player_input.startswith('sell'):
        #get the treasure name
        treasure_name = player_input.replace('sell ','')
        data = json.dumps({'name':treasure_name})
        response,cooldown = do_action(cooldown,SELL_TREASURE,data)
        print(f'Drop treasure response:{response}')
        sell_response = input('Your decision? ')
        
        if sell_response == 'yes':
            data = json.dumps({'name':treasure_name,'confirm':'yes'})
            response,cooldown = do_action(cooldown,SELL_TREASURE,data)
            print(f'Response from selling:{response}')
    
    elif player_input.startswith('buy'):
        #get the treasure name
        treasure_name = player_input.replace('buy ','')
        data = json.dumps({'name':treasure_name})
        response,cooldown = do_action(cooldown,BUY_ITEMS,data)
        print(f'Buy treasure response:{response}')
        sell_response = input('Your decision? ')
        if sell_response == 'yes':
            data = json.dumps({'name':treasure_name,'confirm':'yes'})
            response,cooldown = do_action(cooldown,BUY_ITEMS,data)
            print(f'Response from buying:{response}')
    
    elif player_input == 'status':
        response,cooldown = do_action(cooldown,STATUS_INVENTORY,None)
        print(f'status response:{response}')
    
    elif player_input.startswith('examine'):
        #get the treasure name
        treasure_name = player_input.replace('examine ','')
        data = json.dumps({'name':treasure_name})
        response,cooldown = do_action(cooldown,EXAMINE,data)
        print(f'examine response:{response}')
    
    elif player_input.startswith('name'):
        #get the treasure name
        treasure_name = player_input.replace('name ','')
        data = json.dumps({'name':[treasure_name]})
        print(data)
        response,cooldown = do_action(cooldown,CHANGE_NAME,data)
        print(f'change name response:{response}')
        sell_response = input('Your decision? ')
        if sell_response == 'yes':
            data = json.dumps({'name':[treasure_name],'confirm':'aye'})
            response,cooldown = do_action(cooldown,CHANGE_NAME,data)
            print(f'Response from changing name:{response}')
    
    elif player_input == 'pray':
        response,cooldown = do_action(cooldown,PRAY,None)
        print(f'pray response:{response}')
    
    elif player_input.startswith('carry'):
        #get the treasure name
        treasure_name = player_input.replace('carry ','')
        data = json.dumps({'name':treasure_name})
        response,cooldown = do_action(cooldown,CARRY_ITEM,data)
        print(f'carry item response:{response}')

    
    elif player_input == 'receive':
        response,cooldown = do_action(cooldown,RECEIVE_ITEM,None)
        print(f'pray response:{response}')
    
    elif player_input.startswith('wear'):
        #get the treasure name
        treasure_name = player_input.replace('wear ','')
        data = json.dumps({'name':treasure_name})
        
        response,cooldown = do_action(cooldown,WEAR,data)
        print(f'wear item response:{response}')

    elif player_input == 'undress':
        
        response,cooldown = do_action(cooldown,UNDRESS,None)
        print(f'undress response:{response}')
    
    elif player_input == 'warp':
        
        response,cooldown = do_action(cooldown,WARP,None)
        print(f'warp response:{response}')
        player_room = response['room_id']

    elif player_input == 'recall':
        response,cooldown = do_action(cooldown,RECALL,None)
        print(f'recall response:{response}')

    elif player_input == 'balance':
        response,cooldown = do_action(cooldown,COINS_BALANCE_get,None, actiontype='GET')
        print(f'balance response:{response}')

    elif player_input.startswith('trans'):
        #get the treasure name
        treasure_name = player_input.replace('trans ','')
        data = json.dumps({'name':treasure_name})
        response,cooldown = do_action(cooldown,TRANMORGIGY,data)
        print(f'Transmorgify response:{response}')

    elif player_input == 'proof':
        response,cooldown = do_action(cooldown,PROOF_get,None,actiontype='GET')
        
        proof_difficulty = response['difficulty']
        current_proof = response['proof']
        print(f'balance response:{response}')

    elif player_input == 'mine':
        response,cooldown = do_action(cooldown,PROOF_get,None,actiontype='GET')
        start_time = datetime.now()
        proof_difficulty = response['difficulty']
        current_proof = response['proof']
        print(f'balance response:{response}')
        new_proof = get_new_proof(current_proof,proof_difficulty)
        print(f'proof:{new_proof}')
        data = json.dumps({'proof':new_proof})
        endtime = datetime.now()
        timediff = (end_time - start_time).total_seconds()
        if timediff > cooldown:
            cooldown = 0
        else:
            cooldown -= timediff
        
        response,cooldown = do_action(cooldown,MINE_COINS,data)
        print(f'Mine response:{response}')

    
    elif player_input.startswith('dash'):
        #get the treasure name
        treasure_name = int(player_input.split()[1])
        response,cooldown,room_dict = visit_using_dash(player_room,treasure_name,room_dict,cooldown,HEADERS,[MOVEMENT,DASH])
        previous_room = player_room
        player_room = response['room_id']
        #replace the room dict with new details
        room_dict[player_room].update(response)
        rooms_visited.add(player_room)
        #print(f'dash visit response:{response}')
    
    
    elif player_input == 'visit':
        to_visit = []
        with open('to_visit.txt') as room_data:
            for line in room_data:
                to_visit = ast.literal_eval(line)
        while len(to_visit) > 0:
            room_name = to_visit.pop(0)
            room_path,direction_path  = path_to_current_room(player_room,room_name,room_dict)
            room_path.pop(0)
            direction_path.pop(0)
            for i,room in enumerate(room_path):
                data_direction = {}
                data_direction['direction'] = direction_path[i]
                data_direction['next_room_id'] = str(room)
                data = json.dumps(data_direction)
                room_details,cooldown = do_action(cooldown,MOVEMENT,data)
                room_id = room_details['room_id']
                room_dict[room_id].update(room_details)

                #write the dict to file
                with open('live_room_dict.txt','w') as room_file:
                    room_file.write(str(room_dict))
                
                print(room_dict[room_id]['room_id'])
                print(room_dict[room_id]['description'])
                print("*****************************************")
                if room_id in to_visit:
                    to_visit.remove(room_id)
            player_room = room_id
            print(f'Left to traverse:{len(to_visit)}')
            



    elif player_input.startswith('goto'):
        #get the treasure name
        room_name = int(player_input.split()[1])
        response,cooldown,room_dict = visit_using_normal(player_room,room_name,room_dict,cooldown,HEADERS,MOVEMENT)
        previous_room = player_room
        player_room = response['room_id']
        #replace the room dict with new details
        room_dict[player_room].update(response)
        rooms_visited.add(player_room)
        #print(f'normal visit response:{response}')

    elif player_input == 'show':
        print(f'you have visited {sorted(rooms_visited)}')

    elif player_input.startswith('loopwalk'):
        while True:
            immediate_room = True
            another_room = True
            none_check = []
            for direction in room_dict[player_room]['exits']:
                none_check.append(room_dict[player_room][direction])

            if None in none_check:
                immediate_room = False
                room_no, cooldown = send_for_walk(player_room,cooldown)
                player_room = room_no 
            if immediate_room:
                for room in room_dict.keys():
                    if room > 499:
                        none_check = []
                        for direction in room_dict[room]['exits']:
                            #print(room)
                            none_check.append(room_dict[room][direction])
                        if None in none_check:
                            response,cooldown,room_dict = visit_using_dash(player_room,room,room_dict,cooldown,HEADERS,[MOVEMENT,DASH])
                            player_room = response['room_id']
                            another_room = False
                            break
            if immediate_room & another_room:
                print('Loop walk completed')
                break



    elif player_input.startswith('walk'):
        room_no = player_room
        visit_directions = []
        for direction in room_dict[room_no]['exits']:
            if room_dict[room_no][direction] is None:
                visit_directions.append(direction)
        total_d = len(visit_directions)
        for i,direction in enumerate(visit_directions):
            #go to the direction get the room details
            room_details,cooldown = get_room_details(direction,cooldown)
            
            #add directions to room details
            if room_details['room_id'] not in room_dict.keys():
                room_dict[room_details['room_id']] = room_details
                room_details = add_directions_dict(room_details)
            new_room_no = room_details['room_id']
            player_room = new_room_no
            rooms_visited.add(player_room)
            #add this room to the room dict
            room_dict[new_room_no].update(room_details)
            
            #assign directions to rooms
            assign_direction(room_no,new_room_no,direction)
            print(room_dict[new_room_no])
            #add the room to the queue
            #go back to previous room only if it is not the last room
            if i <  (total_d - 1):
                data_direction = {}
                data_direction['direction'] = opposites[direction]
                data_direction['next_room_id'] = str(room_no)
                data = json.dumps(data_direction)
                room_details,cooldown = do_action(cooldown,MOVEMENT,data)
                
                player_room = room_details['room_id']
                rooms_visited.add(player_room)
                
            
        
        

    elif player_input == 'quit':
        break


    else:
        print(f'input recieved: {player_input}')
        print('There is no such command to execute')


    start_time = datetime.now()

    with open('live_room_dict.txt','w') as room_file:
        room_file.write(str(room_dict))

    with open('playervisits.txt','w') as room_file:
        room_file.write(str(rooms_visited))
    
    with open('room_lines.txt','w') as room_file:
        for key in room_dict:
            room_file.write(str(room_dict[key]))
            room_file.write('\n')




