from testing.testing import Testing
import time
import random
import string

class PodContainerNameSimilarity(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Pod / container name similarity"
        self.mitre_tactic = "TA0005"
        self.mitre_technique = "T1036.005"
        self.microsoft_technique = "MS-TA9023"
        self.random_name = self.generate_random_string()
        self.pod = """apiVersion: v1
kind: Pod
metadata:
  name: {}
  namespace: kube-system
spec:
  containers:
  - image: nginx # would in reality be a malicious image
    name: coredns

""".format(self.random_name)
        
    def run_attack(self):
        if self.check_install_kubectl():   
                # List all Pods in 'kube-system' namespace
                print("# List all Pods in 'kube-system' namespace...")
                self.kubectl_get("pods", "kube-system")
            
                # Creating Pod
                # Print the deployment message along with the random name
                print("\n# Deploy coredns '{}' Pod with random suffix in 'kube-system'...".format(self.random_name))

                self.create_file("coredns.yaml", self.pod)
                self.kubectl_apply("coredns.yaml", add_command= True)
                while not self.kubectl_is_pod_ready(self.random_name, "kube-system"):
                    time.sleep(1)
                
                # verify the Pod
                print("\n# List '{}' in 'kube-system' namespace...".format(self.random_name))
                output, error = self.kubectl_get("pods", "kube-system", add_command= True)
                print(output)
                if self.error:
                    print("An Error has occured: " + error)
                else:
                    self.output["list_pods"] = output 
                
                # Cleanup
                self.cleanup()

    def cleanup(self):
        # Delete Pod cluster-admin-binding
        print("\n# Deleting Pod '{}'...".format(self.random_name))
        self.kubectl_delete(self.random_name, namespace= "kube-system")
        
        print("\n# Deleting bash-cmd-pod.yaml...")
        self.delete_file("coredns.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass
    
    def generate_random_string(self):
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        return f"coredns-{random_chars}-{random_suffix}"
