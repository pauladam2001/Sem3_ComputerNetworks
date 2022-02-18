import socket
import struct

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1234))
except socket.error as error:
    print("Error: {}".format(error))

number = int(input("Enter the number: "))


try:
    # Send the number
    client_socket.sendall(struct.pack('!I', number))

    # Receive the sum
    f_sum = client_socket.recv(4)
    f_sum = struct.unpack('!I', f_sum)[0]

    print("Final sum: {}".format(f_sum))

except socket.error as error:
    print("Error: {}".format(error))

client_socket.close()
