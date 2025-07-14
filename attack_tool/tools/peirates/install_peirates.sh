#!/bin/bash

set -e

PEIRATES_VERSION="v1.1.15"
INSTALL_DIR="/usr/local/bin"
DOWNLOAD_DIR="/tmp"
PEIRATES_PLATFORM="amd64"
PEIRATES_URL="https://github.com/inguardians/peirates/releases/download/${PEIRATES_VERSION}/peirates-linux-${PEIRATES_PLATFORM}.tar.xz"
REPORT_DIR="../../reports/peirates/"

# Check if peirates is already installed
if [ -x "$(command -v peirates)" ]; then
    echo "Peirates is already installed."
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

# Download and extract peirates
echo "Downloading Peirates ${PEIRATES_VERSION}..."
sudo curl -L "$PEIRATES_URL" -o "$DOWNLOAD_DIR/peirates.tar.xz"
sudo tar xvf "$DOWNLOAD_DIR/peirates.tar.xz" -C "$DOWNLOAD_DIR"

# Installing peirates
echo "Installing Peirates ${PEIRATES_VERSION}..."
sudo mv "$DOWNLOAD_DIR/peirates-linux-$PEIRATES_PLATFORM/peirates" "$INSTALL_DIR"
sudo chmod +x "$INSTALL_DIR/peirates"

echo "Cleaning up..."
sudo rm "$DOWNLOAD_DIR/peirates.tar.xz"
sudo rm -rf "$DOWNLOAD_DIR/peirates-linux-$PEIRATES_PLATFORM/"

echo "Peirates ${PEIRATES_VERSION} has been successfully installed."