# KDigger Commands

### Links:
- https://github.com/quarkslab/kdigger

## Install
wget https://go.dev/dl/go1.20.1.linux-amd64.tar.gz
sudo tar -C /usr/local -xvf go1.20.4.linux-amd64.tar.gz
nano ~/.profile
export PATH=$PATH:/usr/local/go/bin
git clone https://github.com/quarkslab/kdigger
cd kdigger/
make install-linter
make
sudo install kdigger /usr/local/bin

## General usage

kdigger dig all
kdigger d a

kdigger help dig
kdigger help gen

kdigger ls
kdigger

### Kubernetes:

