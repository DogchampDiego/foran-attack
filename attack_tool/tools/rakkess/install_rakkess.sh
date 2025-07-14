#!/bin/bash

set -e

RAKKESS_VERSION="v0.4.7"
RAKKESS_PLATFORM="amd64-linux"
INSTALL_DIR=$1
DOWNLOAD_DIR="/tmp"
DOWNLOAD_URL="https://github.com/corneliusweig/rakkess/releases/download/${RAKKESS_VERSION}/access-matrix-${RAKKESS_PLATFORM}.tar.gz"
REPORT_DIR="${2}/reports/rakkess/"
HISTORY_DIR="${2}/history/"

# Check if rakkess is already installed
if [ -x "$(command -v rakkess)" ]; then
    echo "rakkess is already installed."
    exit 0
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

if [ ! -e "${HISTORY_DIR}.rakkess_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.rakkess_history"
  sudo chown -R $USER:$USER ${HISTORY_DIR}.rakkess_history
fi

# Download and extract rakkess
echo "Downloading rakkess ${RAKKESS_VERSION}..."
sudo curl -fSL "$DOWNLOAD_URL" -o "${DOWNLOAD_DIR}/rakkess.tar.xz"
sudo tar xvf "$DOWNLOAD_DIR/rakkess.tar.xz" -C "$DOWNLOAD_DIR"

# Installing rakkess
echo "Installing rakkess ${RAKKESS_VERSION}..."
sudo mv "$DOWNLOAD_DIR/access-matrix-$RAKKESS_PLATFORM" "$INSTALL_DIR/rakkess"
sudo chmod +x "$INSTALL_DIR/rakkess"

# Cleaning up
echo "Cleaning up..."
sudo rm "$DOWNLOAD_DIR/rakkess.tar.xz" && sudo rm "$DOWNLOAD_DIR/LICENSE"
sudo rm -rf "$DOWNLOAD_DIR/access-matrix-$RAKKESS_PLATFORM"

echo "rakkess ${RAKKESS_VERSION} has been successfully installed."
rakkess version

exit 0