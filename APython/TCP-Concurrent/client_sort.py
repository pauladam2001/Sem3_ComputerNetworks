import socket
import struct

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1234))

except socket.error as error:
    print("Error: {}".format(error))


try:
    len_array = int(input("Enter the length of the array: "))

    # Send the length of the array
    client_socket.sendall(struct.pack('!I', len_array))

    # Send the elements
    for i in range(len_array):
        elem = int(input("Element {}: ".format(i)))
        client_socket.sendall(struct.pack('!I', elem))

    # Receive the length of the result
    len_result = client_socket.recv(4)
    len_result = struct.unpack('!I', len_result)[0]

    # Receive the array
    print("The result: ")
    for i in range(len_result):
        elem = client_socket.recv(4)
        elem = struct.unpack('!I', elem)[0]
        print(elem, end=' ')

except socket.error as error:
    print("Error: {}".format(error))

client_socket.close()
