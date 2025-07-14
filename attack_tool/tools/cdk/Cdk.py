import subprocess
from controller.filehistory import ConditionalFileHistory
import help.helper as helper
from state.menu_state import MenuState

from tools.base_classes.tool_base import Tool
from tools.cdk.CdkEnv import CdkEnv
from tools.cdk.CdkWrapper import CdkWrapper

from tools.base_classes.pod_deployment import DeployInPod

class Cdk(DeployInPod, Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.CDK, MenuState.CDK)

        # Wrapper and Environment Variables
        self.local_env = CdkEnv()
        self.wrapper = CdkWrapper(self.local_env)
        
        # Set Tool Name / Tool Version
        self.name = "CDK (Container DucK)"

        # Command Mapping
        self.command_mapping = {
            "evaluate": self.handle_evaluate,
            "evaluate-full": self.handle_evaluate_full,
            "escape": self.handle_auto_escape,
        }
        
        self.command_mapping_db_ignore_db = {
            "help" or "-h": self.handle_help,
            "list": self.handle_list_exploits,
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.cdk_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["help or -h", "View the help menu"],
            ["list", "List all exploits"], 
            ["evaluate", "Evaluate the cluster"],
            ["evaluate-full", "Evaluate the container with file scanning"],
            ["run <exploit> <exploit_args>", "Run exploit"],
            ["<tool> <tool_args>", "Run tool"],
            ["escape", "Auto exploit (deprecated)"],  
        ]
        
        
        self.global_env.set_pod_deployment(True)

        # Pod Deployment
        self.pod_name = "ubuntu-cdk-pod"
        self.pod_yaml = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": self.pod_name,
            },
            "spec": {
                "containers": [
                    {
                        "name": "ubuntu-container",
                        "image": "ubuntu:latest",
                        "command": ["/bin/bash", "-c", "sleep 10000"],  # Keep the pod running
                    }
                ]
            }
        }


        # Kdigger installation variables
        self.VERSION = 'v1.5.0'
        self.PLATFORM = 'linux_amd64'
        self.DOWNLOAD_URL = f'https://github.com/cdk-team/CDK/releases/download/{self.VERSION}/cdk_{self.PLATFORM}'
        if self.global_env.get_pod_deployment():
            if not self.kubectl_is_pod_ready() and not self.is_installed("cdk --help"):
                self.install()
                self.cleanup()

            if not self.is_installed("cdk --help"):
                self.exec_into_pod_and_install()

            self.local_env.set_pod_name(self.pod_name)

        else:
            print("Set Deployment of Tool in Pod 'setg pod_deployment True'")


    def check_installed(self):
        try:
            cmd = ['cdk', '-v']
            subprocess.check_output(cmd)
            return True
        except FileNotFoundError:
            return False
    
    def install_tool(self):
        path = self.global_var.get_base_dir() + "tools/cdk/install_cdk.sh"
        subprocess.run(["sudo", "chmod", "+x", path], check=True)
        print(f"Script '{path}' is now executable.")
        subprocess.call(["bash", path, self.global_var.get_tool_dir(), self.global_var.get_base_dir() ])
        
    def tool_version(self):
        return subprocess.check_output(['cdk', '-v']).decode('utf-8').strip()

    # InputHandle Methods
    def handle_help(self):
        if self.global_env.get_pod_deployment():
            cmd = "cdk " + " ".join(self.wrapper.help())
            return self.wrapper.exec_command_on_pod(cmd)
        return None
    
    def handle_list_exploits(self):
        if self.global_env.get_pod_deployment():
            cmd = "cdk " + " ".join(self.wrapper.list_exploits())
            return self.wrapper.exec_command_on_pod(cmd)
        return None
    
    def handle_auto_escape(self):
        return self.wrapper._execute_command(self.wrapper.auto_escape("id"))
    
    def handle_evaluate(self):
        return self.wrapper._execute_command(self.wrapper.evaluate())
    
    def handle_evaluate_full(self):
        return self.wrapper._execute_command(self.wrapper.evaluate_full())
    
    def handle_run(self, exploit, exploit_args):
        return self.wrapper._execute_command(self.wrapper.exploit(exploit, exploit_args))
    
    def handle_tool(self, tool, tool_args):
        return self.wrapper._execute_command(self.wrapper.tool(tool, tool_args))

    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("evaluate")
        self.completer.words.append("run")
        self.completer.words.append("list")

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
        print("# Executing into the pod to install CDK...")
        # Command to install kdigger inside the Ubuntu pod
        commands = f"""
            apt-get update && apt-get install -y curl tar && \
            curl -fSL "{self.DOWNLOAD_URL}" -o "{self.DOWNLOAD_DIR}/cdk" && \
            mv "{self.DOWNLOAD_DIR}/cdk" "{self.INSTALL_DIR}/cdk" && \
            chmod +x "{self.INSTALL_DIR}/cdk"
        """

        # Execute the command in the pod
        subprocess.run(["kubectl", "exec", "-it", self.pod_name, "--", "bash", "-c", commands], check=True)
        
    def cleanup(self):
        self.delete_file(self.global_var.get_base_dir() + f"{self.pod_name}.yaml")

    def clean(self):
        self.delete_pod()
