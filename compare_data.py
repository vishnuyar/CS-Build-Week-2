import ast
import json

room_dict = {}
visited = []
with open('room_graphs (copy).txt') as room_data:
    for line in room_data:
       room_data = ast.literal_eval(line)
       room_no = room_data['room_id']
       visited.append(room_no)
print(f'Number of Visited Rooms:{len(visited)}')

if 80 in visited:
    print('80 available')

with open('room_dict (copy).txt') as room_data:
    for line in room_data:
       room_dict = ast.literal_eval(line)
    #print(room_dict)

room_list = list(room_dict.keys())

print(f'No of rooms in dict is {len(room_list)}')



with open('room_queue (copy).txt') as room_data:
    for line in room_data:
       room_queue = ast.literal_eval(line)
print(f'Rooms in queue:{len(room_queue)}')

print(set(visited)^set(room_list))