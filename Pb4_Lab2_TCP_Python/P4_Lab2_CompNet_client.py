import struct, socket
from decimal import Decimal

if __name__ == "__main__":

    try:

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("192.168.1.67", 1234))

    except socket.error as se:

        print(str(se))
        exit(-1)

    size = int(input("N = "))

    client_socket.sendall(struct.pack("!I", size))

    nr = float()

    if (size != 0):
        
        for index in range(size):

            nr = input("arr[" + str(index) + "] = ")
            nr = float(nr)

            client_socket.sendall(struct.pack("!f", nr))
    
    main_arr_size = int()

    main_arr_size = client_socket.recv(4)

    main_arr_size = struct.unpack("!I", main_arr_size)[0]

    main_array = []

    for index in range(main_arr_size):
        
        nr = client_socket.recv(4)

        nr = struct.unpack("!f", nr)[0]

        main_array.append(nr)

    print("Main array: ", end='')

    for nr in main_array:
        print(round(nr, 2), end=' ')

    print()
    

