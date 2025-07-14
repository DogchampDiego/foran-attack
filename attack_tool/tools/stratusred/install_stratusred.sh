#!/bin/bash

# Install Scritp Stratus Red Team

set -e

STRATUS_VERSION="v2.17.0"
INSTALL_DIR=$1
DOWNLOAD_DIR="/tmp"
STRATUS_PLATFORM="Linux_x86_64"
STRATUS_URL="https://github.com/DataDog/stratus-red-team/releases/download/${STRATUS_VERSION}/stratus-red-team_${STRATUS_PLATFORM}.tar.gz"
REPORT_DIR="${2}/reports/stratusred/"
HISTORY_DIR="${2}/history/"

# Check if stratus is already installed
if [ -x "$(command -v stratus)" ]; then
    echo "Stratusred is already installed."
    exit 0
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

if [ ! -e "${HISTORY_DIR}.stratusred_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.stratusred_history"
  sudo chown -R $USER:$USER ${HISTORY_DIR}.stratusred_history
fi

# Download and extract stratus
echo "Downloading stratus ${STRATUS_VERSION}..."
sudo curl -L "$STRATUS_URL" -o "$DOWNLOAD_DIR/stratus.tar.xz"
sudo tar xvf "$DOWNLOAD_DIR/stratus.tar.xz" -C "$DOWNLOAD_DIR"

# Installing stratus
echo "Installing Stratus ${STRATUS_VERSION}..."
sudo cp "$DOWNLOAD_DIR/stratus" "$INSTALL_DIR"
sudo chmod +x "$INSTALL_DIR/stratus"

# Cleaning up
echo "Cleaning up..."
sudo rm "$DOWNLOAD_DIR/stratus.tar.xz"
sudo rm -rf "$DOWNLOAD_DIR/stratus-linux-$stratus_PLATFORM/"

echo "Stratus ${STRATUS_VERSION} has been successfully installed."

exit 0