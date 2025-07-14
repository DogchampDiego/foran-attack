from tools.kdigger.kdigger_wrapper import KdiggerWrapper
from tools.kdigger.kdigger_env import KDiggerEnv
from tools.base_classes.args_base import Args

from tools.base_classes.pod_deployment import DeployInPod

import subprocess
from environment.global_const import GlobalVariables
import help.helper as helper

class kdiggerArgs(DeployInPod, Args):

    def __init__(self, priv_container=False, sa_account="default"):
        super().__init__()
        self.global_var = GlobalVariables.get_instance()
        self.local_env = KDiggerEnv()
        self.kdigger_wrapper = KdiggerWrapper(self.local_env)
        self.row = [
            ["buckets", "See all buckets to dig"],
            ["options_dig",  "Dig with given options"],
            ["dig",  "Dig with given options"],
            ["dig_all",  "Dig with given options"],
            ["gen_simple_pod","Create a very simple pod"],
            ["gen_priv_pod","Create a pod named mypod with most security features disabled"],
            ["delete_pod", "deletes the pod, where kdigger is running on"]
        ]
        self.sa_account = sa_account
        if sa_account == "evil-admin":
            helper.create_service_account_and_binding()
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
                "serviceAccountName": sa_account,  # Add the service account here
                "containers": [
                    {
                        "name": "ubuntu-container",
                        "image": "ubuntu:latest",
                        "command": ["/bin/bash", "-c", "sleep 10000"],
                        "securityContext": {
                            "privileged": bool(priv_container)
                        }
                    }
                ]
            }
        }

        # Kdigger installation variables
        self.VERSION = 'v1.5.0'
        self.PLATFORM = 'amd64'
        self.DOWNLOAD_URL = f'https://github.com/quarkslab/kdigger/releases/download/{self.VERSION}/kdigger-linux-{self.PLATFORM}.tar.gz'
        if not self.kubectl_is_pod_ready() and not self.is_installed("kdigger --help"):
            self.install()

        if not self.is_installed("kdigger --help"):
            self.exec_into_pod_and_install()
            self.local_env.set_pod_name(self.pod_name)
            self.local_env.set_pod_yaml(self.pod_yaml)
            self.cleanup()
            
    def handle_args(self, args, param = None):

        if param:
            for param_value in param:
                # Each param_value would look like "key=value"
                param, value = param_value.split("=", 1)

                if param == "kubeconfig" : 
                    self.local_env.set_kubeconfig(value)
                if param == "side_effects" : 
                    self.local_env._side_effects(value)
                if param == "buckets": 
                    self.local_env.set_buckets(value)

        # Handle the input
        try:
            if args == "buckets":
                self.out = self.kdigger_wrapper.show_buckets()  # Assuming a method that lists buckets
                self.parse_output = False
                return
            elif args == "options_dig":
                header = ["Parameter","Value"]
                self.table.print_table(header,self.local_env.get_env_dict_dig())
                self.parse_output = False
                return
            elif args == "dig":
                self.out = self.kdigger_wrapper.dig()  # Assuming a method for digging
                self.parse_output = True
            elif args == "dig_all":
                self.out = self.kdigger_wrapper.dig_all()  # Assuming a method for digging
                self.parse_output = True
            elif args == "gen_simple_pod":
                self.out = self.kdigger_wrapper.create_simple_pod()  # Assuming a method for simple pod creation
                self.parse_output = True
            elif args == "gen_priv_pod":
                self.out = self.kdigger_wrapper.create_priv_pod()  # Assuming a method for privileged pod creation
                self.parse_output = True
            elif args == "help":
                self.table.print_table(self.column, self.row)
                self.parse_output = False
                return
            elif args == "options":
                self.table.print_table(self.column, self.local_env.get_env_dict())
                self.parse_output = False
                return 
            else:
                return None, None, None, False
        except Exception as e:
            print(e)
            return None, None, None, False

        if self.global_var.get_env().get_pod_deployment(): 
            print("# Cleanup")           
            if self.sa_account == "evil-admin":
                print("# Cleanup")
                helper.delete_service_account_and_binding()

            self.delete_pod()

        return self.out, self.kdigger_wrapper.final_command, self.local_env, self.parse_output
    

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

        
    def cleanup(self):
        self.delete_file(self.global_var.get_base_dir() + f"{self.pod_name}.yaml")