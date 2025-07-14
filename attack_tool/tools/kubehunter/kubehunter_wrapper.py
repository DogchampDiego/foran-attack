from tools.base_classes.wrapper_base import Wrapper
from environment.global_const import GlobalVariables
import subprocess
import time

class KubeHunterWrapper(Wrapper):
    def __init__(self,env):
        self.command = 'kube-hunter'
        self.sudo = False
        self.global_env = GlobalVariables.get_instance().get_env()
        self.global_var = GlobalVariables.get_instance()
        self.env = env
        self.pod_name = None

    # Info
    def help(self):
        cmd = ['--help']
        return self._execute_command(cmd,False)
        
    def list(self):
        cmd = ['--list']
        return self._execute_command(cmd,False)
    
    # Scans
    def remote_scan(self):
        cmd = ['--remote']
        return self._execute_command(self._build_command(cmd,local_ip=True,log_level=True,active_mode=True,quick=True,report=True,mapping=True),False)
    
    def deploy_pod(self):
        return self._create_pod()
    
    def info_pod(self):
        if self._name_pod() is not None:
            cmd =['kubectl', 'logs', self._name_pod()]
            return self._execute_command(cmd=cmd,sudo=False, command=False)
        else:
            print("No pod deployed")
            return None
        
    def scan_pod(self):
        out = self.deploy_pod()
        print(out)
        self.out = self.info_pod()
        GlobalVariables.get_instance().get_env().set_pod_deployment(True)
        self.delete_pod()    
        GlobalVariables.get_instance().get_env().set_pod_deployment(False)
            

    def delete_pod(self):
        cmd =['kubectl', 'delete', 'job', 'kube-hunter']
        self.pod_name = None
        return self._execute_command(cmd=cmd,sudo=False, command=False)

    def cidr_scan(self):
        cmd = ['--cidr']
        return self._execute_command(self._build_command(cmd,local_ip=True,log_level=True,active_mode=True,quick=True,report=True,mapping=True,subnet=True),False)
    
    def interface_scan(self):
        cmd = ['--interface']
        return self._execute_command(self._build_command(cmd,log_level=True,active_mode=True,quick=True,report=True,mapping=True),False)
    
    def pod_scan(self):
        cmd = ['--pod']
        return self._execute_command(self._build_command(cmd,log_level=True,report=True,active_mode=True,quick=True,mapping=True),False)
    
    # Helper
    def _build_command(self,cmd ,local_ip=False,log_level=False,active_mode=False,quick=False,report=False,mapping=False,statistics=False,subnet=False):
        if local_ip:
            if self.env.get_ip():
                if cmd[0] == "--remote":
                    ips = self.env.get_ip().split(",")
                    cmd.extend(ips)
                elif len(self.env.get_ip().split(",")) == 1:  
                    if cmd[0] == "--cidr":
                        cmd.extend([(self.env.get_ip() +  self.env.get_subnet())])
    
                    else:
                        print("Error: You can only scan one IP with this command")
                        return ['--help']                    
                else:
                    cmd.append(self.env.get_ip())
        if log_level:         
            if self.env.get_log_level() in ["info","warn","debug"]:
                cmd.extend(['--log', self.env.get_log_level])
        if active_mode:
            if self.env.get_active_mode():
                cmd.append("--active")
        if quick:
            if self.env.get_quick():
                cmd.append("--quick")
        if report:
            if self.env.get_report() in ["json", "yaml", "plain","stdout"]:
                cmd.extend(["--report",self.env.get_report()])
        if mapping:
            if self.env.get_mapping():
                cmd.append("--mapping")   
        if statistics:
            if self.env.get_statistics():
                cmd.append("--statistics")
        if subnet:
            if self.env.get_subnet():
                cmd.append("--statistics")
        return cmd
    
    def _create_pod(self):
        try:
            # Create Pod
            print(self.global_var.get_base_dir())
            out = self._execute_command_without_output(cmd=['kubectl','create','-f',self.global_var.get_base_dir() +'tools/kubehunter/job.yaml'],sudo=False, command=False)
            print("# Waiting until pod is created")
            while not self.check_job_completion("kube-hunter"):
                time.sleep(1)
                    
            return out

        except subprocess.CalledProcessError as e:
            # Handle any errors from the kubectl command
            print(f"Error executing command: {e}")

    def _name_pod(self):
        try:
            # Get Name of Pod
            result = self._execute_command_without_output(cmd=['kubectl','get','pods','-n','default','--selector=job-name=kube-hunter','-o','jsonpath={.items[0].metadata.name}'],sudo=False, command=False)
            return result.captured_output

        except subprocess.CalledProcessError as e:
            # Handle any errors from the kubectl command
            print(f"Error executing command: {e}")
            
            
    def check_job_completion(self, job_name, namespace="default"):
        # Run kubectl command to get job details in the specified namespace
        get_job_cmd = [
            "kubectl", "get", "job", job_name, 
            "--namespace", namespace, 
            "-o", "jsonpath={.status.succeeded}"
        ]
        
        try:
            # Execute the kubectl command
            result = subprocess.run(get_job_cmd, capture_output=True, text=True, check=True)
            
            # Parse the result
            completed = result.stdout.strip()

            # Check if completions is 1 (i.e., the job succeeded once)
            if completed == '1':
                print(f"Job '{job_name}' has completed successfully (1/1).")
                return True
            else:
                print(f"Job '{job_name}' has not yet completed successfully.")
                return False

        except subprocess.CalledProcessError as e:
            print(f"Error checking job completion: {e}")
            return False
