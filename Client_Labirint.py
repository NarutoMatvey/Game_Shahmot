# -*- coding: utf-8 -*-
import socket

conn = socket.socket()

conn.connect(("127.0.0.1", 7000))

vert, gor = 0, 0

# Размер массива
temp_dan = str(conn.recv(5))
temp_dan = temp_dan[2:len(temp_dan)-1]
razmer = []
for i in temp_dan.split(','):
    razmer += [int(i)]

# Подгружаю карту
Karta_podgruz = []
for i in range(razmer[0]):
    Karta_podgruz += [[]]
    for j in range(razmer[1]):
        temp_dan = str(conn.recv(1))
        temp_dan = temp_dan[2:len(temp_dan) - 1]
        print(temp_dan, end='')
        Karta_podgruz[i] += [temp_dan]
        if temp_dan == 'I':
            vert, gor = i, j
    print('\n')

# Игра началась
while 1:
    Naprav = input("Выбирайте направление: ").strip()

    if 'R' in Naprav or 'r' in Naprav:
        conn.send(b'r')
    elif 'L' in Naprav or 'l' in Naprav:
        conn.send(b'l')
    elif 'T' in Naprav or 't' in Naprav:
        conn.send(b't')
    elif 'B' in Naprav or 'b' in Naprav:
        conn.send(b'b')
    else:
        continue

    temp_peremesh = conn.recv(3)
    if temp_peremesh == b'Win':
        print('You Win!')
        break

conn.close()