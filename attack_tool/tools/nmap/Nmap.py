import re
import subprocess
from controller.filehistory import ConditionalFileHistory
import help.helper as helper
from state.menu_state import MenuState

from tools.nmap.NmapEnv import NmapEnv
from tools.nmap.NmapWrapper import NmapWrapper
from tools.base_classes.tool_base import Tool

from tools.base_classes.pod_deployment import DeployInPod
class Nmap(DeployInPod, Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.NMAP,MenuState.NMAP)
        
        # Wrapper and Environment Variables
        self.local_env = NmapEnv()
        self.wrapper = NmapWrapper(self.local_env)

        # Set Tool Name / Tool Version
        self.name = "Nmap"
        
        # Command Mapping
        self.command_mapping = {
            "agg": self.handle_scan_agg,
            "syn": self.handle_scan_syn,
            "con": self.handle_scan_con,
            "udp": self.handle_scan_udp,
            "null": self.handle_scan_null,
            "fin": self.handle_scan_fin,
            "version": self.handle_scan_version,
            "k8s": self.handle_scan_syn_k8s,
        }
        
        self.command_mapping_db_ignore_db = {
            "help": self.handle_help,
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.nmap_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["--help or help", "View the help menu"],
            ["agg", "Scan using the flags -sS (SYN) -sV (Version) -sC (Scripts) -O (OS)"],
            ["syn", "SYN scan (SYN flag)"],
            ["k8s", "SYN scan with k8s ports and script"],
            ["con", "TCP connect scan (SYN/SYN-ACK/ACK)"],
            ["udp", "UDP scan"],
            ["null", "Null scan (no flags set)"],
            ["fin", "FIN scan (FIN flag)"],
            ["version", "TCP Version detection"]
        ]


        # Pod Deployment
        self.pod_name = "ubuntu-nmap-pod"
        self.pod_yaml = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": self.pod_name,
            },
            "spec": {
                "serviceAccountName": self.global_var.get_sa_account(),  # Add the service account here
                "containers": [
                    {
                        "name": "ubuntu-container",
                        "image": "ubuntu:latest",
                        "command": ["/bin/bash", "-c", "sleep 10000"],
                        "securityContext": {
                            "privileged": self.global_var.get_priv_container()
                        }
                    }
                ]
            }
        }
        
        self.SCRIPT_URL="https://gist.githubusercontent.com/jpts/5d23bfd9b8cc08e32a3591c8195482a8/raw/kubernetes-info.nse"
        self.SCRIPT_NAME="kubernetes-info.nse"
        self.NMAP_SCRIPTS_DIR="/usr/share/nmap/scripts"
        
        # Nmap installation variables
        if self.global_env.get_pod_deployment():
            print("sda")
            if not self.kubectl_is_pod_ready() and not self.is_installed("nmap -v"):
                self.install()
                self.cleanup()

            if not self.is_installed("nmap -v"):
                self.exec_into_pod_and_install()

            self.local_env.set_pod_name(self.pod_name)
            self.local_env.set_pod_yaml(self.pod_yaml)



    def check_installed(self):
        try:
            cmd = ['nmap', '--version']
            subprocess.check_output(cmd)
            return True
        except FileNotFoundError:
            return False
    
    def install_tool(self):
        path = self.global_var.get_base_dir() + "tools/nmap/install_nmap.sh"
        subprocess.run(["sudo", "chmod", "+x", path], check=True)
        print(f"Script '{path}' is now executable.")
        subprocess.call(["bash", path, self.global_var.get_base_dir()])
        
    def tool_version(self):
        cmd = ['nmap', '--version']
        version_raw = subprocess.check_output(cmd).decode("utf-8").strip()
        match = re.search(r'Nmap version (\d+\.\d+)', version_raw)
        return match.group(1)
    
    # InputHandle Methods
    def handle_help(self):
        return self.wrapper.help()

    def handle_scan_agg(self):
        return self.wrapper._execute_command(self.wrapper.scan_agg("tcp"))
    
    def handle_scan_syn(self):
        return self.wrapper._execute_command(self.wrapper.scan_syn())

    def handle_scan_syn_k8s(self):
        self.local_env.set_scan_type("-sS")
        self.local_env.set_ports("k8s")
        self.local_env.set_custom_script("/usr/share/nmap/scripts/kubernetes-info.nse")
        print("About to launch")
        return self.wrapper._execute_command(
            self.wrapper._generate_command(scan_type=True, verbose=True, custom_script=True))

    def handle_scan_con(self):
        return self.wrapper._execute_command(self.wrapper.scan_con())
    
    def handle_scan_udp(self):
        return self.wrapper._execute_command(self.wrapper.scan_udp())
    
    def handle_scan_null(self):
        return self.wrapper._execute_command(self.wrapper.scan_null())
    
    def handle_scan_fin(self):
        return self.wrapper._execute_command(self.wrapper.scan_fin())
    
    def handle_scan_version(self):
        return self.wrapper._execute_command(self.wrapper.scan_version("tcp"))

    
    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("agg")
        self.completer.words.append("syn")
        self.completer.words.append("con")
        self.completer.words.append("udp")
        self.completer.words.append("null")
        self.completer.words.append("fin")
        self.completer.words.append("version")
        self.completer.words.append("syn-k8s")
        self.completer.words.append("udp-k8s")

    def add_corrections(self):
        self.corrections = {
            "agg": " ".join(self.wrapper.scan_agg("tcp")),
            "syn": " ".join(self.wrapper.scan_syn()),
            "con": " ".join(self.wrapper.scan_con()),
            "udp": " ".join(self.wrapper.scan_udp()),
            "null": " ".join(self.wrapper.scan_null()),
            "fin": " ".join(self.wrapper.scan_fin()),
            "version": " ".join(self.wrapper.scan_version("tcp")),
        }
        
    
    def cleanup(self):
        pass
        
    def exec_into_pod_and_install(self):
        print("# Executing into the pod to install Kdigger...")
        # Command to install kdigger inside the Ubuntu pod
        commands = f"""
            apt-get update && apt-get install -y curl nmap && \
            curl -o "{self.SCRIPT_NAME}" "{self.SCRIPT_URL}" && \
            mv "{self.SCRIPT_NAME}" "{self.NMAP_SCRIPTS_DIR}" && \
            chown -R $USER:$USER "{self.NMAP_SCRIPTS_DIR}/{self.SCRIPT_NAME}" && \
            chmod 644 "{self.NMAP_SCRIPTS_DIR}/{self.SCRIPT_NAME}"
        """


        # Execute the command in the pod
        subprocess.run(["kubectl", "exec", "-it", self.pod_name, "--", "bash", "-c", commands], check=True)