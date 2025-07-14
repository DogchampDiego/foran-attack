#!/bin/bash

set -e

KUBEHUNTER_VERSION="v0.6.8"
INSTALL_DIR=$2
DOWNLOAD_DIR="/tmp"
KUBEHUNTER_PLATFORM="kube-hunter-linux-x86_64-refs.tags.v0.6.8"
KUBEHUNTER_URL="https://github.com/aquasecurity/kube-hunter/releases/download/${KUBEHUNTER_VERSION}/${KUBEHUNTER_PLATFORM}"
HISTORY="${1}history"
REPORTS="${1}reports/kubehunter/"
#directory_path=$(find / -type d -name "attack")

# History directory
if [ ! -e "${HISTORY}/.prompt_history_kubehunter" ]; then
    echo "Creating history file..."
    sudo touch "${HISTORY}/.prompt_history_kubehunter"
    sudo chown $(whoami) "${HISTORY}/.prompt_history_kubehunter"
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORTS}" ]]; then
  echo "Creating reports directory ${REPORTS}..."
  sudo mkdir -p "${REPORTS}"
  sudo chown $(whoami) "${REPORTS}"
fi

# Download 
echo "Downloading Kubehunter ${KUBEHUNTER_VERSION}..."
sudo curl -L "$KUBEHUNTER_URL" -o "$DOWNLOAD_DIR/kube-hunter"

# Installing 
echo "Installing Kubehunter ${KUBEHUNTER_VERSION}..."
sudo mv "$DOWNLOAD_DIR/kube-hunter" "$INSTALL_DIR"
sudo chmod +x "$INSTALL_DIR/kube-hunter"

echo "Cleaning up..."

echo "Kubehunter ${KUBEHUNTER_VERSION} has been successfully installed."