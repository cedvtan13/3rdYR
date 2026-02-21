#!/bin/bash
# Stop DNS Spoofing Attack (Run on VM2 - Attacker)

echo "=========================================="
echo "STOPPING DNS SPOOFING ATTACK"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "[!] Please run as root (use sudo)"
    exit 1
fi

# Stop ARP spoofing
echo "[*] Stopping ARP spoofing..."
if [ -f /tmp/arpspoof1.pid ]; then
    kill $(cat /tmp/arpspoof1.pid) 2>/dev/null
    rm /tmp/arpspoof1.pid
fi
if [ -f /tmp/arpspoof2.pid ]; then
    kill $(cat /tmp/arpspoof2.pid) 2>/dev/null
    rm /tmp/arpspoof2.pid
fi
killall arpspoof 2>/dev/null
echo "    ✓ ARP spoofing stopped"

# Stop packet capture
echo "[*] Stopping packet capture..."
if [ -f /tmp/tcpdump.pid ]; then
    kill $(cat /tmp/tcpdump.pid) 2>/dev/null
    rm /tmp/tcpdump.pid
fi
killall tcpdump 2>/dev/null
echo "    ✓ Packet capture stopped"

# Stop dnsmasq
echo "[*] Stopping dnsmasq..."
killall dnsmasq 2>/dev/null
echo "    ✓ dnsmasq stopped"

# Flush iptables NAT rules
echo "[*] Flushing iptables rules..."
iptables -t nat -F
echo "    ✓ iptables rules cleared"

# Disable IP forwarding
echo "[*] Disabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=0 > /dev/null
echo "    ✓ IP forwarding disabled"

# Show capture file location
if [ -f /tmp/pcap_file.txt ]; then
    PCAP_FILE=$(cat /tmp/pcap_file.txt)
    echo ""
    echo "=========================================="
    echo "Packet capture saved to:"
    echo "  $PCAP_FILE"
    echo ""
    echo "Analyze with:"
    echo "  wireshark $PCAP_FILE"
    echo "  or"
    echo "  tcpdump -r $PCAP_FILE -A"
    echo "=========================================="
    rm /tmp/pcap_file.txt
fi

echo ""
echo "[+] Attack stopped successfully"
