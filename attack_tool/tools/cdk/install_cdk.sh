#!/bin/bash

set -e

CDK_VERSION="v1.5.3"
CDK_PLATFORM="linux_amd64"
INSTALL_DIR=$1
DOWNLOAD_DIR="/tmp"
DOWNLOAD_URL="https://github.com/cdk-team/CDK/releases/download/${CDK_VERSION}/cdk_${CDK_PLATFORM}"
REPORT_DIR="${2}/reports/cdk/"
HISTORY_DIR="${2}/history/"

# Check if cdk is already installed
if [ -x "$(command -v cdk)" ]; then
    echo "cdk is already installed."
    exit 0
fi

# Check if the reports directory exists, otherwise create it
echo "Checking reports directory..."
if [[ ! -d "${REPORT_DIR}" ]]; then
  echo "Creating reports directory ${REPORT_DIR}..."
  sudo mkdir -p ${REPORT_DIR}
  sudo chown -R $USER:$USER ${REPORT_DIR}
fi

if [ ! -e "${HISTORY_DIR}.cdk_history" ]; then
  echo "File does not exist, creating history file..."
  sudo touch "${HISTORY_DIR}.cdk_history"
  sudo chown -R $USER:$USER "${HISTORY_DIR}.cdk_history"
fi

# Download and extract cdk
echo "Downloading cdk ${CDK_VERSION}..."
sudo curl -fSL "$DOWNLOAD_URL" -o "${DOWNLOAD_DIR}/cdk"

# Installing cdk
echo "Installing cdk ${CDK_VERSION}..."
sudo mv "$DOWNLOAD_DIR/cdk" "$INSTALL_DIR/cdk"
sudo chmod +x "$INSTALL_DIR/cdk"

echo "cdk ${CDK_VERSION} has been successfully installed."
cdk -v

exit 0