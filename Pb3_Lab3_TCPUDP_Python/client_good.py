import select
import socket
import struct
import sys
import threading


def communication_thread():
    try:
        while True:
            # Listen for incoming messages from the server (self_tcp_socket) or other clients(self_udp_socket)
            sockets, _, _ = select.select([self_tcp_socket, self_udp_socket], [], [])
            if self_tcp_socket in sockets:
                operation = self_tcp_socket.recv(1)
                ip = socket.inet_ntoa(self_tcp_socket.recv(4))
                port = struct.unpack("!H", self_tcp_socket.recv(2))[0]

                if operation == b'L':
                    print("Client " + ip + ":" + str(port) + " left the chatroom.")
                    other_clients.discard((ip, port))
                elif operation == b'N':
                    print("Client " + ip + ":" + str(port) + " joined the chatroom.")
                    other_clients.add((ip, port))
                else:
                    print("Unknown operation received from server")
            
            if self_udp_socket in sockets:
                message, adress = self_udp_socket.recvfrom(256)
                print("Client", adress[0] + ":" + str(adress[1]), "-", message.decode())
    except OSError as osError:
        self_tcp_socket.close()
        self_udp_socket.close()
        print("OSError:", osError.strerror)
        print("Type 'Q' to quit:")


if __name__ == "__main__":
    # Connect to the server:
    self_tcp_socket = socket.socket()
    self_tcp_socket.connect((sys.argv[1], int(sys.argv[2])))

    # Receive the list of existing clients from the server:
    number_of_clients = struct.unpack("!I", self_tcp_socket.recv(4))[0]
    other_clients = set() # Store them in a set.
    for _ in range(number_of_clients):
        other_clients.add((
            socket.inet_ntoa(self_tcp_socket.recv(4)),
            struct.unpack("!H", self_tcp_socket.recv(2))[0]
        ))
    
    # Create the UDP socket used to communicate with all other clients:
    self_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Do a random sent to "nowhere", to force the OS to properly allocate the port.
    self_udp_socket.sendto(b'random', ('8.8.8.8', 2355))

    # Now we can get the port associated to this socket and send it to the server
    # which will then send it to all other clients
    _, self_udp_port = self_udp_socket.getsockname()
    print("My UDP port is:", str(self_udp_port))
    self_tcp_socket.send(struct.pack("!H", self_udp_port))

    # Start the thread which will handle incoming messages from other clients and the server
    # daemon = True so that the thread will stop when the main thread stops.
    threading.Thread(target=communication_thread, daemon=True).start()

    while True:
        # Accept user_input (a "chat message") and send it to all other clients,
        # or leave the chat room and stop if the user input is "Q
        user_input = input()
        if user_input == "Q":
            # Tell the server we are leaving:
            self_tcp_socket.send(b'L')
            print("Leaving the chat room and shutting down...")
            self_tcp_socket.close()
            self_udp_socket.close()
            exit(0)
        for other_client in other_clients:
            self_udp_socket.sendto(user_input.encode(), other_client)