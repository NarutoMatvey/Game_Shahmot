# -*- coding: utf-8 -*-
import socket

conn = socket.socket()

conn.connect(("127.0.0.1", 7000))

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
    print('\n')

