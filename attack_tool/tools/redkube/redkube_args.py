from tools.redkube.redkube_wrapper import RedKubeWrapper
from tools.redkube.redkube_env import RedKubeEnv
from help.table import Table
from tools.base_classes.args_base import Args
import yaml, json, time
from tools.redkube.json_modifier import JSONModifier

import subprocess
import os
from environment.global_const import GlobalVariables

class RedKubeArgs(Args):

    def __init__(self):
        super().__init__()
        self.local_env = RedKubeEnv()
        self.global_var = GlobalVariables.get_instance()
        self.redkube_wrapper = RedKubeWrapper(self.local_env)
        self.row = [
            ["privilege_escalation",  "Run kubectl commands to find privilege escalation weaknesses"],
            ["discovery",  "Run kubectl commands to find discovery weaknesses"],
            ["command_and_control",  "Run kubectl commands to find command and control weaknesses"],
            ["credential_access",  "Run kubectl commands to find credential access weaknesses"],
            ["persistence",  "Run kubectl commands to find persistence weaknesses"],
            ["defense_evasion",  "Run kubectl commands to find defense evasion weaknesses"],
            ["reconnaissance",  "Run kubectl commands to find reconnaissance weaknesses"]
        ]
        self.jsonm = JSONModifier(self.local_env.get_pod_name(),
                                  self.local_env.get_namespace(),
                                  self.local_env.get_api_server(), 
                                  self.local_env.get_token())

        # Define the path to the JSON file
        self.path_persistence = self.global_var.get_tool_non_bin_dir()+ "red-kube/attacks/persistence.json"
        self.path_credential_access = self.global_var.get_tool_non_bin_dir()+ "red-kube/attacks/credential_access.json"
        self.path_command_and_control = self.global_var.get_tool_non_bin_dir()+ "red-kube/attacks/command_and_control.json"
        self.path_reconnaissance = self.global_var.get_tool_non_bin_dir()+ "red-kube/attacks/reconnaissance.json"

        self.pod_name = "redkube-pod"
        self.pod_yaml = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": self.pod_name,
            },
            "spec": {
                "automountServiceAccountToken": True,  # Automatically mount the service account token
                "containers": [
                    {
                        "image": "ubuntu:latest",
                        "name": "exec-command-container",
                        "command": ["/bin/bash", "-c"],
                        "args": [
                            "apt-get update && apt-get install -y curl && sleep infinity"
                        ]
                    }
                ]
            }
        }
        # Remove an entry from the JSON file which are cloud
        try:
            try:
                self.jsonm.remove_entry(self.path_reconnaissance, "id", "rk-re02")
                print("Testcase rk-re02 fixed.")
            except Exception:
                print("Testcase rk-re02 was already fixed.")

            try:
                self.jsonm.remove_entry(self.path_persistence, "id", "rk-pr01")
                print("Testcase rk-pr01 fixed.")
            except Exception:
                print("Testcase rk-pr01 was already fixed.")

            try:
                self.jsonm.remove_entry(self.path_credential_access, "id", "rk-ca07")
                print("Testcase rk-ca07 fixed.")
            except Exception:
                print("Testcase rk-ca07 was already fixed.")

            try:
                self.jsonm.remove_entry(self.path_credential_access, "id", "rk-ca08")
                print("Testcase rk-ca08 fixed.")
            except Exception:
                print("Testcase rk-ca08 was already fixed.")

            try:
                self.jsonm.remove_entry(self.path_command_and_control, "id", "rk-cnc02")
                print("Testcase rk-cnc02 fixed.")
            except Exception:
                print("Testcase rk-cnc02 was already fixed.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")



        self.kubectl_create_file(f"{self.pod_name}.yaml", self.pod_yaml)
        self.kubectl_apply(f"{self.pod_name}.yaml")
        self.delete_file(f"{self.pod_name}.yaml")

        print(f"\n# Waiting for {self.pod_name} to be ready...")
        while not self.kubectl_is_pod_ready():
            time.sleep(1)

        
        self.local_env.set_token(self.get_service_account_token())
    def handle_args(self, args, param = None):

        # Split and clean the input
        if param:
             for param_value in param:
                # Each param_value would look like "key=value"
                param, value = param_value.split("=", 1)

                if param == "mode": 
                    self.local_env.set_mode(value)
                if param == "api_server": 
                    self.local_env.set_api_server(value)

        # Handle the input

        try:
            if args == "privilege_escalation":
                self.out = self.redkube_wrapper.run_attack("privilege_escalation")
            elif args == "discovery":
                self.out = self.redkube_wrapper.run_attack("discovery")
            elif args == "command_and_control":
                if self.local_env.get_pod_name() == None or self.local_env.get_namespace() == None:
                    # Logic for command and control attack
                    print("Set POD_NAME and NAMESPACE to use command_and_control in redkube")
                    # Add actual implementation here
                    return ""
                else:
                    self.local_env.set_mode("active")
                    self.jsonm.update(
                        self.local_env.get_pod_name(),
                        self.local_env.get_namespace())
                    
                self.jsonm.update_json_with_class_vars(self.path_command_and_control)
                self.out = self.redkube_wrapper.run_attack("command_and_control")
                self.local_env.set_mode("passive")
                
            elif args == "credential_access":
                if self.local_env.get_pod_name() == None or self.local_env.get_namespace() == None  or self.local_env.get_api_server() == None:
                    if self.local_env.get_mode()=="active" or self.local_env.get_mode()=="all":
                        print("Set API_SERVER to use credential_access active mode in redkube")
                    else:
                        print("Set API_SERVER to use credential_access in redkube")
                    # Add actual implementation here
                    return None, None, None, False
                else:
                    self.jsonm.update(self.local_env.get_pod_name(),
                                    self.local_env.get_namespace(),
                                    self.local_env.get_api_server(),
                                    self.local_env.get_token())
                    self.jsonm.update_json_with_class_vars(self.path_credential_access)  
                self.out = self.redkube_wrapper.run_attack("credential_access")
            elif args == "persistence":
                self.out = self.redkube_wrapper.run_attack("persistence")   
            elif args == "defense_evasion":
                self.out = self.redkube_wrapper.run_attack("defense_evasion")
            elif args == "execution":
                self.out = self.redkube_wrapper.run_attack("execution")
            elif args == "reconnaissance":
                self.redkube_wrapper.run_attack("reconnaissance")
            elif args == "lateral_movement":
                self.out = self.redkube_wrapper.run_attack("lateral_movement")
            elif args == "initial_access":
                self.out = self.redkube_wrapper.run_attack("initial_access")
            elif args == "help":
                self.out = self.table.print_table(self.column, self.row)
                return
            elif args == "options":
                self.table.print_table(self.column, self.local_env.get_env_dict())
                return 
            else:
                return None, None, None, False
        except Exception as e:
            print(e)
            return None, None, None, False

        return self.out, self.redkube_wrapper.final_command, self.local_env, self.parse_output
    
    def kubectl_create_file(self, yaml_name, data):
        with open(yaml_name, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)
             
    def kubectl_apply(self, yaml_file):
        try:
            subprocess.run(["kubectl", "apply", "-f", yaml_file], check=True)
        except Exception as e:
            print(e.args)

    def kubectl_is_pod_ready(self, namespace=None):
        try:
            # Run kubectl command to get Pod info in JSON format
            if namespace:
                output = subprocess.check_output(["kubectl", "get", "pod", self.pod_name,"-n", namespace, "-o", "json"])
            else: 
                output = subprocess.check_output(["kubectl", "get", "pod", self.pod_name, "-o", "json"])
            
            # Parse the JSON output
            pod_info = json.loads(output.decode("utf-8"))
            pod_status = pod_info.get("status", {})
            conditions = pod_status.get("conditions", [])
            for condition in conditions:
                # Check if the Pod is ready
                if condition.get("type") == "Ready" and condition.get("status") == "True":
                    return True
        except subprocess.CalledProcessError as e:    
            return False
    
    def delete_pod(self):
        if self.pod_name and self.kubectl_is_pod_ready():
            print(f"\n# Deleting Pod {self.pod_name}...")
            try:
                subprocess.run(["kubectl", "delete", "pod", self.pod_name], check=True)
                print(f"# Pod {self.pod_name} has been deleted.")
            except subprocess.CalledProcessError as e:
                print(f"Error deleting pod: {e}")
        else:
            print("No pod name specified to delete.")

        return ""

    def get_service_account_token(self):

        try:
            # Run the kubectl exec command to get the service account token
            command = [
                "kubectl", "exec", "-it", "redkube-pod", "-n", "default",
                "--", "/bin/sh", "-c", "cat /var/run/secrets/kubernetes.io/serviceaccount/token"
            ]
            # Execute the command and capture the output
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Check if the command was successful
            if result.returncode == 0:
                # Return the token
                return result.stdout.strip()  # Strip any surrounding whitespace/newlines
            else:
                # If there's an error, print the error message and raise an exception
                print(f"Error executing command: {result.stderr}")
                raise Exception("Failed to retrieve the service account token")
        
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return None


    def delete_file(self,file_path):
        try:
            os.remove(file_path)
            return True
        except OSError as e:
            print(f"Error: {file_path} - {e.strerror}")
            return False


        
    def check_pod_exists(self, pod_name, namespace='default'):
        try:
            # Run the kubectl command to check if the pod exists
            result = subprocess.run(
                ["kubectl", "get", "pod", pod_name, "-n", namespace],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Check if the pod was found (exit code 0 means success)
            if result.returncode == 0:
                return True
            else:
                return False

        except Exception as e:
            print(f"An error occurred: {e}")
            return False