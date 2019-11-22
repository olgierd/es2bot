#!/usr/bin/python3

import hashlib
import socket
import sys
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 7322))

msg = sys.argv[1]
username, pw = open('creds').read().splitlines()[0].split(':')

timestamp = str(int(time.time()/10))

signature = hashlib.md5((msg + pw + timestamp).encode()).hexdigest()

msg = ",,BB,," + username + ",," + msg + ",," + signature[:5] + ",,EE,,"

s.send(msg.encode())
