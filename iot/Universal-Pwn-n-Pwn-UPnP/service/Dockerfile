FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y \
        qemu-user-static && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY upnpd-prod /usr/sbin/upnpd
COPY device.xml /etc/upnp/device.xml
COPY deviceconfig.xml /etc/upnp/deviceconfig.xml

RUN chmod +x /usr/sbin/upnpd

EXPOSE 5000/tcp
EXPOSE 1900/tcp

CMD ["qemu-mipsel-static", "/usr/sbin/upnpd"]

