# -*- coding: utf-8 -*-
import socket  # Подключение библиотеки
import karts  # Библиотека с картами
import random  # Библиотека псевда рандома

global otvet
# Функции

# Блок взаимодействия с картой
def TrevalKarts(karta, conn, player):
    # Отправляет размер карты
    global otvet
    conn.send((str(len(karta)) + ',' + str(len(karta[0]))).encode('utf-8'))

    # Отправляет карту
    for i in range(len(karta)):
        for j in range(len(karta[i])):
            if karta[i][j] == 'I':
                goriz = j
                vertical = i
            elif 'a' <= karta[i][j] <= 'z':
                otvet = karta[i][j]
                print(otvet)
                karta[i][j] = 'E'
            if player == 2:
                if karta[i][j] == 'I':
                    conn.send(karta[i][j].encode('utf-8'))
                else:
                    conn.send(b'.')
            else:
                conn.send(karta[i][j].encode('utf-8'))
    return goriz, vertical


# Проверка возможности
def proverka_na_cctenu(karta, v, g, conn2 = None, shag1=0, shag2=0):

    light = len(karta)
    go = 1
    while 1:
        if 0 <= v + shag1 < light and 0 <= g + shag2 < light:
            if karta[v + shag1][g + shag2] == '.':
                if shag1 == 0:
                    if shag2 < 0:
                        shag2 = -light
                    else:
                        shag2 = light
                else:
                    if shag1 < 0:
                        shag1 = -light
                    else:
                        shag1 = light
            else:
                temp1 = v + shag1
                temp2 = g + shag2
                if shag2 < 0 or shag1 < 0:
                    go = -1
                for i in range(v, temp1, go):  # Неправильные циклы
                    if karta[i][g] == '.':
                        if shag1 < 0:
                            shag1 = -light
                        else:
                            shag1 = light
                        break

                for i in range(g, temp2, go):
                    if karta[v][i] == '.':
                        if shag2 < 0:
                            shag2 = -light
                        else:
                            shag2 = light
                        break

                if shag1 != light and shag2 != light and shag1 != -light and shag2 != -light:
                    while v != temp1:
                        karta[v][g] = '+'
                        v += go

                    while g != temp2:
                        karta[v][g] = '+'
                        g += go

                    if karta[v][g] == 'E':
                        karta[v][g] = 'I'
                        return 'Win'
                    else:
                        karta[v][g] = 'I'
                        return (str(v) + ',' + str(g)).encode('utf-8')

        else:
            # Если смещение на такое число несуществует
            conn2.send(b'Non')
            if shag1 == 0:
                if shag2 < 0:
                    shag2 = str(conn2.recv(1))
                    shag2 = shag2[2:len(shag2)-1]
                    shag2 = int(shag2)
                    shag2 = -shag2
                else:
                    shag2 = str(conn2.recv(1))
                    shag2 = shag2[2:len(shag2)-1]
                    shag2 = int(shag2)
            elif shag1 < 0:
                shag1 = str(conn2.recv(1))
                shag1 = shag1[2:len(shag1)-1]
                shag1 = int(shag1)
                shag1 = -shag1
            else:
                shag1 = str(conn2.recv(1))
                shag1 = shag1[2:len(shag1)-1]
                shag1 = int(shag1)

karta_mass = karts.Karts()
karta_mass = karta_mass.Randomaiz()

# Можно будет выделить в блок
sock = socket.socket()  # Создание сокета

sock.bind(('localhost', 7000))  # Настраиваю определённый порт для общения с клиентом

sock.listen(2)  # Создаю очередь пользователей

conn, adr = sock.accept()  # Ожидаю подключения
conn.send(b'1')
print("Первый игрок!")

conn2, adr2 = sock.accept()
conn2.send(b'2')
print("Второй игрок!")
# Игра началась
for karta in karta_mass:
    conn.send(b'N')
    conn2.send(b'N')
    goriz, vertical = TrevalKarts(karta, conn, 1)
    TrevalKarts(karta, conn2, 2)
    while 1:

        naprawlenie = conn.recv(1)

        if naprawlenie == b'r' and goriz + 1 < len(karta[0]) and karta[vertical][goriz + 1] != '.':
            conn2.send(naprawlenie)
            shag = str(conn2.recv(1))
            shag = shag[2:len(shag) - 1]
            shag = int(shag)
            winer = proverka_na_cctenu(karta, vertical, goriz, conn2, shag2=shag)
        elif naprawlenie == b'l' and goriz - 1 >= 0 and karta[vertical][goriz - 1] != '.':
            conn2.send(naprawlenie)
            shag = str(conn2.recv(1))
            shag = shag[2:len(shag)-1]
            shag = int(shag)
            winer = proverka_na_cctenu(karta, vertical, goriz, conn2, shag2=-shag)
        elif naprawlenie == b'd' and vertical + 1 < len(karta) and karta[vertical + 1][goriz] != '.':
            conn2.send(naprawlenie)
            shag = str(conn2.recv(1))
            shag = shag[2:len(shag) - 1]
            shag = int(shag)
            winer = proverka_na_cctenu(karta, vertical, goriz, conn2, shag1=shag)
        elif naprawlenie == b't' and vertical - 1 >= 0 and karta[vertical - 1][goriz] != '.':
            conn2.send(naprawlenie)
            shag = str(conn2.recv(1))
            shag = shag[2:len(shag) - 1]
            shag = int(shag)
            winer = proverka_na_cctenu(karta, vertical, goriz, conn2, shag1=-shag)
        else:
            conn.send((str(vertical) + ',' + str(goriz)).encode('utf-8'))
            continue

        if winer == "Win":
            conn.send(b'Win')
            conn2.send(b'Win')
            conn2.send(otvet.encode())
            break
        else:
            conn.send(winer)
            conn2.send(winer)
            winer = str(winer)
            winer = winer[2:len(winer) - 1]
            winer = winer.split(',')
            vertical = int(winer[0])
            goriz = int(winer[1])
            winer = ''

conn.send(b'E')
conn2.send(b'E')
conn.close()
conn2.close()
sock.close()
