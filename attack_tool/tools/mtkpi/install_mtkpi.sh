#!/bin/bash

# Install MTKPI
INSTALL_DIR="$1mtkpi"
MTKPI_URL="https://github.com/r0binak/MTKPI.git"
REPORT_DIR="$2reports/mtkpi/"

echo "Checking install of MTKPI..."

# Check if the directory exists
if [ -d "$INSTALL_DIR" ]; then
    echo "[+] MTKPI installed."
    exit 0
else
    echo "[+] MTKPI not installed."
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

if [ ! -e "${HISTORY_DIR}.mtkpi_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.mtkpi_history"
  sudo chown -R $USER:$USER "${HISTORY_DIR}.mtkpi_history"
fi

# Cloning MTKPI repository
echo "[+] Cloning MTKPI repository"
sudo git clone $MTKPI_URL $INSTALL_DIR
sudo chown -R $USER:$USER ${INSTALL_DIR}

echo "MTKPI has been successfully installed."
