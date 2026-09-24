FROM ubuntu:22.04

# 1. Install 32-bit execution environment & socat
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
        libc6:i386 \
        socat && \
    rm -rf /var/lib/apt/lists/*

# 2. Set up challenge workspace
WORKDIR /challenge

# 3. Copy pre-compiled binary (and flag if applicable)
COPY ret2sentctf .

# 4. Create unprivileged CTF user & set execution permissions
RUN useradd -m ctf && \
    chmod +x /challenge/ret2sentctf && \
    chown -R root:ctf /challenge

USER ctf

# 5. Serve the binary on port 1337
EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./ret2sentctf"]