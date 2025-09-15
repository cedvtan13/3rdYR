#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include <regex>

#define BUFFER_SIZE 8192
#define BACKLOG 10

using namespace std;

// Function declarations
void sigchld_handler(int s);
void handle_client(int client_socket);
bool parse_http_request(const string& request, string& method, string& url, string& version);
bool parse_url(const string& url, string& host, int& port, string& path);
void send_error_response(int client_socket, int status_code, const string& message);
void forward_request(int client_socket, const string& host, int port, const string& path, const string& original_request);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <port>" << endl;
        exit(1);
    }

    int port = atoi(argv[1]);
    if (port <= 0 || port > 65535) {
        cerr << "Invalid port number" << endl;
        exit(1);
    }

    // Set up signal handler for zombie processes
    struct sigaction sa;
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    if (sigaction(SIGCHLD, &sa, NULL) == -1) {
        perror("sigaction");
        exit(1);
    }

    // Create socket
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("socket");
        exit(1);
    }

    // Set socket options to reuse address
    int yes = 1;
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
        perror("setsockopt");
        exit(1);
    }

    // Bind socket
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = INADDR_ANY;
    memset(&(server_addr.sin_zero), '\0', 8);

    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("bind");
        exit(1);
    }

    // Listen for connections
    if (listen(server_socket, BACKLOG) == -1) {
        perror("listen");
        exit(1);
    }

    cout << "Proxy server listening on port " << port << endl;

    // Main accept loop
    struct sockaddr_in client_addr;
    socklen_t sin_size;
    int client_socket;

    while (true) {
        sin_size = sizeof(client_addr);
        client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &sin_size);

        if (client_socket == -1) {
            perror("accept");
            continue;
        }

        // Fork to handle client
        if (!fork()) {
            // Child process
            close(server_socket);
            handle_client(client_socket);
            close(client_socket);
            exit(0);
        }
        close(client_socket);
    }

    return 0;
}

void sigchld_handler(int s) {
    // Wait for zombie processes
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

void handle_client(int client_socket) {
    char buffer[BUFFER_SIZE];
    ssize_t bytes_received;

    // Read HTTP request from client
    bytes_received = recv(client_socket, buffer, BUFFER_SIZE - 1, 0);
    if (bytes_received <= 0) {
        return;
    }
    buffer[bytes_received] = '\0';

    string request(buffer);
    string method, url, version;

    // Parse HTTP request
    if (!parse_http_request(request, method, url, version)) {
        send_error_response(client_socket, 400, "Bad Request");
        return;
    }

    // Only support GET method for simplicity
    if (method != "GET") {
        send_error_response(client_socket, 501, "Not Implemented");
        return;
    }

    string host;
    int port;
    string path;

    // Parse URL
    if (!parse_url(url, host, port, path)) {
        send_error_response(client_socket, 400, "Bad Request - Invalid URL");
        return;
    }

    // Forward request to remote server
    forward_request(client_socket, host, port, path, request);
}

bool parse_http_request(const string& request, string& method, string& url, string& version) {
    regex request_line_regex("^([A-Z]+) ([^ ]+) (HTTP/\\d\\.\\d)");
    smatch matches;

    if (regex_search(request, matches, request_line_regex) && matches.size() == 4) {
        method = matches[1];
        url = matches[2];
        version = matches[3];
        return true;
    }
    return false;
}

bool parse_url(const string& url, string& host, int& port, string& path) {
    regex url_regex("^http://([^/:]+)(?::(\\d+))?(/.*)?$");
    smatch matches;

    if (regex_search(url, matches, url_regex)) {
        host = matches[1];

        if (matches[2].matched) {
            port = stoi(matches[2]);
        } else {
            port = 80; // Default HTTP port
        }

        if (matches[3].matched) {
            path = matches[3];
        } else {
            path = "/";
        }

        return true;
    }
    return false;
}

void send_error_response(int client_socket, int status_code, const string& message) {
    string response = "HTTP/1.0 " + to_string(status_code) + " " + message + "\r\n";
    response += "Content-Type: text/plain\r\n";
    response += "Connection: close\r\n";
    response += "\r\n";
    response += message;

    send(client_socket, response.c_str(), response.length(), 0);
}

void forward_request(int client_socket, const string& host, int port, const string& path, const string& original_request) {
    // Create socket to remote server
    int remote_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (remote_socket == -1) {
        send_error_response(client_socket, 500, "Internal Server Error");
        return;
    }

    // Get host information
    struct hostent *he = gethostbyname(host.c_str());
    if (he == NULL) {
        close(remote_socket);
        send_error_response(client_socket, 502, "Bad Gateway");
        return;
    }

    // Set up remote server address
    struct sockaddr_in remote_addr;
    remote_addr.sin_family = AF_INET;
    remote_addr.sin_port = htons(port);
    remote_addr.sin_addr = *((struct in_addr *)he->h_addr);
    memset(&(remote_addr.sin_zero), '\0', 8);

    // Connect to remote server
    if (connect(remote_socket, (struct sockaddr *)&remote_addr, sizeof(remote_addr)) == -1) {
        close(remote_socket);
        send_error_response(client_socket, 502, "Bad Gateway");
        return;
    }

    // Modify request to use absolute path
    string modified_request = original_request;
    size_t url_start = modified_request.find("http://" + host);
    if (url_start != string::npos) {
        modified_request.replace(url_start, string("http://" + host).length(), path);
    }

    // Send request to remote server
    if (send(remote_socket, modified_request.c_str(), modified_request.length(), 0) == -1) {
        close(remote_socket);
        send_error_response(client_socket, 502, "Bad Gateway");
        return;
    }

    // Forward response from remote server to client
    char buffer[BUFFER_SIZE];
    ssize_t bytes_received;

    while ((bytes_received = recv(remote_socket, buffer, BUFFER_SIZE, 0)) > 0) {
        if (send(client_socket, buffer, bytes_received, 0) == -1) {
            break;
        }
    }

    close(remote_socket);
}
