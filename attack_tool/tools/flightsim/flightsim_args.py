from tools.flightsim.FlightsimEnv import FlightsimEnv
from tools.flightsim.FlightsimWrapper import FlightsimWrapper
from tools.base_classes.args_base import Args

from environment.global_const import GlobalVariables

from tools.base_classes.pod_deployment import DeployInPod
import help.helper as helper
import subprocess


class FlightsimArgs(DeployInPod, Args):

    def __init__(self, priv_container=False, sa_account="default"):
        super().__init__()
        self.global_var = GlobalVariables.get_instance()
        self.local_env = FlightsimEnv()
        self.flightsim_wrapper = FlightsimWrapper(self.local_env)
        self.row = [
            ["run --help", "View the help menu for the run command"],
            ["run [--dry|--fast]", "Run all modules"],
            ["run [--dry|--fast] <module>", "Run module of choice"],
            ["list", "List available c2 families"],
            ["run c2:<family>", "Run c2 module emulating specific c2-framework"],
            ["<module>", "Following modules are available:\n" +
              "\t\t\t\tc2, dga, imposter, miner, scan, sink, spambot,\n" + 
              "\t\t\t\tssh-exfil, ssh-transfer, tunnel-dns, tunnel-icmp"],
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
       
    def handle_args(self, args, param = None):

        if param:
            for param_value in param:
                # Each param_value would look like "key=value"
                param, value = param_value.split("=", 1)
                
                if param == "list":
                    self.local_env.set_ip(value)
                if param == "subnet":
                    self.local_env.set_subnet(value)
                if param == "type":
                    self.local_env.set_type(value)
                if param == "access_scope":
                    self.local_env.set_access_scope(value)
                if param == "resource_path":
                    self.local_env.set_resource_path(value)
                if param == "resource":
                    self.local_env.set_resource(value)
                if param == "base_path":
                    self.local_env.set_base_path(value)
                if param == "revshell_port":
                    self.local_env.set_revshell_port(value)
                if param == "revshell_ip": 
                    self.local_env.set_revshell_ip(value)
                
        try:
            if args == "run c2":
                # Show help information
                self.table.print_table(self.column, self.row)
                self.parse_output = False
                return
            elif args == "options":
                # Show help information
                self.table.print_table(self.column, self.local_env.get_env_dict())
                self.parse_output = False
                return
            elif args == "help":
                # Show help information
                self.table.print_table(self.column,self.row)
                self.parse_output = False
                return
            elif args == "list":
                # Show help information
                if self.global_var.get_env().get_pod_deployment():
                    self.out = self.flightsim_wrapper.exec_command_on_pod(self.flightsim_wrapper.list())
                else:
                    self.out = self.flightsim_wrapper._execute_command(self.flightsim_wrapper.list())
                self.parse_output = False
                return
            else:
                try:    
                    if self.global_var.get_env().get_pod_deployment():   
                        cmd = "flightsim " + args
                        self.out = self.flightsim_wrapper.exec_command_on_pod(cmd)   
                    else:
                        self.out = self.flightsim_wrapper.custom_scan(args)
                    if args == "run --help":
                        self.parse_output = False
                        return
                    else:
                        self.parse_output = True
                except Exception as e:
                    print(e)
                    return None, None, None, False
        except Exception as e:
            print(e)
            if self.global_var.get_env().get_pod_deployment(): 
                print("# Cleanup")           
                if self.sa_account == "evil-admin":
                    print("# Cleanup")
                    helper.delete_service_account_and_binding()

                self.delete_pod()

            return None, None, None, False
        
        
        if self.global_var.get_env().get_pod_deployment(): 
            print("# Cleanup")           
            if self.sa_account == "evil-admin":
                print("# Cleanup")
                helper.delete_service_account_and_binding()

            self.delete_pod()


        return self.out, self.flightsim_wrapper.final_command, self.local_env, self.parse_output


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