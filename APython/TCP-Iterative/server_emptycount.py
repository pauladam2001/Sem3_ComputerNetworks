import socket
import struct


# Create, bind and listen for the server socket.
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 1234))
    server_socket.listen(5)
except socket.error as error:
    print("Error: {}".format(error))

# Connect to client and work.
try:

    while True:
        client_socket, _ = server_socket.accept()

        # Receive the string
        string = client_socket.recv(1024)
        string = string.decode('ascii')

        # Count the empty spaces
        count = 0
        for i in range(len(string)):
            if string[i] == ' ':
                count += 1

        # Send the result
        client_socket.sendall(struct.pack('!I', count))

except socket.error as error:
    print("Error: {}".format(error))
