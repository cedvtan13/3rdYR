# 🔐 Secure Client-Server Chat Application

**CPE 3151 - Information Engineering / Cryptography Project**

**Members:** Kent Vincent S. Godinez, Cedric Vince M. Tan

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Security Features](#security-features)
- [Encryption Flow](#encryption-flow)
- [Decryption Flow](#decryption-flow)
- [Key Exchange Protocol](#key-exchange-protocol)
- [Multithreading Architecture](#multithreading-architecture)
- [Message Package Structure](#message-package-structure)
- [Course Coverage](#course-coverage)
- [Installation & Usage](#installation--usage)
- [Technical Documentation](#technical-documentation)
- [Interview Q&A](#interview-qa)

---

## 🎯 Project Overview

A secure real-time chat application implementing hybrid encryption (AES + RSA) with digital signatures, HMAC integrity checks, and timestamp-based replay attack prevention. Built using TCP sockets with full-duplex communication via multithreading.

### Development Timeline

- **12/8/2025**: Created bidirectional TCP socket connection with RSA encryption
- **12/12/2025**: Integrated cryptography library for better security practices
- **12/13/2025**: Implemented hybrid encryption (AES + RSA), timestamps, HMAC, and helper functions

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SECURE CHAT SYSTEM                          │
│                   (CPE 3151 Cryptography)                       │
└─────────────────────────────────────────────────────────────────┘

     CLIENT                                    SERVER
┌──────────────┐                         ┌──────────────┐
│              │    TCP Connection       │              │
│  client.py   │◄──────────────────────►│  server.py   │
│              │   127.0.0.1:8000        │              │
└──────────────┘                         └──────────────┘
       │                                        │
       ├─ Send Thread (input)                  ├─ Send Thread (input)
       └─ Receive Thread (listen)              └─ Receive Thread (listen)
                                                
         FULL-DUPLEX COMMUNICATION
    (Both can send/receive simultaneously)
```

---

## 🔐 Security Features

### Five Layers of Security

```
┌─────────────────────────────────────────────────────────────────┐
│                  5 SECURITY LAYERS APPLIED                      │
└─────────────────────────────────────────────────────────────────┘

Layer 1: CONFIDENTIALITY (Who can read?)
         ┌─────────────────────────────────┐
         │   AES-256 Encryption (CBC)      │  ← Fast symmetric encryption
         │   Random session key per msg    │
         └─────────────────────────────────┘

Layer 2: SECURE KEY EXCHANGE (How to share AES key?)
         ┌─────────────────────────────────┐
         │   RSA-2048 Encryption (OAEP)    │  ← Encrypt AES key
         │   Asymmetric cryptography       │
         └─────────────────────────────────┘

Layer 3: AUTHENTICATION (Who sent this?)
         ┌─────────────────────────────────┐
         │   RSA Digital Signature (PSS)   │  ← Prove sender identity
         │   SHA-256 hashing               │
         └─────────────────────────────────┘

Layer 4: INTEGRITY (Was it modified?)
         ┌─────────────────────────────────┐
         │   HMAC-SHA256                   │  ← Fast tamper detection
         │   Shared secret key             │
         └─────────────────────────────────┘

Layer 5: FRESHNESS (Is it a replay attack?)
         ┌─────────────────────────────────┐
         │   Timestamp Validation          │  ← 60 second window
         │   Unix epoch time               │
         └─────────────────────────────────┘
```

### Security Goals Achieved

✅ **Confidentiality** - Only intended recipient can decrypt messages  
✅ **Integrity** - Tampering is detected via HMAC  
✅ **Authentication** - Sender identity verified through digital signatures  
✅ **Non-repudiation** - Sender cannot deny sending (private key signature)  
✅ **Freshness** - Old messages rejected (60-second validity window)

---

## 🔄 Encryption Flow

### Step-by-Step Message Encryption

```
USER TYPES: "Hello Professor!"
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    ENCRYPTION PROCESS                            │
└──────────────────────────────────────────────────────────────────┘

STEP 1: Add Timestamp
   "Hello Professor!" → "1702468934|Hello Professor!"
                        └─timestamp─┘

STEP 2: Generate Random Keys
   AES Session Key: [32 random bytes] ← Used once, then discarded
   IV (Init Vector): [16 random bytes] ← Randomizes encryption

STEP 3: AES Encryption (Fast!)
   "1702468934|Hello Professor!"
        │ (pad to 16-byte blocks)
        ▼
   [ENCRYPTED BYTES: af3e9b2c...]  ← Ciphertext
        │
        └─ CANNOT be read without AES key!

STEP 4: RSA Encrypt the AES Key (Secure key exchange)
   AES Key [32 bytes]
        │ (encrypt with recipient's PUBLIC key)
        ▼
   [ENCRYPTED KEY: 8f2a4b...]  ← Only recipient can decrypt

STEP 5: Create Digital Signature (Authentication)
   "Hello Professor!" (original message)
        │ (sign with sender's PRIVATE key)
        ▼
   [SIGNATURE: e4d7f1...]  ← Proves WHO sent it

STEP 6: Create HMAC (Integrity check)
   Ciphertext [af3e9b2c...]
        │ (hash with shared secret)
        ▼
   [HMAC TAG: b9c3a8...]  ← Detects tampering

STEP 7: Package Everything
   ┌────────────────────────────────────┐
   │ encrypted_session_key: [256 bytes] │
   │ iv: [16 bytes]                     │
   │ ciphertext: [variable length]      │
   │ signature: [256 bytes]             │
   │ hmac: [32 bytes]                   │
   └────────────────────────────────────┘
        │ (serialize with pickle)
        ▼
   SEND OVER NETWORK →
```

---

## 🔓 Decryption Flow

### Security Checks in Optimal Order

```
← RECEIVE ENCRYPTED PACKAGE
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│                    DECRYPTION PROCESS                            │
│              (Security checks in optimal order)                  │
└──────────────────────────────────────────────────────────────────┘

CHECK 1: Verify HMAC (FASTEST - check first!)
   [HMAC TAG from package] vs [Recalculate HMAC]
        │
        ├─ Match? ✓ Continue
        └─ Mismatch? ✗ REJECT (Data tampered!)

CHECK 2: Decrypt AES Session Key
   [Encrypted AES Key]
        │ (decrypt with recipient's PRIVATE key)
        ▼
   [32-byte AES Key]  ← Now we can decrypt message

CHECK 3: Decrypt Message with AES
   [Ciphertext: af3e9b2c...]
        │ (decrypt with AES key + IV)
        ▼
   "1702468934|Hello Professor!"  ← Decrypted!

CHECK 4: Verify Timestamp (Prevent replay attacks)
   Message time: 1702468934
   Current time: 1702468936
   Age: 2 seconds
        │
        ├─ < 60 seconds? ✓ Fresh message
        └─ > 60 seconds? ✗ REJECT (Too old!)

CHECK 5: Verify Digital Signature
   [Signature] + [Message] + [Sender's PUBLIC key]
        │
        ├─ Valid? ✓ Sender authenticated
        └─ Invalid? ✗ WARNING (Sender unknown!)

RESULT:
   Message: "Hello Professor!"
   Security: ✓ HMAC OK | ✓ Fresh (2s) | ✓ Signature OK
```

---

## 🔑 Key Exchange Protocol

### Initial Handshake Process

```
┌─────────────────────────────────────────────────────────────────┐
│              INITIAL KEY EXCHANGE HANDSHAKE                     │
│         (Happens once at connection start)                      │
└─────────────────────────────────────────────────────────────────┘

CLIENT                                           SERVER
  │                                                 │
  │ 1. Generate RSA-2048 key pair                  │
  │    - client_private_key (KEEP SECRET!)         │
  │    - client_public_key (share with server)     │
  │                                                 │
  │                 TCP CONNECT                     │
  │◄───────────────────────────────────────────────┤
  │                                                 │
  │                                                 │ 2. Generate RSA-2048 key pair
  │                                                 │    - server_private_key (SECRET!)
  │                                                 │    - server_public_key (share)
  │                                                 │
  │          3. SERVER SENDS PUBLIC KEY             │
  │◄────────────[server_public_key]────────────────┤
  │                                                 │
  │          4. CLIENT SENDS PUBLIC KEY             │
  ├────────────[client_public_key]────────────────►│
  │                                                 │
  │         ✓ KEY EXCHANGE COMPLETE!                │
  │                                                 │
  │   Now client has: server_public_key            │
  │   Now server has: client_public_key            │
  │                                                 │
  │        SECURE COMMUNICATION READY               │
  │◄──────────────────────────────────────────────►│
  │                                                 │
```

---

## 🧵 Multithreading Architecture

### Full-Duplex Communication Implementation

```
┌─────────────────────────────────────────────────────────────────┐
│           WHY MULTITHREADING? (Full-Duplex Chat)                │
└─────────────────────────────────────────────────────────────────┘

WITHOUT THREADS (Half-Duplex):
   User → Type message → Send → Wait → Receive → Type next
                    └─ BLOCKED! Can't receive while typing

WITH THREADS (Full-Duplex):
   
   MAIN THREAD              BACKGROUND THREAD
   ┌─────────┐              ┌──────────┐
   │ Send    │              │ Receive  │
   │ Thread  │              │ Thread   │
   └────┬────┘              └────┬─────┘
        │                        │
   ┌────▼──────────────┐    ┌───▼──────────────┐
   │ Read user input   │    │ Listen for msgs  │
   │ Encrypt message   │    │ Decrypt messages │
   │ Send to socket    │    │ Print to screen  │
   └───────────────────┘    └──────────────────┘
        │                        │
        └────────────┬───────────┘
                     ▼
            SIMULTANEOUS OPERATION!
   Type while receiving messages in real-time
```

---

## 📦 Message Package Structure

```
┌─────────────────────────────────────────────────────────────────┐
│             ENCRYPTED MESSAGE PACKAGE (pickled)                 │
└─────────────────────────────────────────────────────────────────┘

Python Dictionary:
{
    'encrypted_session_key': bytes,  # 256 bytes (RSA-2048 encrypted)
    'iv': bytes,                     # 16 bytes (AES initialization)
    'ciphertext': bytes,             # Variable (AES-256 encrypted msg)
    'signature': bytes,              # 256 bytes (RSA digital signature)
    'hmac': bytes                    # 32 bytes (SHA-256 HMAC tag)
}
         │
         │ pickle.dumps()
         ▼
    [BINARY DATA]
         │
         │ socket.sendall()
         ▼
   TRANSMITTED OVER TCP
         │
         │ socket.recv(16384)
         ▼
    [BINARY DATA]
         │
         │ pickle.loads()
         ▼
Python Dictionary (reconstructed)
```

---

## 📚 Course Coverage

### Complete Implementation of All 6 Units

```
✓ Unit 1: Cryptography Overview
  - Confidentiality, Integrity, Authentication, Non-repudiation

✓ Unit 2: Symmetric Cryptography
  - AES-256 in CBC mode
  - PKCS7 padding
  - Initialization vectors (IV)

✓ Unit 3: Asymmetric Cryptography  
  - RSA-2048 key generation
  - OAEP padding for encryption
  - Public/Private key pairs

✓ Unit 4: Hash Functions & Message Authentication
  - SHA-256 hashing
  - HMAC-SHA256 for integrity
  - Timestamp inclusion

✓ Unit 5: Digital Signatures
  - RSA-PSS signature scheme
  - Non-repudiation (sender can't deny)
  - Signature verification

✓ Unit 6: Authentication Applications
  - Public key exchange protocol
  - Full-duplex secure communication
  - Replay attack prevention (timestamps)
```

---

## 🚀 Installation & Usage

### Prerequisites

```bash
pip install cryptography
```

### Running the Application

**Terminal 1 (Server):**
```bash
python server.py
```

**Terminal 2 (Client):**
```bash
python client.py
```

### Sample Output

```
TERMINAL 1 (Server):                 TERMINAL 2 (Client):
===================                  ===================

$ python server.py                   $ python client.py
Generating RSA key pair...           Generating RSA key pair...
Listening on 127.0.0.1:8000...      Connecting to server...
                                     
Connection accepted!                 Connected!
Exchanging keys...                   Exchanging keys...
Keys exchanged ✓                     Keys exchanged ✓

Type Message: Hello Client!          
                                     Message: Hello Client!
                                     Security: ✓ HMAC VERIFIED | 
                                               ✓ Message verified(1s old) | 
                                               ✓ Signature verified!
                                     
                                     Type Message: Hi Server!
Message: Hi Server!
Security: ✓ HMAC VERIFIED | 
          ✓ Message verified(2s old) | 
          ✓ Signature verified!
```

---

## 🔧 Technical Documentation

### Cryptographic Algorithms Used

| Component | Algorithm | Key Size | Purpose |
|-----------|-----------|----------|---------|
| Symmetric Encryption | AES-256-CBC | 256-bit | Fast message encryption |
| Asymmetric Encryption | RSA-OAEP | 2048-bit | Secure key exchange |
| Digital Signature | RSA-PSS | 2048-bit | Authentication |
| Hash Function | SHA-256 | 256-bit | Integrity & signatures |
| MAC | HMAC-SHA256 | 256-bit | Fast integrity check |
| Padding (Symmetric) | PKCS7 | 128-bit blocks | AES block alignment |
| Padding (Asymmetric) | OAEP/PSS | - | Secure RSA operations |

### Helper Functions

**`encrypt_message(message, recipient_public_key, sender_private_key)`**
- Performs hybrid encryption with all 5 security layers
- Returns dictionary package ready for transmission

**`decrypt_message(package, recipient_private_key, sender_public_key)`**
- Performs all security checks in optimal order
- Returns decrypted message and security status

### Network Protocol

- **Transport**: TCP (SOCK_STREAM)
- **Host**: 127.0.0.1 (localhost)
- **Port**: 8000
- **Buffer Size**: 16384 bytes
- **Serialization**: Python pickle

---

## 💡 Interview Q&A

### Q: Why hybrid encryption (AES + RSA)?

**A:** "RSA is secure but slow and has size limits (~245 bytes for 2048-bit key). AES is fast but requires secure key exchange. Our solution uses AES to encrypt the message (fast, unlimited size) and RSA to encrypt the AES key (secure, small key). This is industry standard - used in TLS/HTTPS!"

### Q: Why do you need both HMAC and digital signatures?

**A:** "Different purposes with defense in depth:

**HMAC (Unit 4):**
- FAST integrity check
- Uses shared secret
- Detects tampering

**Digital Signature (Unit 5):**
- PROVES identity (authentication)
- Non-repudiation (sender can't deny)
- Uses private key

Both together provide layered security!"

### Q: How do timestamps prevent replay attacks?

**A:** "Without timestamp, an attacker could capture a 'Transfer $100' message and replay it multiple times. With timestamps, each message has a creation time, and our system rejects messages older than 60 seconds. This makes captured messages expire quickly and become useless to attackers."

### Q: Why use threads?

**A:** "For full-duplex communication (Unit 6 - Applications). Without threads, we can only send OR receive at a time (like a walkie-talkie). With threads, we can send AND receive simultaneously (like a phone call). The main thread handles user input and sending, while the background thread continuously listens for incoming messages."

### Q: What is the purpose of the Initialization Vector (IV)?

**A:** "The IV randomizes AES encryption. Without it, encrypting the same message twice produces identical ciphertext, revealing patterns to attackers. With a random IV, each encryption is unique, even for identical messages. This is critical for CBC mode security."

### Q: How does your code ensure confidentiality?

**A:** "Multiple layers:
1. AES-256 encryption ensures only someone with the session key can decrypt
2. Session key is encrypted with RSA using recipient's public key
3. Only the recipient's private key can decrypt the session key
4. Each message uses a fresh, random session key

Result: Only intended recipient can read the message!"

---

## 📊 Project Summary

### What We Built
- Real-time encrypted chat application using TCP sockets
- Full-duplex communication (multithreaded)
- Industry-standard cryptographic practices

### Cryptography Applied
- **AES-256** (symmetric encryption - confidentiality)
- **RSA-2048** (asymmetric - key exchange & signatures)
- **HMAC-SHA256** (integrity check)
- **Digital signatures** (authentication & non-repudiation)
- **Timestamps** (replay attack prevention)

### Security Goals Achieved
✅ Confidentiality - Only intended recipient can read  
✅ Integrity - Tampering is detected  
✅ Authentication - Sender identity verified  
✅ Non-repudiation - Sender can't deny sending  
✅ Freshness - Old messages rejected  

### References
- [Python Cryptography Documentation](https://cryptography.io/en/latest/)
- [RSA Encryption Documentation](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
- CPE 3151 Course Materials - Introduction to Cryptography

---

**© 2025 Kent Vincent S. Godinez & Cedric Vince M. Tan**

*This project demonstrates practical application of cryptographic principles learned in CPE 3151 Information Engineering course.*
