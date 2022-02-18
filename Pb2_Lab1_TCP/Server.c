//2.   A client sends to the server a string. The server returns the count of spaces in the string.

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

#include <WinSock2.h>
#include <stdint.h>

#endif

int main() {
    SOCKET s;
    struct sockaddr_in server, client;
    int c, l, err;

#ifdef WIN32
    WSADATA wsaData;

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) < 0) {
        printf("Error initializing the Windows Sockets Library\n");
        return -1;
    }
#endif

    s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) {
        printf("Eroare la creare socketului server\n");
        return 1;
    }

    int enable = 1;
    setsockopt(s, SOL_SOCKET, SO_REUSEADDR, (void*)&enable, sizeof(int));

    memset(&server, 0, sizeof(server));

    server.sin_port = htons(1234);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;

    if (bind(s, (struct sockaddr *) &server, sizeof(server)) < 0) {
        printf("Bind error\n");
        return 1;
    }

    listen(s, 5);

    l = sizeof(client);

    memset(&client, 0, sizeof(client));

    while (1) {
        printf("Listening for incoming connections\n");
        c = accept(s, (struct sockaddr *) &client, &l);
        err = errno;

        uint16_t  length;

#ifdef WIN32
        err = WSAGetLastError();
#endif

        if (c < 0) {
            printf("Accept error: %d\n", err);
            continue;
        }

        printf("Incomming connected client from: %s:%d\n", inet_ntoa(client.sin_addr), ntohs(client.sin_port));

        int res = recv(c, (char*)&length, sizeof(length), 0);
        if (res != sizeof(length)) printf("Error receiving operand\n");

        length = ntohs(length);

//        char* data = (char*)malloc(sizeof(char)*(length+1));

        char data[length + 1];

        res = recv(c, (char*)data, length*sizeof(char), 0);
        if (res != length*sizeof(char)) printf("Error receiving operand\n");

        printf("Length is %hu\n", length);
        printf("The string is: %s\n", data);

        uint16_t ct = 0;

        for (int i = 0; i < length ; i++)
            if (data[i] == ' ')
                ct++;

        printf("Number of spaces is %hu\n", ct);

        ct = htons(ct);

        res = send(c, (const char *) &ct, sizeof(ct), 0);
        if (res != sizeof(ct)) printf("Error sending result\n");

        printf("Done\n\n");

//        free(data);

        closesocket(c);
    }

#ifdef WIN32
    WSACleanup();
#endif
}
