#!/usr/bin/env python3
"""Build the player-facing NANYANG-EYE-03 exercise capture.

This generator intentionally produces routine LAN, camera-streaming and NVR
traffic around the one relevant legacy PTZ request.  It keeps the control
request in a single TCP segment so Wireshark can dissect it as HTTP.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from scapy.all import ARP, DNS, DNSQR, DNSRR, Ether, IP, PcapNgWriter, Raw, TCP, UDP


BASE_TIME = 1_768_951_980.0  # 2026-01-15 02:13:00 UTC
MACS = {
    "10.33.7.1": "02:33:07:00:00:01",       # router
    "10.33.7.7": "02:33:07:00:00:07",       # NVR
    "10.33.7.23": "02:33:07:00:00:23",      # maintenance workstation
    "10.33.7.30": "02:33:07:00:00:30",      # retired camera VLAN gateway
    "10.33.7.42": "02:33:07:00:00:42",      # isolated maintenance gateway
    "10.33.7.53": "02:33:07:00:00:53",      # DNS resolver
}


class Capture:
    def __init__(self) -> None:
        self.packets = []
        self.offset = 0.0

    def emit(self, packet, delay: float = 0.03) -> None:
        packet.time = BASE_TIME + self.offset
        self.packets.append(packet)
        self.offset += delay

    def eth_ip(self, source: str, destination: str, payload):
        return Ether(src=MACS[source], dst=MACS[destination]) / IP(
            src=source, dst=destination
        ) / payload

    def tcp_dialogue(
        self,
        client: str,
        server: str,
        sport: int,
        dport: int,
        request: bytes,
        response: bytes,
        seed: int,
    ) -> None:
        """Add a compact but complete TCP request/response exchange."""
        client_seq = seed
        server_seq = seed + 100_000
        self.emit(self.eth_ip(client, server, TCP(sport=sport, dport=dport, flags="S", seq=client_seq)))
        self.emit(self.eth_ip(server, client, TCP(sport=dport, dport=sport, flags="SA", seq=server_seq, ack=client_seq + 1)))
        client_seq += 1
        server_seq += 1
        self.emit(self.eth_ip(client, server, TCP(sport=sport, dport=dport, flags="A", seq=client_seq, ack=server_seq)))
        self.emit(self.eth_ip(client, server, TCP(sport=sport, dport=dport, flags="PA", seq=client_seq, ack=server_seq) / Raw(request)))
        client_seq += len(request)
        self.emit(self.eth_ip(server, client, TCP(sport=dport, dport=sport, flags="A", seq=server_seq, ack=client_seq)))
        self.emit(self.eth_ip(server, client, TCP(sport=dport, dport=sport, flags="PA", seq=server_seq, ack=client_seq) / Raw(response)))
        server_seq += len(response)
        self.emit(self.eth_ip(client, server, TCP(sport=sport, dport=dport, flags="A", seq=client_seq, ack=server_seq)))


def http_request(method: str, path: str, host: str, body: str = "", extra: tuple[str, ...] = ()) -> bytes:
    headers = [f"{method} {path} HTTP/1.1", f"Host: {host}", "User-Agent: NANYANG-NVR/3.8"]
    headers.extend(extra)
    if body:
        headers.extend(("Content-Type: application/x-www-form-urlencoded", f"Content-Length: {len(body.encode())}"))
    return ("\r\n".join(headers) + "\r\n\r\n" + body).encode()


def http_response(body: str = "ok\n") -> bytes:
    return (
        "HTTP/1.1 200 OK\r\n"
        "Server: lighttpd/1.4.32\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body.encode())}\r\n\r\n{body}"
    ).encode()


def rtsp_request(method: str, uri: str, cseq: int, extra: str = "") -> bytes:
    suffix = f"\r\n{extra}" if extra else ""
    return f"{method} {uri} RTSP/1.0\r\nCSeq: {cseq}\r\nUser-Agent: NVR-Agent/3.8{suffix}\r\n\r\n".encode()


def rtsp_response(cseq: int, extra: str = "") -> bytes:
    suffix = f"\r\n{extra}" if extra else ""
    return f"RTSP/1.0 200 OK\r\nCSeq: {cseq}\r\nServer: D-Link DCS-5030L{suffix}\r\n\r\n".encode()


def build_capture() -> Capture:
    capture = Capture()

    # Ordinary VLAN discovery traffic.
    for source, destination in (("10.33.7.7", "10.33.7.30"), ("10.33.7.23", "10.33.7.42"), ("10.33.7.30", "10.33.7.1")):
        capture.emit(Ether(src=MACS[source], dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, hwsrc=MACS[source], psrc=source, hwdst="00:00:00:00:00:00", pdst=destination))
        capture.emit(Ether(src=MACS[destination], dst=MACS[source]) / ARP(op=2, hwsrc=MACS[destination], psrc=destination, hwdst=MACS[source], pdst=source))

    for number, name in enumerate(("pool.ntp.org.", "ntp.ntu.edu.sg.", "nvr-update.local."), start=1):
        sport = 53000 + number
        capture.emit(capture.eth_ip("10.33.7.7", "10.33.7.53", UDP(sport=sport, dport=53) / DNS(id=number, rd=1, qd=DNSQR(qname=name))))
        capture.emit(capture.eth_ip("10.33.7.53", "10.33.7.7", UDP(sport=53, dport=sport) / DNS(id=number, qr=1, aa=1, qd=DNSQR(qname=name), an=DNSRR(rrname=name, rdata="10.33.7.1"))))

    # HTTP operational noise: several POSTs, none of which is the camera PTZ control.
    noise = [
        ("GET", "/status.xml", "10.33.7.30", ""),
        ("POST", "/nvr/heartbeat", "10.33.7.7", "uptime=18422&channels=6"),
        ("GET", "/video.cgi?profile=low", "10.33.7.30", ""),
        ("POST", "/event/ack", "10.33.7.7", "event=motion&camera=03"),
        ("GET", "/cgi-bin/admin/getparam.cgi", "10.33.7.30", ""),
        ("POST", "/telemetry/upload", "10.33.7.7", "cpu=18&disk=72"),
        ("GET", "/snapshot.cgi", "10.33.7.30", ""),
        ("POST", "/maintenance/audit", "10.33.7.42", "action=keepalive"),
    ]
    for index, (method, path, host, body) in enumerate(noise):
        client = "10.33.7.7" if host in {"10.33.7.30", "10.33.7.7"} else "10.33.7.23"
        server = host
        capture.tcp_dialogue(client, server, 41000 + index, 80, http_request(method, path, host, body), http_response(), 10_000 + index * 1_000)

    # RTSP session traffic is deliberately much more numerous than the control exchange.
    uri = "rtsp://10.33.7.30:554/live1.sdp"
    rtsp = [
        ("OPTIONS", uri, 1, ""),
        ("DESCRIBE", uri, 2, "Accept: application/sdp"),
        ("SETUP", uri + "/trackID=1", 3, "Transport: RTP/AVP;unicast;client_port=5004-5005"),
        ("PLAY", uri, 4, "Session: 41414141"),
    ]
    for index, (method, request_uri, cseq, extra) in enumerate(rtsp):
        capture.tcp_dialogue("10.33.7.7", "10.33.7.30", 42000 + index, 554, rtsp_request(method, request_uri, cseq, extra), rtsp_response(cseq), 30_000 + index * 1_000)

    # Simulated RTP payloads account for the bulk of a camera capture.
    for sequence in range(420):
        rtp_header = bytes((0x80, 0x60, (sequence >> 8) & 0xFF, sequence & 0xFF, 0, 0, 0, sequence & 0xFF, 0x12, 0x34, 0x56, 0x78))
        payload = rtp_header + (b"\x65" if sequence % 60 == 0 else b"\x41") + bytes((sequence % 251,)) * 96
        capture.emit(capture.eth_ip("10.33.7.30", "10.33.7.7", UDP(sport=5004, dport=5004) / Raw(payload)), delay=0.01)

    # The one relevant legacy maintenance request.  It is surrounded by normal traffic,
    # but remains recoverable with an HTTP POST filter and stream inspection.
    control_body = "PanSingleMoveDegree=10&TiltSingleMoveDegree=0&PanTiltSingleMove=5"
    control = http_request(
        "POST",
        "/setControlPanTilt",
        "10.33.7.42",
        control_body,
        extra=("Authorization: Basic b3BzLXN2Yzp0dW5lX3RoZV9sZW5z", "Connection: keep-alive"),
    )
    capture.tcp_dialogue("10.33.7.23", "10.33.7.42", 43881, 80, control, http_response("PTZ accepted\n"), 70_000)

    # A final set of non-control health traffic prevents the target request being last.
    for index in range(12):
        payload = bytes((0x1B,)) + b"\x00" * 47
        capture.emit(capture.eth_ip("10.33.7.7", "10.33.7.1", UDP(sport=54000 + index, dport=123) / Raw(payload)))
        capture.emit(capture.eth_ip("10.33.7.1", "10.33.7.7", UDP(sport=123, dport=54000 + index) / Raw(payload)))
    return capture


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="destination .pcapng path")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    capture = build_capture()
    writer = PcapNgWriter(str(args.output))
    for packet in capture.packets:
        writer.write(packet)
    writer.close()
    print(f"wrote {len(capture.packets)} packets to {args.output}")


if __name__ == "__main__":
    main()
