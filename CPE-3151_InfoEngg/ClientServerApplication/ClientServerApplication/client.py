# Members: Kent Vincent S. Godinez, Cedric Vince M. Tan
# Updates:
#   (12/8/2025) - created this client-server socket sonnection using TCP
#               - updated the code from Dr. Philip since it was not bi directional and the server can only send one message at a time.
#               > based on AI study:
#                   - this is a full duplex communication, which means that both sides can receive simultaneously
#                   - multithreaded, since it uses threads to handle sending and receiving at the same time
#               - initially i thought it was peer to peer but its not

import socket
import rsa
import pickle
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))
run = True
# storage for client's publicK
client_public_key = None

def sendMessage():
    global run
    while run:
        try:
            msg = input("Type Message: ")
            if msg.lower() == 'exit' or msg.lower() == 'quit':
                print("disconnectring...")
                run = False
                s.close()
                break

            # encrypt message with server's privateK
            ciphertext = rsa.encrypt(msg.encode(), server_public_key)

            # sign the hash(digest) with client's privateK
            digest = rsa.sign(ciphertext, client_private_key, 'SHA-1')

            # concatenate ciphoertext and digest into a package
            package = {
                'ciphertext': ciphertext, 'digest': digest
            }

            s.sendall(pickle.dumps(package))
            
        except socket.error as err:
            run = False
        except KeyboardInterrupt:
            run = False
            s.close()

def receiveMsg():
    global run
    while run:
        try:
            data = s.recv(4096) #increase to 4096 for encrypted data
            if not data:
                run = False
                break

            # desrializzr the package
            package = pickle.loads(data)
            ciphertext = package['ciphertext']
            digest = package['digest']

            # decrypt using the server's private key
            decrypted_msg = rsa.decrypt(ciphertext, client_private_key).decode()

            # verify signature using the client's public key
            try:
                rsa.verify(ciphertext, digest, server_public_key)
                print(f"\nMessage Received (verified): {decrypted_msg}")
            except:
                print("\nMessage Received (verification failed): {}".format(decrypted_msg))

        except socket.error as msg:
            run = False
        except KeyboardInterrupt:
            run = False

# rsa key pair for client
print("Gneerating RSA key pair")
(client_public_key, client_private_key) = rsa.newkeys(1024)

# exchange publicK
# receive server's publicK
server_public_key = pickle.loads(s.recv(4096))

# sned client's publicK to server
s.sendall(pickle.dumps(client_public_key))
print("Public keys exchanged successfully!")

# receive thread initialization
recv_thread = Thread(target=receiveMsg)
recv_thread.start()

# sned message to main thread
sendMessage()

# wait for receive thread to finish
recv_thread.join()
