import socket
import struct

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1234
BUFFER_SIZE = 1024


def count_spaces(s):
    count = 0
    for i in range(len(s)):
        if s[i] == ' ':
            count += 1
    return count


if __name__ == '__main__':

    try:
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_udp.bind((SERVER_IP, SERVER_PORT))
    except socket.error as error:
        print("Error: {}".format(error))

    try:
        while True:
            string, addr = socket_udp.recvfrom(BUFFER_SIZE)
            string = string.decode('ascii')

            print("Message received: ".format(string))
            num_spaces = count_spaces(string)
            print("Number of spaces computed: {}".format(num_spaces))

            socket_udp.sendto(string.encode('ascii'), addr)
            socket_udp.sendto(struct.pack('!I', num_spaces), addr)

    except socket.error as error:
        print("Error: {}".format(error))


