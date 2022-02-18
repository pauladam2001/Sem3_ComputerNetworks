import threading, socket, struct
from decimal import Decimal

threads = []
subarrays = []
sockets = []
main_array = []

def thread(cs, N):
    
    global subarrays

    subarray = []

    nr = float()

    for index in range(N):

        nr = cs.recv(4)
        nr = struct.unpack("!f", nr)[0]
        subarray.append(nr)

    subarray.sort()
    subarrays.append(subarray)

    print("Thread ended.")


if __name__ == "__main__":
    
    try:

        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        ss.bind(("192.168.1.67", 1234))
        ss.listen(5)
    
    except socket.error as se:

        print(str(se))
        exit(-1)

    subarr_size = 1

    while subarr_size != 0:

        print("Listening for incoming connections...")

        client_socket, client_addr = ss.accept()

        subarr_size = client_socket.recv(4)

        subarr_size = struct.unpack("!I", subarr_size)[0]

        sockets.append(client_socket)

        print("Client connected from: ", client_socket.getpeername())

        if subarr_size != 0:

            thr = threading.Thread(target=thread, args=(client_socket, subarr_size, ))

            threads.append(thr)

            thr.start()


    for thr in threads:
        thr.join()

    main_array = subarrays[0]

    del subarrays[0]

    for array in subarrays:
        
        i = 0
        j = 0
        k = 0

        merge_array = [None for i in range(len(array) + len(main_array))]

        while i < len(array) and j < len(main_array):

            if (array[i] < main_array[j]):

                merge_array[k] = array[i]
                i += 1
                k += 1
            
            else:

                merge_array[k] = main_array[j]
                j += 1
                k += 1

        while i < len(array):

            merge_array[k] = array[i]
            i += 1
            k += 1
        
        while j < len(main_array):
            
            merge_array[k] = main_array[j]
            j += 1
            k += 1

        main_array = merge_array

    l = len(main_array)

    for cs in sockets:

        cs.sendall(struct.pack("!I", l))
        
        for nr in main_array:
            cs.sendall(struct.pack("!f", nr))

        cs.close()

    print("Main array:")

    for nr in main_array:
        print(round(nr, 2), end=' ')

    print()
