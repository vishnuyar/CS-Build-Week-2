def check_dash(rooms,directions):
    rooms.pop(0)
    directions.pop(0)
    i = 0
    con_rooms = []
    while i < len(directions)-1:
        if directions[i] == directions[i+1]:
            con_rooms.append(rooms[i])        
            del directions[i]
        else:
            i = i+1
    print(con_rooms)    

rooms = [364,257,455,34,66,126,23,5,300]
source_list = ['e','e','w','w','n','e','s','s','s']

result_list = []
current = source_list[0]
count = 0
for value in source_list:
    if value == current:
        count += 1
    else:
        result_list.append((current, count))
        current = value
        count = 1
result_list.append((current, count))

#{"direction":"s", "next_room_id": "0"}
#{"direction":"n", "num_rooms":"5", "next_room_ids":"10,19,20,63,72"}
i = 0
for result in result_list:
    direction, number = result
    if number == 1:
        data_direction = {'direction':direction,'next_room_id':str(rooms[i])}
        print('single',data_direction)
        i += 1
    else:
        data_direction = {"direction":direction, "num_rooms":str(number), "next_room_ids":str(rooms[i:i+number])}
        print('multiple',data_direction)
        i += number





print(result_list)

