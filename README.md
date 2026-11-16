# Python TCP Port Scanner

A multithreaded TCP connect scanner that checks a port range and prints a text banner from each open port.

## Features

- Scans an inclusive range of IPv4 TCP ports with a pool of threads.
- Default range is ports 1 through 1024. Set another range with `-p` / `--ports START END`.
- Default pool size is 100 threads. Set another size with `-w` / `--workers N`.
- Sends a short plaintext probe, then reads up to 1024 bytes:
  - ports 80 and 443: an HTTP/1.1 `GET /` request
  - port 21: `HELP` (the usual FTP probe)
  - port 25: `HELP` (the usual SMTP probe)
  - port 6379: `PING` (the usual Redis probe)
  - every other port: a carriage return and line feed
- Decodes the reply as text and skips bytes that are not valid UTF-8.
- Prints a line only when a port accepts a connection. Each open connection waits up to 2.5 seconds for a banner.
- The port 443 probe is plaintext HTTP. A TLS-only service often returns no useful banner.

## Requirements

Python 3. The script uses the standard library only: `socket`, `argparse`, and `concurrent.futures`.

## Install

```bash
git clone https://github.com/tabooy747/Python_Port_Scanner.git
cd Python_Port_Scanner
```

## Usage

```bash
python3 Port_Scanner.py --help
```

```
usage: Port_Scanner.py [-h] [-p PORTS PORTS] [-w WORKERS] target

Multithreaded Banner Grabber.

positional arguments:
  target                Target IP address

options:
  -h, --help            show this help message and exit
  -p PORTS PORTS, --ports PORTS PORTS
                        Port range (default: 1 1024)
  -w WORKERS, --workers WORKERS
```

`target` is an IPv4 address, or a hostname that resolves to one. `--ports` takes the first and last port, and both ends are included. `--workers` takes an integer. The flag has no help text; omitting it uses 100 threads.

Scan this machine on the default range:

```bash
python3 Port_Scanner.py 127.0.0.1
```

Scan a smaller range with fewer threads:

```bash
python3 Port_Scanner.py 127.0.0.1 --ports 20 25 --workers 20
```

The same options have short forms:

```bash
python3 Port_Scanner.py 127.0.0.1 -p 18079 18081 -w 10
```

Nmap publishes `scanme.nmap.org` so people can test a scanner. Use it only while that offer still stands:

```bash
python3 Port_Scanner.py scanme.nmap.org -p 20 80 -w 20
```

## Sample output

This run targeted `127.0.0.1`. Port 18080 returned the text `portfolio-demo`. Port 18081 accepted the connection and sent no text. Open ports can finish out of numeric order.

```
[!] Scanning 127.0.0.1 for banners...
------------------------------------------------------------
[OPEN]  Port 18080 | Banner: portfolio-demo
[OPEN]  Port 18081 | Banner: Connected (No text banner)
```

A range with nothing listening prints the header and no port lines. When a read fails or times out, the banner text is `No banner returned`.

## Responsible use

Scan only systems you own or have explicit permission to test. Unauthorized scanning can violate the law and the rules of the network you are on. You are responsible for how you use this script.
