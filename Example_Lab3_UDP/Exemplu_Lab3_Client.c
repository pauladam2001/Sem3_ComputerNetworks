#include <stdio.h>
#include <winsock2.h>
#include <WinSock2.h>
#pragma comment(lib, "Ws2_32.lib")

int main() {
#ifdef WIN32
    WSADATA wsaData;

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) < 0) {
        printf("Error initializing the Windows Sockets LIbrary");
        return -1;
    }
#endif

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("error on creating socket!");
        exit(-1);
    }

    struct sockaddr_in server, from;

    memset(&server, 0, sizeof(server));

    server.sin_family = AF_INET;
    server.sin_port = htons(1234);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    char buffer[1024];
    scanf("%s", buffer);

    int length = sizeof(struct sockaddr_in);
    int n = sendto(sock, buffer, strlen(buffer)+1, 0, (struct sockaddr *)&server, length);
    if(n < 0) {
        perror("error o sending data");
        exit(-2);
    }

    int r = recvfrom(sock, buffer, 1024, 0, &from, &length);
    if(r < 0) {
        int err = WSAGetLastError();
        printf("codul de eroare este %d", err);
        exit(-2);
    }
    printf("%s\n", buffer);

    closesocket(sock);
}
