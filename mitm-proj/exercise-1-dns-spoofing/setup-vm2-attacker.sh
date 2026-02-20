#!/bin/bash
# Setup script for VM2 (Attacker - MITM)

echo "=========================================="
echo "Setting up VM2 (Attacker/MITM)"
echo "=========================================="

# Network configuration
echo "[*] Configuring network..."
sudo ip addr flush dev eth0
sudo ip addr add 192.168.1.20/24 dev eth0
sudo ip link set eth0 up
sudo ip route add default via 192.168.1.254

# Enable IP forwarding (critical for MITM)
echo "[*] Enabling IP forwarding..."
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf

# Install required tools
echo "[*] Installing required packages..."
sudo apt update
sudo apt install -y dsniff dnsmasq iptables tcpdump

# Stop and disable systemd-resolved (conflicts with dnsmasq)
echo "[*] Stopping systemd-resolved..."
sudo systemctl stop systemd-resolved 2>/dev/null
sudo systemctl disable systemd-resolved 2>/dev/null

# Backup original dnsmasq config
if [ -f /etc/dnsmasq.conf ]; then
    sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup
fi

# Copy our custom dnsmasq configuration
echo "[*] Configuring dnsmasq..."
sudo cp dnsmasq.conf /etc/dnsmasq.conf
sudo cp dnsmasq.hosts /etc/dnsmasq.hosts

# Set permissions
sudo chmod 644 /etc/dnsmasq.conf /etc/dnsmasq.hosts

echo ""
echo "[+] VM2 setup complete!"
echo ""
echo "Network Configuration:"
ip addr show eth0 | grep "inet "
echo ""
echo "IP Forwarding:"
cat /proc/sys/net/ipv4/ip_forward
echo ""
echo "=========================================="
echo "Attack is ready to launch!"
echo "Run: ./start-attack.sh"
echo "=========================================="
