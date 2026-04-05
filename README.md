# 🔎 Python Multithreaded Port Scanner & Banner Grabber

## 📌 Overview
This project is a multithreaded Python-based port scanner designed to identify open ports and perform banner grabbing on detected services. It enhances traditional scanning by actively probing services to extract identifying information, even from "quiet" services that do not respond by default.

This tool demonstrates practical applications of networking, socket programming, and basic security reconnaissance techniques commonly used in cybersecurity and SOC environments.

---

## 🚀 Features

- Multithreaded scanning for improved performance  
- Scans custom port ranges  
- Banner grabbing for service identification  
- Intelligent probing for "quiet" services (HTTP, FTP, SMTP, Redis, etc.)  
- Graceful handling of non-text/binary responses  
- Configurable worker threads  
- Command-line interface (CLI) support  

---

## 🧠 How It Works

1. The scanner attempts a TCP connection to each port in the specified range.
2. If a connection is successful, the port is marked as **OPEN**.
3. A probe payload is sent to trigger a response from the service.
4. The response (banner) is captured and displayed.
5. Multithreading allows multiple ports to be scanned simultaneously for speed.

---

## 🛠️ Technologies Used

- Python 3  
- `socket` (network communication)  
- `argparse` (CLI argument parsing)  
- `concurrent.futures.ThreadPoolExecutor` (multithreading)  

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/python-port-scanner.git
cd python-port-scanner
