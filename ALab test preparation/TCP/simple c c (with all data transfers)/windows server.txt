#include <stdio.h>
#ifndef WIN32
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <arpa/inet.h>

#include <unistd.h>
#include <errno.h>

#define closesocket close
typedef int SOCKET;
#else

#include<WinSock2.h>
#include <stdint.h>

#pragma comment(lib,"Ws2_32.lib")
#endif

void treat_request(int connection_socket){
    uint16_t a, b, suma;

    uint32_t length1;
    char message1[1024] = "Successfully connected to server!\n";
    length1 = strlen(message1) + 1;
    length1 = htonl(length1);
    if(send(connection_socket, (char*)&length1, sizeof(length1), 0) < sizeof(length1))
        printf("Error on sending array length\n");

    length1 = ntohl(length1);
    if(send(connection_socket, message1, length1, 0) < length1)
        printf("Error on sending array\n");


    uint32_t length2;
    char message2[1024] = "Another message!\n";
    length2 = strlen(message2) + 1;
    length2 = htonl(length2);
    if(send(connection_socket, (char*)&length2, sizeof(length2), 0) < sizeof(length2))
        printf("Error on sending array length\n");

    length2 = ntohl(length2);
    if(send(connection_socket, message2, length2, 0) < length2)
        printf("Error on sending array\n");

    // serving the connected client
    int res = recv(connection_socket, (char*)&a, sizeof(a), 0);
    //check we got an unsigned short value
    if (res != sizeof(a)) printf("Error receiving operand\n");
    res = recv(connection_socket, (char*)&b, sizeof(b), 0);
    if (res != sizeof(b)) printf("Error receiving operand\n");
    //decode the value to the local representation
    a = ntohs(a);
    b = ntohs(b);
    suma = a + b;
    suma = htons(suma);
    res = send(connection_socket, (char*)&suma, sizeof(suma), 0);

    if (res != sizeof(suma)) printf("Error sending result\n");
    //on Linux closesocket does not exist but was defined above as a define to close
    closesocket(connection_socket);

}

int main() {
    SOCKET s;
    struct sockaddr_in server, client;
    int c, l, err;

#ifdef WIN32
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) < 0) {
        printf("Error initializing the Windows Sockets LIbrary");
        return -1;
    }

#endif
    s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) {
        printf("Eroare la crearea socketului server\n");
        return 1;
    }
    memset(&server, 0, sizeof(server));
    server.sin_port = htons(1234);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;

    if (bind(s, (struct sockaddr *) &server, sizeof(server)) < 0) {
        perror("Bind error:");
        return 1;
    }
    listen(s, 5);
    l = sizeof(client);
    memset(&client, 0, sizeof(client));

    while (1) {

        printf("Listening for incomming connections\n");
        c = accept(s, (struct sockaddr *) &client, &l);
        err = errno;
#ifdef WIN32
        err = WSAGetLastError();
#endif
        if (c < 0) {
            printf("accept error: %d", err);
            continue;
        }
        printf("Incoming connected client from: %s:%d\n", inet_ntoa(client.sin_addr), ntohs(client.sin_port));
        //if(fork()==0)   ///fork only works on linux, but this is the way we would do concurrent programming
            treat_request(c);
    }
    // never reached
    // Release the Windows Sockets Library
#ifdef WIN32
    WSACleanup();
#endif

}