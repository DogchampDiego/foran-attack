#!/bin/bash

REPORT_DIR="${1}/reports/nmap/"
HISTORY_DIR="${1}/history/"

# Check if Nmap is already installed
if command -v nmap &>/dev/null; then
    echo "Nmap is already installed."
    exit 0
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

if [ ! -e "${HISTORY_DIR}.nmap_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.nmap_history"
  sudo chown -R $USER:$USER ${HISTORY_DIR}.nmap_history
fi

# Update package lists
sudo apt update

# Install Nmap
sudo apt install -y nmap

# Download K8s NSE Script
SCRIPT_URL="https://gist.githubusercontent.com/jpts/5d23bfd9b8cc08e32a3591c8195482a8/raw/kubernetes-info.nse"
SCRIPT_NAME="kubernetes-info.nse"

sudo curl -o "$SCRIPT_NAME" "$SCRIPT_URL"

# Move the NSE Script to Nmap's Scripts Directory
NMAP_SCRIPTS_DIR="/usr/share/nmap/scripts"
sudo mv "$SCRIPT_NAME" "$NMAP_SCRIPTS_DIR"
sudo chown -R $USER:$USER "$NMAP_SCRIPTS_DIR/$SCRIPT_NAME"
sudo chmod 644 "$NMAP_SCRIPTS_DIR/$SCRIPT_NAME"

# Verify the installation
if command -v nmap &>/dev/null; then
    echo "Nmap has been successfully installed."
else
    echo "Nmap installation failed. Please try again."
fi

exit 0