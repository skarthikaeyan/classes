"""Multi-Chat server application"""
import socket
import sys
import select
import threading


class StartServer(threading.Thread):
    """Server Class"""

    def __init__(self, port=10000):
        threading.Thread.__init__(self)
        self.host = ''
        self.port = port
        self.clientlist = []
        self.hostname = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def socketbind(self):
        """Binds host and port to form socket"""

        try:
            self.server.bind((self.host, self.port))
        except socket.error as msg:
            print('Check IP and Port number', msg)
            sys.exit()
        self.server.listen(100)
        self.clientlist.append(self.server)
        self.serverinfo(self.host, self.port)

    @classmethod
    def serverinfo(cls, host, port):
        """Prints server details"""
        print('Server Started on port: ', port)
        print('IP address', host)
        print('Ctrl+C to halt', )
        print('Waiting for client', )

    @classmethod
    def receivedata(cls, sock):
        """Receiving data"""
        data = ''
        data = sock.recv(2048)
        return data

    def broadcast(self, sock, message):
        """Send messages to all active clients"""

        for clients in self.clientlist:
            if message:
                if clients != self.server and clients != sock:
                    try:
                        clients.send(message)
                    except socket.error:
                        clients.close()
                        self.clientlist.remove(clients)
            else:
                if clients in self.clientlist:
                    self.clientlist.remove(clients)

    def validate(self):
        """Validates if socket is ready"""
        while True:
            try:
                readsock, writesock, errorsock = select.select(
                    self.clientlist, [], [])
            except socket.error:
                continue
            else:
                # self.runserver(readsock)
                for sock in readsock:
                    if sock == self.server:
                        try:
                            conn, addr = self.server.accept()
                        except socket.error:
                            break
                        else:
                            self.clientlist.append(conn)
                            print('Connected on: ', addr)
                    else:
                        try:
                            data = self.receivedata(sock)
                            self.broadcast(sock, data)
                        except socket.error:
                            sock.close()
                            self.clientlist.remove(sock)
                            continue
        self.stop()
