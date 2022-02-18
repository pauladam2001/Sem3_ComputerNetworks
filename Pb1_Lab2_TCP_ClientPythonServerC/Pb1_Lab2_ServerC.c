//1.   A client sends to the server an array of numbers. Server returns the sum of the numbers.

#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <arpa/inet.h>

int c;


void tratare() {
    int cod;
    int32_t r;
    uint8_t b;
    struct sockaddr_in server;
    char string[201];

    if (c < 0) {
        fprintf(stderr, "Eroare la stabilirea conexiunii cu clientul.\n");
        exit(1);
    }
    else
        printf("Un nou client s-a conectat cu succes.\n");

    recv(c, (char*)string, 201, 0);

    printf("\nThe string is: %s\n", string);

    //execute the command

    FILE* fd = popen(string, "r");
    char buffer[128];
    char result[500];

    while(!feof(fd)) {
        if (fgets(buffer, 128, fd) != NULL)
            strcat(result, buffer);
    }
    printf("%s", result);
    // send data
    int32_t exit_code = WEXITSTATUS(pclose(fd));
    exit_code = htonl(exit_code);

    send(c, (char*)result, 500, 0);
    send(c, &exit_code, sizeof(exit_code), 0);
    printf("\nSent the data.\n");

    close(c);
    exit(0);
}


int main() {
    int s, l, cod;
    struct sockaddr_in client, server;

    s = socket(PF_INET, SOCK_STREAM, 0);
    if (s < 0) {
        fprintf(stderr, "Eroare la creare socket server.\n");
        return 1;
    }

    memset(&server, 0, sizeof(struct sockaddr_in));
    server.sin_family = AF_INET;
    server.sin_port = htons(1235);
    server.sin_addr.s_addr = INADDR_ANY;

    cod = bind(s, (struct sockaddr *) &server, sizeof(struct sockaddr_in));
    if (cod < 0) {
        fprintf(stderr, "Eroare la bind. Portul este deja folosit.\n");
        return 1;
    }

    listen(s, 5);

    while (1) { // deserveste oricati clienti

        memset(&client, 0, sizeof(client));
        l = sizeof(client);

        printf("Astept sa se conecteze un client.\n");
        c = accept(s, (struct sockaddr *) &client, &l);
        printf("S-a conectat clientul cu adresa %s si portul %d.\n", inet_ntoa(client.sin_addr), ntohs(client.sin_port));

        if (fork() == 0) { // server concurent, conexiunea va fi tratata de catre un proces fiu separat
            tratare();
        }
        // parintele continua bucla while asteptand un nou client
    }

}
