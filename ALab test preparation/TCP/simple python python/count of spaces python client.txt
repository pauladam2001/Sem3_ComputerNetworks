import socket
import struct

def main():
    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # now connect to the web server on port 80 - the normal http port
    s.connect(('192.168.100.18', 1234))

    string = input("Enter string: ")
    #byte_string = bytes(string, 'ascii') + b'\x00'
    byte_string = string.encode('ascii')
    s.send(byte_string) # encode si decode sunt pentru stringuri
    result = s.recv(4) # result are 4 octeti de la server
    result = struct.unpack("!I", result) # acum result e un unsigned int,  numai pentru date numerice!!
    print("Numarul de spatii este: ", result[0])
    s.close() # close the socket

main()
