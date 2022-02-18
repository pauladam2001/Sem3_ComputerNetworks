# 1. The client takes a string from the command line and sends it to the server. The server interprets the string as a command with
# its parameters. It executes the command and returns the standard output and the exit code to the client.

import socket
import struct


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.100.20", 1235))

data = input("String: ")        # input 'pwd'
# s.send(data.encode())

byte_string = bytes(data, 'ascii') + b'\x00'
s.send(byte_string)                               # because the server is in C and we need the terminating 0


# res = s.recv(4)                           # pentru numere
# res = struct.unpack("!i", res)

# output = s.recv(100)                    # pentru stringuri
# output = output.decode('utf-8')
# while output != "over":
#         print(output)
#         print("\n")
#         output = s.recv(100)
#         output = output.decode("utf-8")
#
# exit_code = s.recv(4)
# exit_code = struct.unpack("!i", exit_code)
# print(exit_code)

output = s.recv(100)
output = output.decode("latin-1")
print(output)

exit_code = s.recv(4)
exit_code = struct.unpack("!i", exit_code)
print(exit_code)

s.close()
