# AI Agent Instructions for 3rdYR Student Projects

This repository contains academic coursework for 3rd year Computer Engineering students. Keep solutions simple and educational.

## Project Overview

### CPE-3106_OS/ - Operating Systems Course
- **proxy_server.c**: Basic HTTP proxy using sockets and fork()
- **howToTest.md**: Simple testing instructions for students

### CPE-3151_InfoEngg/ - Information Engineering Course  
- **cpe3151_2023.py**: Python scripts for data processing

## Key Principles for This Codebase

### Keep It Simple
- Use basic C concepts students are learning
- Avoid advanced features or optimizations
- Include lots of comments explaining each step
- Focus on core socket programming and process concepts

### HTTP Proxy Architecture
- Main process listens on a port from command line
- Fork() creates child process for each client
- Child process handles: read request → connect to server → forward data
- Simple HTTP parsing (GET requests only)
- Uses standard port 80 for target servers

### Educational Focus
- **Socket Programming**: socket(), bind(), listen(), accept(), connect()
- **Process Management**: fork() for concurrent client handling  
- **HTTP Basics**: Request parsing and data forwarding
- **Error Handling**: Simple error messages with printf()

## Development Guidelines

### Compilation
```bash
gcc -o proxy_server proxy_server.c
```
No Makefile needed - keep it simple for students.

### Testing
- Use curl with --proxy flag for testing
- Test with multiple concurrent connections
- Focus on common websites (example.com, httpbin.org)

### Code Style
- Heavy commenting for learning
- Simple variable names
- Basic error handling with printf()
- One function per major task
- No dynamic memory allocation

When helping with this code, prioritize educational clarity over efficiency. Students are learning fundamental concepts, not building production systems.