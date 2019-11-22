#!/usr/bin/env python3

import hashlib
import socket
import re
import time

MSGPREFIX = ",,BB,,"
MSGEND = ",,EE,,"
BUFLEN = 200


class MessageParser:

    def __init__(self, port, credsfile):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.creds = self.read_creds(credsfile)

    def start_rx(self):
        self.s.connect(('127.0.0.1', self.port))

        buf = [' ']*BUFLEN
        bid = 0

        while True:
            d = self.s.recv(1)
            try:
                c = d.decode("UTF-8")
                buf[bid] = c
                bid = bid+1
                if bid >= BUFLEN:
                    bid = 0
            except UnicodeDecodeError:
                pass

            msgbuf = ''.join(buf[bid:]) + ''.join(buf[:bid])

            if self.parse_buf(msgbuf):
                buf = [' ']*BUFLEN

    def parse_buf(self, msg):
        res = re.findall(MSGPREFIX+".+"+MSGEND, msg)
        if len(res) > 0:
            message = res[0][len(MSGPREFIX):-len(MSGEND)]
            print("Message received:", message)
            msg = message.split(',,')
            call, signature = msg[0], msg[-1]
            content = message[(len(call)+2):-(len(signature)+2)]
            if self.check_validity(call, content, signature):
                self.parse_command(call, content)
            return True
        else:
            return None

    def check_validity(self, call, message, signature_rx):

        if call not in self.creds:
            print("Invalid callsign")
            return

        stamps = [str(int(time.time()/10)+shift) for shift in range(-6, 7)]

        for stamp in stamps:
            verification = (message + self.creds[call] + stamp).encode()
            signature_hash = hashlib.md5(verification).hexdigest()[:5]
            if signature_hash == signature_rx:
                print(f"The message from {call} is authentic.")
                return True

        print(f"AUTH FAILED for {call}")
        return False

    def read_creds(self, filename):
        creds = {}
        for x in open(filename).read().splitlines():
            if len(x) > 0:
                d = x.split(':')
                creds[d[0]] = d[1]
        return creds

    def parse_command(self, call, command):
        if 'hello' in command:
            self.send_message(f"Hello, {call}!")

    def send_message(self, message):
        self.s.send(message.encode())


mp = MessageParser(7324, 'people.txt')
mp.start_rx()
