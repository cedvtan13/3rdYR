# Members: Kent Vincent S. Godinez, Cedric Vince M. Tan
# Updates:
#   (12/8/2025) > created this client-server socket sonnection using TCP 
#               > updated the code from Dr. Philip since it was not bi directional and the server can only send one message at a time.
#               > based on AI study:
#                   - this is a full duplex communication, which means that both sides can receive simultaneously
#                   - multithreaded, since it uses threads to handle sending and receiving at the same time
#               > initially i thought it was peer to peer but its not
#   (12/8/2025) > added the RSA implementation
#               > 

import socket
import rsa
import pickle
from threading import Thread

run = True
# storage for client's pubK
client_public_key = None

def receiveMsg(conn):
    global run
    while run:
        try:
            data = conn.recv(4096) #increase to 4096 for encrypted data
            if not data:
                run = False
                break

            # desrializzr the package
            package = pickle.loads(data)
            ciphertext = package['ciphertext']
            digest = package['digest']

            # decrypt using the server's private key
            decrypted_msg = rsa.decrypt(ciphertext, server_private_key).decode()

            # verify signature using the client's public key
            try:
                rsa.verify(ciphertext, digest, client_public_key)
                print(f"\nMessage Received (verified): {decrypted_msg}")
            except:
                print("\nMessage Received (verification failed): {}".format(decrypted_msg))
            # if not data:
            #     continue
            # print('\nMessage Received: {}'.format(data.decode()))

        except socket.error as msg:
            run = False
        except KeyboardInterrupt:
            run = False

    conn.close()


def sendMessage(conn):
    global run
    while run:
        try:
            msg = input("Type Message: ")
            if msg.lower() == 'exit' or msg.lower() == 'quit':
                print("disconnectring...")
                run = False
                break

            # encrypt message with client's Kp
            ciphertext = rsa.encrypt(msg.encode(), client_public_key)

            # sign the hash(digest) with server's private key
            digest = rsa.sign(ciphertext, server_private_key, 'SHA-1')

            # concatenate ciphertext and digest into a package
            package = {
                'ciphertext': ciphertext, 'digest': digest
            }

            # serializze and then transmit
            conn.sendall(pickle.dumps(package))

        except socket.error as err:
            run = False
        except KeyboardInterrupt:
            run = False


def listenConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 8000))
    s.listen(1)
    conn, addr = s.accept()
    print('Server accepted client connection...')
    return conn, addr, s


if __name__ == '__main__':
    # rsa key pair generation for the server
    print("Gneerating RSA key pair")
    (server_public_key, server_private_key) = rsa.newkeys(1024)

    conn, addr, s = listenConnection()
    # exchange puclic keys
    # send receiver's public key to client
    print("\nSending my public key to client...")
    conn.sendall(pickle.dumps(server_public_key))

    # receive client's public key
    client_public_key = pickle.loads(conn.recv(4096))
    print("\nPublic keys exchanged successfuly!")

    #start comms
    rcv = Thread(target=receiveMsg, args=(conn, ))
    rcv.start()
    sendMessage(conn)

    # wait for rcv thread to finish
    rcv.join()

    # close both connection and server socket
    conn.close()
    s.close()
