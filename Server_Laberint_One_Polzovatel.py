# -*- coding: utf-8 -*-

import socket  # Подключение библиотеки
import karts  # Библиотека с картами
import random  # Библиотека псевда рандома

winer = ''
goriz = 0
vertical = 0

# Можно будет выделить в блок
sock = socket.socket()  # Создание сокета

sock.bind(('localhost', 7000))  # Настраиваю определённый порт для общения с клиентом

sock.listen(1)  # Создаю очередь пользователей

conn, adr = sock.accept()  # Ожидаю подключения

# Блок взаимодействия с картой

karta = karts.Karts.raznoobrazie[1]


def TrevalKarts(karta, conn):
    # Отправляет размер карты
    conn.send((str(len(karta)) + ',' + str(len(karta[0]))).encode('utf-8'))

    # Отправляет карту
    for i in range(len(karta)):
        for j in range(len(karta[i])):
            if karta[i][j] == 'I':
                goriz = j
                vertical = i
            conn.send(karta[i][j].encode('utf-8'))


TrevalKarts(karta, conn)


# Проверка возможности
def proverka_na_cctenu(karta, v, g, shag1=0, shag2=0):
    light = len(karta)
    go = 1
    while 1:
        if 0 <= v + shag1 < light and 0 <= g + shag2 < light:
            if karta[v + shag1][g + shag2] == '.':
                if shag1 == 0:
                    shag2 = light
                else:
                    shag1 = light
            else:
                temp1 = v + shag1
                temp2 = g + shag2
                if shag2 < 0 or shag1 < 0:
                    go = -1

                while v != temp1:
                    karta[v][g] = '+'
                    v += go

                while g != temp2:
                    karta[v][g] = '+'
                    g += go

                if karta[v][g] == 'e':
                    karta[v][g] = 'I'
                    return 'Win'
                else:
                    karta[v][g] = 'I'
                    return ''

        else:
            # Если смещение на такое число несуществует
            if shag1 == 0:
                if shag2 < 0:
                    shag2 = random.randint(1, light - 1)
                    shag2 = -shag2
                else:
                    shag2 = random.randint(1, light - 1)
            elif shag1 < 0:
                shag1 = random.randint(1, light - 1)
                shag1 = -shag1
            else:
                shag1 = random.randint(1, light - 1)


# Игра началась
while 1:
    naprawlenie = conn.recv(1)
    shag = random.randint(1, len(karta) - 1)
    if naprawlenie == b'r':
        winer = proverka_na_cctenu(karta, vertical, goriz, shag2=shag)
    elif naprawlenie == b'l':
        winer = proverka_na_cctenu(karta, vertical, goriz, shag2=-shag)
    elif naprawlenie == b'd':
        winer = proverka_na_cctenu(karta, vertical, goriz, shag1=-shag)
    elif naprawlenie == b't':
        winer = proverka_na_cctenu(karta, vertical, goriz, shag1=shag)

    if winer == "Win":
        conn.send(b'Win')
        break
    else:
        conn.send((str(vertical) + ',' + str(goriz)).encode('utf-8'))
