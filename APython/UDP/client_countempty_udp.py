import socket
import struct

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1234
BUFFER_SIZE = 1024

if __name__ == '__main__':
    try:
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        string = input("Enter a message: ")

        socket_udp.sendto(string.encode('ascii'), (SERVER_IP, SERVER_PORT))

        string, _ = socket_udp.recvfrom(BUFFER_SIZE)

        num_spaces, _ = socket_udp.recvfrom(BUFFER_SIZE)
        num_spaces = struct.unpack('!I', num_spaces)[0]

        print("Message received back: {}".format(string.decode('ascii')))
        print("Number of spaces in string: {}".format(num_spaces))

    except socket.error as error:
        print("Error: {}".format(error))
