#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <errno.h>

#define SERVER_PORT 9999

typedef int SOCKET;
#define closesocket close

#define WORD_COUNT "wc -m "
#define AWK " | awk '{print $1}'"
#define CAT "cat "

int get_length(char *filename) {
    char wc_command[71] = WORD_COUNT;
        strcat(wc_command, filename);
        strcat(wc_command, AWK);

        FILE *wc_fd = popen(wc_command, "r");

        char buf[4096] = {0}, c = getc(wc_fd);
        int pos = 0;
        while(c != EOF && c != ' ') {
            buf[pos++] = c;
            c = getc(wc_fd);
        }
        pclose(wc_fd);

        if(pos == 0)
            return -1;
        return atoi(buf);
}

void send_content(char *filename) {
    char wc_command[61] = CAT;
    strcat(wc_command, filename);

    FILE *cat_fd = popen(wc_command, "r");
    
    char c = getc(cat_fd);
    while(c != EOF) {
        putchar(c);
        c = getc(cat_fd);
    }
}

int main() {
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if(sock < 0) {
        perror("Socket creation error!");
        printf("Error code %d\n", errno);
        exit(1);
    }

    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);

    if(bind(sock, (struct sockaddr*) &server, sizeof(server)) < 0) {
        perror("Bind error!");
        printf("Error code %d\n", errno);
        exit(2);
    }
    listen(sock, 2);

    struct sockaddr_in client;
    ssize_t client_size = sizeof(client);
    memset(&client, 0, client_size);

    printf("Waiting for connections...\n\n");
    while(1) {
        SOCKET client_sock = accept(sock, (struct sockaddr*) &client, (void*) &client_size);
        if(client_sock < 0) {
            perror("Accept error!");
            printf("Error code %d\n", errno);
            continue;
        }   

        int fork_code = fork();
        if(fork_code < 0) {
            perror("Error on creating child process!");
            printf("Error code %d\n", errno);
            continue;
        }
        else if(fork_code == 0) {
            SOCKET child_sock = client_sock;
            struct sockaddr_in child = client;
            printf("Client connected -> %s:%d\n", inet_ntoa(child.sin_addr), ntohs(child.sin_port));

            char filename[51];
            recv(child_sock, (void*) filename, sizeof(filename), 0);

            int len = get_length(filename), network_len = htonl(len);
            send(child_sock, (void*) &network_len, sizeof(len), 0);

            if(len != -1) {
                dup2(child_sock, STDOUT_FILENO);
                send_content(filename);
            }

            closesocket(child_sock);
        }
    }

    return 0;
}