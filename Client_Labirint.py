# -*- coding: utf-8 -*-
import socket

conn = socket.socket()

conn.connect(("127.0.0.1", 7000))

# Размер массива
temp = str(conn.recv(5))
temp = temp[2:len(temp)-1]
razmer = []
for i in temp.split(','):
    razmer += [int(i)]

