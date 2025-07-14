from testing.testing import Testing
import time

class ClusterInternalNetworking(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Cluster internal networking"
        self.pod = """apiVersion: v1
kind: Namespace
metadata:
  name: secret
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: web
  name: web
  namespace: secret
spec:
  containers:
  - image: nginx
    name: web
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: web
  name: web
  namespace: secret
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: web
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: web-secret-only
  name: web-secret-only
  namespace: secret
spec:
  containers:
  - image: nginx
    name: web
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: web-secret-only
  name: web-secret-only
  namespace: secret
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: web-secret-only
---
apiVersion: v1
kind: Namespace
metadata:
  name: test-namespace
---
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  namespace: test-namespace
spec:
  containers:
  - image: nginx
    name: web
"""
        self.network_policy = """kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  namespace: secret
  name: deny-from-other-namespaces
spec:
  podSelector:
    matchLabels:
  ingress:
  - from:
    - podSelector: {}
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-allow-all-namespaces
  namespace: secret
spec:
  podSelector:
    matchLabels:
      app: web
  ingress:
    - from:
        - namespaceSelector: {}
"""
        self.mitre_tactic = "TA0008"
        self.mitre_technique = "T1210"
        self.microsoft_technique = "MS-TA9034"
    def run_attack(self):
        if self.check_install_kubectl():   
            
            # Creating Pod cluster-internal
            print("# Creating Demo setup...")
            self.create_file("cluster-internal.yaml", self.pod)
            self.kubectl_apply("cluster-internal.yaml")
        
            while not self.kubectl_is_pod_ready("web", namespace="secret") and not self.kubectl_is_pod_ready("web-secret-only",namespace="secret") and not self.kubectl_is_pod_ready("test-pod", namespace= "test-namespace"):
                time.sleep(1)
                
            print("\n# Check internal networking before applying Network Policy")
            print("foran@near-dev:/# kubectl exec -it test-pod -n test-namespace -- curl http://web.secret")
            self.cmd = ["kubectl", "exec", "test-pod", "-n", "test-namespace", "--", "curl", "http://web.secret"]
            out = self.kubectl_exec_command()
            print(out)
            print("foran@near-dev:/# kubectl exec -it test-pod -n test-namespace -- curl http://web-secret-only.secret")
            self.cmd = ["kubectl", "exec", "test-pod", "-n", "test-namespace", "--", "curl","-m","10", "http://web-secret-only.secret"]
            out = self.kubectl_exec_command()
            print(out)
            print("foran@near-dev:/# kubectl exec -it web -n secret -- curl http://web-secret-only.secret")
            self.cmd = ["kubectl", "exec", "web", "-n", "secret", "--", "curl", "http://web-secret-only.secret"]
            out = self.kubectl_exec_command()
            print(out)
            
            print("\n Apply Network Policys")
            self.create_file("network-policy.yaml", self.network_policy)
            self.kubectl_apply("network-policy.yaml")
            
            print("\n# Check internal networking after applying Network Policy")
            print("foran@near-dev:/# kubectl exec -it test-pod -n test-namespace -- curl http://web.secret")
            self.cmd = ["kubectl", "exec", "test-pod", "-n", "test-namespace", "--", "curl", "http://web.secret"]
            output, error_exec = self.kubectl_exec_command()

            print(output)
            self.cmd = ["kubectl", "exec", "test-pod", "-n", "test-namespace", "--", "curl","-m","10", "http://web-secret-only.secret"]
            output_2, error_exec2  = self.kubectl_exec_command()
            print("foran@near-dev:/# kubectl exec -it test-pod -n test-namespace -- curl http://web-secret-only.secret")
            print(error_exec2)
            print("foran@near-dev:/# kubectl exec -it web -n secret -- curl http://web-secret-only.secret")
            self.cmd = ["kubectl", "exec", "web", "-n", "secret", "--", "curl", "http://web-secret-only.secret"]
            output3, error_exec3  = self.kubectl_exec_command()
            print(output)
            
            if self.error:
                print("Errors first command: ", error_exec)
                print("Errors second command: ", output_2)
                print("Errors third command: ", error_exec3)   
            else:
                self.output["kubectl exec -it test-pod -n test-namespace -- curl http://web.secret"] = output
                self.output["kubectl exec -it test-pod -n test-namespace -- curl http://web-secret-only.secret"] = error_exec2
                self.output["kubectl exec -it web -n secret -- curl http://web-secret-only.secret"] = output3

            # Cleanup
            self.cleanup()  

    def cleanup(self):
        # Delete Pod web
        print("\n# Deleting Pod web...")
        self.kubectl_delete("web", namespace="secret")

        # Delete Pod web-secret-only
        print("\n# Deleting Pod web-secret-only...")
        self.kubectl_delete("web-secret-only", namespace="secret")
        
        # Delete Pod test-pod
        print("\n# Deleting Pod test-pod...")
        self.kubectl_delete("test-pod", namespace="test-namespace")

        # Delete NetworkPolicy
        print("\n# Deleting NetworkPolicy...")
        self.kubectl_delete("deny-from-other-namespaces", "networkpolicies", namespace="secret")
        self.kubectl_delete("web-allow-all-namespaces", "networkpolicies", namespace="secret")
        
        # Deleting Yaml
        print("\n# Deleting YAML...")
        self.delete_file("cluster-internal.yaml")
        self.delete_file("network-policy.yaml")
        
    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass