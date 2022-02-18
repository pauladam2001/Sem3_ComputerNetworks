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
#include <time.h>

typedef int SOCKET;

void ping(SOCKET c, struct sockaddr_in srv) {

    const char ping_data[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890;,.";
    char echoed_data[40];

    struct sockaddr_in from;
    memset(&from, 0, sizeof(from));

    int32_t bs, br;
    uint32_t l = sizeof(srv);

    clock_t t;
    t = clock();

    bs = sendto(c, ping_data, strlen(ping_data)+1, 0, (const struct sockaddr*)&srv, l);

    if (bs < 0) {
        
        perror("Error on sending ping packets.");
        return;
    }

    br = recvfrom(c, echoed_data, strlen(ping_data)+1, 0, (struct sockaddr*)&from, &l);

    if (br < 0) {

        perror("Errror on receiving ping packets.");
        return;
    }

    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC;

    if (strcmp(ping_data, echoed_data) == 0) {

        printf("Sent and received %lu bytes of data from %s. Round trip time %lf.\n", strlen(ping_data)+1, inet_ntoa(from.sin_addr), time_taken);
    }
    else {

        printf("Echoed PING data mismatched.\n");
    }
    
}

int main(int argc, char** argv) {

    SOCKET clnt_sock;
    struct sockaddr_in server;
    struct hostent *host_address;
    char buf[128];

    if (argc != 3) { 

        printf("Usage: %s <server_name> <port>\n", argv[0]);
        return 1;
    }

    clnt_sock = socket(AF_INET, SOCK_DGRAM, 0);

    if (clnt_sock < 0) {

        perror("Error on opening socket");
        return 1;
    }

    memset(&server, 0, sizeof(server));
    memset(buf, 0, 128);
    host_address = gethostbyname(argv[1]);

    server.sin_family = AF_INET;
    memmove(&server.sin_addr, host_address->h_addr, host_address->h_length);
    server.sin_port = htons(strtol(argv[2], NULL, 10));

    while (true) {

        ping(clnt_sock, server);
        sleep(1);
    }

    close(clnt_sock);
    return 0;
}