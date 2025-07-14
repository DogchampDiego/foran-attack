
from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv
from environment.global_const import GlobalVariables

class MTKPIEnv(LocalEnv):
                        
    def __init__(self):
        super().__init__()
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._base_path = GlobalVariables.get_instance().get_tool_non_bin_dir() + "mtkpi/"
        self._resource_path = ""
        self._command = "whoami"
        self._revshell_port = 3000
        self._revshell_ip = GlobalVariables.get_instance().get_master_host()
    
    # Getter and Setter for local_ip
    def get_ip(self):
        return self._ip
    
    def set_ip(self, value):
        self._ip = value
        
    # Getter and Setter for subnet
    def get_subnet(self):
        return self._subnet
    
    def set_subnet(self, value):
        self._subnet = value
    
    # Getter and Setter for resource_path
    def get_resource_path(self):
        self.set_resource_path()
        return self._resource_path
    
    def set_resource_path(self):
        self._resource_path =  self.get_base_path() + "deploy/mtkpi.yaml"
    
    # Getter and Setter for base path
    def get_base_path(self):
        return self._base_path

    def set_base_path(self, path):
        self._base_path = path
    
    # Getter and Setter for command
    def get_command(self):
        return self._command
    
    def set_command(self, value):
        self._command = value
    
        # Getter and Setter for revshell_port
    def get_revshell_port(self):
        return self._revshell_port
    
    def set_revshell_port(self, value):
        self._revshell_port = value
        
    # Getter and Setter for revshell_ip
    def get_revshell_ip(self):
        return self._revshell_ip
    
    def set_revshell_ip(self, value):
        self._revshell_ip = value
    
    def get_env_dict(self):
        ret = [
            ["ip", self.get_ip()],
            ["subnet",  self.get_subnet()],
            ["resource_path", self.get_resource_path()],
            ["command", self.get_command()],
            ["revshell_port", self.get_revshell_port()],
            ["revshell_ip", self.get_revshell_ip()]
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "resource_path", "command", "revshell_port", "revshell_ip"]
        res = variable
        if res in options:
            res = "_" + res
        return res
    
    