# HTTP Proxy Server - Implementation Report

## Overview
This document describes a simple HTTP proxy server implementation that handles multiple client connections using fork() and basic socket programming in C.

## Implementation Details

### Core Functionality
- **Proxy Server**: Accepts HTTP requests from clients and forwards them to target web servers
- **Multi-client Support**: Uses fork() to create separate processes for each client connection
- **HTTP Parsing**: Extracts hostname from GET requests (supports both full URLs and Host headers)
- **Data Forwarding**: Relays requests to target servers and responses back to clients

### Key Components

#### 1. Main Server Loop
- Creates and binds socket to specified port from command line
- Listens for incoming client connections
- Forks child process for each new client
- Parent process continues accepting new connections

#### 2. Client Handler (`handle_client` function)
- Reads HTTP request from client
- Parses request to extract target hostname
- Connects to target web server on port 80
- Forwards original request to target server
- Relays response data back to client

#### 3. HTTP Request Parsing
- Supports GET method only (for simplicity)
- Handles two URL formats:
  - Full URL: `GET http://example.com/path HTTP/1.1`
  - Relative URL: `GET /path HTTP/1.1` (with Host header)
- Extracts hostname for server connection

### Technical Specifications
- **Language**: C
- **Required Libraries**: Standard POSIX socket libraries
- **Compilation**: `gcc -o proxy_server proxy_server.c`
- **Usage**: `./proxy_server <port>`
- **Supported Protocol**: HTTP (port 80 only)
- **Request Method**: GET only

### Architecture Benefits
- **Simple Design**: Easy to understand for learning purposes
- **Process Isolation**: Each client handled in separate process
- **Concurrent Handling**: Multiple clients can connect simultaneously
- **Basic Error Handling**: Simple error messages for debugging

### Limitations
- HTTP only (no HTTPS support)
- GET requests only
- Fixed port 80 for target servers
- No advanced error recovery
- Basic request parsing

---

# How to Test Your Proxy Server

## Step 1: Compile
```bash
gcc -o proxy_server proxy_server.c
```

## Step 2: Run the proxy
```bash
./proxy_server 8080
```

You should see:
```
Starting proxy server on port 8080...
Proxy server running! Waiting for connections...
```

## Step 3: Test with curl

Open a new terminal and try:

```bash
# Test 1: Simple website
curl --proxy http://localhost:8080 http://example.com

# Test 2: Different website  
curl --proxy http://localhost:8080 http://httpbin.org/get
```

## What you should see:

In the proxy terminal:
```
New client connected!
Received request:
GET http://example.com/ HTTP/1.1
...

Connecting to host: example.com
Connected to example.com, forwarding request...
Request completed!
```

In the curl terminal:
You should see the HTML content from the website.

## Common Issues:

**"Address already in use"**
- Wait a few seconds and try again, or use a different port

**"Connection refused"**  
- Make sure the proxy is running first

**No output from curl**
- Check that you typed the proxy URL correctly
- Try a different website

## Test multiple clients:
You can run several curl commands at the same time to test that the proxy handles multiple connections with fork().
