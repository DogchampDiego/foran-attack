import subprocess

import subprocess
import os
import yaml
import json
import paramiko
import textwrap

from abc import ABC, abstractmethod
from database.mongo_db_handler import MongoDBWrapper as db
from environment.global_const import GlobalVariables
from help.helper import get_current_timestamp, detect_hostname, get_ip_address

import help.helper as helper
class Testing(ABC):
    def __init__(self, executor='bash'):
        self.cmd = None
        self.command = []
        self.executor = executor
        self.executable_path = None

        self.global_var = GlobalVariables.get_instance()
        self.db = db(self.global_var.get_base_dir() + "database/config.ini")

        # Database fields
        self.start_date = None
        self.end_date = None
        self.error = False

        # Declare in the child class
        self.name = None
        self.pod = None
        
        # Output
        self.output = {}
        
        # Mapping
        self.mitre_tactic = None
        self.mitre_technique = None
        self.microsoft_technique = None
        
        # Cleanup
        self.docker = None
        self.kubectl = None

    # Kubectl commands
    def kubectl_apply(self, yaml_file, add_command = False):
        if add_command:
            self.command.append(["kubectl", "apply", "-f", yaml_file])
        try:
            subprocess.run(["kubectl", "apply", "-f", yaml_file])
            
        except Exception as e:
            print(e.args)
            self.command.pop()
            self.error = True
            return

    def kubectl_delete(self, name, ressource_type="pod", namespace=None, all=False, add_command = False):
        try:      
            if add_command:
                self.command.append(self.cmd)
            if name == "all" and all: 
                self.cmd = ["kubectl", "delete", name, "--all","--all-namespaces","--grace-period=0","--force"]
            elif name == None and all:
                self.cmd = ["kubectl", "delete", ressource_type,  "--all", "--all-namespaces"]
            elif namespace:
                self.cmd = ["kubectl", "delete", ressource_type, name, "-n", namespace]
            else:
                self.cmd = ["kubectl", "delete", ressource_type, name]

            out = subprocess.run(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  
        except Exception as e:
            self.command.pop()
            self.error = True
            print(e.args)
            return out.stdout, e.args
            
        return out.stdout, out.stderr

    def kubectl_get(self, resource_type, namespace=None, additional_args=None, add_command=False):
            try:
                if add_command:
                    self.command.append(self.cmd)
                if namespace:
                    self.cmd = ["kubectl", "get", resource_type, "-n", namespace ,"-o", "json"]
                elif additional_args:
                    self.cmd = ["kubectl", "get", resource_type, *additional_args ,"-o", "json"]
                else:
                    self.cmd = ["kubectl", "get", resource_type ,"-o", "json"]
                    
                out = subprocess.run(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
            except Exception as e:
                self.command.pop()
                self.error = True
                print(e.args)
                return out.stdout, e.args
                
            return out.stdout, out.stderr

            
    def kubectl_describe(self, resource_type, name):
        try:
            self.command.append(self.cmd)
            self.cmd = ["kubectl", "describe", resource_type, name]
            out = subprocess.run(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            self.command.pop()
            self.error = True
            print(e.args)
            return out.stdout, e.args
         
        return out.stdout, out.stderr


    def kubectl_create_file(self, yaml_name, data):
        with open(yaml_name, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)
             
    def create_file(self, file_name, data):
        with open(file_name, 'w') as file:
            file.write(textwrap.dedent(data))
            
    def kubectl_run(self):
        try:
            self.command.append(self.cmd)
            out =subprocess.run(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            self.command.pop()
            self.error = True
            print(e.args)
        return out.stdout, out.stderr

        
    def kubctl_exec(self, commands=None, shell=1,):
        try:
            if not commands: self.command.append(self.cmd)
            # Open a subprocess with the shell of the container
            if shell==1: p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if shell ==2: p = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if commands:
                for command in commands:
                    p.stdin.write(command)
                    p.stdin.flush()
            output, error = p.communicate()

        except Exception as e:
            self.command.pop()
            self.error = True
            print("Error:", e)
            return output, e.args
            
        return output, error


    def kubectl_exec_command(self, decoding=None, add_command =True):
        if add_command:
            self.command.append(self.cmd)
        try:
            if decoding:
               out = subprocess.run(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
               stdout_decoded = out.stdout.decode('utf-8', errors='replace')
               return stdout_decoded, out.stderr
            else:
                out = subprocess.run(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            self.command.pop()
            self.error = True
            print(e.args)
            return out.stdout, e.args
        
        return out.stdout, out.stderr
            

    def kubectl_is_pod_ready(self, pod_name, namespace=None):
        try:
            # Run kubectl command to get Pod info in JSON format
            if namespace:
                output = subprocess.check_output(["kubectl", "get", "pod", pod_name, "-n", namespace, "-o", "json"])
            else: 
                output = subprocess.check_output(["kubectl", "get", "pod", pod_name, "-o", "json"])
            
            # Parse the JSON output
            pod_info = json.loads(output.decode("utf-8"))
            pod_status = pod_info.get("status", {})
            conditions = pod_status.get("conditions", [])
            for condition in conditions:
                # Check if the Pod is ready
                if condition.get("type") == "Ready" and condition.get("status") == "True":
                    return True
        except subprocess.CalledProcessError as e:
            print("Error:", e)
        
        return False
    
    def kubectl_is_deployment_ready(self, deployment_name):
        try:
            # Run kubectl command to get Deployment info in JSON format
            output = subprocess.check_output(["kubectl", "get", "deployment", deployment_name, "-o", "json"])
            
            # Parse the JSON output
            deployment_info = json.loads(output.decode("utf-8"))
            deployment_status = deployment_info.get("status", {})
            replicas = deployment_status.get("replicas", 0)
            updated_replicas = deployment_status.get("updatedReplicas", 0)
            ready_replicas = deployment_status.get("readyReplicas", 0)
            available_replicas = deployment_status.get("availableReplicas", 0)

            return replicas == updated_replicas == ready_replicas == available_replicas

        except subprocess.CalledProcessError as e:
            print("Error:", e)
        
        return False

    def kubectl_is_cronjob_ready(self, cronjob_name):
        try:
            # Run kubectl command to get CronJob info in JSON format
            output = subprocess.check_output(["kubectl", "get", "cronjob", cronjob_name, "-o", "json"])
            
            # Parse the JSON output
            cronjob_info = json.loads(output.decode("utf-8"))
            status = cronjob_info.get("status", {})
            last_schedule_time = status.get("lastScheduleTime")
            last_successful_time = status.get("lastSuccessfulTime")
            
            # CronJob is considered ready if both lastScheduleTime and lastSuccessfulTime are filled with correct values
            return last_schedule_time is not None and last_successful_time is not None
        except subprocess.CalledProcessError:
            return False
    
    def kubectl_is_daemonset_ready(self, daemonset_name):
        try:
            # Run kubectl command to get DaemonSet info in JSON format
            output = subprocess.check_output(["kubectl", "get", "daemonset", daemonset_name, "-o", "json"])
            daemonset_info = json.loads(output.decode("utf-8"))
            
            # Get DaemonSet status
            daemonset_status = daemonset_info.get("status", {})
            
            # Get the relevant counts
            current = daemonset_status.get("currentNumberScheduled", 0)
            desire = daemonset_status.get("desiredNumberScheduled", 0)
            ready = daemonset_status.get("numberReady", 0)
            up_to_date = daemonset_status.get("updatedNumberScheduled", 0)
            available = daemonset_status.get("numberAvailable", 0)
            
            # Check if all counts are 1
            return current == ready == up_to_date == available == desire == 1
        
        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return False

    def uninstall_kubectl(self):
        try:
            # Uninstall kubectl by removing the kubectl package
            subprocess.run(['sudo', 'apt-get', 'remove', 'kubectl', '-y'], check=True)
            print("kubectl has been successfully uninstalled.")
        except Exception as e:
            print("Failed to uninstall kubectl:", e)


    def check_install_kubectl(self):
        try:
            # Check if kubectl is installed
            subprocess.run(["kubectl", "version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            print("# Kubectl is not installed. Installing...")
            
            # Install kubectl using apt
            try:
                subprocess.run(["sudo", "apt", "update"])
                subprocess.run(["sudo", "apt", "install", "-y", "kubectl"])
                print("kubectl has been installed.")
            except Exception:
                print("Failed to install kubectl.")
                return False
            
            return True
    
    # Docker
    def check_install_docker(self):
        try:
            # Check if Docker is installed by attempting to run a Docker command
            subprocess.run(['docker', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            print("Docker is not installed. Installing...")
            try:
                # Install Docker using the official Docker installation script
                subprocess.run(['curl', '-fsSL', 'https://get.docker.com', '-o', 'get-docker.sh'], check=True)
                subprocess.run(['sudo', 'sh', 'get-docker.sh'], check=True)
                print("Docker has been successfully installed.")
                return True
            except Exception as e:
                print("Failed to install Docker:", e)
                return False

    def uninstall_docker(self):
        try:
            # Uninstall Docker by removing the Docker package
            subprocess.run(['sudo', 'apt-get', 'remove', 'docker-ce', 'docker-ce-cli', 'containerd.io', '-y'], check=True)
            print("Docker has been successfully uninstalled.")
        except subprocess.CalledProcessError as e:
            print("Failed to uninstall Docker:", e)
    
    def delete_file(self,file_path):
        try:
            os.remove(file_path)
            return True
        except OSError as e:
            print(f"Error: {file_path} - {e.strerror}")
            return False

    def ssh_execute_command(self, hostname, port, username, password, command):
        
        # Create SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the server           
            ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
            # Execute command
            stdin, stdout, stderr = ssh_client.exec_command(command)
            
            # Read the output
            output = stdout.read().decode()
            error = stderr.read().decode()

            # Check for errors
            self.command.append(["ssh", f"{username}@{hostname}", command])
            return output.strip(), error
        
        except paramiko.AuthenticationException:
            print("Authentication failed, please check your credentials")
            self.error = True
            return e.args
        except paramiko.SSHException as ssh_err:
            print("Unable to establish SSH connection:", ssh_err)
            self.error = True
            return e.args
        except Exception as e:
            print("An error occurred:", e)
            self.error = True
            return e.args
        finally:
            # Close the SSH connection
            ssh_client.close()
            
    def cat_folder(self, folder):
        try:
            # Define the command
            command = ["sudo","cat", folder]
            out =subprocess.run(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.command.append(command)
        except Exception as e:
            self.command.pop()
            self.error = True
            print(e.args)
        return out.stdout, out.stderr 

  
    
    def database_insert(self):
        # connect
        # mongosh 10.0.0.12 --tls --tlsCertificateKeyFile /etc/ssl/mongodb/foran.pem --tlsCAFile /etc/ssl/mongodb/ca.crt --authenticationMechanism MONGODB-X509 --tlsAllowInvalidHostnames=true
        self.db.connect_db("collection-testing")
        print(self.to_json())
        # insert Testcase into DB
        self.id = self.db.insert_document(self.to_json())
        print("Testcase inserted with id:", self.id)
        self.db.close_connection() 

    def to_json(self):
        return {
            "output": self.output,
            "hostname": detect_hostname(),
            "ip": get_ip_address(),
            "tool_name": self.name,
            "timestamp_start": self.start_date,
            "timestamp_end": self.end_date,
            "yaml": self.pod,
            "command": self.command,
            "mitre": {self.mitre_tactic:[self.mitre_technique,self.microsoft_technique]}

        }
        
    def run_testcase(self, case = None):
        print("-------------------------")
        self.start_date = get_current_timestamp()
        print(self.start_date)
        if case:
            self.run_attack(case)
        else:
            self.run_attack()
        self.end_date = get_current_timestamp()

        if not self.error:
            if not self.global_var.get_lite_version():
                self.database_insert()
            else:
                print("No DB insert due to usage of light version")
        else:
            print(f"An error occurred Testcase: , {self.name} will not be written into the DB!")
        
    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def display_help(self):
        pass

    @abstractmethod
    def check_prerequisites(self):
        pass

    @abstractmethod
    def determine_executable_path(self):
        pass

    @abstractmethod
    def run_attack(self):
        pass 
