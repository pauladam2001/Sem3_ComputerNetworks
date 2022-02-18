import socket
import struct

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1234
BUFFER_SIZE = 1024

if __name__ == '__main__':

    try:
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        socket_udp.bind((SERVER_IP, SERVER_PORT))

        message, addr = socket_udp.recvfrom(BUFFER_SIZE)
        message = message.decode('ascii')
        print("Received message: {}".format(message))

        socket_udp.sendto(message.encode('ascii'),  ('<broadcast>', 1234))

    except socket.error as error:
        print("Error: {}".format(error))
