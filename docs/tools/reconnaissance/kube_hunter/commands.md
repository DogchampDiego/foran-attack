# Kube-hunter Commands

### Link:
- https://github.com/aquasecurity/kube-hunter

## General usage
- kube-hunter --active --> per default in active mode
- python3 kube-hunter.py
- docker run -it --rm --network host aquasec/kube-hunter

## Kubernetes
- Run the job with kubectl create -f ./job.yaml
- Find the pod name with kubectl describe job kube-hunter
- View the test results with kubectl logs <pod name>
