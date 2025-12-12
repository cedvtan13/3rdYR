'''
Members: Kent Vincent S. Godinez, Cedric Vince M. Tan
Updates:
  (12/8/2025)     > created this client-server socket sonnection using TCP 
                  > updated the code from Dr. Philip since it was not bi directional and the server can only send one message at a time.
                  > based on AI study:
                      - this is a full duplex communication, which means that both sides can receive simultaneously
                      - multithreaded, since it uses threads to handle sending and receiving at the same time
                  > initially i thought it was peer to peer but its not
  (12/8/2025)     > added the RSA implementation for secure comms
  (12/12/2025)    > added the cryptography library for better security practices
  (12/13/2025)    > old: only RSA encrypts entire message; New: AES encrypts message, then RSA encrypts AES key
                  > old: no timestamp; new: 60 second validity timestamp
                  > old: only has digital signature; new: digital signature + HMAC
                  > old: 4096B buffer; new: 16384B buffer
                  > old: manual encrypt/decrypt; new: helper functions for clarity
'''

import socket
import pickle
import time  # For timestamps (prevent replay attacks)
import os   # For generating random bytes
from threading import Thread
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # For AES encryption
from cryptography.hazmat.primitives import padding as sym_padding  # For AES padding
from cryptography.hazmat.primitives import hmac  # For message authentication code

# this is the shared secret code for HMAC for both client and server (hardcoded)
SHARED_SECRET = b"CPE3151_shared_secret_key_2025"

run = True
# storage for client's pubK
client_public_key = None

def encrypt_message(message, recipient_public_key, sender_private_key):
    '''
    hybrid encryption:
    1. timestaps to prevent replay attacks
    2. random AES session key generation for fast symmetric encryption (256b = 32B) (encryption)
    3. message encryption with AES
    4. AES key encryption with RSA (secure key exchange)
    5. sign the original message with RSA (authentication)
    6. generate HMAC (integrity)
    '''

    # 1
    timestamp = str(int(time.time())) #current time in seconds
    timestamped_message = f"{timestamp}|{message}"

    # 2
    session_key = os.urandom(32)
    iv = os.urandom(16) #initialization vector (random starting point for AES)

    # 3
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    # since AES requires message length to be multiple of 16 bytes, we need to add the padding 
    padder = sym_padding.PKCS7(128).padder()
    padded_msg = padder.update(timestamped_message.encode()) + padder.finalize()
    # encryption with the padding
    ciphertext = encryptor.update(padded_msg) + encryptor.finalize()

    # 4
    encrypted_session_key = recipient_public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm= hashes.SHA256(),
            label=None
        )
    )

    # 5
    signature = sender_private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ), 
        hashes.SHA256()
    )

    # 6 
    h = hmac.HMAC(SHARED_SECRET, hashes.SHA256())
    h.update(ciphertext) #HMAC of encrypted data
    hmac_tag = h.finalize()

    return{
        'encrypted_session_key': encrypted_session_key,
        'iv': iv,
        'ciphertext': ciphertext,
        'signature': signature,
        'hmac': hmac_tag
    }

def decrypt_message(package, recipient_private_key, sender_public_key):
    '''
    hybrid decryption:
    1. verify HMAC - fast integrity check (if ever it was tampered)
    2. decrypt AES session key using the RSA provate key
    3. decrypt message with AES session key
    4. remove padding
    5. verify timestamp
    6. verification of digital signature (who sent the message)
    '''

    encrypted_session_key = package['encrypted_session_key']
    iv = package['iv']
    ciphertext = package['ciphertext']
    signature = package['signature']
    received_hmac = package['hmac']

    # 1
    h = hmac.HMAC(SHARED_SECRET, hashes.SHA256())
    h.update(ciphertext)
    try:
        h.verify(received_hmac)
        hmac_status = "HMAC VERIFIED"
    except:
        return None, "HMAC VERIFICATION FAILED, DATA TAMPERED!"
    
    # 2
    session_key = recipient_private_key.decrypt(
        encrypted_session_key,
        padding.OAEP(
            mgf = padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext ) + decryptor.finalize()

    # 4
    unpadder = sym_padding.PKCS7(128).unpadder()
    timestamped_message = unpadder.update(padded_message) + unpadder.finalize()
    timestamped_message = timestamped_message.decode()

    # 5
    try:
        timestamp_str, message = timestamped_message.split('|', 1)
        message_time = int(timestamp_str)
        current_time = int(time.time())
        age_seconds = current_time - message_time

        if age_seconds > 60: # if the message is older than 60 seconds
            return None, f"Message too old ({age_seconds}s old) - possibly a replay attack"
        
        timestamp_status = f"Message verified({age_seconds}s old)"
    except:
        return None, "Invalid timestamp format"
    
    # 6
    try: 
        sender_public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        signature_status = "Signature verified!"
    except:
        signature_status = "Signature verification failed."

    # conbination of all security results
    security_status = f"{hmac_status} | {timestamp_status} | {signature_status}"

    return message, security_status

def receiveMsg(conn):
    global run
    while run:
        try:
            data = conn.recv(16384) #increase to 8192 for encrypted data
            if not data:
                run = False
                break

            # desrializzr the package
            package = pickle.loads(data)
            
            decrypted_message, security_status = decrypt_message(
                package,
                server_private_key,
                client_public_key
            )

            if decrypted_message:
                print(f"\r{' '* 80}\rMessage: {decrypted_message}")
                print(f"Security: {security_status}")
            else:
                print(f"\r{' '* 80}\r{security_status}")
            
            print("Type Message: ", end='', flush=True)

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
                s.close()
                break

            package = encrypt_message(msg, client_public_key, server_private_key)

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
    print("Sending my public key to client...")
    conn.sendall(server_public_key_bytes)

    # receive client's public key
    client_public_key_bytes = conn.recv(4096)
    client_public_key = serialization.load_pem_public_key(
        client_public_key_bytes,
        backend=default_backend()
    )
    print("Public keys exchanged successfuly!\n\n")

    #start comm threads
    rcv = Thread(target=receiveMsg, args=(conn, ))
    rcv.start()
    sendMessage(conn)

    # wait for rcv thread to finish
    rcv.join()

    # close both connection and server socket
    conn.close()
    s.close()
