import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
server_address = ('10.0.0.100', 20000)
sock.connect(server_address)

def main():
    while True:
        message = sock.recv(16)
        print('received "%s" from the server' % message)

        # Send a response to the server
        sock.sendall(b'I received the message.')

        # Receive a message from the server to close the connection
        message = sock.recv(16)
        print('received "%s" from the server' % message)