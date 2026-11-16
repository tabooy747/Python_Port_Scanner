import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def grab_banner(s, port):
    """Send a short probe and return any text banner the service sends back."""
    # A few services stay silent until they receive a protocol-specific payload.
    probes = {
        80: b"GET / HTTP/1.1\r\nHost: target\r\n\r\n",
        443: b"GET / HTTP/1.1\r\nHost: target\r\n\r\n",
        21: b"HELP\r\n",
        25: b"HELP\r\n",
        6379: b"PING\r\n"
    }

    try:
        # Known ports get a matching probe; every other port gets a newline.
        payload = probes.get(port, b"\r\n")
        s.sendall(payload)

        # Decode the reply as text and skip bytes that are not valid UTF-8.
        banner = s.recv(1024).decode(errors='ignore').strip()
        return banner if banner else "Connected (No text banner)"
    except Exception:
        return "No banner returned"

def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow time for the service to answer after the probe is sent.
        s.settimeout(2.5)
        if s.connect_ex((target, port)) == 0:
            banner = grab_banner(s, port)
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
