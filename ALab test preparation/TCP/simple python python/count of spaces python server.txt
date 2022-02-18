import socket
import struct
from multiprocessing import Process

def treat_request(connection_socket):
    string = connection_socket.recv(1024)
    string = string.decode("ascii")

    spaces_count = string.count(' ')
    spaces_count = struct.pack("!I", spaces_count)
    connection_socket.send(spaces_count)
    connection_socket.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 1234)) # listen on every address of the server
    s.listen(10)
    clients = []
    while True:
        print('Listening for incoming connections....')
        connection_socket, client_info = s.accept()

        string = connection_socket.recv(1024)
        string = string.decode("ascii")

        spaces_count = string.count(' ')
        spaces_count = struct.pack("!I", spaces_count)
        connection_socket.send(spaces_count)
        connection_socket.close()

        #new_client = Process(target=treat_request, args=(connection_socket,))
        #clients.append(new_client)
        #new_client.start()
        #new_client.join()

main()