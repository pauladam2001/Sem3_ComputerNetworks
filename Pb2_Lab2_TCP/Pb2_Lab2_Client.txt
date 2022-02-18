#include <stdio.h>
#include <stdint.h>
#include <WinSock2.h>

#define SERVER_IP "192.168.1.5"
#define SERVER_PORT 9999

void win_init() {
    WSADATA wsaData;
    if(WSAStartup(MAKEWORD(2, 2), &wsaData) < 0) {
        perror("Error initializing windows socket library!");
        printf("Error code: %d\n", WSAGetLastError());
        exit(-99);
    }
}

void get_name(char *full_path, char *name) {
    int last_slash_idx = 0, extension_idx = 0;
    for(int i=0; i<strlen(full_path); i++)
        if(full_path[i] == '/')
            last_slash_idx = i;
        else if(full_path[i] == '.')
            extension_idx = i;

    int pos = 0;
    for(int i=last_slash_idx+1; i<extension_idx; i++)
        name[pos++] = full_path[i];

    strcat(name, "-COPY");

    for(int i=extension_idx; i<strlen(full_path); i++)
        strncat(name, &full_path[i], 1);
}

int main() {
    win_init();

    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if(sock < 0) {
        perror("Socket creation error!");
        printf("Error code: %d\n", WSAGetLastError());
        exit(1);
    }

    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_addr.s_addr = inet_addr(SERVER_IP);
    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);

    if(connect(sock, (struct sockaddr*) &server, sizeof(server)) < 0) {
        perror("Could not connect to server!");
        printf("Error code: %d\n", WSAGetLastError());
        exit(2);
    }

    char command[51];
    printf("Enter command:\n");
    fgets(command, 51, stdin);
    command[strlen(command)-1] = '\0';
    send(sock, (void*) command, sizeof(command), 0);

    int len;
    recv(sock, (void*) &len, sizeof(len), 0);
    len = ntohl(len);
    printf("File length: %d\n", len);

    if(len != -1) {
        char name[20];
        get_name(command, name);
        
        FILE *fd = fopen(name, "w");

        char buf[4096] = {0};
        recv(sock, (void*) buf, sizeof(buf), 0);
      
        fputs(buf, fd);
        fclose(fd);
    }

    closesocket(sock);
    WSACleanup();
 
    return 0;
}