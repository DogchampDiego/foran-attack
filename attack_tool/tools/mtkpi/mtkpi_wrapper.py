import subprocess
import time
import docker
import sys
from environment.global_const import GlobalVariables
from tools.base_classes.wrapper_base import Wrapper

class MTKPIWrapper(Wrapper):

    def __init__(self, env):
        self.command = 'kubectl'
        self.sudo = True
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env
        self.pod_name = "mtkpi-pod"

    def start(self):
        print("Starting MTKPI pod...", self.env.get_resource_path())
        cmd = ['apply', '-f', self.env.get_resource_path()]
        return cmd
    
    def clean(self):
        print("Cleaning up MTPKI pod...")
        cmd = ["delete", "pods", "-l", "app=mtkpi"]
        return cmd
    
    def status(self):
        print("Checking status of MTKPI pod...")
        cmd = ["get", "pods", "-l", "app=mtkpi", "-o", "wide"]
        return cmd
    
    def status_verbose(self):
        print("Checking extended status of MTKPI pod...")
        cmd = ["get", "pods", "-l", "app=mtkpi", "-o", "yaml"]
        return cmd
    
    def _is_pod_running(self):
        # Execute 'kubectl get pods' command
        try:
            result = subprocess.run(['sudo', 'kubectl', 'get', 'pods', self.pod_name, '-o', 'jsonpath={.status.phase}'],
                                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # The output will be the status of the pod
            status = result.stdout.strip()
            return status == "Running"
        except subprocess.CalledProcessError as e:
            print("An error occurred: ", e.stderr)
            return False
    
    def exec(self):
        if not self._is_pod_running():
            # Start container and wait for it to be running
            self._execute_command(self.start())   
                 
            # Watch for status
            command = ["watch", "-n", "1", "sudo", "kubectl", "get", "pods", "-l", "app=mtkpi", "-o", "wide"]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

            # Loop through the output line by line
            for line in process.stdout:
                print(line, end="")  # Print output in real-time
                if "Running" in line:
                    process.terminate()
                    break
            process.wait()
       
        # BASH shell in pod command
        kubectl_command = ['sudo', 'kubectl', 'exec', '-it', self.pod_name, '--', 'bash']

        print("Launching bash shell into MTKPI pod...")
        process = subprocess.Popen(kubectl_command, stdout=sys.stdout, stderr=sys.stderr)
        
        # Wait for the process to complete
        process.wait()
        print("Shell execution completed.")
        
        # Delete
        print("Cleaning up MTPKI pod...")
        cmd = ["delete", "pods", "-l", "app=mtkpi"]
        return cmd
    
    def exec_custom(self, cmd):
        if not self._is_pod_running():
            # Start container and wait for it to be running
            self._execute_command(self.start())
        
        while(not self._is_pod_running()):
            time.sleep(0.1)
        
        # TODO Parse cmd argument properly
        #print("Executing command in MTKPI pod - User Input: ", cmd) 
                 
        print("Executing command in MTKPI pod: ", self.env.get_command().split())
        
        cmd = ['exec', self.pod_name, '--', '/bin/sh', '-c', self.env.get_command()]
        return cmd
    
    def start_docker(self):
        # Initialize the Docker client
        client = docker.from_env()

        # Define the Docker image and pod name
        image_name = "mtkpi:latest"

        # Path to the directory containing the Dockerfile
        path_to_dockerfile = self.global_var.get_tool_non_bin_dir() + "mtkpi"

        # Build the image
        image, build_log = client.images.build(path=path_to_dockerfile, tag=image_name)

        # Output the build logs
        for line in build_log:
            if 'stream' in line:
                print(line['stream'].strip())

        # Run a container using the built image
        container = client.containers.run(image_name, detach=True)

        print(f"Running container {container.id} from image ", image_name)
    
    def init_revshell_listener(self, port):
        # Start ncat listener
        ret = subprocess.call(["ncat", "--ssl", "-vnlp", str(port)])
        print("ReverseShell Listener started:\nReturn code: " + str(ret))

    def _generate_command(self, cmd):
        return cmd

