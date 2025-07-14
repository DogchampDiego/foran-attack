from testing.testing import Testing
import time
from prompt_toolkit import prompt

class NetworkMapping(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Network mapping"
        self.mitre_tactic = "TA0007"
        self.mitre_technique = "T1046"
        self.microsoft_technique = "MS-TA9031"
        self.ip = prompt("Enter the IP and Subnet of the target (Example: 10.0.0.0/24): ")
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "naabu"
            },
            "spec": {
                "containers": [
                    {
                        "image": "projectdiscovery/naabu",
                        "name": "naabu",
                        "command": [
                        "naabu",
                        "--host",
                        self.ip,
                        "-p",
                        "22,53,80,8080,443,8443,6443,2379-2380,10250,10259,10257,10250",
                        "-silent"
                        ]
                    }
                ]
            }
        }

    def run_attack(self):
        if self.check_install_kubectl():
            # Creating Pod naabu
            print("# Creating Pod naabu with naabu container...")
            self.kubectl_create_file("naabu-pod.yaml", self.pod)
            self.kubectl_apply("naabu-pod.yaml")

            while not self.kubectl_is_pod_ready("naabu"):
                time.sleep(1)

            # Exec into Container with bash
            print("\n# Executing Naabu to scan the network...")
            time.sleep(5)
            self.cmd = ["kubectl", "logs", "naabu"]
            output, error = self.kubectl_run()
            print(output)
            
            if self.error:
                print("An Error has occured: " + error)
            else:
                self.output["naabu"] = output

            self.cleanup()
        
    def cleanup(self):
        # Delete ClusterRole secret-reader
        print("\n# Deleting Naabu-pod...")
        self.kubectl_delete("naabu", "pod")
     
        print("\n# Deleting YAML...")
        self.delete_file("naabu-pod.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass