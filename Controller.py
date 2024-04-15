import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 20000)
sock.bind(server_address)

sock.listen(1)

CLIENTS = [][]

def listen_for_clients():
    while True:
        connection, client_address = sock.accept()

        print('connection from', client_address)
        