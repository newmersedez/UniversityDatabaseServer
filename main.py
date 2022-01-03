from source.server import *

if __name__ == '__main__':
    server = Server(port=5430)
    server.run()
