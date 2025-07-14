#!/bin/bash

# Install  Red Kube
REDKUBE_URL="https://github.com/lightspin-tech/red-kube.git"
HISTORY="${1}history"
REPORTS="${1}reports/redkube/"
INSTALL_DIR=$2


# History directory
if [ ! -e "${HISTORY}/.prompt_history_redkube.txt" ]; then
    echo "Creating history file..."
    sudo touch "${HISTORY}/.prompt_history_redkube.txt"
    sudo chown $(whoami) "${HISTORY}/.prompt_history_redkube.txt"
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORTS}" ]]; then
  echo "Creating reports directory ${REPORTS}..."
  sudo mkdir -p "${REPORTS}"
  sudo chown $(whoami) "${REPORTS}"
fi

# Cloning  Red Kube repository
echo "[+] Cloning Red Kube repository"
cd $INSTALL_DIR

# Clone the repository
sudo git clone $REDKUBE_URL && cd ${INSTALL_DIR%/}/red-kube

# install requirements
sudo pip install -r requirements.txt
