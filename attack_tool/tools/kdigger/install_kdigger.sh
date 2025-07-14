#!/bin/bash

set -e

KDIGGER_VERSION="v1.5.0"
KDIGGER_PLATFORM="amd64"
HISTORY="${1}history"
REPORTS="${1}reports/kdigger/"
INSTALL_DIR=$2
DOWNLOAD_DIR="/tmp"
DOWNLOAD_URL="https://github.com/quarkslab/kdigger/releases/download/${KDIGGER_VERSION}/kdigger-linux-${KDIGGER_PLATFORM}.tar.gz"

# History directory
if [ ! -e "${HISTORY}/.prompt_history_kdigger.txt" ]; then
    echo "Creating history file..."
    sudo touch "${HISTORY}/.prompt_history_kdigger.txt"
    sudo chown $(whoami) "${HISTORY}/.prompt_history_kdigger.txt"
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORTS}" ]]; then
  echo "Creating reports directory ${REPORTS}..."
  sudo mkdir -p "${REPORTS}"
  sudo chown $(whoami) "${REPORTS}"
fi

# Download and extract kdigger
echo "Downloading kdigger ${KDIGGER_VERSION}..."
sudo curl -fSL "$DOWNLOAD_URL" -o "${DOWNLOAD_DIR}/kdigger.tar.xz"
sudo tar xvf "$DOWNLOAD_DIR/kdigger.tar.xz" -C "$DOWNLOAD_DIR"

# Installing kdigger
echo "Installing kdigger ${KDIGGER_VERSION}..."
sudo mv "$DOWNLOAD_DIR/kdigger-linux-$KDIGGER_PLATFORM" "$INSTALL_DIR/kdigger"
sudo chmod +x "$INSTALL_DIR/kdigger"

# Cleaning up
echo "Cleaning up..."
sudo rm "$DOWNLOAD_DIR/kdigger.tar.xz"
sudo rm -rf "$DOWNLOAD_DIR/kdigger-linux-$KDIGGER_PLATFORM"

echo "kdigger ${KDIGGER_VERSION} has been successfully installed."
kdigger version
