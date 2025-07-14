import help.helper as helper
from state.menu_state import MenuState
from tools.base_classes.tool_base import Tool
from tools.base_classes.pod_deployment import DeployInPod
import subprocess
from controller.filehistory import ConditionalFileHistory
from tools.kdigger.kdigger_env import KDiggerEnv
from tools.kdigger.kdigger_wrapper import KdiggerWrapper
import os

class KDigger(DeployInPod, Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.KDIGGER,MenuState.KDIGGER)

        # Wrapper and Metadata Variables
        self.local_env = KDiggerEnv()
        self.wrapper = KdiggerWrapper(self.local_env)

        # Set Tool Name / Tool Version
        self.name = "kdigger"

        # Command Mapping
        self.command_mapping = {
            "dig": self.handle_dig,
            "dig_all": self.handle_dig_all,
            #"gen": self.handle_gen,
            "gen_simple_pod": self.handle_simple_pod,
            "gen_priv_pod": self.handle_lowsec_pod,
        }
        self.command_mapping_db_ignore_db = {
            "--help": self.handle_help,
            "help_gen": self.handle_help_gen,
            "help_dig": self.handle_help_dig,
            "buckets": self.show_buckets,
            "ls": self.show_buckets,
            "options_dig":self.settings_dig,
            "options_gen":self.settings_gen,
            "delete_pod": self.clean
        }
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() +  "history/.prompt_history_kdigger.txt")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False  

        # self.custom_style = Style.from_dict({'prompt': 'blue'})
        self.column = ["Method", "Description"]
        self.row = [
            ["--help", "Display command help information"],
            ["buckets", "See all buckets to dig"],
            ["options_dig",  "Dig with given options"],
            ["dig",  "Dig with given options"],
            ["dig_all",  "Dig with given options"],
            ["gen_simple_pod","Create a very simple pod"],
            ["gen_priv_pod","Create a pod named mypod with most security features disabled"],
            ["delete_pod", "deletes the pod, where kdigger is running on"]
        ]

        self.global_env.set_pod_deployment(True)
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


        # Kdigger installation variables
        self.VERSION = 'v1.5.0'
        self.PLATFORM = 'amd64'
        self.DOWNLOAD_URL = f'https://github.com/quarkslab/kdigger/releases/download/{self.VERSION}/kdigger-linux-{self.PLATFORM}.tar.gz'
        if self.global_env.get_pod_deployment():
            if not self.kubectl_is_pod_ready() and not self.is_installed("kdigger --help"):
                self.install()
                self.cleanup()

            if not self.is_installed("kdigger --help"):
                self.exec_into_pod_and_install()

            self.local_env.set_pod_name(self.pod_name)
            self.local_env.set_pod_yaml(self.pod_yaml)

        else:
            print("Set Deployment of Tool in Pod 'setg pod_deployment True'")


    # Abstract Methods  
    def settings(self):
        print("To see the parameter for gen or dig use 'options_gen' or 'options_dig'")
        header = ["Parameter","Value"]
        self.table.print_table(header,self.local_env.get_env_dict())

    def tool_version(self):
        return "1"

    def settings_dig(self):
        header = ["Parameter","Value"]
        self.table.print_table(header,self.local_env.get_env_dict_dig())
    
    def settings_gen(self):
        header = ["Parameter","Value"]
        self.table.print_table(header,self.local_env.get_env_dict_gen())

    def check_installed(self):
        try:
            # Run the kubehunter command with the `--help` flag to check if it is installed
            subprocess.check_output(['kdigger', '--help'])
            return True
        except FileNotFoundError:
            return False
    
    def install_tool(self):
        subprocess.call(["bash", self.global_var.get_base_dir() +  "tools/kdigger/install_kdigger.sh", self.global_var.get_base_dir(),self.global_var.get_tool_dir()])
        
    # InputHandle Methods
    def handle_help(self):
        return self.wrapper.help_base()

    def handle_help_gen(self):
        return self.wrapper.help("gen")

    def handle_help_dig(self):
        return self.wrapper.help("dig")

    def show_buckets(self):
        return self.wrapper.show_buckets()

    def handle_dig(self):
        return self.wrapper.dig()

    def handle_dig_all(self):
        return self.wrapper.dig_all()

    def handle_gen(self):
        return self.wrapper.generate_pod_template()

    def handle_simple_pod(self):
        cmd = "gen | kubectl apply -f -"
        return self.wrapper.string_execute(cmd)

    def handle_lowsec_pod(self):
        cmd = "gen --all priv-pod | kubectl apply -f -"
        return self.wrapper.string_execute(cmd)

    def cleanup(self):
        pass

    def clean(self):
        self.delete_pod()

    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("buckets")
        self.completer.words.append("help_gen")
        self.completer.words.append("help_dig")
        self.completer.words.append("ls")
        self.completer.words.append("options_dig")
        self.completer.words.append("options_gen")
        self.completer.words.append("delete_pod")
        self.completer.words.append("gen_priv_pod")
        self.completer.words.append("gen_simple_pod")
        self.completer.words.append("dig_all")
        self.completer.words.append("dig")
        self.completer.words.append("gen")
        self.completer.words.append("gen")


    def add_corrections(self):
        self.corrections["dig_lal"] = "dig_all"

    def exec_into_pod_and_install(self):
        print("# Executing into the pod to install Kdigger...")
        # Command to install kdigger inside the Ubuntu pod
        commands = f"""
            apt-get update && apt-get install -y curl tar && \
            curl -fSL "{self.DOWNLOAD_URL}" -o "{self.DOWNLOAD_DIR}/kdigger.tar.gz" && \
            tar xvzf "{self.DOWNLOAD_DIR}/kdigger.tar.gz" -C "{self.DOWNLOAD_DIR}" && \
            mv "{self.DOWNLOAD_DIR}/kdigger-linux-{self.PLATFORM}" "{self.INSTALL_DIR}/kdigger" && \
            chmod +x "{self.INSTALL_DIR}/kdigger"
        """

        # Execute the command in the pod
        subprocess.run(["kubectl", "exec", "-it", self.pod_name, "--", "bash", "-c", commands], check=True)