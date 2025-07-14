
from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv
from environment.global_const import GlobalVariables

class BadpodsEnv(LocalEnv):
     
    type_list = ['exec', 'revshell']
    access_scope_list = ['everything-allowed', 'priv-and-hostpid', 'priv', 'hostpath', 'hostpid', 'hostnetwork', 'hostipc', 'nothing-allowed'] 
    resoure_list = ['pod', 'cronjob', 'deamonset', 'deployment', 'job', 'replicaset', 'replicationcontroller', 'statefulset']
                        
    def __init__(self):
        super().__init__()
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._type = "exec"
        self._access_scope = "everything-allowed"
        self._resource = "pod"
        self._base_path = GlobalVariables.get_instance().get_tool_non_bin_dir() + "badpods"
        self._resource_path = ""
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
        
    # Getter and Setter for type
    def get_type(self):
        return self._type
    
    def set_type(self, value):
        if value in self.type_list:
            self._type = value
        else:
            print("Invalid type. Valid types are: " + str(self.type_list))
    
    # Getter and Setter for access_scope
    def get_access_scope(self):
        return self._access_scope
    
    def set_access_scope(self, value):
        if value in self.access_scope_list:
            self._access_scope = value
    
    # Getter and Setter for resource
    def get_resource(self):
        return self._resource
    
    def set_resource(self, value):
        if value in self.resoure_list:
            self._resource = value
    
    # Getter and Setter for resource_path
    def get_resource_path(self):
        self.set_resource_path()
        return self._resource_path
    
    def set_resource_path(self):
        self._resource_path =  self.get_base_path() + "/manifests/" + self.get_access_scope() + "/" + self.get_resource() + \
                              "/" + self.get_access_scope() + "-" + self.get_type() + "-" + self.get_resource() + ".yaml"
    
    # Getter and Setter for base path
    def get_base_path(self):
        return self._base_path

    def set_base_path(self, path):
        self._base_path = path
            
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
            ["type", self.get_type()],
            ["access_scope", self.get_access_scope()],
            ["resource", self.get_resource()],
            ["resource_path", self.get_resource_path()],
            ["revshell_port", self.get_revshell_port()],
            ["revshell_ip", self.get_revshell_ip()]
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "type", "access_scope", "resource", "resource_path", "revshell_port", "revshell_ip"]
        res = variable
        if res in options:
            res = "_" + res
        return res
    
    