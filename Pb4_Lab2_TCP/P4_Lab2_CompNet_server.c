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

#define closesocket close
typedef uint32_t SOCKET;

float main_arr[1024];
uint16_t arr_length = 0;
pthread_t T[256];
pthread_mutex_t mtx;

typedef struct {

    SOCKET client_socket;
    uint16_t arr_size;

} s_args;

s_args a[256];

void insert(float nr) {

    uint16_t index = 0;

    while (nr > main_arr[index] && index < arr_length) {
        
        index++;
    }

    
    if (arr_length != 0) {
        
        for (int i = arr_length-1; i >= index; i--)
            main_arr[i+1] = main_arr[i];
    }

    main_arr[index] = nr;
    arr_length++;
}

void* thread(void* a) {

    s_args *args = (s_args*) a;

    float nr;
    for (uint16_t i = 0; i < args->arr_size; i++) {
        
        int br = recv(args->client_socket, &nr, sizeof(float), 0);

        if (br != sizeof(float)) {

            printf("Error on receiving an array element.\n");
            return NULL;
        }

        pthread_mutex_lock(&mtx);
        insert(nr);
        pthread_mutex_unlock(&mtx);

    }
    return NULL;
}


int main(int argc, char** args) {

    SOCKET s;
    struct sockaddr_in server, client;

    pthread_mutex_init(&mtx, NULL);

    memset(&server, 0, sizeof(server));
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(1234);
    server.sin_family = AF_INET;

    s = socket(AF_INET, SOCK_STREAM, 0);

    if (bind(s, (const struct sockaddr*)&server, sizeof(server)) < 0) {

        perror("Bind error: ");
    }

    listen(s, 5);

    memset(&client, 0, sizeof(client));

    SOCKET c;
    uint32_t l, err;
    uint16_t N = 1;
    uint8_t no_t = 0;

    l = sizeof(client);

    while (N != 0) {

        printf("Listening for incoming connections...\n");

        c = accept(s, (struct sockaddr*)&client, &l);

        err = errno;

        if (c < 0) {

            printf("Accept error: %d", err);
        }

        printf("Client connected from: %s:%d\n", inet_ntoa(client.sin_addr), htons(client.sin_port));

        int br = recv(c, &N, sizeof(uint16_t), 0);

        N = ntohs(N);

        if (br != sizeof(uint16_t)) {

            printf("Error on receiving array length.\n");
        }

        if (N != 0) {

            a[no_t].arr_size = N;
            a[no_t].client_socket = c;

            pthread_create(&T[no_t], NULL, &thread, (void*)&a[no_t]);
        }
        else {

            a[no_t].arr_size = 0;
            a[no_t].client_socket = c;
        }

        no_t++;
    }

    
    for (uint8_t i = 0; i < no_t; i++) {

        pthread_join(T[i], NULL);
    }
    

    pthread_mutex_destroy(&mtx);

    
    printf("Final array: ");
    for (uint16_t i = 0; i < arr_length; i++) {

        printf("%f ", main_arr[i]);
    }
    
    printf("\n");

    for (uint16_t i = 0; i < no_t; i++) {

        send(a[i].client_socket, &arr_length, sizeof(uint16_t), 0);
        send(a[i].client_socket, main_arr, arr_length*sizeof(float), 0);
    }

    return 0;
}