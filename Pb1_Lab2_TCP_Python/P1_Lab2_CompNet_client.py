from os import error
import socket, struct

if __name__ == '__main__':

    try:

        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect(("192.168.1.67", 1234))

    except socket.error as se:
        
        print(str(se))
        exit(-1)

    command = input("Input command: ")

    try:
        cs.sendall(bytes(command, 'ascii'))

    except socket.error as se:

        print(str(se))
        exit(-1)

    output = cs.recv(16384)

    output = output.decode('ascii')

    print(output)

    exit_code = cs.recv(4)
    exit_code = struct.unpack("!i", exit_code)[0]

    print("Exit code: " + str(exit_code))

    cs.close()

