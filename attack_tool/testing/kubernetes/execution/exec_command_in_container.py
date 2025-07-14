from testing.testing import Testing
import time

class ExecCommandContainer(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Execute nslookup, curl, and ssh command in Container"
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "exec-command-container"
            },
            "spec": {
                "containers": [
                    {
                        "image": "ubuntu:latest", 
                        "name": "exec-command-container",
                        "command": ["/bin/bash", "-c"],
                        "args": [
                            "apt-get update && apt-get install -y dnsutils curl openssh-client && sleep infinity"
                        ]
                    }
                ]
            }
        }
        self.mitre_tactic = "TA0002"
        self.mitre_technique = "T1059.0047"
        self.microsoft_technique = None
        
    def run_attack(self, case):
        if self.check_install_kubectl():
            
            # Creating Pod bash-cmd-pod
            print("# Creating Pod exec-command-container...")
            self.kubectl_create_file("exec-command-container.yaml", self.pod)
            self.kubectl_apply("exec-command-container.yaml", add_command=True)  
        
            print("\n# Waiting for the Pod to be ready...")
            while not self.kubectl_is_pod_ready("exec-command-container"):
                time.sleep(1)

            if self.error:
                print("An error has occurred while creating the container.")
            else:
                result = case.split()[0]
                # Wait until the tools are installed and ready
                print(f"\n# Verifying that the command {result} is successfully installed on the container...")

                while not self.are_tools_installed("exec-command-container", result):
                    time.sleep(1)

                if result == "nslookup":
                    print("\n# Executing nslookup...")
                    self.cmd = ["kubectl", "exec", "-it", "exec-command-container", "--", "/bin/bash", "-c", case]
                    output1, error1 = self.kubectl_exec_command()
                    if self.error:
                        print(error1)
                    else:
                        
                        self.output["nslookup"] = output1
                        print(output1)
                if result == "curl":
                    print("\n# Executing curl...")
                    self.cmd = ["kubectl", "exec", "-it", "exec-command-container", "--", "/bin/bash", "-c", case]
                    output2, error2 = self.kubectl_exec_command(decoding=True)
                    if self.error:
                        print(error2)
                    else:
                        self.output["curl"] = output2
                        print(output2)
                if result == "ssh":
                    print("\n# Executing ssh...")
                    self.cmd = ["kubectl", "exec", "-it", "exec-command-container", "--", "/bin/bash", "-c", case]
                    output3, error3 = self.kubectl_exec_command()
                    if self.error:
                        print(error3)
                    else:
                        self.output["ssh"] = output3
                        print(output3)

            # Cleanup
            self.cleanup()

    def cleanup(self):
        # Delete Pod bash-cmd-pod
        print("\n# Deleting Pod exec-command-container...")
        self.kubectl_delete("exec-command-container")
        
        print("\n# Deleting exec-command-container.yaml...")
        self.delete_file("exec-command-container.yaml")


    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass


    def are_tools_installed(self, pod_name, case):
        # Checking for nslookup, curl, and ssh using the "which" command

        if case =="ssh":
            self.cmd = ["kubectl", "exec", "-it", pod_name, "--", "/bin/bash", "-c", "which ssh"]
            output, error = self.kubectl_exec_command(add_command=False)
            if self.error or not output.strip():  # If any tool is not found, return False
                return False
            
        elif case =="nslookup":
            self.cmd = ["kubectl", "exec", "-it", pod_name, "--", "/bin/bash", "-c", "which nslookup"]
            output, error = self.kubectl_exec_command(add_command=False)
            if self.error or not output.strip():  # If any tool is not found, return False
                return False
        elif case =="curl":
            self.cmd = ["kubectl", "exec", "-it", pod_name, "--", "/bin/bash", "-c", "which curl"]
            output, error = self.kubectl_exec_command(add_command=False)
            if self.error or not output.strip():  # If any tool is not found, return False
                return False
        return True
       