import yaml
import subprocess
import time
import json
import os
from abc import ABC, abstractmethod

class DeployInPod(ABC):
    def __init__(self):
        super().__init__()
        self.pod_name=None
        self.pod_yaml=None
        self.VERSION = None
        self.INSTALL_DIR = '/usr/local/bin'
        self.DOWNLOAD_DIR = '/tmp/'
        self.DOWNLOAD_URL = None

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
    
    def is_installed(self, command):
        try:
            subprocess.run(
                ["kubectl", "exec","-it",  self.pod_name, "--", "/bin/bash", "-c",command],
                check=True,
                stdout=subprocess.DEVNULL,  # Suppress standard output
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception as e :
            print("Error")
            print(e)
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

    def delete_file(self,file_path):
        try:
            os.remove(file_path)
            return True
        except OSError as e:
            print(f"Error: {file_path} - {e.strerror}")
            return False


    def delete_file(self,file_path):
        try:
            os.remove(file_path)
            return True
        except OSError as e:
            print(f"Error: {file_path} - {e.strerror}")
            return False

    def kubectl_create_file(self, yaml_name, data):
        with open(yaml_name, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)
             
    def kubectl_apply(self, yaml_file):
        try:
            subprocess.run(["kubectl", "apply", "-f", yaml_file], check=True)
        except Exception as e:
            print(e.args)

    
    def install(self):
        print("# Creating Ubuntu Pod for installation...")
        self.kubectl_create_file(f"{self.pod_name}.yaml", self.pod_yaml)
        self.kubectl_apply(f"{self.pod_name}.yaml")
        self.delete_file(f"{self.pod_name}.yaml")
        print(f"\n# Waiting for {self.pod_name} to be ready...")
        while not self.kubectl_is_pod_ready():
            time.sleep(1)

        print(f"# {self.pod_name} is ready. Executing installation...")
        self.exec_into_pod_and_install()

        print("# Tool has been installed in the pod.")
        



    @abstractmethod
    def exec_into_pod_and_install(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass