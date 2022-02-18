import struct
import socket
import threading
import time

lock = threading.Lock()
e = threading.Event()
threads = []
clients = []
result = []
client_count = 0
done = False


def worker(cs):
    global lock, e, result, client_count, done

    my_id_count = client_count
    print("Client {} from {}".format(cs.getpeername(), cs))

    try:

        len_array = cs.recv(4)
        len_array = struct.unpack('!I', len_array)[0]

        for i in range(len_array):
            elem = cs.recv(4)
            elem = struct.unpack('!I', elem)[0]
            lock.acquire()
            result.append(elem)
            lock.release()

        if len_array == 0:
            lock.acquire()
            done = True
            result.sort()
            lock.release()

    except socket.error as error:
        print("Error: {}".format(error))

    if done:
        e.set()

    time.sleep(1)
    print("Thread {} finished.".format(my_id_count))


def reset_server():
    global lock, e, done, threads, clients, result, client_count

    while True:
        e.wait()

        for c in clients:
            c.sendall(struct.pack('!I', len(result)))

            for elem in result:
                c.sendall(struct.pack('!I', elem))

        for t in threads:
            t.join()

        print("All threads are finished.")
        e.clear()
        lock.acquire()
        threads = []
        clients = []
        result = []
        done = False
        client_count = 0
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
            client_socket, _ = server_socket.accept()
            t = threading.Thread(target=worker, args=(client_socket,))
            threads.append(t)
            clients.append(client_socket)
            client_count += 1
            t.start()

    except socket.error as error:
        print("Error: {}".format(error))