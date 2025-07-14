#!/bin/bash

set -e

# Check if curl is installed
if ! command -v curl &> /dev/null; then
  echo "curl is not installed. Installing..."
  if [[ -f /etc/debian_version ]]; then
    sudo apt update
    sudo apt install -y curl
  elif [[ -f /etc/redhat-release ]]; then
    sudo yum install -y curl
  else
    echo "Unsupported OS. Please install curl manually."
    exit 1
  fi
else
  echo "curl is already installed."
fi