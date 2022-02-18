import select
import socket
import struct
import threading


def connection_thread():
    print("Starting thread...")

    listening_sock = socket.create_server(('', 1024))
    listening_sock.listen()

    clients = {}  # <socket_tcp : (ip, port_udp))
    select_socket_rlist = [listening_sock]

    while True:
        # Get a list of all the sockets from which there is data to be read at the current time
        rlist, _, _ = select.select(select_socket_rlist, [], [])
        for sock in rlist:

            # If a new client wants to connect:
            if sock == listening_sock:
                client_socket, (client_ip, _) = listening_sock.accept()

                # Send this new client the number of existing clients
                client_socket.sendall(struct.pack("!I", len(clients)))

                # Send the ip and UDP port of all existing clients to this new client,
                # so that the new client may communicate with them.
                for other_client_socket in clients:
                    other_client = clients[other_client_socket]
                    client_socket.sendall(other_client[0])
                    client_socket.sendall(struct.pack("!H", other_client[1]))

                # Receive the new client's UDP port and store it in a pair:
                new_client = (
                    socket.inet_aton(client_ip),
                    struct.unpack("!H", client_socket.recv(2))[0]
                )
                print("New client connected:", client_ip + ":" + str(new_client[1]))

                # Send the new client's info to all other clients:
                for other_client_socket in clients:
                    other_client_socket.send(b'N')  # N for 'new client'
                    other_client_socket.send(new_client[0])
                    other_client_socket.send(struct.pack("!H", new_client[1]))

                # Add the new client to the dictionary and the select list:
                clients[client_socket] = new_client
                select_socket_rlist.append(client_socket)

            else:
                operation = sock.recv(1)  # can be only b'L'
                if operation == b'L':  # L for 'leave'
                    # Close the socket with the client that just left and delete him from the dictionary
                    print("Client is leaving...")
                    sock.close()
                    deleted_client = clients[sock]
                    del clients[sock]
                    select_socket_rlist.remove(sock)
                    # Tell all other clients that this client has leaving:
                    for other_client_socket in clients:
                        other_client_socket.send(b'L')
                        other_client_socket.send(deleted_client[0])
                        other_client_socket.send(struct.pack("!H", deleted_client[1]))
                else:
                    print("Unknown operation code.")


if __name__ == "__main__":
    # daemon = True so that the thread will stop when the main thread calls 'exit'
    threading.Thread(target=connection_thread, daemon=True).start()

    # For stopping the server
    while True:
        user_input = input()
        if user_input == "Q":
            print("Shutting down...")
            exit(0)
