FROM ubuntu:22.04

# Prevent interactive timezone/apt prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Set UTF-8 encoding so Python in GDB renders GEF properly
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# 1. Enable 32-bit support and install core debugging tools
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
        gdb \
        curl \
        python3 \
        python3-pip \
        libc6:i386 \
        libstdc++6:i386 \
        file \
        netcat \
        && rm -rf /var/lib/apt/lists/*

# 2. Install pwntools
RUN pip3 install --no-cache-dir pwntools

# 3. Download GEF from GitHub Raw
RUN curl -fsSL https://raw.githubusercontent.com/hugsy/gef/main/gef.py -o /root/.gdbinit-gef.py && \
    echo "source /root/.gdbinit-gef.py" > /root/.gdbinit

# 4. Set working directory
WORKDIR /workspace

# 5. Copy target challenge binary
COPY ret2sentctf .
RUN chmod +x ret2sentctf

# Default entrypoint
CMD ["/bin/bash"]