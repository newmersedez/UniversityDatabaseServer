from socket import socket, AF_INET, SOCK_STREAM
from os import getpid
from source.connect import *

class Server:
    def __init__(self, host='localhost', port=1234):
        self._socket = None
        self._host = host
        self._port = port

    def run(self):
        print('Server PID = {}'.format(getpid()))
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self._host, self._port))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print(data)
                    except ConnectionError:
                        pass
                    except KeyboardInterrupt:
                        print("press control-c again to quit")
