import subprocess
from controller.filehistory import ConditionalFileHistory
import help.helper as helper
from state.menu_state import MenuState
from tools.base_classes.pod_deployment import DeployInPod

from tools.base_classes.tool_base import Tool
from tools.rakkess.RakkessEnv import RakkessEnv
from tools.rakkess.RakkessWrapper import RakkessWrapper

class Rakkess(DeployInPod, Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.RAKKESS, MenuState.RAKKESS)

        # Wrapper and Environment Variables
        self.local_env = RakkessEnv()
        self.wrapper = RakkessWrapper(self.local_env)

        self.name = "Rakkess"

        # Command Mapping
        self.command_mapping = {
            "cluster": self.handle_cluster,
            "namespace": self.handle_namespace,
            "resource": self.handle_resource,
            "user": self.handle_user,
            "service_account": self.handle_sa,
        }
        
        self.command_mapping_db_ignore_db = {
            "--help": self.handle_help,
            "help": self.handle_help,
            "-h": self.handle_help,
            "delete_pod": self.clean,
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.rakkess_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["--help or help", "View the help menu"],
            ["cluster", "View access-matrix on cluster level"],
            ["namespace <namespace>", "View access-matrix on namespace level"],
            ["resource <resource>", "View access-matrix on resource level"],
            ["user <user>", "Impersonate user"],
            ["service_account <service_account>", "Impersonate service account <namespace>:<sa-name>"],
            ["delete_pod", "deletes the pod, where rakkess is running on"]
        ]
        
        
        
        # Pod Deployment
        self.pod_name = "ubuntu-rakkess-pod"
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
        self.VERSION = 'v0.4.7'
        self.PLATFORM = 'amd64-linux'
        self.DOWNLOAD_URL = f'https://github.com/corneliusweig/rakkess/releases/download/{self.VERSION}/access-matrix-{self.PLATFORM}.tar.gz'
        

        if self.global_env.get_pod_deployment():
            if not self.kubectl_is_pod_ready() and not self.is_installed("rakkess --help"):
                self.install()

            if not self.is_installed("rakkess --help"):
                self.exec_into_pod_and_install()
        
            self.local_env.set_pod_name(self.pod_name)

        else:
            print("To Run Rakkess inside of a Pod Set Deployment of Tool in Pod 'setg pod_deployment True' and reenter Rakkess ")


    def check_installed(self):
        try:
            cmd = ['rakkess', 'version']
            subprocess.check_output(cmd)
            return True
        except FileNotFoundError:
            return False
        
    
    def install_tool(self):
        path = self.global_var.get_base_dir() + "tools/rakkess/install_rakkess.sh"
        subprocess.run(["sudo", "chmod", "+x", path], check=True)
        print(f"Script '{path}' is now executable.")
        subprocess.call(["bash", path, self.global_var.get_tool_dir(), self.global_var.get_base_dir()])

    def tool_version(self):
        cmd = ['rakkess', 'version']
        return subprocess.check_output(cmd).decode("utf-8").strip()

    # InputHandle Methods
    def handle_help(self):
        if self.global_env.get_pod_deployment():
            cmd = "rakkess " + " ".join(self.wrapper.help())
            return self.wrapper.exec_command_on_pod(cmd)   
        return self.wrapper._execute_command(self.wrapper.help())
    
    def handle_cluster(self):
        if self.global_env.get_pod_deployment():
            cmd = "rakkess " + " ".join(self.wrapper.cluster())
            return self.wrapper.exec_command_on_pod(cmd)   
        return self.wrapper._execute_command(self.wrapper.cluster())
    
    def handle_namespace(self):
        if self.global_env.get_pod_deployment():
            cmd = "rakkess " + " ".join(self.wrapper.namespace())
            return self.wrapper.exec_command_on_pod(cmd)   
        return self.wrapper._execute_command(self.wrapper.namespace())
    
    def handle_resource(self):
        if self.global_env.get_pod_deployment():
            cmd = "rakkess " + " ".join(self.wrapper.resource())
            return self.wrapper.exec_command_on_pod(cmd)   
        return self.wrapper._execute_command(self.wrapper.resource())

    
    def handle_user(self):
        if self.global_env.get_pod_deployment():
            cmd = "rakkess " + " ".join(self.wrapper.user())
            return self.wrapper.exec_command_on_pod(cmd)      
        return self.wrapper._execute_command(self.wrapper.user())
    
    def handle_group(self):
        if self.global_env.get_pod_deployment():
            cmd = "rakkess " + " ".join(self.wrapper.group())
            return self.wrapper.exec_command_on_pod(cmd)    
        return self.wrapper._execute_command(self.wrapper.group())
          
  
    def handle_sa(self):
        if self.global_env.get_pod_deployment():
            cmd = "rakkess " + " ".join(self.wrapper.sa())
            return self.wrapper.exec_command_on_pod(cmd)   
        return self.wrapper._execute_command(self.wrapper.sa())
    


    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("cluster")
        self.completer.words.append("namespace")
        self.completer.words.append("resource")
        self.completer.words.append("user")
        self.completer.words.append("group")
        self.completer.words.append("service_account")

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
        print("# Executing into the pod to install Kdigger...")
        # Command to install kdigger inside the Ubuntu pod
        commands = f"""
            apt-get update && apt-get install -y curl tar && \
            curl -fSL "{self.DOWNLOAD_URL}" -o "{self.DOWNLOAD_DIR}/rakkess.tar.xz" && \
            tar xvzf "{self.DOWNLOAD_DIR}/rakkess.tar.xz" -C "{self.DOWNLOAD_DIR}" && \
            mv "{self.DOWNLOAD_DIR}/access-matrix-{self.PLATFORM}" "{self.INSTALL_DIR}/rakkess" && \
            chmod +x "{self.INSTALL_DIR}/rakkess"
        """

        # Execute the command in the pod
        subprocess.run(["kubectl", "exec", "-it", self.pod_name, "--", "bash", "-c", commands], check=True)
        
        
    def cleanup(self):
        self.delete_file(self.global_var.get_base_dir() + f"{self.pod_name}.yaml")

    def clean(self):
        self.delete_pod()