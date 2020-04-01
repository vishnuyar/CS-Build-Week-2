import ast
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


def dash_current_room(rooms,directions,cooldown,headers,list_urls,room_dict):
    dash_results = get_dash_results(directions)
    print(f'dash_results:{dash_results}')
    i=0
    for result in dash_results:
        direction, number = result
        if number == 1:
            room_no,cooldown = move_known_room(direction,rooms[i],cooldown,headers,list_urls[0])
            room_dict[room_no['room_id']].update(room_no)
            #print('normal move',room_dict[room_no['room_id']])
            i += 1
        else:
            room_no,cooldown = move_dash_rooms(direction,number,rooms[i:i+number],cooldown,headers,list_urls[1])
            room_dict[room_no['room_id']].update(room_no)
            #print('dash move',room_dict[room_no['room_id']])
            i += number
    return room_no, cooldown,room_dict


with open('live_room_dict.txt') as room_data:
    for line in room_data:
       room_dict = ast.literal_eval(line)

to_snitch_path = {}
to_well_path = {}

for room in room_dict.keys():
    if (room > 499) & (room !=555):
        #Find path to this room from 555
        print(room)
        room_path,direction_path = path_to_current_room(555,room,room_dict)
        room_path.pop(0)
        direction_path.pop(0)
        dash_results = get_dash_results(direction_path)
        to_snitch_path[room] = {'dash':dash_results,'rooms':room_path}
        #Find path to 555 from this room
        room_path,direction_path = path_to_current_room(room,555,room_dict)
        room_path.pop(0)
        direction_path.pop(0)
        dash_results = get_dash_results(direction_path)
        to_well_path[room] = {'dash':dash_results,'rooms':room_path}


with open('snitchpath_dict.txt','w') as room_file:
        room_file.write(str(to_snitch_path))

with open('wellpath_dict.txt','w') as room_file:
        room_file.write(str(to_well_path))