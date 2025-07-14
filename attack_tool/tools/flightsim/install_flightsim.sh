#!/bin/bash

set -e

# Install Scritp Flightsim
# https://github.com/alphasoc/flightsim

FLIGHTSIM_VERSION="2.5.0"
INSTALL_DIR=$1
DOWNLOAD_DIR="/tmp"
FLIGHTSIM_PLATFORM="linux_64-bit"
FLIGHTSIM_URL="https://github.com/alphasoc/flightsim/releases/download/v${FLIGHTSIM_VERSION}/flightsim_${FLIGHTSIM_VERSION}_${FLIGHTSIM_PLATFORM}.deb"
REPORT_DIR="${2}/reports/flightsim/"
HISTORY_DIR="${2}/history/"

# Check if flightsim is already installed
if [ -x "$(command -v flightsim)" ]; then
    echo "Flightsim is already installed."
    exit 0
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

if [ ! -e "${HISTORY_DIR}.flightsim_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.flightsim_history"
  sudo chown -R $USER:$USER ${HISTORY_DIR}.flightsim_history
fi

# Download and extract flightsim
echo "Downloading flightsim ${FLIGHTSIM_VERSION}..."
sudo curl -L "$FLIGHTSIM_URL" -o "$DOWNLOAD_DIR/flightsim.deb"

# Installing flightsim
echo "Installing flightsim ${FLIGHTSIM_VERSION}..."
sudo chmod +x "$DOWNLOAD_DIR/flightsim.deb"
sudo dpkg -i "$DOWNLOAD_DIR/flightsim.deb"

# Cleaning up
echo "Cleaning up..."
sudo rm "$DOWNLOAD_DIR/flightsim.deb"

echo "Flightsim ${FLIGHTSIM_VERSION} has been successfully installed."

exit 0