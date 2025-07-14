from testing.testing import Testing
import time

class NewContainer(Testing):
    def __init__(self):
        super().__init__()
        self.name = "New Container"
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "evil-pod"
            },
            "spec": {
                "containers": [
                    {
                        "image": "evil-container-image",
                        "name": "evil"
                    }
                ]
            }
        }
        self.mitre_tactic = "TA0002"
        self.mitre_technique = "T1610"
        self.microsoft_technique = "MS-TA9008"
        
        
    def run_attack(self):
        if self.check_install_kubectl():
            
            # Creating Pod bash-cmd-pod
            print("# Creating Pod evil-pod...")
            self.kubectl_create_file("evil-pod.yaml", self.pod)
            self.kubectl_apply("evil-pod.yaml", add_command=True)  
        
            if self.error:
                print("An Error has occured while creating the Container")
            else:
                self.output["pod_created"] = "pod/evil-pod created"


            # Cleanup
            self.cleanup()

    def cleanup(self):
        # Delete Pod bash-cmd-pod
        print("\n# Deleting Pod evil-pod...")
        self.kubectl_delete("evil-pod")
        
        print("\n# Deleting evil-pod.yaml...")
        self.delete_file("evil-pod.yaml")


    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass