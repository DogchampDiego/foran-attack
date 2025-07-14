from testing.testing import Testing
import time

class ListK8sSecrets(Testing):
    def __init__(self,name=None):
        super().__init__()
        self.name = name
        self.role = {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRole",
            "metadata": {
                "name": "secret-reader"
            },
            "rules": [
                {
                "apiGroups": [""],
                "resources": ["secrets"],
                "verbs": ["get", "watch", "list"]
                }
            ]
        }
        self.service_account = """apiVersion: v1
kind: ServiceAccount
metadata:
  name: secret-reader
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: secret-reader-binding
subjects:
  - kind: ServiceAccount
    name: secret-reader
    namespace: default
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
"""
        self.service_account_token =  {
            "apiVersion": "v1",
            "kind": "Secret",
            "type": "kubernetes.io/service-account-token",
            "metadata": {
                "name": "secret-reader",
                "annotations": {
                "kubernetes.io/service-account.name": "secret-reader"
                }
            }
        }

        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "list-secrets-pod",
            },
            "spec": {
                "serviceAccountName": "secret-reader",
                "containers": [
                    {
                        "name": "list-secrets-container",
                        "image": "nginx"
                    }
                ]
            }
        }
        
        self.mitre_tactic = "TA0006"
        self.mitre_technique = None
        self.microsoft_technique = "MS-TA9025"

    def run_attack(self):
        if self.check_install_kubectl():   
            
                # Creating ClusterRole secret-reader
                print("# Creating ClusterRole secret-reader...")
                self.kubectl_create_file("secret-reader.yaml", self.role)
                self.kubectl_apply("secret-reader.yaml", add_command= True)
                
                # Creating ServiceAccount and ClusterRoleBindung
                print("# Creating ServiceAccount and ClusterRoleBinding...")
                self.create_file("service-account.yaml", self.service_account)
                self.kubectl_apply("service-account.yaml", add_command= True)
                
                # Creating ServiceAccountToken
                print("# Creating ServiceAccountToken...")
                self.kubectl_create_file("service-account-token.yaml", self.service_account_token)
                self.kubectl_apply("service-account-token.yaml", add_command= True)
                
                # Creating Pod list-secrets-pod
                print("# Creating Pod list-secrets-pod with created Service Account...")
                self.kubectl_create_file("list-secrets-pod.yaml", self.pod)
                self.kubectl_apply("list-secrets-pod.yaml", add_command= True)
                
                print("\n# Waiting for list-secrets-pod to be ready...")
                while not self.kubectl_is_pod_ready("list-secrets-pod"):
                    time.sleep(1)
                        
                # List secrets
                if self.name == "List K8s secrets":
                    self.mitre_technique = "T1552.007"
                    print("\n# Listing all Secrets with Service Account...")
                    print("foran@near-dev:/# kubectl get -A secrets --as system:serviceaccount:default:secret-reader")
                    output, error = self.kubectl_get("secrets", additional_args=["-A","--as", "system:serviceaccount:default:secret-reader"])
                    print(output)
                if self.name == "Access Container Service Account":
                    
                    # Creating Pod list-secrets-pod
                    print("# Creating Pod list-secrets-pod with created Service Account...")
                    self.kubectl_create_file("list-secrets-pod.yaml", self.pod)
                    self.kubectl_apply("list-secrets-pod.yaml", add_command= True)
                    
                    print("\n# Waiting for list-secrets-pod to be ready...")
                    while not self.kubectl_is_pod_ready("list-secrets-pod"):
                        time.sleep(1)
                    
                    self.mitre_technique = "T1552"
                    print("\n# Access Container and listing secret-reader token...")
                    self.cmd = ["kubectl", "exec", "list-secrets-pod", "--", "cat", "/var/run/secrets/kubernetes.io/serviceaccount/token"]
                    output, error = self.kubectl_exec_command()
                    print(output)
            
                if self.error:
                    print("An Error has occured: " + error)
                else:
                    self.output[self.name] = output 
                
                # Cleanup
                self.cleanup()
  
    def cleanup(self):
        # Delete ClusterRole secret-reader
        print("\n# Deleting ClusterRole secret-reader...")
        self.kubectl_delete("secret-reader", "clusterroles")

        # Delete ServiceAccount and ClusterRoleBinding
        print("\n# Deleting ServiceAccount and ClusterRoleBinding...")
        self.kubectl_delete("secret-reader", "serviceaccounts")
        self.kubectl_delete("secret-reader-binding", "clusterrolebindings")
        
        # Delete ServiceAccountToken

        # Delete Pod list-secrets-pod
        print("\n# Deleting Pod list-secrets-pod...")
        self.kubectl_delete("list-secrets-pod")
        
        print("\n# Deleting YAML...")
        self.delete_file("secret-reader.yaml")
        self.delete_file("service-account.yaml")
        self.delete_file("service-account-token.yaml")
        self.delete_file("list-secrets-pod.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass