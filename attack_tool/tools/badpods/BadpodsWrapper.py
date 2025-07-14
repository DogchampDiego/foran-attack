import subprocess
from environment.global_const import GlobalVariables
from tools.base_classes.wrapper_base import Wrapper

class BadpodsWrapper(Wrapper):

    def __init__(self, env):
        self.command = 'kubectl'
        self.sudo = False
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env

    def launch(self):
        if self.env.get_type() == "revshell":
            resource = self.env.get_resource_path()
            deploy_path = "/tmp/revshell-resource.yaml"
            
            with open(resource, 'r') as file:
                resource_content = file.read()
            
            env_vars = {
                'HOST': str(self.env.get_revshell_ip()),
                'PORT': str(self.env.get_revshell_port()),
            }

            # Call envsubst and provide the file's content as input
            result = subprocess.run('envsubst', input=resource_content, text=True, capture_output=True, env=env_vars)
            updated_resource = result.stdout
            
            # TODO update database entry to reflect old revshell port -1
            # Increment revshell port
            self.env.set_revshell_port(self.env.get_revshell_port() + 1)

            resource_handle = open(deploy_path, "w+")
            resource_handle.write(updated_resource)
            resource_handle.close()   
            
            # TODO overwrite "back" command and delete yaml file
            cmd = ['apply', '-f', deploy_path]
        else:
            cmd = ['apply', '-f', self.env.get_resource_path()]
        return cmd
    
    def launch_custom(self, type, access_scope, resource):
        self.env.set_type(type)
        self.env.set_access_scope(access_scope)
        self.env.set_resource(resource)
        return self.launch()
    
    def status(self):
        print("Checking status of BadPods pod...")
        cmd = ["get", "pods", "-l", "app=pentest", "-o", "wide"]
        return cmd
    
    def status_verbose(self):
        print("Checking extended status of BadPods pod...")
        cmd = ["get", "pods", "-l", "app=pentest", "-o", "yaml"]
        return cmd
    
    # TODO Finish a clean method and specific clean method
    def clean(self):
        print("Cleaning up all BadPods...")
        cmd = ["delete", "pods", "-l", "app=pentest"]
        return cmd

    def _generate_command(self, cmd):
        return cmd

