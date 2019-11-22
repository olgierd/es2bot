#!/usr/bin/env python3

import socket
import re

MSGPREFIX = ",,BB,,"
MSGEND = ",,EE,,"
BUFLEN = 80 

def rxloop(fld_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', fld_port))

    buf = [' ']*BUFLEN
    bid=0

    while True:
        d = s.recv(1)
        try:
            c = d.decode("UTF-8")
            buf[bid] = c
            bid = bid+1
            if bid >= BUFLEN:
                bid = 0
        except:
            pass

        msgbuf = ''.join(buf[bid:]) + ''.join(buf[:bid])
#        print(msgbuf)
        
        if parse_buf(msgbuf):
            buf = [' ']*BUFLEN


def parse_buf(msg):
    res = re.findall(MSGPREFIX+".+"+MSGEND, msg)
    if len(res) > 0:
        print("Message received")
        message = res[0][len(MSGPREFIX):-len(MSGEND)]
        print(message)
        return True
    else:
        return None

def parse_command(command):
    return "XD"

rxloop(7324)
