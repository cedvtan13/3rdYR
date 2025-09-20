import socket
from threading import Thread

run = True


def receiveMsg(conn):
    global run
    while run:
        try:
            data = conn.recv(1024)
            if not data:
                print("Client disconnected.")
                run = False
                break
            print('Message Received: {}'.format(data.decode()))

        except socket.error as msg:
            print(f"Socket error: {msg}")
            run = False
            break
        except KeyboardInterrupt:
            run = False
            break


def sendMessage(conn):
    global run
    while run:
        try:
            msg = input("Type Message: ")
            if msg.lower() == 'quit':
                run = False
                break
            conn.sendall(msg.encode())
        except socket.error as err:
            print(f"Socket error: {err}")
            run = False
            break
        except KeyboardInterrupt:
            run = False
            break


def listenConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.0.186', 6000))
    s.listen(1)
    conn, addr = s.accept()
    print('Server accepted client connection...')
    return conn, addr, s


if __name__ == '__main__':
    conn, addr, s = listenConnection()
    
    print("Server started. You can now send and receive messages.")
    print("Type 'quit' to stop the server.")
    
    # Start receiving thread
    rcv = Thread(target=receiveMsg, args=(conn,))
    rcv.daemon = True  # Dies when main thread dies
    rcv.start()
    
    # Start sending thread  
    snd = Thread(target=sendMessage, args=(conn,))
    snd.daemon = True  # Dies when main thread dies
    snd.start()
    
    # Keep main thread alive until user quits
    try:
        while run:
            pass
    except KeyboardInterrupt:
        run = False
    
    # Clean up
    conn.close()
    s.close()
    print("Server shut down.")
