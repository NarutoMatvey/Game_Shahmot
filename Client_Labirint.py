# -*- coding: utf-8 -*-
import socket

otvet = []
conn = socket.socket()

conn.connect(("127.0.0.1", 7000))

player = conn.recv(1)

while 1:
    Next_End = conn.recv(1)
    if Next_End == b'E':
        print('The End!\nYou Win!')
        break
    # Размер массива

    temp_dan = str(conn.recv(3))
    print(temp_dan)
    temp_dan = temp_dan[2:len(temp_dan)-1]
    razmer = []
    print()
    print(temp_dan)
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
        if player == b'1':
            #Первый пользователь
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
        else:
            #Второй пользователь
            Naprav = conn.recv(1)

            if b'r' == Naprav:
                print('Right')
            elif b'l' == Naprav:
                print('Left')
            elif b't' == Naprav:
                print('Top')
            elif b'd' == Naprav:
                print('Down')

            while 1:
                while 1:
                    Step = input("Сколько клеток пройти?: ").strip()
                    try:
                        if Step > '0' and int(Step) < len(Karta_podgruz):
                            break
                    except:
                        continue
                conn.send(Step.encode())
                temp_peremesh = conn.recv(3)
                if temp_peremesh == b'Non':
                    print('Много!!!')
                    continue
                break

        if temp_peremesh == b'Win':
            print('You Win!')
            if player == b'2':
                otvet += [conn.recv(1)]
                print(otvet)
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