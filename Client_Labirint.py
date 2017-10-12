# -*- coding: utf-8 -*-
import socket

answer = []
conn = socket.socket()
conn.connect(("127.0.0.1", 7000))
player = conn.recv(1)

while 1:
    next_or_end = conn.recv(1)
    if next_or_end == b'E':
        print('The End!\nYou Win!')
        break

    # Размер массива
    temp_data = str(conn.recv(3))
    temp_data = temp_data[2:len(temp_data) - 1]
    card_sizes = []
    for i in temp_data.split(','):
        card_sizes += [int(i)]

    # Подгружаю карту
    map_labyrinth = []
    for i in range(card_sizes[0]):
        map_labyrinth += [[]]
        for j in range(card_sizes[1]):
            temp_data = str(conn.recv(1))
            temp_data = temp_data[2:len(temp_data) - 1]
            map_labyrinth[i] += [temp_data]
            if temp_data == 'I':
                vertical_point, horizon_point = i, j

    for i in range(card_sizes[0]):
        print(map_labyrinth[i])

    # Игра началась
    while 1:
        if player == b'1':

            # Первый пользователь
            direction = input("Выбирайте направление: ").strip()

            if 'R' in direction or 'r' in direction:
                conn.send(b'r')
            elif 'L' in direction or 'l' in direction:
                conn.send(b'l')
            elif 'T' in direction or 't' in direction:
                conn.send(b't')
            elif 'D' in direction or 'd' in direction:
                conn.send(b'd')
            else:
                continue
            state_of_the_game = conn.recv(3)
        else:
            # Второй пользователь
            direction = conn.recv(1)

            if b'r' == direction:
                print('Right')
            elif b'l' == direction:
                print('Left')
            elif b't' == direction:
                print('Top')
            elif b'd' == direction:
                print('Down')

            while True:

                while True:
                    step = input("Сколько клеток пройти?: ").strip()
                    try:
                        if step > '0' and int(step) < len(map_labyrinth):
                            break
                    except:
                        continue
                conn.send(step.encode())
                state_of_the_game = conn.recv(3)
                if state_of_the_game == b'Non':
                    print('Много!!!')
                    continue
                break

        if state_of_the_game == b'Win':
            print('You Win!')
            if player == b'2':
                answer += [conn.recv(1)]
                print(answer)
            break
        state_of_the_game = str(state_of_the_game)
        state_of_the_game = state_of_the_game[2:len(state_of_the_game) - 1]
        state_of_the_game = state_of_the_game.split(',')

        switch = 1
        if vertical_point == int(state_of_the_game[0]):
            if int(state_of_the_game[1]) < horizon_point:
                switch = -1
            while horizon_point != int(state_of_the_game[1]):
                map_labyrinth[vertical_point][horizon_point] = '+'
                horizon_point += switch
        else:
            if int(state_of_the_game[0]) < vertical_point:
                switch = -1
            while vertical_point != int(state_of_the_game[0]):
                map_labyrinth[vertical_point][horizon_point] = '+'
                vertical_point += switch

        map_labyrinth[vertical_point][horizon_point] = 'I'

        for i in range(len(map_labyrinth)):
            print(map_labyrinth[i])

conn.close()
