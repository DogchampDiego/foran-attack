from testing.testing import Testing
import time

class BashCmdContainer(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Bash/Cmd in container"
        self.mitre_tactic = "TA0002"
        self.mitre_technique = "T1059"
        self.microsoft_technique = "MS-TA9007"
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "bash-cmd-pod"
            },
            "spec": {
                "containers": [
                    {
                        "image": "nginx",
                        "name": "bash-cmd-pod"
                    }
                ]
            }
        }
        self.commands = [
            ["whoami"],
            ["exit"]
        ]

    def run_attack(self):
        if self.check_install_kubectl():   
            
                # Creating Pod bash-cmd-pod
                print("# Creating Pod bash-cmd-pod...")
                self.kubectl_create_file("bash-cmd-pod.yaml",self.pod)
                self.kubectl_apply("bash-cmd-pod.yaml")
            
                while not self.kubectl_is_pod_ready("bash-cmd-pod"):
                    time.sleep(1)
                
                # Exec into Container with bash
                self.cmd = ["kubectl", "exec", "-i", "bash-cmd-pod", "--", "sh"]        
                
                print("\n# Exec into Container with bash...")
                for cmd in self.commands:
                    print("\n# Executing", ''.join(cmd), "on pod...")
                    print("root@bash-cmd-pod:/#", ' '.join(cmd))
                    self.cmd = ["kubectl", "exec", "-i", "bash-cmd-pod", "--", "bash"]
                    output, error = self.kubctl_exec(''.join(cmd))
                    if ''.join(cmd) == "whoami":
                        print(output)
                    print(error)
                
                    if self.error:
                        print("An Error has occured: " + error)
                    else:
                        self.output[' '.join(cmd)] = output
                        self.command.append(cmd)

                # Cleanup
                self.cleanup()

    def cleanup(self):
        # Delete Pod bash-cmd-pod
        print("\n# Deleting Pod bash-cmd-pod...")
        self.kubectl_delete("bash-cmd-pod")
        
        print("\n# Deleting bash-cmd-pod.yaml...")
        self.delete_file("bash-cmd-pod.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass
