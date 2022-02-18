import socket
import struct
import threading
import time

clients = []
lock = threading.Lock()
e = threading.Event()
e.clear()
threads = []
stopping_thread = -1
client_count = 0
f_sum = 0
done = False


def worker(c_socket):
    global lock, done, threads, e, stopping_thread, client_count, f_sum

    my_id_count = client_count
    print("Client {} from {}".format(c_socket.getpeername(), c_socket))

    try:

        # Receive a number
        number = c_socket.recv(4)
        number = struct.unpack('!I', number)[0]

        if number != 0:
            lock.acquire()
            f_sum = f_sum + number
            lock.release()

        if number == 0:
            lock.acquire()
            done = True
            stopping_thread = threading.get_ident()
            lock.release()

    except socket.error as error:
        print("Error: {}".format(error))

    if done:
        e.set()

    time.sleep(1)
    print("Thread {} end.\n".format(my_id_count))


def reset_server():
    global lock, done, threads, stopping_thread, e, client_count, f_sum, clients

    while True:
        e.wait()

        for cs in clients:
            cs.sendall(struct.pack('!I', f_sum))
            cs.close()

        for t in threads:
            t.join()

        print("All threads are finished now.")
        e.clear()
        lock.acquire()
        threads = []
        done = False
        client_count = 0
        clients = []
        f_sum = 0
        stopping_thread = -1
        lock.release()


if __name__ == '__main__':
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 1234))
        server_socket.listen(5)
    except socket.error as error:
        print("Error: {}".format(error))
        exit(1)

    t = threading.Thread(target=reset_server, daemon=True)
    t.start()

    try:

        while True:
            client_socket, addr = server_socket.accept()
            t = threading.Thread(target=worker, args=(client_socket,))
            threads.append(t)
            client_count += 1
            clients.append(client_socket)
            t.start()

    except socket.error as error:
        print("Error: {}".format(error))
