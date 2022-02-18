//10.The client sends to the server two strings. The server sends back the character with the largest number
// of occurrences on the same positions in both strings together with its count.

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

        char string1[201], string2[201];
        uint32_t  length, length1, length2;

#ifdef WIN32
        err = WSAGetLastError();
#endif

        if (c < 0) {
            printf("Accept error: %d\n", err);
            continue;
        }

        printf("Incomming connected client from: %s:%d\n", inet_ntoa(client.sin_addr), ntohs(client.sin_port));


        int res = recv(c, (char*)&length1, sizeof(length1), 0);

        //check we got an unsigned long value

        if (res != sizeof(length1))
        {
            printf("Error receiving count\n");
            continue;
        }

        length1 = ntohl(length1);

        res = recv(c, (char*)string1, length1 * sizeof(char), 0);

        if (res != sizeof(char) * length1) {
            printf("Error receiving first string!\n");
            continue;
        }

        res = recv(c, (char*)&length2, sizeof(length2), 0);

        if (res != sizeof(length2))
        {
            printf("Error receiving count\n");
            continue;
        }

        length2 = ntohl(length2);

        res = recv(c, (char*)string2, length2 * sizeof(char), 0);

        if (res != sizeof(char) * length2) {
            printf("Error receiving second string!\n");
            continue;
        }

        printf("First string : %s\n", string1);
        printf("Second string : %s\n", string2);

//        length1 = strlen(string1);
//        length2 = strlen(string2);

        uint32_t i, imax, ctmax = 0;
        char ch[2];
        int freq[26] = {0};
        if (length1 < length2)
            imax = length1;
        else
            imax = length2;
        for (i = 0; i < imax; i++) {
            if (string1[i] == string2[i] && string1[i] != ' ') {
                freq[string1[i] - 97]++;
                if (freq[string1[i] - 97] > ctmax) {
                    ctmax = freq[string1[i] - 97];
                    ch[0] = string1[i];
                }
            }
        }

        printf("Letter %s has the largest number of occurrences, %u\n", ch, ctmax);

        ctmax = htonl(ctmax);

        res = send(c, ch, 2*sizeof(char), 0);          //SAU &ch?
        if (res != sizeof(ch)) printf("Error sending result\n");

        res = send(c, (const char *) &ctmax, sizeof(ctmax), 0);
        if (res != sizeof(ctmax)) printf("Error sending result\n");

        printf("Done\n\n");

        closesocket(c);
    }

#ifdef WIN32
    WSACleanup();
#endif
}
