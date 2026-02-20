import socket
from datetime import datetime

def start_monitor():
    """Monitor that receives and displays sniffed packets"""
    
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 9001
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    
    print("="*60)
    print(" " * 15 + "MITM MONITOR - ATTACKER VM")
    print("="*60)
    print(f"[*] Monitor listening on port {PORT}")
    print(f"[*] Waiting for sniffer connection...")
    print("="*60 + "\n")
    
    conn, addr = s.accept()
    print(f"[+] Sniffer connected from {addr[0]}:{addr[1]}")
    print(f"[*] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            
            # Display sniffed data
            print(data.decode('utf-8', errors='ignore'), flush=True)
            
    except KeyboardInterrupt:
        print("\n[*] Monitor stopped by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()
        s.close()
        print("\n[*] Monitor closed")

if __name__ == "__main__":
    start_monitor()
