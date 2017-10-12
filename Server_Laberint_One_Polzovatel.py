# -*- coding: utf-8 -*-
import socket  # Подключение библиотеки

import karts  # Библиотека с картами

global answer


# Блок взаимодействия с картой
def loading_map(map_labyrinth_local, connect, player):
    # Отправляет размер карты
    global answer, horizon_local
    connect.send((str(len(map_labyrinth_local)) + ',' + str(len(map_labyrinth_local[0]))).encode('utf-8'))

    # Отправляет карту
    for i in range(len(map_labyrinth_local)):
        for j in range(len(map_labyrinth_local[i])):
            if map_labyrinth_local[i][j] == 'I':
                horizon_local = j
                vertical_local = i
            elif 'a' <= map_labyrinth_local[i][j] <= 'z':
                answer = map_labyrinth_local[i][j]
                map_labyrinth_local[i][j] = 'E'

            if player == 2:
                if map_labyrinth_local[i][j] == 'I':
                    connect.send(map_labyrinth_local[i][j].encode('utf-8'))
                else:
                    connect.send(b'.')
            else:
                connect.send(map_labyrinth_local[i][j].encode('utf-8'))
    return horizon_local, vertical_local


# Проверка возможности
def check_the_wall(map_labyrinth_local, vertical_local, horizon_local, conn2=None, vertical_step=0, horizon_step=0):

    light_map_labyrinth = len(map_labyrinth_local)
    iconic_switch = 1
    while 1:
        if 0 <= vertical_local + vertical_step < light_map_labyrinth and 0 <= horizon_local + horizon_step < light_map_labyrinth:
            if map_labyrinth_local[vertical_local + vertical_step][horizon_local + horizon_step] == '.':
                if vertical_step == 0:
                    if horizon_step < 0:
                        horizon_step = -light_map_labyrinth
                    else:
                        horizon_step = light_map_labyrinth
                else:
                    if vertical_step < 0:
                        vertical_step = -light_map_labyrinth
                    else:
                        vertical_step = light_map_labyrinth
            else:
                temp_vertical = vertical_local + vertical_step
                temp_horizon = horizon_local + horizon_step
                if horizon_step < 0 or vertical_step < 0:
                    iconic_switch = -1
                for i in range(vertical_local, temp_vertical, iconic_switch):  # Неправильные циклы
                    if map_labyrinth_local[i][horizon_local] == '.':
                        if vertical_step < 0:
                            vertical_step = -light_map_labyrinth
                        else:
                            vertical_step = light_map_labyrinth
                        break

                for i in range(horizon_local, temp_horizon, iconic_switch):
                    if map_labyrinth_local[vertical_local][i] == '.':
                        if horizon_step < 0:
                            horizon_step = -light_map_labyrinth
                        else:
                            horizon_step = light_map_labyrinth
                        break

                if vertical_step != light_map_labyrinth and horizon_step != light_map_labyrinth \
                        and vertical_step != -light_map_labyrinth and horizon_step != -light_map_labyrinth:

                    while vertical_local != temp_vertical:
                        map_labyrinth_local[vertical_local][horizon_local] = '+'
                        vertical_local += iconic_switch

                    while horizon_local != temp_horizon:
                        map_labyrinth_local[vertical_local][horizon_local] = '+'
                        horizon_local += iconic_switch

                    if map_labyrinth_local[vertical_local][horizon_local] == 'E':
                        map_labyrinth_local[vertical_local][horizon_local] = 'I'
                        return 'Win'
                    else:
                        map_labyrinth_local[vertical_local][horizon_local] = 'I'
                        return (str(vertical_local) + ',' + str(horizon_local)).encode('utf-8')

        else:
            # Если смещение на такое число несуществует
            conn2.send(b'Non')
            if vertical_step == 0:
                if horizon_step < 0:
                    horizon_step = str(conn2.recv(1))
                    horizon_step = horizon_step[2:len(horizon_step) - 1]
                    horizon_step = int(horizon_step)
                    horizon_step = -horizon_step
                else:
                    horizon_step = str(conn2.recv(1))
                    horizon_step = horizon_step[2:len(horizon_step) - 1]
                    horizon_step = int(horizon_step)
            elif vertical_step < 0:
                vertical_step = str(conn2.recv(1))
                vertical_step = vertical_step[2:len(vertical_step) - 1]
                vertical_step = int(vertical_step)
                vertical_step = -vertical_step
            else:
                vertical_step = str(conn2.recv(1))
                vertical_step = vertical_step[2:len(vertical_step) - 1]
                vertical_step = int(vertical_step)

map_list = karts.Karts()
map_list = map_list.random_cards()

# Можно будет выделить в блок
sock = socket.socket()  # Создание сокета
sock.bind(('localhost', 7000))  # Настраиваю определённый порт для общения с клиентом
sock.listen(2)  # Создаю очередь пользователей
conn, adr = sock.accept()  # Ожидаю подключения
conn2, adr2 = sock.accept()

conn.send(b'1')
print("Первый игрок!")

conn2.send(b'2')
print("Второй игрок!")

# Игра началась
for map_labyrinth in map_list:
    conn.send(b'N')
    conn2.send(b'N')
    horizon, vertical = loading_map(map_labyrinth, conn, 1)
    loading_map(map_labyrinth, conn2, 2)
    while 1:

        direction = conn.recv(1)

        if direction == b'r' and horizon + 1 < len(map_labyrinth[0]) and map_labyrinth[vertical][horizon + 1] != '.':
            conn2.send(direction)
            step = str(conn2.recv(1))
            step = step[2:len(step) - 1]
            step = int(step)
            winner = check_the_wall(map_labyrinth, vertical, horizon, conn2, horizon_step=step)
        elif direction == b'l' and horizon - 1 >= 0 and map_labyrinth[vertical][horizon - 1] != '.':
            conn2.send(direction)
            step = str(conn2.recv(1))
            step = step[2:len(step) - 1]
            step = int(step)
            winner = check_the_wall(map_labyrinth, vertical, horizon, conn2, horizon_step=-step)
        elif direction == b'd' and vertical + 1 < len(map_labyrinth) and map_labyrinth[vertical + 1][horizon] != '.':
            conn2.send(direction)
            step = str(conn2.recv(1))
            step = step[2:len(step) - 1]
            step = int(step)
            winner = check_the_wall(map_labyrinth, vertical, horizon, conn2, vertical_step=step)
        elif direction == b't' and vertical - 1 >= 0 and map_labyrinth[vertical - 1][horizon] != '.':
            conn2.send(direction)
            step = str(conn2.recv(1))
            step = step[2:len(step) - 1]
            step = int(step)
            winner = check_the_wall(map_labyrinth, vertical, horizon, conn2, vertical_step=-step)
        else:
            conn.send((str(vertical) + ',' + str(horizon)).encode('utf-8'))
            continue

        if winner == "Win":
            conn.send(b'Win')
            conn2.send(b'Win')
            conn2.send(answer.encode())
            break
        else:
            conn.send(winner)
            conn2.send(winner)
            winner = str(winner)
            winner = winner[2:len(winner) - 1]
            winner = winner.split(',')
            vertical = int(winner[0])
            horizon = int(winner[1])
            winner = ''

conn.send(b'E')
conn2.send(b'E')
conn.close()
conn2.close()
sock.close()
