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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))
run = True

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

            # encrypt message with server's publicK
            ciphertext = server_public_key.encrypt(
                msg.encode(),
                padding.OAEP(
                    mgf = padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm = hashes.SHA256(),
                    label = None
                )
            )

            # sign the message with client's privateK
            signature = client_private_key.sign(
                msg.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            # concatenate ciphoertext and signature into a package
            package = {
                'ciphertext': ciphertext, 'signature': signature
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
            data = s.recv(8192) #increase to 8192 for encrypted data
            if not data:
                run = False
                break

            # desrializzr the package
            package = pickle.loads(data)
            ciphertext = package['ciphertext']
            signature = package['signature']

            # decrypt using the server's private key
            decrypted_msg = client_private_key.decrypt(
                ciphertext, 
                padding.OAEP(
                    mgf = padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm = hashes.SHA256(),
                    label = None
                )
            ).decode()

            # verify signature using the client's public key
            try:
                server_public_key.verify(
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

        except socket.error as msg:
            run = False
        except KeyboardInterrupt:
            run = False

# rsa key pair for client
print("Gneerating RSA key pair")
client_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
client_public_key = client_private_key.public_key()

# serialize publicK for transmission
client_public_key_bytes = client_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("Exchanging public keys...")

# receive server's publicK
server_public_key_bytes = s.recv(4096)
server_public_key = serialization.load_pem_public_key(
    server_public_key_bytes,
    backend=default_backend()
)

# sned client's publicK to server
s.sendall(client_public_key_bytes)
print("Public keys exchanged successfully!")

# receive thread initialization
recv_thread = Thread(target=receiveMsg)
recv_thread.start()

# sned message to main thread
sendMessage()

# wait for receive thread to finish
recv_thread.join()
