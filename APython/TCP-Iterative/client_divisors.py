import socket
import struct


try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1234))
except socket.error as error:
    print("Error: {}".format(error))


number = int(input("Enter the number: "))

try:
    client_socket.sendall(struct.pack('!I', number))

    num_divisors = client_socket.recv(4)
    num_divisors = struct.unpack('!I', num_divisors)[0]
    print("Number of divisors: {}".format(num_divisors))

    print("Divisors: ")
    for i in range(num_divisors):
        divisor = client_socket.recv(4)
        divisor = struct.unpack('!I', divisor)[0]
        print(divisor, end=' ')

except socket.error as error:
    print("Error: {}".format(error))

client_socket.close()
