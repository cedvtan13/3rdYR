/*
 * Simple HTTP Proxy Server - Student Version
 * 
 * This is a basic proxy that:
 * 1. Takes a port number from command line
 * 2. Listens for client connections
 * 3. Creates a new process for each client (using fork)
 * 4. Forwards HTTP requests to web servers
 * 5. Sends responses back to clients
 * 
 * Usage: ./proxy_server 8080
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <sys/wait.h>

#define BUFFER_SIZE 4096

// Function to handle each client
void handle_client(int client_fd);

int main(int argc, char *argv[]) {
    int server_fd, client_fd, port;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    
    // Check command line arguments
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
        printf("Example: %s 8080\n", argv[0]);
        return 1;
    }
    
    port = atoi(argv[1]);
    printf("Starting proxy server on port %d...\n", port);
    
    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        printf("Error: Cannot create socket\n");
        return 1;
    }
    
    // Setup server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;  // Accept from any IP
    server_addr.sin_port = htons(port);
    
    // Bind socket to port
    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        printf("Error: Cannot bind to port %d\n", port);
        return 1;
    }
    
    // Start listening
    if (listen(server_fd, 5) < 0) {
        printf("Error: Cannot listen on port\n");
        return 1;
    }
    
    printf("Proxy server running! Waiting for connections...\n");
    
    // Main loop - accept connections
    while (1) {
        // Accept client connection
        client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
        if (client_fd < 0) {
            printf("Error accepting connection\n");
            continue;
        }
        
        printf("New client connected!\n");
        
        // Create child process to handle this client
        if (fork() == 0) {
            // This is the child process
            close(server_fd);  // Child doesn't need the main server socket
            handle_client(client_fd);
            close(client_fd);
            exit(0);  // Child exits after handling client
        } else {
            // This is the parent process
            close(client_fd);  // Parent doesn't need the client socket
        }
    }
    
    return 0;
}

// Handle one client connection
void handle_client(int client_fd) {
    char buffer[BUFFER_SIZE];
    char host[256];
    char method[16], url[512], version[16];
    int target_fd, bytes;
    struct sockaddr_in target_addr;
    struct hostent *target_host;
    
    // Read request from client
    bytes = recv(client_fd, buffer, BUFFER_SIZE - 1, 0);
    if (bytes <= 0) {
        printf("Error reading from client\n");
        return;
    }
    buffer[bytes] = '\0';  // Add null terminator
    
    printf("Received request:\n%s\n", buffer);
    
    // Parse the first line: GET http://example.com/path HTTP/1.1
    if (sscanf(buffer, "%s %s %s", method, url, version) != 3) {
        printf("Error: Bad request format\n");
        return;
    }
    
    // We only handle GET requests
    if (strcmp(method, "GET") != 0) {
        printf("Error: Only GET method supported\n");
        return;
    }
    
    // Extract hostname from URL
    // URL format: http://hostname/path or just /path
    if (strncmp(url, "http://", 7) == 0) {
        // Full URL: http://hostname/path
        char *hostname_start = url + 7;  // Skip "http://"
        char *path_start = strchr(hostname_start, '/');
        
        if (path_start) {
            *path_start = '\0';  // Temporarily cut the string
            strcpy(host, hostname_start);
            *path_start = '/';   // Restore the '/'
        } else {
            strcpy(host, hostname_start);
        }
    } else {
        // Relative URL: /path (need to find Host header)
        char *host_line = strstr(buffer, "Host: ");
        if (!host_line) {
            printf("Error: No Host header found\n");
            return;
        }
        
        host_line += 6;  // Skip "Host: "
        char *host_end = strstr(host_line, "\r\n");
        if (host_end) {
            *host_end = '\0';
            strcpy(host, host_line);
            *host_end = '\r';  // Restore
        } else {
            strcpy(host, host_line);
        }
    }
    
    printf("Connecting to host: %s\n", host);
    
    // Create socket to target server
    target_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (target_fd < 0) {
        printf("Error creating target socket\n");
        return;
    }
    
    // Get target server IP
    target_host = gethostbyname(host);
    if (!target_host) {
        printf("Error: Cannot resolve hostname %s\n", host);
        close(target_fd);
        return;
    }
    
    // Setup target server address
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(80);  // HTTP port
    memcpy(&target_addr.sin_addr, target_host->h_addr_list[0], target_host->h_length);
    
    // Connect to target server
    if (connect(target_fd, (struct sockaddr*)&target_addr, sizeof(target_addr)) < 0) {
        printf("Error connecting to %s\n", host);
        close(target_fd);
        return;
    }
    
    printf("Connected to %s, forwarding request...\n", host);
    
    // Send original request to target server
    send(target_fd, buffer, bytes, 0);
    
    // Forward response from target server to client
    while ((bytes = recv(target_fd, buffer, BUFFER_SIZE, 0)) > 0) {
        send(client_fd, buffer, bytes, 0);
    }
    
    printf("Request completed!\n");
    close(target_fd);
}
