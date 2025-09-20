import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))
run = True
while run:
    try:
        msg = input("Type Message: ")
        s.sendall(msg.encode())
    except socket.error as err:
        run = False
    except KeyboardInterrupt:
        run = False

s.close()