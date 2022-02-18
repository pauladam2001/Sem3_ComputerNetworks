import socket
import struct

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1234
BUFFER_SIZE = 1024

if __name__ == '__main__':

    try:
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        message = input("Enter a message for broadcast: ")
        message = message.encode('ascii')

        socket_udp.sendto(message, (SERVER_IP, SERVER_PORT))

        answer, addr = socket_udp.recvfrom(BUFFER_SIZE)
        answer = answer.decode('ascii')
        print("Received message: {}".format(message))
    except socket.error as error:
        print("Error: {}".format(error))
