import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))
run = True


def receiveMsg():
    global run
    while run:
        try:
            data = s.recv(1024)
            if not data:
                print("Server disconnected.")
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


def sendMessage():
    global run
    while run:
        try:
            msg = input("Type Message: ")
            if msg.lower() == 'quit':
                run = False
                break
            s.sendall(msg.encode())
        except socket.error as err:
            print(f"Socket error: {err}")
            run = False
            break
        except KeyboardInterrupt:
            run = False
            break


if __name__ == '__main__':
    print("Connected to server. Type 'quit' to exit.")
    
    # Start receiving thread
    rcv = Thread(target=receiveMsg)
    rcv.start()
    
    # Start sending thread
    snd = Thread(target=sendMessage)
    snd.start()
    
    # Keep main thread alive until user quits
    try:
        while run:
            pass
    except KeyboardInterrupt:
        run = False
    
    # Clean up
    s.close()
    print("Client disconnected.")