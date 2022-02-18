import socket, struct, os
import multiprocessing as mp


def worker(cs):

    command = cs.recv(1024)

    command = command.decode('ascii')

    pipe = os.popen(command, 'r')

    buf = bytes()
    
    buf = pipe.read(16384)

    exit_code = pipe.close()

    if (exit_code == None):
        exit_code = 0

    try:

        cs.sendall(bytes(buf, 'ascii'))
        print(buf)
    
        cs.sendall(struct.pack("!i", exit_code))
        print(exit_code)
        
    except socket.error as se:

        print(str(se))
        exit(-1)

    cs.close()
    print("Process terminated.")


if __name__ == "__main__":

    try:
        
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.bind(("192.168.1.67", 1234))
        ss.listen(5)
    
    except socket.error as se:

        print(str(se))
        exit(-1)

    mp.set_start_method('spawn')

    while True:

        print("Listening for incoming connections...")
        cs, caddr = ss.accept()
        print("Client connected from: ", cs.getpeername())
        p = mp.Process(target=worker, args=(cs,))

        p.start()
        