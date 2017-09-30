# -*- coding: utf-8 -*-

import socket  # Подключение библиотеки
import karts  # Библиотека с картами
import random  # Библиотека псевда рандома

winer = ''

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
    return goriz, vertical


goriz, vertical = TrevalKarts(karta, conn)


# Проверка возможности
def proverka_na_cctenu(karta, v, g, shag1=0, shag2=0):
    print('#0', v, g, shag1, shag2)
    light = len(karta)
    print('#1', light)
    go = 1
    while 1:
        print('#2', v + shag1, g + shag2 )
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

                print('#3', shag1, shag2)
            else:
                temp1 = v + shag1
                temp2 = g + shag2
                print('#4', temp1, temp2)
                if shag2 < 0 or shag1 < 0:
                    go = -1
                print('#5', go)
                for i in range(v, temp1, go): #Неправильные циклы
                    print('#', i, karta[i][g])
                    if karta[i][g] == '.':
                        if shag1 < 0:
                            shag1 = -light
                        else:
                            shag1 = light
                        break

                for i in range(g, temp2, go):
                    print('#', i, karta[v][i])
                    if karta[v][i] == '.':
                        if shag2 < 0:
                            shag2 = -light
                        else:
                            shag2 = light
                        break

                if shag1 != light and shag2 != light and shag1 != -light and shag2 != -light:
                    while v != temp1:
                        print(karta[v][g])
                        karta[v][g] = '+'
                        print(karta[v][g])
                        v += go

                    while g != temp2:
                        print(karta[v][g])
                        karta[v][g] = '+'
                        print(karta[v][g])
                        g += go

                    if karta[v][g] == 'e':
                        karta[v][g] = 'I'
                        return 'Win'
                    else:
                        print(karta[v][g])
                        karta[v][g] = 'I'
                        print(karta[v][g])
                        return (str(v) + ',' + str(g)).encode('utf-8')

        else:
            # Если смещение на такое число несуществует
            if shag1 == 0:
                if shag2 < 0:
                    shag2 = random.randint(1, light - 1)
                    shag2 = -shag2
                else:
                    shag2 = random.randint(1, light - 1)
                print('#9', shag2)
            elif shag1 < 0:
                shag1 = random.randint(1, light - 1)
                shag1 = -shag1
                print('#10', shag1)
            else:
                shag1 = random.randint(1, light - 1)
                print('#11', shag1)


# Игра началась
while 1:
    naprawlenie = conn.recv(1)
    shag = random.randint(1, len(karta) - 1)
    print("Новый этап \n")
    if naprawlenie == b'r' and goriz + 1 < len(karta[0]) and karta[vertical][goriz + 1] != '.':
        winer = proverka_na_cctenu(karta, vertical, goriz, shag2=shag)
    elif naprawlenie == b'l' and goriz - 1 >= 0 and karta[vertical][goriz - 1] != '.':
        input()
        winer = proverka_na_cctenu(karta, vertical, goriz, shag2=-shag)
    elif naprawlenie == b'd' and vertical + 1 < len(karta) and karta[vertical + 1][goriz] != '.':
        winer = proverka_na_cctenu(karta, vertical, goriz, shag1=shag)
    elif naprawlenie == b't' and vertical - 1 > 0 and karta[vertical - 1][goriz] != '.':
        winer = proverka_na_cctenu(karta, vertical, goriz, shag1=-shag)
    else:
        conn.send((str(vertical) + ',' + str(goriz)).encode('utf-8'))
        continue

    print('# ', winer)
    if winer == "Win":
        conn.send(b'Win')
        break
    else:
        conn.send(winer)
        winer = str(winer)
        winer = winer[2:len(winer)-1]
        winer = winer.split(',')
        vertical = int(winer[0])
        goriz = int(winer[1])
        winer = ''

conn.close()
sock.close()