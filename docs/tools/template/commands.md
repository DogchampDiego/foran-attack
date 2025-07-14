# Falco Commands

### Links:
- https://github.com/falcosecurity/falco

## Install
- https://falco.org/docs/getting-started/installation/

curl -fsSL https://falco.org/repo/falcosecurity-packages.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/falco-archive-keyring.gpg

sudo cat >>/etc/apt/sources.list.d/falcosecurity.list <<EOF
deb [signed-by=/usr/share/keyrings/falco-archive-keyring.gpg] https://download.falco.org/packages/deb stable main
EOF

sudo apt-get update -y

Dependencies:
sudo apt install -y dkms make linux-headers-$(uname -r)
sudo apt install -y clang llvm
sudo apt install -y dialog

Falco:
sudo apt-get install -y falco

Kmod -> Automatic rules set update: YES

Run Check:
systemctl list-units | grep falco

## General usage



### Kubernetes: