import socket
import struct

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1234))
except socket.error as error:
    print("Error: {}".format(error))


string = input("Enter the string: ")

try:

    # Send the string.
    client_socket.sendall(bytes(string, 'ascii'))

    # Receive the number of spaces.
    num_spaces = client_socket.recv(4)
    num_spaces = struct.unpack('!I', num_spaces)[0]

    print("Number of spaces: {}".format(num_spaces))

except socket.error as error:
    print("Error: {}".format(error))

client_socket.close()
