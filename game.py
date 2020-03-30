import requests
import json
from datetime import datetime
from util import Stack
import csv
import time
from datetime import datetime
from game_functions import visit_using_dash,visit_using_normal,get_new_proof



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





def do_action(cooldown,visiturl,data,actiontype='POST'):
    time.sleep(cooldown+0.25)
    if actiontype == 'GET':
        r = requests.get(visiturl)
    else:
        r = requests.post(visit_url,data=data,headers=HEADERS)
    response = json.loads(r.text)
    cooldown = response['cooldown']
    return response,cooldown



# Load the room dictionary
with open('room_dict.txt') as room_data:
    for line in room_data:
       room_dict = ast.literal_eval(line)
    #print(room_dict)

room_list = list(room_dict.keys())

print(f'No of rooms in dict is {len(room_list)}')

#Initialise and find the player's room

current_proof = None
previous_room = None
player_room = None
player_input = None


try:
    r = requests.get(GAME_INIT_get)
    start_time = datetime.now()
    if r.status_code == 200:
        
        player_room = response[room_id]
        
        print(f'you are in room:{player_room} \n {response}')
    
    while True:
        player_input = input('What is your next move ? ')

        if player_input in ['n','s','e','w']:
            room_name = room_dict[player_room][player_input]
            data = json.loads('direction':player_input,'next_room_id':str(room_name))
            room_details,cooldown = do_action(cooldown,MOVEMENT,data)
            previous_room = player_room
            player_room = room_details['room_id']
            #replace the room dict with new details
            room_dict[player_room].update(room_details)
            print(f'The room response:'{room_details})
        
        elif player_input.startswith('take'):
            #get the treasure name
            treasure_name = player_input.replace('take','')
            data = json.dumps({'name':treasure_name})
            response,cooldown = do_action(cooldown,TAKE_TREASURE,data)
            print(f'Take treasure response:{response}')
        
        
        elif player_input.startswith('drop'):
            #get the treasure name
            
            treasure_name = player_input.replace('drop','')
            data = json.dumps({'name':treasure_name})
            response,cooldown = do_action(cooldown,DROP_TREASURE,data)
            print(f'Drop treasure response:{response}')
        
        elif player_input.startswith('sell'):
            #get the treasure name
            treasure_name = player_input.replace('sell','')
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
            treasure_name = player_input.replace('buy','')
            data = json.dumps({'name':treasure_name})
            response,cooldown = do_action(cooldown,BUY_ITEMS,data)
            print(f'Buy treasure response:{response}')
            sell_response = input('Your decision? ')
            if sell_response == 'yes':
                data = json.dumps({'name':treasure_name,'confirm':'yes'})
                response,cooldown = do_action(cooldown,BUY_ITEMS,data)
                print(f'Response from buying:{response}')
        
        elif player_input == 'status':
            response,cooldown = do_action(cooldown,STATUS_INVENTORY)
            print(f'status response:{response}')
        
        elif player_input.startswith('examine')
            #get the treasure name
            treasure_name = player_input.replace('examine','')
            data = json.dumps({'name':treasure_name})
            response,cooldown = do_action(cooldown,EXAMINE,data)
            print(f'examine response:{response}')
        
        elif player_input.startswith('name'):
            #get the treasure name
            treasure_name = player_input.replace('name','')
            data = json.dumps({'name':treasure_name})
            r = requests.post(CHANGE_NAME,data)
            print(f'change name response:{response}')
        
        elif player_input == 'pray':
            response,cooldown = do_action(cooldown,PRAY)
            print(f'pray response:{response}')
        
        elif player_input.startswith('carry'):
            #get the treasure name
            treasure_name = player_input.replace('carry','')
            data = json.dumps({'name':treasure_name})
            response,cooldown = do_action(cooldown,CARRY_ITEM,data)
            print(f'carry item response:{response}')
        
        elif player_input == 'receive':
            response,cooldown = do_action(cooldown,RECEIVE_ITEM)
            print(f'pray response:{response}')
        
        elif player_input.startswith('wear'):
            #get the treasure name
            treasure_name = player_input.replace('wear','')
            data = json.dumps({'name':treasure_name})
            
            response,cooldown = do_action(cooldown,WEAR,data)
            print(f'wear item response:{response}')

        elif player_input == 'undress':
            
            response,cooldown = do_action(cooldown,UNDRESS)
            print(f'undress response:{response}')
        
        elif player_input == 'warp':
            
            response,cooldown = do_action(cooldown,WARP)
            print(f'warp response:{response}')

        elif player_input == 'recall':
            response,cooldown = do_action(cooldown,RECALL)
            print(f'recall response:{response}')

        elif player_input == 'balance':
            response,cooldown = do_action(cooldown,COINS_BALANCE_get, actiontype='GET')
            print(f'balance response:{response}')

        elif player_input.startswith('trans'):
            #get the treasure name
            treasure_name = player_input.replace('trans','')
            data = json.dumps({'name':treasure_name})
            response,cooldown = do_action(cooldown,TRANMORGIGY,data)
            print(f'Transmorgify response:{response}')

        elif player_input == 'proof':
            response,cooldown = do_action(cooldown,PROOF_get,actiontype='GET')
            
            proof_difficulty = response['difficulty']
            current_proof = response['proof']
            print(f'balance response:{response}')

        elif player_input == 'mine':
            response,cooldown = do_action(cooldown,PROOF_get,actiontype='GET')
            start_time = datetime.now()
            proof_difficulty = response['difficulty']
            current_proof = response['proof']
            print(f'balance response:{response}')
            new_proof = get_new_proof(current_proof,proof_difficulty)
            data = json.loads('proof':new_proof)
            endtime = datetime.now()
            timediff = (end_time - start_time).total_seconds()
            if timediff > cooldown:
                cooldown = 0
            else:
                cooldown -= timediff
            cooldown = cooldown - (endtime - start_time)
            response,cooldown = do_action(cooldown,MINE_COINS,data)
            print(f'Mine response:{response}')

        elif player_input == 'quit':
            break

        elif player_input.startswith('dash'):
            #get the treasure name
            treasure_name = int(player_input.split()[1])
            response,cooldown = visit_using_dash(player_room,room_name,room_dict,cooldown,headers,[MOVEMENT,DASH])
            previous_room = player_room
            player_room = response['room_id']
            #replace the room dict with new details
            room_dict[player_room].update(response)
            print(f'dash visit response:{response}')
        
        elif player_input.startswith('goto'):
            #get the treasure name
            room_name = int(player_input.split()[1])
            response,cooldown = visit_using_normal(player_room,room_name,room_dict,cooldown,headers,MOVEMENT)
            previous_room = player_room
            player_room = response['room_id']
            #replace the room dict with new details
            room_dict[player_room].update(response)
            print(f'normal visit response:{response}')

        else:
            print(f'input recieved: {player_input}')
            print('There is no such command to execute')
        
        with open('live_room_dict.txt','w') as room_file:
            room_file.write(str(room_dict))
        
        with open('room_lines.txt','w') as room_file:
            for key in room_dict:
            room_file.write(str(room_dict[key]))


except Exception E:
    print('Error:',E)

