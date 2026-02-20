import socket
from threading import Thread

run = True

def receive_messages(s):
    """Receive messages from server"""
    global run
    while run:
        try:
            data = s.recv(1024)
            if not data:
                continue
            msg = data.decode()
            print(f'\n[SERVER]: {msg}')
            print('Type message: ', end='', flush=True)
        except socket.error:
            run = False
            break
        except KeyboardInterrupt:
            run = False
            break

def send_messages(s):
    """Send messages to server"""
    global run
    while run:
        try:
            msg = input('Type message: ')
            s.sendall(msg.encode())
        except socket.error:
            run = False
            break
        except KeyboardInterrupt:
            run = False
            break

def start_client():
    """Connect to chat server"""
    # Connect to server VM IP
    SERVER_IP = '192.168.100.10'  # Server VM IP
    SERVER_PORT = 8000
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print(f'[*] Connecting to server {SERVER_IP}:{SERVER_PORT}...')
    try:
        s.connect((SERVER_IP, SERVER_PORT))
        print('[+] Connected to server!\n')
    except socket.error as e:
        print(f'[!] Connection failed: {e}')
        return
    
    # Start receiver thread
    rcv_thread = Thread(target=receive_messages, args=(s,))
    rcv_thread.start()
    
    # Start sender thread
    send_thread = Thread(target=send_messages, args=(s,))
    send_thread.start()
    
    rcv_thread.join()
    send_thread.join()
    s.close()
    print('\n[*] Disconnected from server.')

if __name__ == '__main__':
    try:
        start_client()
    except KeyboardInterrupt:
        print('\n[*] Client shutting down...')
        run = False
