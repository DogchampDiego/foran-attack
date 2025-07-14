#!/bin/bash

directory="/opt/tools"

# Check if the directory exists
if [ ! -d "$directory" ]; then
  # Create the directory
  sudo mkdir -p "$directory"
  echo "Directory created: $directory"
fi
# Download and install dependencies
apt-get update
apt-get -y install exploitdb git

# Clone the cve_searchsploit repository
cd /opt/tools/
sudo git clone https://github.com/andreafioraldi/cve_searchsploit.git

cd ./cve_searchsploit
# Check if Python 3 is available, otherwise use Python
if command -v python3 &>/dev/null; then
  sudo python3 setup.py install
else
  sudo python setup.py install
fi

sudo cve_searchsploit >/dev/null 2>&1