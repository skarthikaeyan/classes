#!/usr/bin/python3
"""Client Program - Minimum 2 clients needed"""
import socket
import sys
import select
import threading


class StartClient(threading.Thread):
    """Client chat class"""

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientlist = []
        self.name = ''

    def startconnection(self):
        """Connecting to server"""
        self.server.settimeout(2)
        try:
            self.server.connect((self.host, self.port))
        except socket.error as msg:
            print("Can't connect ", msg)
            sys.exit()
        print("Connected to server", )
        sys.stdout.flush()
        self.getuserdata()

    @classmethod
    def waitfordata(cls):
        """Getting user data and flushing the buffer"""
        sys.stdout.write('>')
        sys.stdout.flush()

    @classmethod
    def getuserdata(cls):
        """Getting user data"""
        cls.name = input('Your name: ')
        print('You can start the chat', cls.name)
        cls.name.encode()
        print('Use Ctrl+C to exit', )
        cls.waitfordata()

    def startchat(self):
        """Start to receive and send data simultaneously"""

        while True:
            self.clientlist = [sys.stdin, self.server]
            readsock, writesock, errorsock = select.select(
                self.clientlist, [], [])
            for clients in readsock:
                if clients == self.server:
                    data = clients.recv(2048)
                    if not data:
                        print('\n Disconnected', )
                        self.server.close()
                        sys.exit()
                    else:
                        sys.stdout.write(data.decode('utf-8'))
                        self.waitfordata()

                else:
                    message = sys.stdin.readline()
                    if message == '\n':
                        continue
                    message = self.name + ': ' + message
                    self.server.send(message.encode('utf-8'))
                    self.waitfordata()
                    continue

        self.stop()
