# Kubescape Commands

### Links:
- https://github.com/kubescape/kubescape

## Overview
Scan Kubernetes Clusters, YAML files and HELM charts.

Remediation Tipps and managable cloud frontend:
https://hub.armosec.io/docs/controls

## Install
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
OR
sudo add-apt-repository ppa:kubescape/kubescape
sudo apt update
sudo apt install kubescape

## General usage

### Kubernetes:
kubescape scan --enable-host-scan --verbose

(Use with --enable-host-scan -v)

kubescape scan framework nsa
kubescape scan framework mitre
kubescape scan control "Privileged container"

Scan HELM charts:
kubescape scan </path/to/directory>

Output to JSON/PDF/HTML/Prometheus:
kubescape scan --format json --format-version v2 --output results.json
kubescape scan --format pdf --output results.pdf
kubescape scan --format html --output results.html
