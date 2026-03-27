import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def grab_banner(s):
    """Try to read the initial greeting from the service."""
    try:
        # Some services (like SSH) send a banner immediately.
        # Others (like HTTP) need a request first.
        return s.recv(1024).decode().strip()
    except:
        return "No banner returned"

def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.5) # Increased timeout to wait for banner response
        if s.connect_ex((target, port)) == 0:
            # Once connected, try to see what service it is
            banner = grab_banner(s)
            print(f"[OPEN]  Port {port:5} | Banner: {banner}")

def main():
    parser = argparse.ArgumentParser(description="Multithreaded Banner Grabber.")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("-p", "--ports", nargs=2, type=int, default=[1, 1024],
                        help="Port range (default: 1 1024)")
    parser.add_argument("-w", "--workers", type=int, default=100)

    args = parser.parse_args()
    start_port, end_port = args.ports

    print(f"\n[!] Scanning {args.target} for banners...\n" + "-"*60)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, args.target, port)

if __name__ == "__main__":
    main()
