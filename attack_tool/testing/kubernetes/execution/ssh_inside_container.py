from testing.testing import Testing
import subprocess
import time

class SSHServerContainer(Testing):
    def __init__(self):
        super().__init__()
        self.name = "SSH-Server running in inside Container"
        self.mitre_tactic = "TA0002"
        self.mitre_technique = "T1569.002"
        self.microsoft_technique = "MS-TA9010"
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "openssh-server"
            },
            "spec": {
                "containers": [
                    {
                        "image": "linuxserver/openssh-server:latest",
                        "name": "openssh-server",
                        "env": [
                            {
                                "name": "SUDO_ACCESS",
                                "value": "true"
                            },
                            {
                                "name": "PASSWORD_ACCESS",
                                "value": "true"
                            },
                            {
                                "name": "USER_NAME",
                                "value": "eviluser"
                            },
                            {
                                "name": "USER_PASSWORD",
                                "value": "dontDoThisInProd!"
                            }
                        ],
                        "ports": [ 
                            {
                                "containerPort": 2222
                            }
                        ]
                    }
                ]
            }
        }
        self.pod_yaml = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "ssh-lateral-movement-pod",
            },
            "spec": {
                "serviceAccountName": "default",  # Add the service account here
                "containers": [
                    {
                        "name": "python-container",
                        "image": "python:3.9-slim",
                        "command": ["/bin/bash", "-c", "sleep 10000"],
                        "securityContext": {
                            "privileged": True
                        }
                    }
                ]
            }
        }
                        
        
    def run_attack(self):
        if self.check_install_kubectl():
            # Creating Pod openssh-server
            print("# Creating Pod openssh-server...")
            self.kubectl_create_file("openssh-server.yaml", self.pod)
            self.kubectl_apply("openssh-server.yaml")

            print("# Creating Pod openssh-server...")
            self.kubectl_create_file("ssh-lateral-movement.yaml", self.pod_yaml)
            self.kubectl_apply("ssh-lateral-movement.yaml")


            while not self.kubectl_is_pod_ready("openssh-server"):
                    time.sleep(1)
                
            
            while not self.kubectl_is_pod_ready("ssh-lateral-movement-pod"):
                    time.sleep(1)
            
            self.cmd = ["kubectl", "get", "pod", "openssh-server", "-o=jsonpath='{.status.podIP}'"]
            
            # Getting Pod IP
            print("\n# Getting Pod IP...")
            output_ip, error1 = self.kubectl_run()
            ip = output_ip.strip("'")
            print("Pod IP:", ip)


            # Install SSH client and Paramiko inside the pod
            print("# Installing SSH client and Paramiko on ssh-lateral-movement-pod...")
            install_output = self.install_ssh_and_paramiko("ssh-lateral-movement-pod", "default")
            print(install_output)

            print("\n# Executing command 'whoami' in the source container...")   
            print("eviluser@ssh-lateral-movement-pod:/# whoami")   
            subprocess.run(["kubectl", "exec", "-it", "ssh-lateral-movement-pod", "--", "bash", "-c", 'whoami'], check=True)
            
            # Now SSH into the OpenSSH server pod using Paramiko
            print(f"\n# Connecting via SSH to {ip}...")
    
    
    
            # Generate the script
            script = self.generate_paramiko_script(ip, 2222, "eviluser", "dontDoThisInProd!")
            # Pod and destination details
            pod_name = "ssh-lateral-movement-pod"
            container_name = "python-container"  # Update if needed
            destination_path = "/tmp/paramiko_script.py"

            # Copy the script to the pod
            self.copy_script_to_pod(script, pod_name, container_name, destination_path)
            
            # Step 2: Execute the script inside the pod
            error = self.execute_script_in_pod(pod_name, container_name, destination_path)


            if not error:
                print("An Error has occured while establishing SSH Connection... " )
            else:
                self.output["get_pod_id"] = ip
                self.output["lateral_movement_pod_whoami"] = "root"
                self.output["ssh_into_container_whoami"] = "eviluser"

            # Cleanup
            self.cleanup()

    def cleanup(self):
        # Delete Pod openssh-server
        print("\n# Deleting Pod openssh-server...")
        self.kubectl_delete("openssh-server")
        
        print("\n# Deleting openssh-server.yaml...")
        self.delete_file("openssh-server.yaml")
        
        print("\n# Deleting Pod ssh-lateral-movement-pod...")
        self.kubectl_delete("ssh-lateral-movement-pod")
        
        print("\n# Deleting ssh-lateral-movement.yaml...")
        self.delete_file("ssh-lateral-movement.yaml")


    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass
    
    
    def execute_command(self, command):
        try:
            """Executes a shell command and returns the output."""
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
            
        except Exception as e:
            print (e)
            return None



    def install_ssh_and_paramiko(self, pod_name, namespace):
        """Install SSH client and paramiko library on the given pod."""
        try:
                        
            subprocess.run(["kubectl", "exec", "-it", pod_name, "--", "bash", "-c", 'pip3 install paramiko'], check=True)
        
        except Exception as e:
            print (e)
            return None


    def generate_paramiko_script(self, target_pod_ip, target_port, ssh_user, ssh_password):
        script_template = """
import paramiko
import time

def ssh_connect_and_execute(target_pod_ip, target_port, ssh_user, ssh_password):
    print(f"Connecting to {{target_pod_ip}} via SSH...")
    
    # Initialize the SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the target pod
        client.connect(target_pod_ip, port=target_port, username=ssh_user, password=ssh_password)
        
        # Example command to run on the target pod (you can modify this)
        command = "whoami"  # Replace with your desired command
        stdin, stdout, stderr = client.exec_command(command)
        
        output = stdout.read().decode("utf-8").strip()
        print("eviluser@ssh-lateral-movement-pod:/# whoami")   
        print(output)
        
        # Optionally, you can wait for the command to complete
        time.sleep(2)

    except Exception as e:
        print(f"SSH connection failed: {{e}}")
    finally:
        client.close()

if __name__ == "__main__":
    # Call the SSH connect function with dynamic parameters
    ssh_connect_and_execute("{target_pod_ip}", {target_port}, "{ssh_user}", "{ssh_password}")
"""
        # Format the script with the provided parameters
        formatted_script = script_template.format(
            target_pod_ip=target_pod_ip,
            target_port=target_port,
            ssh_user=ssh_user,
            ssh_password=ssh_password
        )
        return formatted_script


    def copy_script_to_pod(self, script_content, pod_name, container_name, destination_path):
        script_file = "paramiko_script.py"  # Temporary file to store the script
        try:
            # Write the script content to a temporary file
            with open(script_file, "w") as f:
                f.write(script_content)
            
            # Use kubectl cp to copy the file to the pod
            print(f"Copying {script_file} to pod {pod_name}...")
            subprocess.run(
                ["kubectl", "cp", script_file, f"{pod_name}:{destination_path}", "-c", container_name],
                check=True
            )
            print(f"Script successfully copied to {pod_name}:{destination_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to copy the script to the pod: {e}")
        finally:
            # Cleanup the temporary file
            try:
                import os
                os.remove(script_file)
            except OSError as cleanup_error:
                print(f"Error cleaning up temporary script file: {cleanup_error}")


    def execute_script_in_pod(self, pod_name, container_name, script_path):
        try:
            print(f"Executing script {script_path} in pod {pod_name}...\n")
            
            subprocess.run(
                ["kubectl", "exec", pod_name, "-c", container_name, "--", "python3", script_path],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute the script on the pod: {e}")
            return False