#!/bin/bash

directory="/opt/tools"

# Check if the directory exists
if [ ! -d "$directory" ]; then
  # Create the directory
  sudo mkdir -p "$directory"
  echo "Directory created: $directory"
fi

cd /opt/tools/
sudo git clone https://github.com/redcanaryco/atomic-red-team.git

# Install Kubehunter
cd ./atomic-red-team

# install requirements
sudo pip install -r requirements.txt

# Update package lists
sudo apt-get update

# Install required packages
sudo apt-get install -y apt-transport-https ca-certificates curl

# Download Kubernetes archive keyring
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

# Add Kubernetes repository to package sources
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Update package lists again
sudo apt-get update

# Install kubectl
sudo apt-get install -y kubectl