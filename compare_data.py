import ast
import json

room_dict = {}

with open('live_room_dict.txt','r') as room_data:
    for line in room_data:
       room_dict = ast.literal_eval(line)
    #print(room_dict)

visit_list = []
for room in room_dict:
    if room_dict[room]['description'] == 'You cannot see anything.':
        visit_list.append(room_dict[room]['room_id'])


# treasure_type = set()
# for room in room_dict:
#     check_type = 'description'
#     if check_type in room_dict[room].keys():
#     #print(room_dict[room]['description'])
#         print(room_dict[room]['room_id'],':',room_dict[room][check_type])
#         # for item in room_dict[room][check_type]:
#         #     treasure_type.add(item)
#         treasure_type.add(room_dict[room][check_type])
#     else:
#         print(room_dict[room]['room_id'],'****************************')

# print('**************************')
# for item in treasure_type:
#     print(item)
# print('**************************')
print(f'rooms to visit is:{len(visit_list)}')

#print(visit_list)

with open('to_visit.txt','w') as room_data:
    room_data.write(str(visit_list))

to_visit = []
with open('to_visit.txt') as room_data:
    for line in room_data:
        to_visit = ast.literal_eval(line)

# print(type(to_visit))

# while len(to_visit)> 0:
#     room = to_visit.pop(0)
#     print(room)