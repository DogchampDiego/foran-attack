# Check if ssh is installed
if ! command -v ssh &> /dev/null; then
  echo "ssh is not installed. Installing..."
  if [[ -f /etc/debian_version ]]; then
    sudo apt update
    sudo apt install -y openssh-client
  elif [[ -f /etc/redhat-release ]]; then
    sudo yum install -y openssh-clients
  else
    echo "Unsupported OS. Please install ssh manually."
    exit 1
  fi
else
  echo "ssh is already installed."
fi