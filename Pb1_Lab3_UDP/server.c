#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdbool.h>
#include <pthread.h>

typedef int SOCKET;

int main(int argc, char** argv) {

    int32_t bs, br;
    SOCKET srv_sock;
    struct sockaddr_in server, from;
    char buf[128];

    if (argc != 2) {

        printf("Usage: %s <port_no>\n", argv[0]);
        return 1;
    }

    memset(&server, 0, sizeof(server));
    memset(&from, 0, sizeof(from));
    memset(buf, 0, 128);

    srv_sock = socket(AF_INET, SOCK_DGRAM, 0);

    if (srv_sock < 0) {

        perror("Error on opening socket.");
        return 1;
    }

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(strtol(argv[1], NULL, 10));

    if (bind(srv_sock, (const struct sockaddr*)&server, sizeof(server)) < 0) {

        perror("Bind error");
        return 1;
    }

    uint32_t l = sizeof(from);

    while (true) {

        br = recvfrom(srv_sock, buf, 40, 0, (struct sockaddr*)&server, &l);

        printf("Received %lu bytes from %s, echoing back.\n", strlen(buf)+1, inet_ntoa(server.sin_addr));
        
        if (br < 0) {

            perror("Error on receiving packets.");
        }

        bs = sendto(srv_sock, buf, 40, 0, (const struct sockaddr*)&server, l);

        if (bs < 0) {

            perror("Error on sending packets.");
        }
    }

    close(srv_sock);
    return 0;
}