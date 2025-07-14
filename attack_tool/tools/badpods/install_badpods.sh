#!/bin/bash

# TODO - Install (Check) Kubectl?

# Install BadPods
INSTALL_DIR="$1/badpods"
BADPODS_URL="https://github.com/BishopFox/badPods.git"
REPORT_DIR="$2/reports/badpods/"
HISTORY_DIR="$2/history/"

echo "Checking install of BadPods..."

# Check if the directory exists
if [ -d "$INSTALL_DIR" ]; then
    echo "[+] BadPods installed."
    exit 0
else
    echo "[+] BadPods not installed."
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

if [ ! -e "${HISTORY_DIR}.badpods_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.badpods_history"
  sudo chown -R $USER:$USER "${HISTORY_DIR}.badpods_history"
fi

# Cloning BadPods repository
echo "[+] Cloning BadPods repository"
sudo git clone $BADPODS_URL $INSTALL_DIR
sudo chown -R $USER:$USER ${INSTALL_DIR}

# Installing ncat
echo "[+] Installing ncat"
sudo apt update
sudo apt install ncat

echo "BadPods has been successfully installed."

