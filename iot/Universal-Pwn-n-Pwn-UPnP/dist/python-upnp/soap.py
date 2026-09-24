#!/usr/bin/env python3
import argparse
import socket
import ssl

SERVICE_TYPE = "urn:schemas-upnp-org:service:DeviceConfig:1"
SOAP_ENDPOINT = "/upnp/control/deviceconfig"


def build_envelope(action, arguments):
    body = "".join(f"<{key}>{value}</{key}>" for key,
                   value in arguments.items())

    return f"""<?xml version="1.0"?>
<s:Envelope
    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
    s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">

    <s:Body>
        <u:{action} xmlns:u="{SERVICE_TYPE}">
            {body}
        </u:{action}>
    </s:Body>

</s:Envelope>
"""


def is_local_target(host):
    """Detects if target is local loopback or private IP."""
    return host in ("127.0.0.1", "localhost", "0.0.0.0") or host.startswith("192.168.") or host.startswith("10.")


def send_request(host, port, action, arguments):
    local = is_local_target(host)

    # 1. Determine Port and SSL setting
    if local:
        use_ssl = False
        target_port = port if port is not None else 5000
    else:
        use_ssl = True if (port is None or port == 443) else False
        target_port = port if port is not None else 443

    xml_payload = build_envelope(action, arguments).strip()

    # 2. Construct raw HTTP POST request
    http_request = (
        f"POST {SOAP_ENDPOINT} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f'Content-Type: text/xml; charset="utf-8"\r\n'
        f'SOAPAction: "{SERVICE_TYPE}#{action}"\r\n'
        f"Content-Length: {len(xml_payload.encode('utf-8'))}\r\n"
        f"Connection: close\r\n"
        "\r\n"
        f"{xml_payload}"
    )

    print(f"[+] Connecting to {host}:{target_port} (SSL: {use_ssl})...")
    print("\n===== Request Payload =====")
    print(http_request)

    # 3. Create raw socket
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.settimeout(10)

    if use_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        # Wrap socket with SSL and set SNI
        sock = ctx.wrap_socket(raw_sock, server_hostname=host)
    else:
        sock = raw_sock

    try:
        sock.connect((host, target_port))
        sock.sendall(http_request.encode("utf-8"))

        # 4. Receive response
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

        print("\n===== Response =====")
        if response:
            print(response.decode("utf-8", errors="ignore"))
        else:
            print("[!] Connection closed by server with no data returned.")

    except socket.timeout:
        print("\n[!] Request timed out.")
    except Exception as e:
        print(f"\n[!] Socket connection error: {e}")
    finally:
        sock.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send UPnP SOAP request over raw socket to local or remote target."
    )

    parser.add_argument(
        "host",
        nargs="?",
        default="127.0.0.1",
        help="Target hostname or IP (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Target port (Defaults: 5000 for localhost, 443 for remote CTFd domains)"
    )

    parser.add_argument(
        "--action",
        required=True,
        help="SOAP Action to execute"
    )

    parser.add_argument(
        "--arg",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="Arguments in key=value format"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    arguments = {}
    for item in args.arg:
        if "=" in item:
            key, value = item.split("=", 1)
            arguments[key] = value

    send_request(
        args.host,
        args.port,
        args.action,
        arguments
    )


if __name__ == "__main__":
    main()
