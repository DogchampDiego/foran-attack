from testing.testing import Testing
import time

class ClearContainerLogs(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Clear Container Logs"
        self.mitre_tactic = "TA0005"
        self.mitre_technique = "T1070"
        self.microsoft_technique = "MS-TA9021"
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "clear-container-pod"
            },
            "spec": {
                "containers": [
                    {
                        "name": "clear-container",
                        "image": "nginx:latest",  # Replace with your desired container image
                        "command": ["sleep", "3600"],  # Example command to keep the container running
                        "imagePullPolicy": "IfNotPresent"
                    }
                ]   
            }
        }

    def run_attack(self):
        if self.check_install_kubectl():   
            
            # Creating Pod clear-container
            print("# Creating Pod clear-container-pod with ...")
            self.kubectl_create_file("clear-container-pod.yaml", self.pod)
            self.kubectl_apply("clear-container-pod.yaml")
            
            print("\n# Waiting for the Pod to be ready...")
            while not self.kubectl_is_pod_ready("clear-container-pod"):
                time.sleep(1)
                                
            print("# Show logs of the container...")
            print("root@clear-container:/#ls -al /var/log/")
            self.cmd = ["kubectl", "exec", "-it", "clear-container-pod", "--", "/bin/bash", "-c", "ls -al /var/log/"]
            output, error1 = self.kubectl_exec_command()
            print(output)
            
            # Exec into Container with bash
            print("\n# Exec into Container with bash and delete all /var/log/ files...")
            self.cmd = ["kubectl", "exec", "-it", "clear-container-pod", "--", "/bin/bash", "-c", "rm -rf /var/log/*"]
            output, error2 = self.kubectl_exec_command()
            print("root@clear-container:/# rm -rf /var/log/*")
            print(output)

            print("# Verify Deletion of Logs...")
            print("root@clear-container:/#ls -al /var/log/")
            self.cmd = ["kubectl", "exec", "-it", "clear-container-pod", "--", "/bin/bash", "-c", "ls -al /var/log/"]
            output, error3 = self.kubectl_exec_command()
            print(output)
            
        
            if self.error:
                print("An Error has occured: " + error1)
                print("An Error has occured: " + error2)
                print("An Error has occured: " + error3)
            else:
                self.output["show_logs_container"] = output
                self.output["exec_into_container_and_delete"] = output 
                self.output["verify_deletion"] = output 
            
            # Cleanup
            self.cleanup()

    def cleanup(self):
        # Delete Pod disable-namespacing
        print("# Deleting Pod clear-container...")
        self.kubectl_delete("clear-container-pod")
        
        print("\n# Deleting disable-namespacing.yaml...")
        self.delete_file("clear-container-pod.yaml")
        
        
    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass