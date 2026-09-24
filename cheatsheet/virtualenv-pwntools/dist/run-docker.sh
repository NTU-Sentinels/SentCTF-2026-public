#!/usr/bin/env bash
set -e

# Determine the actual non-root user and home directory even if executed via sudo
TARGET_USER="${SUDO_USER:-$USER}"
USER_HOME=$(eval echo "~$TARGET_USER")
WORKING_DIR="$USER_HOME/sentctf-2026"

mkdir -p "$WORKING_DIR"

# Move Dockerfile only if it exists in current directory and we aren't already in WORKING_DIR
if [ "$(pwd)" != "$WORKING_DIR" ] && [ -f "Dockerfile" ]; then
    echo "[+] Moving Dockerfile to $WORKING_DIR..."
    cp Dockerfile "$WORKING_DIR/"
fi

# Switch into the workspace directory
cd "$WORKING_DIR"

# Ensure Dockerfile is actually available
if [ ! -f "Dockerfile" ]; then
    echo "[!] Error: No Dockerfile found in $(pwd)."
    echo "[!] Please place your Dockerfile in this directory and re-run."
    exit 1
fi

# Ensure docker group exists on system before attempting usermod
if ! getent group docker &>/dev/null; then
    echo "[+] Creating 'docker' group..."
    sudo groupadd docker
fi

# Ensure target user is in the docker group to run docker without sudo
if ! getent group docker | grep -q "\b${TARGET_USER}\b"; then
    echo "[+] Adding user '$TARGET_USER' to the docker group..."
    sudo usermod -aG docker "$TARGET_USER"
    echo "[!] Group updated."
fi

echo "[+] Building Docker image 'pwntools-env'..."
sg docker -c "docker build -t pwntools-env ."

echo "[+] Launching container with current directory mounted..."
sg docker -c "docker run --rm -it -v \"$(pwd):/app\" pwntools-env"