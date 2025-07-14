Link:

https://aquasecurity.github.io/trivy/v0.41/docs/target/kubernetes/


General usage
trivy  [--scanners <scanner1,scanner2>] 
Examples:
trivy image python:3.4-alpine
Result
trivy fs --scanners vuln,secret,config myproject/
Result
trivy k8s --report summary cluster

Kubernetes:
trivy k8s --report summary cluster
trivy k8s --report=all cluster
Filter by severity:
$ trivy k8s --severity=CRITICAL --report=all cluster
Filter by scanners (Vulnerabilities, Secrets or Misconfigurations):
$ trivy k8s --scanners=secret --report=summary cluster
$ trivy k8s --scanners=config --report=summary cluster