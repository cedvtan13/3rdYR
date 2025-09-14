#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>

// Link with Winsock library
#pragma comment(lib, "ws2_32.lib")

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

// Function to initialize Windows sockets
int init_winsock() {
    WSADATA wsaData;
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (result != 0) {
        printf("WSAStartup failed: %d\n", result);
        return 0;
    }
    printf("Winsock initialized successfully!\n");
    return 1;
}

// Function to clean up Windows sockets
void cleanup_winsock() {
    WSACleanup();
    printf("Winsock cleaned up.\n");
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

// Simple function to parse HTTP request
HttpRequest parse_request(char* request) {
    HttpRequest req;
    memset(&req, 0, sizeof(req));  // Clear everything to 0
    req.port = 80;  // Default HTTP port
    req.is_valid = 0;
    
    printf("\n=== Parsing HTTP Request ===\n");
    printf("Raw request:\n%s\n", request);
    
    // Make a copy we can modify
    char temp[BUFFER_SIZE];
    strcpy_s(temp, sizeof(temp), request);
    
    // Get first line: "GET http://www.google.com/ HTTP/1.1"
    char* first_line = strtok_s(temp, "\r\n", NULL);
    if (!first_line) {
        printf("ERROR: No first line found!\n");
        return req;
    }
    
    printf("First line: %s\n", first_line);
    
    // Parse: METHOD URL VERSION
    char url[512];
    if (sscanf_s(first_line, "%15s %511s", req.method, (unsigned)sizeof(req.method), url, (unsigned)sizeof(url)) != 2) {
        printf("ERROR: Cannot parse method and URL!\n");
        return req;
    }
    
    printf("Method: %s\n", req.method);
    printf("URL: %s\n", url);
    
    // Check if URL starts with http://
    if (strncmp(url, "http://", 7) == 0) {
        // Full URL like: http://www.google.com/search
        char* host_start = url + 7;  // Skip "http://"
        char* path_start = strchr(host_start, '/');
        
        if (path_start) {
            // Copy path
            strcpy_s(req.path, sizeof(req.path), path_start);
            *path_start = '\0';  // Cut off path from host
        } else {
            strcpy_s(req.path, sizeof(req.path), "/");
        }
        
        // Check for port in host (like www.google.com:8080)
        char* port_start = strchr(host_start, ':');
        if (port_start) {
            *port_start = '\0';
            req.port = atoi(port_start + 1);
        }
        
        strcpy_s(req.host, sizeof(req.host), host_start);
    } else {
        // Relative URL like: /search?q=hello
        strcpy_s(req.path, sizeof(req.path), url);
        
        // Need to find host in headers
        char* line_context = NULL;
        char* line = strtok_s(NULL, "\r\n", &line_context);
        while (line) {
            if (strncmp(line, "Host:", 5) == 0) {
                char* host_value = line + 5;
                host_value = trim_string(host_value);
                
                // Check for port
                char* port_pos = strchr(host_value, ':');
                if (port_pos) {
                    *port_pos = '\0';
                    req.port = atoi(port_pos + 1);
                }
                
                strcpy_s(req.host, sizeof(req.host), host_value);
                break;
            }
            line = strtok_s(NULL, "\r\n", &line_context);
        }
    }
    
    // Check if we got a valid host
    if (strlen(req.host) > 0) {
        req.is_valid = 1;
        printf("✓ Valid request parsed!\n");
        printf("  Host: %s\n", req.host);
        printf("  Port: %d\n", req.port);
        printf("  Path: %s\n", req.path);
    } else {
        printf("✗ Invalid request - no host found!\n");
    }
    
    return req;
}

// Function to send error message to client
void send_error(SOCKET client_socket, char* error_message) {
    char response[1024];
    sprintf_s(response, sizeof(response),
        "HTTP/1.1 400 Bad Request\r\n"
        "Content-Type: text/html\r\n"
        "Content-Length: %d\r\n"
        "\r\n"
        "%s", (int)strlen(error_message), error_message);
    
    send(client_socket, response, (int)strlen(response), 0);
    printf("Sent error response to client.\n");
}

// Function to connect to the web server
SOCKET connect_to_server(char* hostname, int port) {
    printf("\n=== Connecting to Server ===\n");
    printf("Connecting to %s:%d...\n", hostname, port);
    
    // Create socket
    SOCKET server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_socket == INVALID_SOCKET) {
        printf("ERROR: Cannot create server socket!\n");
        return INVALID_SOCKET;
    }
    
    // Get server address
    struct addrinfo hints, *result;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    
    char port_str[16];
    sprintf_s(port_str, sizeof(port_str), "%d", port);
    
    if (getaddrinfo(hostname, port_str, &hints, &result) != 0) {
        printf("ERROR: Cannot resolve hostname %s\n", hostname);
        closesocket(server_socket);
        return INVALID_SOCKET;
    }
    
    // Connect to server
    if (connect(server_socket, result->ai_addr, (int)result->ai_addrlen) == SOCKET_ERROR) {
        printf("ERROR: Cannot connect to %s:%d\n", hostname, port);
        freeaddrinfo(result);
        closesocket(server_socket);
        return INVALID_SOCKET;
    }
    
    freeaddrinfo(result);
    printf("✓ Connected to server successfully!\n");
    return server_socket;
}

// Function to forward data from one socket to another
void forward_data(SOCKET from_socket, SOCKET to_socket, char* direction) {
    char buffer[BUFFER_SIZE];
    int bytes_received;
    
    printf("Forwarding data %s...\n", direction);
    
    while ((bytes_received = recv(from_socket, buffer, sizeof(buffer), 0)) > 0) {
        int bytes_sent = send(to_socket, buffer, bytes_received, 0);
        if (bytes_sent <= 0) {
            printf("Error sending data %s\n", direction);
            break;
        }
        printf("Forwarded %d bytes %s\n", bytes_received, direction);
    }
    
    printf("Done forwarding %s\n", direction);
}

// Main function to handle one client
void handle_client(SOCKET client_socket) {
    char buffer[BUFFER_SIZE];
    
    printf("\n=== New Client Connected ===\n");
    
    // Read request from client
    int bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
    if (bytes_received <= 0) {
        printf("ERROR: No data received from client!\n");
        closesocket(client_socket);
        return;
    }
    
    buffer[bytes_received] = '\0';  // Make it a proper string
    printf("Received %d bytes from client\n", bytes_received);
    
    // Parse the HTTP request
    HttpRequest request = parse_request(buffer);
    if (!request.is_valid) {
        send_error(client_socket, "Bad Request - Cannot parse your request");
        closesocket(client_socket);
        return;
    }
    
    // Connect to the actual web server
    SOCKET server_socket = connect_to_server(request.host, request.port);
    if (server_socket == INVALID_SOCKET) {
        send_error(client_socket, "Cannot connect to requested server");
        closesocket(client_socket);
        return;
    }
    
    // Send original request to server
    printf("\n=== Forwarding Request to Server ===\n");
    if (send(server_socket, buffer, bytes_received, 0) <= 0) {
        printf("ERROR: Cannot send request to server!\n");
        closesocket(server_socket);
        closesocket(client_socket);
        return;
    }
    printf("✓ Request sent to server!\n");
    
    // Forward response from server back to client
    printf("\n=== Forwarding Response to Client ===\n");
    forward_data(server_socket, client_socket, "server->client");
    
    // Clean up
    closesocket(server_socket);
    closesocket(client_socket);
    printf("✓ Client handled successfully!\n");
}

int main(int argc, char* argv[]) {
    printf("=== Simple HTTP Proxy Server ===\n");
    
    // Check command line arguments
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
        printf("Example: %s 8080\n", argv[0]);
        return 1;
    }
    
    int port = atoi(argv[1]);
    if (port <= 0 || port > 65535) {
        printf("Invalid port! Use a number between 1 and 65535.\n");
        return 1;
    }
    
    // Initialize Windows sockets
    if (!init_winsock()) {
        return 1;
    }
    
    // Create listening socket
    SOCKET proxy_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (proxy_socket == INVALID_SOCKET) {
        printf("ERROR: Cannot create proxy socket!\n");
        cleanup_winsock();
        return 1;
    }
    
    // Set up address
    struct sockaddr_in proxy_addr;
    proxy_addr.sin_family = AF_INET;
    proxy_addr.sin_addr.s_addr = INADDR_ANY;  // Listen on all interfaces
    proxy_addr.sin_port = htons(port);
    
    // Bind socket to port
    if (bind(proxy_socket, (struct sockaddr*)&proxy_addr, sizeof(proxy_addr)) == SOCKET_ERROR) {
        printf("ERROR: Cannot bind to port %d! (Maybe it's already in use?)\n", port);
        closesocket(proxy_socket);
        cleanup_winsock();
        return 1;
    }
    
    // Start listening
    if (listen(proxy_socket, 5) == SOCKET_ERROR) {
        printf("ERROR: Cannot listen on port %d!\n", port);
        closesocket(proxy_socket);
        cleanup_winsock();
        return 1;
    }
    
    printf("✓ Proxy server is listening on port %d\n", port);
    printf("✓ Configure your browser to use 127.0.0.1:%d as HTTP proxy\n", port);
    printf("✓ Press Ctrl+C to stop the server\n\n");
    
    // Main server loop - handle clients one by one (simple approach)
    while (1) {
        struct sockaddr_in client_addr;
        int client_len = sizeof(client_addr);
        
        printf("Waiting for client connection...\n");
        
        // Accept a client connection
        SOCKET client_socket = accept(proxy_socket, (struct sockaddr*)&client_addr, &client_len);
        if (client_socket == INVALID_SOCKET) {
            printf("ERROR: Failed to accept client connection!\n");
            continue;
        }
        
        printf("Client connected from %s\n", inet_ntoa(client_addr.sin_addr));
        
        // Handle this client (one at a time for simplicity)
        handle_client(client_socket);
        
        printf("\nReady for next client...\n");
    }
    
    // Clean up (this won't be reached, but good practice)
    closesocket(proxy_socket);
    cleanup_winsock();
    return 0;
}