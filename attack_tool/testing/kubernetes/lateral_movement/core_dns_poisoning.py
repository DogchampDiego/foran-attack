from testing.testing import Testing
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
import time
import subprocess
import yaml

class CoreDNSPoisoning(Testing):
    def __init__(self):
        super().__init__()
        self.name = "CoreDNS poisoning"
        self.mitre_tactic = "TA0008"
        self.mitre_technique = "T1557"
        self.microsoft_technique = "MS-TA9035"
        self.original_config = None  # To store the original CoreDNS ConfigMap
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "dns-manipulation-pod"
            },
            "spec": {
                "containers": [
                    {
                        "image": "ubuntu:latest", 
                        "name": "exec-command-container",
                        "command": ["/bin/bash", "-c"],
                        "args": [
                            "apt-get update && apt-get install -y iputils-ping && sleep infinity"
                        ]
                    }
                ]
            }
        }
            
    def run_attack(self):
        if self.check_install_kubectl():
            print("# Creating Pod dns-manipulation-pod...")
            self.kubectl_create_file("dns-manipulation-pod.yaml", self.pod)
            self.kubectl_apply("dns-manipulation-pod.yaml")

            while not self.kubectl_is_pod_ready("dns-manipulation-pod"):
                time.sleep(1)

            self.check_ping_installed()

            print("# Executing ping command to example.com from dns-manipulation-pod before poisoning...")
            self.cmd = ["kubectl", "exec", "-it", "dns-manipulation-pod", "--", "/bin/bash", "-c", "ping -c 1 example.com"]
            output, error = self.kubectl_exec_command()
            print(output)

            print("Run Coredns Poisoning and wait until chnages taken place")  
            self.modify_coredns_configmap()
            time.sleep(20)

            print("# Executing ping command to example.com from dns-manipulation-pod after poisoning...")
            self.cmd = ["kubectl", "exec", "-it", "dns-manipulation-pod", "--", "/bin/bash", "-c", "ping -c 1 example.com"]
            output, error = self.kubectl_exec_command()
            print(output)

            if error:
                print("An Error has occurred: " + error)
            else:
                self.output["ping example.com"] = output
                
            self.cleanup()


    def cleanup(self):
        print("Restoring the original CoreDNS ConfigMap...")
        try:

            result = subprocess.run(
                ["kubectl", "replace", "--force","-f","original-coredns-configmap.yaml"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("Successfully restored the original CoreDNS ConfigMap.")
                subprocess.run(["kubectl", "rollout", "restart", "deployment/coredns", "-n", "kube-system"])
            else:
                print("Failed to restore the original CoreDNS ConfigMap:", result.stderr)

        except FileNotFoundError:
            print("The original CoreDNS ConfigMap file not found. Unable to restore it.")

        # Delete Pod bash-cmd-pod
        print("\n# Deleting Pod dns-manipulation-pod...")
        self.kubectl_delete("dns-manipulation-pod")
        
        print("\n# Deleting dns-manipulation-pod.yaml...")
        self.delete_file("dns-manipulation-pod.yaml")
        
        print("\n# Deleting original-coredns-configmap.yaml...")
        self.delete_file("original-coredns-configmap.yaml")
                
        print("\n# Deleting modified-coredns-configmap.yaml...")
        self.delete_file("modified-coredns-configmap.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass
    
    
    def check_ping_installed(self):
        print("Checking if ping is installed in the pod...")
        while True:
            result = subprocess.run(
                ["kubectl", "exec", "-it", "dns-manipulation-pod", "--", "which", "ping"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("Ping is installed.")
                break
            print("Ping is not installed, waiting 1 second...")
            time.sleep(1)

    
    def modify_coredns_configmap(self, domain="example.com", ip="127.0.0.1"):
        # Step 1: Get the CoreDNS ConfigMap
        result = subprocess.run(
            ["kubectl", "get", "configmaps", "-n", "kube-system", "coredns", "-o", "yaml"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("Failed to fetch CoreDNS ConfigMap:", result.stderr)
            return


        coredns_configmap = yaml.safe_load(result.stdout)

        # Save the original CoreDNS ConfigMap to a file
        with open("original-coredns-configmap.yaml", "w") as f:
            yaml.dump(coredns_configmap, f)
        print("Saved the original CoreDNS ConfigMap to 'original-coredns-configmap.yaml'.")

        # Step 2: Check if "NodeHosts" exists in the ConfigMap
        corefile = coredns_configmap["data"].get("Corefile", "")
        node_hosts = coredns_configmap["data"].get("NodeHosts", None)

        if node_hosts is not None:
            # Add the domain mapping to NodeHosts
            if f"{ip} {domain}" not in node_hosts:
                node_hosts += f"{ip} {domain}\n"
                coredns_configmap["data"]["NodeHosts"] = node_hosts
                print(f"Added {domain} to NodeHosts.")
            else:
                print(f"{domain} already exists in NodeHosts.")
        else:
            # Add a `hosts` block to Corefile
            hosts_block = f"""
            hosts {{
                {ip} {domain}
                fallthrough
            }}"""
            if "hosts {" not in corefile:
                # Add the hosts block after the `forward` line
                corefile = corefile.replace("forward . /etc/resolv.conf", f"forward . /etc/resolv.conf{hosts_block}")
                coredns_configmap["data"]["Corefile"] = corefile
                print(f"Added a hosts block for {domain} to Corefile.")
            else:
                print("A hosts block already exists in Corefile. Modify it manually if necessary.")

        # Step 3: Write back the modified ConfigMap
        with open("modified-coredns-configmap.yaml", "w") as f:
            yaml.dump(coredns_configmap, f)

        # Step 4: Apply the modified ConfigMap
        result = subprocess.run(
            ["kubectl", "apply", "-f", "modified-coredns-configmap.yaml"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Successfully applied the updated CoreDNS ConfigMap.")
        else:
            print("Failed to apply the updated CoreDNS ConfigMap:", result.stderr)

        # Step 5: Restart CoreDNS Pods
        result = subprocess.run(
            ["kubectl", "rollout", "restart", "deployment/coredns", "-n", "kube-system"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Successfully restarted CoreDNS Pods.")
        else:
            print("Failed to restart CoreDNS Pods:", result.stderr)
