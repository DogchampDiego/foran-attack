# Attack Vector Analysis and Feasability

## Initial access

Tool: 
- Scanner:
    - https://github.com/aquasecurity/trivy
    - dockerscan
    


### Cloud credentials

- Summary
- Tooling
- CVE

### Compromised images in registry

### Kubeconfig file

### Application vulnerability

### Exposed Dashboard (depracated)

### Exposed sensistive Interfaces (new)



## Execution

### Exec into container

### bash/cmb inside container

### New container

### Application exploit (RCE)

### SSH server running inside container

### Sidecar injection (new)



## Persistence

### Backdoor container

### Writable hostPath mount

### Kubernetes CronJob

### Malicious admission controller (new)



## Privilege escalation

### Privileged container

### Cluster-admin binding

### hostPath mount

### Access cloud resources



## Defense evasion

### Clear container logs

### Delete K8S events

### Pod / container name similarity

### Connect from Proxy server



## Credential access

### List K8S secretes

### Mount service principal

### Access container service account

### Applications credentials in configuration files

### Access mannaged identity credential (new)

### Malicous admission controller (new)


## Discovery

### Access the K8S API server

### Access Kubelet API

### Network mapping

### Access Kubernetes dashboard

### Instance Metadata API



## Lateral movement

### Access cloud resources

### Container service account

### Cluster internal networking

### Applications credentials in cofiguration files

### Writable volume mounts on the host

### Access Kubernetes dashboard (old)

### Access tiller endpoint (old)

### CoreDNS poisoning (new)

### ARP poisoning and IP spoofing (new)


## Collection

### Images from a private registry (new)


## Impact

### Data Destruction
### Resource Hijacking
### Denial of Service

