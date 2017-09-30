# -*- coding: utf-8 -*-
import socket

conn = socket.socket()

conn.connect(("127.0.0.1", 7000))

while 1:
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
            Karta_podgruz[i] += [temp_dan]
            if temp_dan == 'I':
                vert, gor = i, j

    for i in range(razmer[0]):
        print(Karta_podgruz[i])


    # Игра началась
    while 1:
        Naprav = input("Выбирайте направление: ").strip()

        if 'R' in Naprav or 'r' in Naprav:
            conn.send(b'r')
        elif 'L' in Naprav or 'l' in Naprav:
            conn.send(b'l')
        elif 'T' in Naprav or 't' in Naprav:
            conn.send(b't')
        elif 'D' in Naprav or 'd' in Naprav:
            conn.send(b'd')
        else:
            continue

        temp_peremesh = conn.recv(3)
        if temp_peremesh == b'Win':
            print('You Win!')
            break

        temp_peremesh = str(temp_peremesh)
        temp_peremesh = temp_peremesh[2:len(temp_peremesh)-1]
        temp_peremesh = temp_peremesh.split(',')

        koo = 1
        if vert == int(temp_peremesh[0]):
            if int(temp_peremesh[1]) < gor :
                koo  = -1
            while gor != int(temp_peremesh[1]):
                Karta_podgruz[vert][gor] = '+'
                gor += koo
        else:
            if int(temp_peremesh[0]) < vert :
                koo  = -1
            while vert != int(temp_peremesh[0]):
                Karta_podgruz[vert][gor] = '+'
                vert += koo

        Karta_podgruz[vert][gor] = 'I'

        for i in range(len(Karta_podgruz)):
            print(Karta_podgruz[i])

conn.close()