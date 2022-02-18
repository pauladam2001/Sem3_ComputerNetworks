import socket
import struct


SERVER_IP = '127.0.0.1'
SERVER_PORT = 1234

# Create, bind and listen for the server socket.
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
except socket.error as error:
    print("Error: {}".format(error))

# Connect to client and work.
try:

    while True:
        # Receive the number
        client_socket, addr = server_socket.accept()

        number = client_socket.recv(4)
        number = struct.unpack('!I', number)[0]

        # Compute the divisors
        divisors = [1]
        num_divisors = 1
        for i in range(2, number // 2 + 1):
            if number % i == 0:
                num_divisors += 1
                divisors.append(i)
        num_divisors += 1
        divisors.append(number)

        # Send the divisors:
        client_socket.sendall(struct.pack('!I', num_divisors))

        for divisor in divisors:
            client_socket.sendall(struct.pack('!I', divisor))

except socket.error as error:
    print("Error: {}".format(error))