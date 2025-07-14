#!/bin/bash

set -e

# Install Script Botb

BOTB_VERSION="1.8.0"
INSTALL_DIR="/usr/local/bin"
DOWNLOAD_DIR="/tmp"
BOTB_PLATFORM="linux-amd64"
BOTB_URL="https://github.com/brompwnie/botb/releases/download/${BOTB_VERSION}/botb-${BOTB_PLATFORM}"
REPORT_DIR="../../reports/botb/"

# Check if Botb is already installed
if [ -x "$(command -v botb)" ]; then
    echo "Botb is already installed."
    exit 0
fi

# Check if the installation directory exists, otherwise create it
echo "Checking installation directory..."
if [[ ! -d "${INSTALL_DIR}" ]]; then
  echo "Creating installation directory ${INSTALL_DIR}..."
  sudo mkdir -p "${INSTALL_DIR}"
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
fi

# Download and extract botb
echo "Downloading stratus ${BOTB_VERSION}..."
sudo curl -L "$BOTB_URL" -o "$DOWNLOAD_DIR/botb"

# Installing stratus
echo "Installing Botb ${BOTB_VERSION}..."
sudo mv "$DOWNLOAD_DIR/botb" "$INSTALL_DIR"
sudo chmod +x "$INSTALL_DIR/botb"

# Cleaning up
echo "Cleaning up..."

echo "Botb ${BOTB_VERSION} has been successfully installed."