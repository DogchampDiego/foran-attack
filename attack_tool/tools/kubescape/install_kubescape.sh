#!/bin/bash

set -e

KUBESCAPE_VERSION="v3.0.1"
KUBESCAPE_PLATFORM="kubescape-ubuntu-latest"
INSTALL_DIR=$1
KUBESCAPE_URL="https://github.com/armosec/kubescape/releases/download/${KUBESCAPE_VERSION}/${KUBESCAPE_PLATFORM}"
DOWNLOADED_FILE="/tmp/kubescape"
REPORT_DIR="${2}/reports/kubescape/"
HISTORY_DIR="${2}/history/"

# Check if Kubescape is already installed
if command -v kubescape &>/dev/null; then
  INSTALLED_VERSION=$(kubescape version 2>&1 | sed -n 's/.*\(v[0-9.]*\).*/\1/p')
  if [[ "${INSTALLED_VERSION}" == "${KUBESCAPE_VERSION}" ]]; then
    echo "Kubescape ${KUBESCAPE_VERSION} is already installed."
    echo ""
    exit 0
  else
    echo "Kubescape ${INSTALLED_VERSION} is already installed. Please uninstall it before proceeding."
    exit 1
  fi
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

if [ ! -e "${HISTORY_DIR}.kubescape_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.kubescape_history"
  sudo chown -R $USER:$USER ${HISTORY_DIR}.kubescape_history
fi

# Download Kubescape binary
echo "Downloading Kubescape ${KUBESCAPE_VERSION}..."
curl -Lo "${DOWNLOADED_FILE}" $KUBESCAPE_URL
chmod +x "${DOWNLOADED_FILE}"

# Move Kubescape binary to the installation directory
echo "Installing Kubescape..."
sudo mv "${DOWNLOADED_FILE}" "${INSTALL_DIR}"

# Verify the installation
echo "Verifying Kubescape installation..."
kubescape version

echo "Kubescape ${KUBESCAPE_VERSION} has been successfully installed."

exit 0