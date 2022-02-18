import socket
import threading
import random
import struct
import sys
import time

random.seed()
start = 1
stop = 2 ** 17 - 1
my_num = random.randint(start, stop)
print('Server number: ', my_num)
my_lock = threading.Lock()
client_guessed = False
winner_thread = 0
event = threading.Event() # e un semnal folosit de un thread ca sa notifice alte threaduri
event.clear()
threads = []
client_count = 0


def worker(client_socket):
    global my_lock, client_guessed, my_num, winner_thread, client_count, event

    my_id = client_count
    print('client #', client_count, 'from: ', client_socket.getpeername())
    message = 'Hello client #' + str(client_count) + ' ! You are entering the number guess competition now !'
    client_socket.sendall(bytes(message, 'ascii'))

    while not client_guessed:
        try:
            client_number = client_socket.recv(4)
            client_number = struct.unpack('!I', client_number)[0]
            if client_number > my_num:
                client_socket.sendall(b'S')
            if client_number < my_num:
                client_socket.sendall(b'H')
            if client_number == my_num:
                my_lock.acquire()
                client_guessed = True
                winner_thread = threading.get_ident()
                my_lock.release()

        except socket.error as message:
            print('Error:', message.strerror)
            break

    if client_guessed:
        if threading.get_ident() == winner_thread:
            client_socket.sendall(b'G')
            print('We have a winner', client_socket.getpeername())
            print("Thread ", my_id, " winner")
            event.set()
        else:
            client_socket.sendall(b'L')
            print("Thread ", my_id, " looser")
    time.sleep(1)
    client_socket.close()
    print("Worker Thread ", my_id, " end")


def resetSrv():
    global my_lock, client_guessed, winner_thread, my_num, threads, event, client_count
    while True:
        event.wait()
        for thread in threads:
            thread.join()
        print("all threads are finished now")
        event.clear()
        my_lock.acquire()
        threads = []
        client_guessed = False
        winner_thread = -1
        client_count = 0
        my_num = random.randint(start, stop)
        print('Server number: ', my_num)
        my_lock.release()


if __name__ == '__main__':
    try:
        welcoming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        welcoming_socket.bind(('0.0.0.0', 1234))
        welcoming_socket.listen(5)
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)
    new_thread = threading.Thread(target=resetSrv, daemon=True)   # daemon threads run in the background
    new_thread.start()

    while True:
        client_socket, client_info = welcoming_socket.accept()
        new_thread = threading.Thread(target=worker, args=(client_socket,))
        threads.append(new_thread)
        client_count += 1
        new_thread.start()

