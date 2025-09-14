#define _GNU_SOURCE
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
#include <errno.h>
#include <ctype.h>
#include <sys/types.h>

#define BUFFER_SIZE 4096
#define MAX_HOST_LENGTH 256

// Simple structure to hold HTTP request info
typedef struct {
    char method[16];      // GET, POST, etc.
    char host[MAX_HOST_LENGTH];  // www.google.com
    int port;             // 80, 443, etc.
    char path[512];       // /search?q=hello
    int is_valid;         // 1 if request is good, 0 if bad
} HttpRequest;

// Global proxy socket for cleanup
int proxy_socket = -1;

// Signal handler for SIGCHLD to clean up zombie processes
void sigchld_handler(int sig) {
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

// Signal handler for graceful shutdown
void sigint_handler(int sig) {
    printf("\nShutting down proxy server...\n");
    if (proxy_socket >= 0) {
        close(proxy_socket);
    }
    exit(0);
}

// Function to remove spaces from beginning and end of string
char* trim_string(char* str) {
    // Remove spaces from beginning
    while (*str == ' ' || *str == '\t' || *str == '\r' || *str == '\n') {
        str++;
    }
    
    // Remove spaces from end
    char* end = str + strlen(str) - 1;
    while (end > str && (*end == ' ' || *end == '\t' || *end == '\r' || *end == '\n')) {
        *end = '\0';
        end--;
    }
    
    return str;
}

// Function to get hostname from "Host:" header
int get_host_from_header(char* header_line, char* hostname, int* port) {
    // Look for "Host:" (case insensitive)
    char* host_start = strchr(header_line, ':');
    if (!host_start) return 0;
    
    host_start++; // Move past ':'
    host_start = trim_string(host_start);
    
    // Check if port is specified
    char* port_pos = strchr(host_start, ':');
    if (port_pos) {
        *port_pos = '\0';
        strcpy(hostname, host_start);
        *port = atoi(port_pos + 1);
    } else {
        strcpy(hostname, host_start);
        *port = 80; // Default HTTP port
    }
    
    return 1;
}

// Function to parse HTTP request and get important info
HttpRequest parse_request(char* request_text) {
    HttpRequest req;
    memset(&req, 0, sizeof(req));
    req.port = 80; // Default port
    req.is_valid = 0;
    
    // Make a copy to work with
    char* request_copy = malloc(strlen(request_text) + 1);
    strcpy(request_copy, request_text);
    
    // Get first line (request line)
    char* first_line = strtok(request_copy, "\r\n");
    if (!first_line) {
        free(request_copy);
        return req;
    }
    
    // Parse: METHOD URL HTTP/1.1
    char url[1024];
    char version[32];
    
    if (sscanf(first_line, "%15s %1023s %31s", req.method, url, version) != 3) {
        free(request_copy);
        return req;
    }
    
    // Check if it's a supported method
    if (strcmp(req.method, "GET") != 0 && strcmp(req.method, "POST") != 0 && 
        strcmp(req.method, "HEAD") != 0 && strcmp(req.method, "CONNECT") != 0) {
        free(request_copy);
        return req;
    }
    
    // Parse URL
    if (strncmp(url, "http://", 7) == 0) {
        // Full URL: http://hostname:port/path
        char* hostname_start = url + 7;
        char* path_start = strchr(hostname_start, '/');
        char* port_start = strchr(hostname_start, ':');
        
        if (path_start) {
            strcpy(req.path, path_start);
            *path_start = '\0';
        } else {
            strcpy(req.path, "/");
        }
        
        if (port_start && (!path_start || port_start < path_start)) {
            *port_start = '\0';
            req.port = atoi(port_start + 1);
        }
        
        strcpy(req.host, hostname_start);
    } else {
        // Relative URL - need to find Host header
        strcpy(req.path, url);
        
        // Look for Host header
        char* line = strtok(NULL, "\r\n");
        while (line) {
            if (strncasecmp(line, "Host:", 5) == 0) {
                if (get_host_from_header(line, req.host, &req.port)) {
                    break;
                }
            }
            line = strtok(NULL, "\r\n");
        }
    }
    
    if (strlen(req.host) > 0) {
        req.is_valid = 1;
    }
    
    free(request_copy);
    return req;
}

// Function to send error response to client
void send_error(int client_socket, char* error_message) {
    char response[BUFFER_SIZE];
    int content_length = strlen(error_message);
    
    snprintf(response, sizeof(response),
        "HTTP/1.1 502 Bad Gateway\r\n"
        "Content-Type: text/html\r\n"
        "Content-Length: %d\r\n"
        "\r\n"
        "%s",
        content_length, error_message);
    
    send(client_socket, response, strlen(response), 0);
}

// Function to connect to remote server
int connect_to_server(char* hostname, int port) {
    printf("Connecting to %s:%d...\n", hostname, port);
    
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        printf("Failed to create socket\n");
        return -1;
    }
    
    struct addrinfo hints, *result;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    
    char port_str[16];
    snprintf(port_str, sizeof(port_str), "%d", port);
    
    int status = getaddrinfo(hostname, port_str, &hints, &result);
    if (status != 0) {
        printf("getaddrinfo failed: %s\n", gai_strerror(status));
        close(server_socket);
        return -1;
    }
    
    if (connect(server_socket, result->ai_addr, result->ai_addrlen) < 0) {
        printf("Connection failed: %s\n", strerror(errno));
        freeaddrinfo(result);
        close(server_socket);
        return -1;
    }
    
    freeaddrinfo(result);
    printf("✓ Connected to %s:%d successfully!\n", hostname, port);
    return server_socket;
}

// Function to forward data between sockets
void forward_data(int from_socket, int to_socket, char* direction) {
    char buffer[BUFFER_SIZE];
    int bytes_received;
    int total_forwarded = 0;
    
    printf("Forwarding data %s...\n", direction);
    
    while ((bytes_received = recv(from_socket, buffer, sizeof(buffer), 0)) > 0) {
        int bytes_sent = 0;
        int total_sent = 0;
        
        while (total_sent < bytes_received) {
            bytes_sent = send(to_socket, buffer + total_sent, 
                            bytes_received - total_sent, 0);
            if (bytes_sent < 0) {
                printf("Error sending data\n");
                return;
            }
            total_sent += bytes_sent;
        }
        total_forwarded += bytes_received;
    }
    
    printf("Forwarded %d bytes %s\n", total_forwarded, direction);
}

// Function to handle each client connection
void handle_client(int client_socket) {
    char buffer[BUFFER_SIZE];
    
    printf("\n=== Handling Client (PID: %d) ===\n", getpid());
    
    // Read HTTP request from client
    int bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
    if (bytes_received <= 0) {
        printf("Failed to receive data from client\n");
        close(client_socket);
        return;
    }
    
    buffer[bytes_received] = '\0';
    printf("Received %d bytes from client\n", bytes_received);
    
    // Parse the request
    HttpRequest request = parse_request(buffer);
    
    if (!request.is_valid) {
        printf("Invalid HTTP request\n");
        send_error(client_socket, "Invalid HTTP request");
        close(client_socket);
        return;
    }
    
    printf("=== Parsed Request ===\n");
    printf("Method: %s\n", request.method);
    printf("Host: %s\n", request.host);
    printf("Port: %d\n", request.port);
    printf("Path: %s\n", request.path);
    
    // Connect to remote server
    int server_socket = connect_to_server(request.host, request.port);
    if (server_socket < 0) {
        printf("Failed to connect to server\n");
        send_error(client_socket, "Cannot connect to requested server");
        close(client_socket);
        return;
    }
    
    // Forward original request to server
    printf("Forwarding request to server...\n");
    if (send(server_socket, buffer, bytes_received, 0) < 0) {
        printf("Failed to send request to server\n");
        close(server_socket);
        close(client_socket);
        return;
    }
    
    // Forward response from server to client
    forward_data(server_socket, client_socket, "server->client");
    
    printf("✓ Client handled successfully!\n");
    
    // Clean up
    close(server_socket);
    close(client_socket);
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
        printf("Example: %s 8080\n", argv[0]);
        return 1;
    }
    
    int port = atoi(argv[1]);
    if (port <= 0 || port > 65535) {
        printf("Invalid port number. Must be between 1 and 65535.\n");
        return 1;
    }
    
    // Set up signal handlers
    signal(SIGCHLD, sigchld_handler);
    signal(SIGINT, sigint_handler);
    
    // Create proxy socket
    proxy_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (proxy_socket < 0) {
        perror("Failed to create socket");
        return 1;
    }
    
    // Set socket options
    int opt = 1;
    if (setsockopt(proxy_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("Failed to set socket options");
        return 1;
    }
    
    // Bind to port
    struct sockaddr_in proxy_addr;
    memset(&proxy_addr, 0, sizeof(proxy_addr));
    proxy_addr.sin_family = AF_INET;
    proxy_addr.sin_addr.s_addr = INADDR_ANY;
    proxy_addr.sin_port = htons(port);
    
    if (bind(proxy_socket, (struct sockaddr*)&proxy_addr, sizeof(proxy_addr)) < 0) {
        perror("Failed to bind socket");
        printf("Port %d may already be in use\n", port);
        return 1;
    }
    
    // Listen for connections
    if (listen(proxy_socket, 10) < 0) {
        perror("Failed to listen");
        return 1;
    }
    
    printf("=== Simple HTTP Proxy Server (Linux) ===\n");
    printf("✓ Proxy server listening on port %d\n", port);
    printf("✓ Configure your browser to use 127.0.0.1:%d as HTTP proxy\n", port);
    printf("✓ Press Ctrl+C to stop the server\n\n");
    
    int client_count = 0;
    
    // Main server loop
    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        
        printf("Waiting for client connection...\n");
        
        // Accept connection
        int client_socket = accept(proxy_socket, (struct sockaddr*)&client_addr, &client_len);
        if (client_socket < 0) {
            if (errno == EINTR) continue; // Interrupted by signal
            perror("Failed to accept connection");
            continue;
        }
        
        client_count++;
        printf("✓ Client #%d connected from %s:%d\n", 
               client_count, inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
        
        // Fork child process to handle client
        pid_t pid = fork();
        if (pid == 0) {
            // Child process
            close(proxy_socket); // Child doesn't need listening socket
            handle_client(client_socket);
            exit(0);
        } else if (pid > 0) {
            // Parent process
            close(client_socket); // Parent doesn't need client socket
        } else {
            // Fork failed
            perror("Failed to fork");
            close(client_socket);
        }
    }
    
    return 0;
}
