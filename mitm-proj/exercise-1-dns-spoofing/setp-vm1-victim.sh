#!/bin/bash
# Setup script for VM1 (Victim)

echo "=========================================="
echo "Setting up VM1 (Victim)"
echo "=========================================="

# Network configuration
echo "[*] Configuring network..."
sudo ip addr flush dev eth0
sudo ip addr add 192.168.1.10/24 dev eth0
sudo ip link set eth0 up
sudo ip route add default via 192.168.1.254

# Set DNS to use the gateway (which attacker will intercept)
echo "[*] Configuring DNS..."
sudo bash -c 'echo "nameserver 192.168.1.254" > /etc/resolv.conf'

# Disable systemd-resolved if running (can interfere)
sudo systemctl stop systemd-resolved 2>/dev/null
sudo systemctl disable systemd-resolved 2>/dev/null

# Install Firefox if not present
if ! command -v firefox &> /dev/null; then
    echo "[*] Installing Firefox..."
    sudo apt update
    sudo apt install -y firefox-esr
fi

echo ""
echo "[+] VM1 setup complete!"
echo ""
echo "Network Configuration:"
ip addr show eth0 | grep "inet "
echo ""
echo "DNS Configuration:"
cat /etc/resolv.conf
echo ""
echo "=========================================="
echo "Next steps:"
echo "1. Open Firefox"
echo "2. Type 'about:config' in address bar"
echo "3. Search for 'network.stricttransportsecurity.preloadlist'"
echo "4. Set it to 'false' (to allow HTTP for protonmail)"
echo "5. Try accessing http://protonmail.com"
echo "=========================================="
