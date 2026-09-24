#!/usr/bin/env python3
import argparse
import socket
import ssl

DEFAULT_TARGET = "127.0.0.1"

parser = argparse.ArgumentParser(
    description="Send SSDP M-SEARCH payload over TCP to CTFd instance."
)
parser.add_argument(
    "target",
    nargs="?",
    default=DEFAULT_TARGET,
    help=f"Target hostname or IP (default: {DEFAULT_TARGET})"
)
parser.add_argument(
    "-p", "--port",
    type=int,
    default=None,
    help="Target port (Defaults to 443 for remote hosts, 1900 for local)"
)

args = parser.parse_args()
TARGET = args.target

# Auto-select port: 443 for hosted CTFd domain (internally routes to 1900), 1900 for IP/localhost
if args.port:
    PORT = args.port
elif TARGET in ("127.0.0.1", "localhost") or TARGET.startswith("192.168."):
    PORT = 1900
else:
    PORT = 443

# Construct SSDP payload compatible with reverse proxies
request = (
    "M-SEARCH * HTTP/1.1\r\n"
    f"Host: {TARGET}\r\n"
    'MAN: "ssdp:discover"\r\n'
    "MX: 2\r\n"
    "ST: ssdp:all\r\n"
    "Connection: close\r\n"
    "\r\n"
)


def send_msearch(target_port, use_ssl=False):
    protocol_label = "HTTPS/TLS" if use_ssl else "HTTP/TCP"
    print(f"[+] Trying {protocol_label} on {TARGET}:{target_port}...")

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.settimeout(6)

    if use_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        # SNI is MANDATORY for CTFd reverse proxies (chals.io)
        sock = ctx.wrap_socket(raw_sock, server_hostname=TARGET)
    else:
        sock = raw_sock

    try:
        sock.connect((TARGET, target_port))
        print(f"[+] Sending payload...")
        sock.sendall(request.encode("utf-8"))

        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

        if response:
            print(f"\n[+] Received Response from {TARGET}:\n")
            print(response.decode(errors="ignore"))
            return True
        else:
            print(f"[!] No data returned over {protocol_label}.")
            return False

    except Exception as e:
        print(f"[!] Failed over {protocol_label}: {e}")
        return False
    finally:
        sock.close()


if __name__ == "__main__":
    # For remote chals.io domains, HTTPS (443) with SNI is usually required
    is_remote = not (TARGET in ("127.0.0.1", "localhost")
                     or TARGET.startswith("192.168."))

    if is_remote and PORT == 443:
        # Try SSL/TLS on port 443 first for remote CTFd instances
        if not send_msearch(443, use_ssl=True):
            print("[*] Retrying over plain HTTP (port 80)...")
            send_msearch(80, use_ssl=False)
    else:
        # Local testing defaults to plain TCP on specified port
        if not send_msearch(PORT, use_ssl=False):
            print("[*] Retrying with SSL/TLS wrapper...")
            send_msearch(PORT, use_ssl=True)
