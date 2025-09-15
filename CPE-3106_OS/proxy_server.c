/*
 * Simple HTTP Proxy Server in C
 * Uses fork() to handle multiple clients
 * Educational version - easy to understand
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/wait.h>
#include <signal.h>

#define BUFFER_SIZE 4096
#define MAX_CLIENTS 10

// Global variable for main proxy socket
int proxy_socket;

// Signal handler to clean up zombie child processes
void handle_sigchld(int sig) {
    // Clean up any finished child processes
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

// Signal handler for Ctrl+C
void handle_sigint(int sig) {
    printf("\nShutting down proxy server...\n");
    close(proxy_socket);
    exit(0);
}

// Simple function to extract hostname from HTTP request
void get_hostname_from_request(char* request, char* hostname) {
    char* line = strtok(request, "\r\n");
    
    // Look through HTTP headers for "Host:" line
    while (line != NULL) {
        if (strncmp(line, "Host:", 5) == 0) {
            // Found Host header, extract hostname
            sscanf(line, "Host: %s", hostname);
            // Remove port number if present
            char* port_pos = strchr(hostname, ':');
            if (port_pos) {
                *port_pos = '\0';  // Cut string at port
            }
            return;
        }
        line = strtok(NULL, "\r\n");
    }
    
    // If no Host header found, use default
    strcpy(hostname, "www.google.com");
}

// Connect to the target server
int connect_to_server(char* hostname) {
    struct hostent* server;
    struct sockaddr_in server_addr;
    int server_socket;
    
    printf("Connecting to %s...\n", hostname);
    
    // Create socket for server connection
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        printf("Error creating server socket\n");
        return -1;
    }
    
    // Get server info
    server = gethostbyname(hostname);
    if (server == NULL) {
        printf("Cannot find server: %s\n", hostname);
        close(server_socket);
        return -1;
    }
    
    // Set up server address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(80);  // HTTP port
    memcpy(&server_addr.sin_addr.s_addr, server->h_addr, server->h_length);
    
    // Connect to server
    if (connect(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        printf("Cannot connect to %s\n", hostname);
        close(server_socket);
        return -1;
    }
    
    printf("Connected to %s successfully!\n", hostname);
    return server_socket;
}

// Copy data from one socket to another
void copy_data(int from_socket, int to_socket) {
    char buffer[BUFFER_SIZE];
    int bytes_read;
    
    while ((bytes_read = recv(from_socket, buffer, BUFFER_SIZE, 0)) > 0) {
        send(to_socket, buffer, bytes_read, 0);
    }
}

// Handle one client connection (this runs in child process)
void handle_client(int client_socket) {
    char buffer[BUFFER_SIZE];
    char hostname[256];
    int server_socket;
    int bytes_received;
    
    printf("\n=== Child Process %d: Handling Client ===\n", getpid());
    
    // Read HTTP request from client
    bytes_received = recv(client_socket, buffer, BUFFER_SIZE - 1, 0);
    if (bytes_received <= 0) {
        printf("Failed to read from client\n");
        close(client_socket);
        return;
    }
    
    buffer[bytes_received] = '\0';  // Null terminate
    printf("Received %d bytes from client\n", bytes_received);
    
    // Make a copy of the request for parsing
    char request_copy[BUFFER_SIZE];
    strcpy(request_copy, buffer);
    
    // Extract hostname from the request
    get_hostname_from_request(request_copy, hostname);
    printf("Target server: %s\n", hostname);
    
    // Connect to the target server
    server_socket = connect_to_server(hostname);
    if (server_socket < 0) {
        // Send error response to client
        char error_msg[] = "HTTP/1.1 502 Bad Gateway\r\n\r\nCannot connect to server";
        send(client_socket, error_msg, strlen(error_msg), 0);
        close(client_socket);
        return;
    }
    
    // Forward the original request to server
    printf("Forwarding request to server...\n");
    send(server_socket, buffer, bytes_received, 0);
    
    // Copy response from server back to client
    printf("Forwarding response to client...\n");
    copy_data(server_socket, client_socket);
    
    printf("Client handled successfully!\n");
    
    // Clean up
    close(server_socket);
    close(client_socket);
}

int main(int argc, char* argv[]) {
    struct sockaddr_in proxy_addr, client_addr;
    socklen_t client_len;
    int client_socket;
    int port;
    int client_count = 0;
    
    // Check command line arguments
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
        printf("Example: %s 8080\n", argv[0]);
        return 1;
    }
    
    port = atoi(argv[1]);
    if (port <= 0 || port > 65535) {
        printf("Invalid port number\n");
        return 1;
    }
    
    // Set up signal handlers
    signal(SIGCHLD, handle_sigchld);  // Handle zombie processes
    signal(SIGINT, handle_sigint);    // Handle Ctrl+C
    
    // Create main proxy socket
    proxy_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (proxy_socket < 0) {
        printf("Error creating proxy socket\n");
        return 1;
    }
    
    // Allow socket reuse
    int opt = 1;
    setsockopt(proxy_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    // Set up proxy address
    memset(&proxy_addr, 0, sizeof(proxy_addr));
    proxy_addr.sin_family = AF_INET;
    proxy_addr.sin_addr.s_addr = INADDR_ANY;  // Listen on all interfaces
    proxy_addr.sin_port = htons(port);
    
    // Bind socket to port
    if (bind(proxy_socket, (struct sockaddr*)&proxy_addr, sizeof(proxy_addr)) < 0) {
        printf("Error binding to port %d\n", port);
        printf("Port might be in use. Try a different port.\n");
        return 1;
    }
    
    // Start listening
    if (listen(proxy_socket, MAX_CLIENTS) < 0) {
        printf("Error listening on socket\n");
        return 1;
    }
    
    printf("=== Simple HTTP Proxy Server ===\n");
    printf("✓ Listening on port %d\n", port);
    printf("✓ Each client will be handled by a separate process using fork()\n");
    printf("✓ Test with: curl -x http://127.0.0.1:%d http://example.com\n", port);
    printf("✓ Press Ctrl+C to stop\n\n");
    
    // Main server loop
    while (1) {
        printf("Waiting for client connection...\n");
        
        client_len = sizeof(client_addr);
        client_socket = accept(proxy_socket, (struct sockaddr*)&client_addr, &client_len);
        
        if (client_socket < 0) {
            printf("Error accepting client connection\n");
            continue;
        }
        
        client_count++;
        printf("✓ Client #%d connected from %s\n", 
               client_count, inet_ntoa(client_addr.sin_addr));
        
        // This is where fork() happens!
        pid_t pid = fork();
        
        if (pid == 0) {
            // CHILD PROCESS: Handle the client
            close(proxy_socket);  // Child doesn't need the listening socket
            handle_client(client_socket);
            exit(0);  // Child process exits when done
            
        } else if (pid > 0) {
            // PARENT PROCESS: Continue accepting new clients
            close(client_socket);  // Parent doesn't need this client socket
            printf("✓ Forked child process %d to handle client\n", pid);
            
        } else {
            // FORK FAILED
            printf("Error: fork() failed\n");
            close(client_socket);
        }
    }
    
    return 0;
}