/*
 this is a simple proxy server that handles HTTP GET requests. This utilizes
 socket programing and forking.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#define BUFFER_SIZE 4096

// extract host from HTTP request
void getHostfromReq(char *request, char *host){
    char *start = strstr(request, "Host: ");
    if (start) {
        start += 6; // Skip "Host: "
        char *end = strstr(start, "\r\n");
        if (end) {
            int len = end - start;
            strncpy(host, start, len);
            host[len] = '\0';
        }
    }
}

// handle one client connection
void handle_client(int client_fd) {
    char buffer[BUFFER_SIZE];
    char host[256] = "";
    
    // read HTTP request from client
    int bytes = recv(client_fd, buffer, BUFFER_SIZE - 1, 0);
    buffer[bytes] = '\0';
    
    printf("Got request from client\n");
    
    // get the host from the request
    getHostfromReq(buffer, host);
    printf("Connecting to host: %s\n", host);
    
    // create socket to connect to the real server
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    
    // look up the server's IP address
    struct hostent *server = gethostbyname(host);
    
    // connect to the real server (port 80)
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(80);
    memcpy(&server_addr.sin_addr, server->h_addr_list[0], server->h_length);
    
    connect(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    
    printf("Connected to server!\n");
    
    // send the original request to the real server
    send(server_fd, buffer, bytes, 0);
    
    // forward response from server back to client
    while ((bytes = recv(server_fd, buffer, BUFFER_SIZE, 0)) > 0) {
        send(client_fd, buffer, bytes, 0);
    }
    
    // close connections
    close(server_fd);
    close(client_fd);
    printf("Done with this client\n");
}

int main(int argc, char *argv[]) {
    int port = atoi(argv[1]);
    
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    
    int yes = 1;
    setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));
    
    struct sockaddr_in my_addr;
    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(port);
    my_addr.sin_addr.s_addr = INADDR_ANY;
    
    bind(listen_fd, (struct sockaddr*)&my_addr, sizeof(my_addr));
    
    listen(listen_fd, 5);
    
    printf("Proxy listening on port %d\n", port);
    
    // main loop: accept clients and fork for each one
    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        
        int client_fd = accept(listen_fd, (struct sockaddr*)&client_addr, &client_len);
        
        printf("New client connected\n");
        
        pid_t pid = fork();
        
        if (pid == 0) {
            // this is the child process
            close(listen_fd);
            handle_client(client_fd);
            exit(0);
            
        } else {
            close(client_fd);
        }
    }
    
    return 0;
}