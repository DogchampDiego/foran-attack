#!/bin/bash

set -e

# Check if nslookup is installed
if ! command -v nslookup &> /dev/null; then
  echo "nslookup is not installed. Installing..."
  if [[ -f /etc/debian_version ]]; then
    sudo apt update
    sudo apt install -y dnsutils
  elif [[ -f /etc/redhat-release ]]; then
    sudo yum install -y bind-utils
  else
    echo "Unsupported OS. Please install nslookup manually."
    exit 1
  fi
else
  echo "nslookup is already installed."
fi