import socket
import struct
import sys
import time
import threading
import datetime
import re

port = 7777


def timequery_worker(sock):
    while True:
        time.sleep(3)
        message = 'TIMEQUERY'
        print('Sending timequery')
        sock.sendto(message.encode(), (broadcast_addr, port))


def datequery_worker(sock):
    while True:
        time.sleep(10)
        message = 'DATEQUERY'
        print('Sending datequery')
        sock.sendto(message.encode(), (broadcast_addr, port))


def process_request(sock):
    while True:
        message, address = sock.recvfrom(32)
        message = message.decode()
        if message == 'TIMEQUERY':
            my_time = 'TIME ' + time.strftime("%H:%M:%S")
            sock.sendto(my_time.encode(), address)
        elif message == 'DATEQUERY':
            my_date = 'DATE ' + str(datetime.date.today())
            sock.sendto(my_date.encode(), address)
        elif re.search("TIME [0-9][0-9]:[0-9][0-9]:[0-9][0-9]", message):
            print("Got time")
            # hostname = socket.gethostname()
            # ip = socket.gethostbyname(hostname)
            # print(ip)
            # port = socket.getsockname()[1]
            print(address[0], address[1])
        elif re.search("DATE [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", message):
            print("Got date")
        else:
            print("Malformed")


# my_time = 'TIME ' + time.strftime("%H:%M:%S")
# print(my_time)
# my_date = 'DATE ' + str(datetime.date.today())
# print(my_date)


client_scoket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_scoket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_scoket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# client_scoket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

client_scoket.bind(("", port))

broadcast_addr = sys.argv[1]

tqthread = threading.Thread(target=timequery_worker, args=(client_scoket,))
dqthread = threading.Thread(target=datequery_worker, args=(client_scoket,))
prthread = threading.Thread(target=process_request, args=(client_scoket,))
tqthread.start()
dqthread.start()
prthread.start()
tqthread.join()
tqthread.join()
prthread.join()
