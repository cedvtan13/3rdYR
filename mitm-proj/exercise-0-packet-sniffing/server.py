import socket
from threading import Thread

run = True

def receive_messages(conn, addr):
    """Receive messages from client"""
    global run
    while run:
        try:
            data = conn.recv(1024)
            if not data:
                continue
            msg = data.decode()
            print(f'\n[CLIENT]: {msg}')
            print('Type message: ', end='', flush=True)
        except socket.error:
            run = False
            break
        except KeyboardInterrupt:
            run = False
            break
    conn.close()

def send_messages(conn):
    """Send messages to client"""
    global run
    while run:
        try:
            msg = input('Type message: ')
            conn.sendall(msg.encode())
        except socket.error:
            run = False
            break
        except KeyboardInterrupt:
            run = False
            break

def start_server():
    """Start the chat server"""
    # Bind to all interfaces so client can connect
    HOST = '0.0.0.0'
    PORT = 8000
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    
    print(f'[*] Server listening on port {PORT}...')
    print('[*] Waiting for client connection...\n')
    
    conn, addr = s.accept()
    print(f'[+] Client connected from {addr[0]}:{addr[1]}\n')
    
    # Start receiver thread
    rcv_thread = Thread(target=receive_messages, args=(conn, addr))
    rcv_thread.start()
    
    # Start sender thread
    send_thread = Thread(target=send_messages, args=(conn,))
    send_thread.start()
    
    rcv_thread.join()
    send_thread.join()
    s.close()
    print('\n[*] Server closed.')

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        print('\n[*] Server shutting down...')
        run = False
