# Tools to Implement

## Offensive Tools
### Peirates
Peirates, a Kubernetes penetration tool, enables an attacker to escalate privilege and pivot through a Kubernetes cluster. It automates known techniques to steal and collect service account tokens, secrets, obtain further code execution, and gain control of the cluster.
https://github.com/inguardians/peirates

### CDK - Zero Dependency Container Penetration Toolkit
CDK is an open-sourced container penetration toolkit, designed for offering stable exploitation in different slimmed containers without any OS dependency. It comes with useful net-tools and many powerful PoCs/EXPs and helps you to escape container and take over K8s cluster easily.
https://github.com/cdk-team/CDK

### Botb
BOtB is a container analysis and exploitation tool designed to be used by pentesters and engineers.
https://github.com/brompwnie/botb

### Kdigger
kdigger, short for "Kubernetes digger", is a context discovery tool for Kubernetes penetration testing. This tool is a compilation of various plugins called buckets to facilitate pentesting Kubernetes from inside a pod.
https://github.com/quarkslab/kdigger

## Adversary Simulation/Emulation
### Stratus Red Team
Stratus Red Team is "Atomic Red Team™" for the cloud, allowing to emulate offensive attack techniques in a granular and self-contained manner.
https://github.com/DataDog/stratus-red-team

## Enumeration, Discovery and Assessment:
## Rakkes:
RBAC - can-i permissions:
https://github.com/corneliusweig/rakkess

## Coredns-enum
A tool to enumerate Kubernetes network information through DNS alone. It attempts to list service IPs, ports, and service endpoint IPs where possible.
https://github.com/jpts/coredns-enum

## Container Deployment
### BadPods
A collection of manifests that create pods with different elevated privileges. 
https://github.com/BishopFox/badPods

### Hacker Container
Container with all the list of useful tools/commands while hacking Kubernetes Clusters. 
https://github.com/madhuakula/hacker-container


## Rootkits and C2 Deployments
### TripleCross 
epBPF Rootkit with C2 capabilities
https://github.com/h3xduck/TripleCross

### Kubesploit
Kubesploit is a cross-platform post-exploitation HTTP/2 Command & Control server and agent dedicated for containerized environments written in Golang and built on top of Merlin project by Russel Van Tuyl (@Ne0nd0g).
https://github.com/cyberark/kubesploit

### Silver
General C2 Tool
https://github.com/BishopFox/sliver


## Kubernetes API CLI and Containrd CLI
### kubectl 
https://github.com/kubernetes/kubectl

### krew
Krew is the package manager for kubectl plugins.
https://github.com/kubernetes-sigs/krew

### kubeletctl
Kubeletctl is a command line tool that implement kubelet's API.
Part of kubelet's API is documented but most of it is not.
This tool covers all the documented and undocumented APIs.
https://github.com/cyberark/kubeletctl

### Nerdctl
nerdctl is a Docker-compatible CLI for containerd.
https://github.com/containerd/nerdctl

## Kubernetes Vulnerability Scanning
### ConMachi
Conmachi is a tool written in Golang intended to be used to collect information about a container environment and list potential security issues.
https://github.com/nccgroup/ConMachi

### Clair
Clair is an open source project for the static analysis of vulnerabilities in application containers (currently including OCI and docker).
https://github.com/quay/clair

### Grype
A vulnerability scanner for container images and filesystems.
https://github.com/anchore/grype

### Inspektor Gadget
Inspektor Gadget is a collection of tools (or gadgets) to debug and inspect Kubernetes resources and applications
https://github.com/inspektor-gadget/inspektor-gadget

### Kubebench
kube-bench is a tool that checks whether Kubernetes is deployed securely by running the checks documented in the CIS Kubernetes Benchmark.
https://github.com/aquasecurity/kube-bench

### Dive
A tool for exploring a docker image, layer contents, and discovering ways to shrink the size of your Docker/OCI image.
https://github.com/wagoodman/dive

### Kubesec
Security risk analysis for Kubernetes resources
https://github.com/controlplaneio/kubesec

## Threat Detection and Analysis and Evasion
### Falco
Falco is a cloud native runtime security tool for Linux operating systems. It is designed to detect and alert on abnormal behavior and potential security threats in real-time.
https://github.com/falcosecurity/falco

### Falco bypasses
This project describes my research on various techniques to bypass default falco ruleset (based on falco v0.28.1).
https://github.com/blackberry/Falco-bypasses

### Falco Generator
Generate a variety of suspect actions that are detected by Falco rulesets.
https://github.com/falcosecurity/event-generator


## Tools to Watch
Either currently in development and not ready, or no K8s support 
### Cloudfox
https://github.com/BishopFox/cloudfox

## Interesting
Intersting, but no highly relevant.

### Pillage registries
This project takes a Docker registry and pillages the manifest and configuration for each image in its catalog.
https://github.com/nccgroup/go-pillage-registries

### Kubestriker
Kubestriker is a platform-agnostic tool designed to tackle Kuberenetes cluster security issues due to misconfigurations and will help strengthen the overall IT infrastructure of any organisation.
https://github.com/vchinnipilli/kubestriker