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

#define closesocket close
typedef uint32_t SOCKET;

int main(int argc, char** args) {

    SOCKET c;
    struct sockaddr_in server;

    memset(&server, 0, sizeof(server));

    server.sin_addr.s_addr = inet_addr(args[1]);
    server.sin_port = htons(1234);
    server.sin_family = AF_INET;

    c = socket(AF_INET, SOCK_STREAM, 0);

    if (connect(c, (const struct sockaddr*)&server, sizeof(server)) < 0) {

        printf("Error: Unable to connect to server.\n");
        return 1;
    }

    uint16_t N = strtol(args[2], NULL, 10);
    float nr;

    N = htons(N);
    send(c, &N, sizeof(uint16_t), 0);
    N = ntohs(N);

    for (uint16_t i = 0; i < N; i++) {

        printf("arr[%u] = ", i);
        scanf("%f", &nr);

        send(c, &nr, sizeof(float), 0);

    }

    uint16_t size;
    int br;
    float arr[1024];

    br = recv(c, &size, sizeof(uint16_t), 0);

    if (br != sizeof(uint16_t)) {

        printf("Error on receiving merge-sorted array size.\n");
        return 1;
    }

    br = recv(c, arr, size*sizeof(float), 0);

    if (br != size*sizeof(float)) {

        printf("Error on receiving merge-sorted array.\n");
        return 1;
    }

    printf("Merge-sorted array: ");
    for (uint16_t i = 0; i < size; i++) {

        printf("%f ", arr[i]);
    }
    
    printf("\n");
    return 0;
}