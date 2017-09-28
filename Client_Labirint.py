# -*- coding: utf-8 -*-
import socket

conn = socket.socket()

conn.connect(("127.0.0.1", 5000))

hod = conn.recv(1024)
