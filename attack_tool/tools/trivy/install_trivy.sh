#!/bin/bash

set -e

# Install Script Trivy

TRIVY_VERSION="0.47.0"
DOWNLOAD_DIR="/tmp"
TRIVY_PLATFORM="Linux-64bit.deb"
TRIVY_URL="https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_${TRIVY_PLATFORM}"
REPORT_DIR="${2}/reports/trivy/"
HISTORY_DIR="${2}/history/"

# Check if already installed
if [ -x "$(command -v trivy)" ]; then
    echo "Trivy is already installed."
    exit 0
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

# Check if the history directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${HISTORY_DIR}" ]]; then
  echo "Creating reports directory ${HISTORY_DIR}..."
  sudo mkdir -p ${HISTORY_DIR}
  sudo chown -R $USER:$USER ${HISTORY_DIR}
fi

if [ ! -e "${HISTORY_DIR}.trivy_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.trivy_history"
  sudo chown -R $USER:$USER ${HISTORY_DIR}.trivy_history
fi

# Download and extract
echo "Downloading Trivy ${TRIVY_VERSION}..."
sudo curl -L "$TRIVY_URL" -o "$DOWNLOAD_DIR/trivy.deb"

# Installing trivy
echo "Installing Trivy ${TRIVY_VERSION}..."
sudo dpkg -i "$DOWNLOAD_DIR/trivy.deb"

# Cleaning up
echo "Cleaning up..."
sudo rm "$DOWNLOAD_DIR/trivy.deb"

echo "Trivy ${TRIVY_VERSION} has been successfully installed."

exit 0