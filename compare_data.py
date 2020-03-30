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

no_visits = []

print(f'max:{max(visited)}')
print(f'min:{min(visited)}')
for i in range(0,500):
    if i not in visited:
        no_visits.append(i)


print(f'not visited number:{len(no_visits)}')
# with open('room_dict (copy).txt') as room_data:
#     for line in room_data:
#        room_dict = ast.literal_eval(line)
#     #print(room_dict)

# room_list = list(room_dict.keys())

# print(f'No of rooms in dict is {len(room_list)}')



# with open('room_queue (copy).txt') as room_data:
#     for line in room_data:
#        room_queue = ast.literal_eval(line)
# print(f'Rooms in queue:{len(room_queue)}')

# for room in room_queue:
#     print(room)
#     if room in visited:
#         print(f'{room} is visited')

# old_dict = {'room_id': 336, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,74)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['tiny treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.'],'s':23,'w':56,'n':21}

# print(old_dict)
# new_dict = {'room_id': 336, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,69)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['tiny treasure', 'tiny treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.'], 'w': 153}

# old_dict.update(new_dict)

# print(old_dict)