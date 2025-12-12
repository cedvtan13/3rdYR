# Members: Kent Vincent S. Godinez, Cedric Vince M. Tan
# Updates:
#   (12/8/2025)     > created this client-server socket sonnection using TCP 
#                   > updated the code from Dr. Philip since it was not bi directional and the server can only send one message at a time.
#                   > based on AI study:
#                       - this is a full duplex communication, which means that both sides can receive simultaneously
#                       - multithreaded, since it uses threads to handle sending and receiving at the same time
#                   > initially i thought it was peer to peer but its not
#   (12/8/2025)     > added the RSA implementation for secure comms
#   (12/12/2025)    > added the cryptography library for better security practices

import socket
import pickle
from threading import Thread
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

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
            signature = package['signature']

            # decrypt using the server's private key
            decrypted_msg = server_private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ).decode()

            # verify signature using the client's public key
            try:
                client_public_key.verify(
                    signature,
                    decrypted_msg.encode(),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                print(f"\nMessage Received (verified): {decrypted_msg}")
            except:
                print(f"\nMessage Received (verification failed): {decrypted_msg}")
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
            ciphertext = client_public_key.encrypt(
                msg.encode(),
                padding.OAEP(
                    mgf = padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm = hashes.SHA256(),
                    label = None
                )
            )

            # sign the message with server's private key
            signature = server_private_key.sign(
                msg.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            # concatenate ciphertext and singature into a package
            package = {
                'ciphertext': ciphertext, 'signature': signature
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
    server_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    ) 
    server_public_key = server_private_key.public_key()

    # serialize server's public key for transmission
    server_public_key_bytes = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # establish connection with client
    conn, addr, s = listenConnection()

    # exchange puclic keys
    # send receiver's public key to client
    print("\nSending my public key to client...")
    conn.sendall(server_public_key_bytes)

    # receive client's public key
    client_public_key_bytes = conn.recv(4096)
    client_public_key = serialization.load_pem_public_key(
        client_public_key_bytes,
        backend=default_backend()
    )
    print("\nPublic keys exchanged successfuly!")

    #start comm threads
    rcv = Thread(target=receiveMsg, args=(conn, ))
    rcv.start()
    sendMessage(conn)

    # wait for rcv thread to finish
    rcv.join()

    # close both connection and server socket
    conn.close()
    s.close()
