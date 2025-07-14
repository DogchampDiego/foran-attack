import re
import subprocess

import help.helper as helper
from controller.filehistory import ConditionalFileHistory
from state.menu_state import MenuState
from tools.base_classes.tool_base import Tool
from tools.flightsim.FlightsimEnv import FlightsimEnv
from tools.flightsim.FlightsimWrapper import FlightsimWrapper


class Flightsim(Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.FLIGHTSIM, MenuState.FLIGHTSIM)

        # Wrapper and Environment Variables
        self.local_env = FlightsimEnv()
        self.wrapper = FlightsimWrapper(self.local_env)

        # Set Tool Name / Tool Version
        self.name = "Flightsim"

        # Command Mapping
        self.command_mapping = {
            "run c2": self.handle_run_c2,
        }
        
        self.command_mapping_db_ignore_db = {
            "help": self.handle_help,
            "list": self.handle_list,
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.flightsim_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["help", "View the help menu"],
            ["run --help", "View the help menu for the run command"],
            ["run [--dry|--fast]", "Run all modules"],
            ["run [--dry|--fast] <module>", "Run module of choice"],
            ["list", "List available c2 families"],
            ["run c2:<family>", "Run c2 module emulating specific c2-framework"],
            ["<module>", "Following modules are available:\n" +
              "\t\t\t\tc2, dga, imposter, miner, scan, sink, spambot,\n" + 
              "\t\t\t\tssh-exfil, ssh-transfer, tunnel-dns, tunnel-icmp"],
        ]
        # Pod Deployment
        self.pod_name = helper.get_modified_pod_name()
        self.local_env.set_pod_name(self.pod_name)
        self.pod_yaml = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": self.pod_name,
            },
            "spec": {
                "serviceAccountName":  self.global_var.get_sa_account(),  # Add the service account here
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

        # Kdigger installation variables
        self.VERSION = '2.5.0'
        self.PLATFORM = 'linux_64-bit'
        self.DOWNLOAD_URL = f'https://github.com/alphasoc/flightsim/releases/download/v{self.VERSION}/flightsim_{self.VERSION}_{self.PLATFORM}.deb'
        
        if self.global_var.get_env().get_pod_deployment():
            if not self.kubectl_is_pod_ready() and not self.is_installed("flightsim --help"):
                self.install()

            if not self.is_installed("flightsim --help"):
                self.exec_into_pod_and_install()
                self.local_env.set_pod_name(self.pod_name)
                self.local_env.set_pod_yaml(self.pod_yaml)
                self.cleanup()
                
    def check_installed(self):
        try:
            cmd = ['flightsim', 'version']
            subprocess.check_output(cmd)
            return True
        except FileNotFoundError:
            return False
    
    def install_tool(self):
        path = self.global_var.get_base_dir() + "tools/flightsim/install_flightsim.sh"
        subprocess.run(["sudo", "chmod", "+x", path], check=True)
        print(f"Script '{path}' is now executable.")
        subprocess.call(["bash", path, self.global_var.get_tool_dir(), self.global_var.get_base_dir() ])
        
    def tool_version(self):
        cmd = ['flightsim', 'version']
        version_raw = subprocess.check_output(cmd).decode("utf-8").strip()
        match = re.search(r'version (\d+\.\d+\.\d+)', version_raw)
        return match.group(1) 

    # InputHandle Methods
    def handle_help(self):
        return self.wrapper._execute_command(self.wrapper.help())
    
    def handle_list(self):
         # Show help information
        if self.global_var.get_env().get_pod_deployment():
           return self.flightsim_wrapper.exec_command_on_pod(self.flightsim_wrapper.list())
        else:
            return self.flightsim_wrapper._execute_command(self.flightsim_wrapper.list())
        
    def handle_run_c2(self):
        return self.wrapper._execute_command(self.wrapper.run_custom("c2"))

    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("list")
        self.completer.words.append("run")
        
        self.completer.words.append("c2")
        self.completer.words.append("cleartext")
        self.completer.words.append("dga")
        self.completer.words.append("imposter")
        self.completer.words.append("irc")
        self.completer.words.append("miner")
        self.completer.words.append("oast")
        self.completer.words.append("scan")
        self.completer.words.append("sink")
        self.completer.words.append("spambot")
        self.completer.words.append("ssh-exfil")
        self.completer.words.append("ssh-transfer")
        self.completer.words.append("telegram-bot")
        self.completer.words.append("tunnel-dns")
        self.completer.words.append("tunnel-icmp")

    def add_corrections(self):
        self.corrections = {
            "h": "help",
            "hepl": "help",
            "helpp": "help",
            "heelp": "help",
            "helep": "help",
            "helps": "help"
        }
        
    def exec_into_pod_and_install(self):
        print("# Executing into the pod to install Flighsim...")
        # Command to install kdigger inside the Ubuntu pod
        commands = f"""
            apt-get update && apt-get install -y curl && \
            curl -L "{self.DOWNLOAD_URL}" -o "{self.DOWNLOAD_DIR}/flightsim.deb" && \
            chmod +x "{self.DOWNLOAD_DIR}/flightsim.deb" && \
            dpkg -i "{self.DOWNLOAD_DIR}/flightsim.deb" || apt-get install -f -y
        """

        # Execute the command in the pod
        subprocess.run(["kubectl", "exec", "-it", self.pod_name, "--", "bash", "-c", commands], check=True)

        
    def cleanup(self):
        self.delete_file(self.global_var.get_base_dir() + f"{self.pod_name}.yaml")