from testing.testing import Testing
import subprocess
import time

class Kubeconfig(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Kubeconfig"
        self.mitre_tactic = "TA0001"
        self.mitre_technique = "T1078"
        self.microsoft_technique = "MS-TA9003"
        self.pod = {
                "apiVersion": "v1",
                "kind": "Pod",
                "metadata": {
                    "name": "kubeconfig-pod"
                },
                "spec": {
                    "containers": [
                        {
                            "image": "bitnami/kubectl:latest",  # Image with kubectl pre-installed
                            "name": "kubectl-container",
                            "command": ["/bin/bash", "-c", "while true; do sleep 30; done;"]
                        }
                    ]
                }
            }
        
    def copy_kubeconfig_to_pod(self, kubeconfig_path="/home/foran/.kube/config"):
        # Assuming the kubeconfig file is located on the local machine at /home/user/.kube/config
        # This will copy the kubeconfig file to the container at /root/.kube/config
        command = [
            "kubectl", "cp", kubeconfig_path,
            "kubeconfig-pod:/tmp/config"
        ]
        
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to copy kubeconfig to container: {e}")
            return False
        return True
        
    def run_attack(self):
        if self.check_install_kubectl():
                      
            # Creating Pod bash-cmd-pod
            print("# Creating Pod evil-pod...")
            self.kubectl_create_file("kubeconfig-pod.yaml", self.pod)
            self.kubectl_apply("kubeconfig-pod.yaml")  
        
            
            while not self.kubectl_is_pod_ready("kubeconfig-pod"):
                    time.sleep(1)
                
            
        
            if self.error:
                print("An Error has occured while creating the Container")
            else:
                self.output["kubeconfig_create"] = "pod/kubeconfig-pod created"

            print("# Copy Kubfig to container...")          
            if self.copy_kubeconfig_to_pod():
                print("Successful")
            else:
                print("Error")
                
            print("# List pods in kube-system namespace with kube-config from inside pod...")
            self.cmd = ["kubectl", "exec", "-it", "kubeconfig-pod", "--", "/bin/bash", "-c", 'kubectl --kubeconfig /tmp/config get pods --namespace kube-system']
            output, error = self.kubectl_exec_command()
            print(output)

            if self.error:
                print("An Error has occured: " + error)
            else:
                self.output["kubectl get pods"] = output
                
            
            # Cleanup
            self.cleanup()

            
    def cleanup(self):
        # Delete Pod bash-cmd-pod
        print("\n# Deleting Pod exec-command-container...")
        self.kubectl_delete("kubeconfig-pod")
        
        print("\n# Deleting exec-command-container.yaml...")
        self.delete_file("kubeconfig-pod.yaml")


    def display_help(self):
        pass

    def check_prerequisites(self):
        pass
    
    def determine_executable_path(self):
        pass