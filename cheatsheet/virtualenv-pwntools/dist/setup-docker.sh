#!/usr/bin/env bash
set -e


# Update packages and install Docker
echo "[+] Updating package lists..."
sudo apt-get update -y

echo "[+] Installing Docker and prerequisites..."
sudo apt-get install -y docker.io

echo "[+] Starting and enabling Docker service..."
sudo systemctl enable --now docker




