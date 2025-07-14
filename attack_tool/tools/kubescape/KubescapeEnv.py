
from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class KubescapeEnv(LocalEnv):
    
    resource_list = {'', 'cluster', 'namespace', 'workload', 'risk', 'compliance', 'framework'}
    framework_list = {'ac': 'AllControls', 'ab': 'ArmoBest', 'dob': 'DevOpsBest', 'mitre': 'MITRE',
                      'nsa': 'NSA', 'caks': 'cis-aks-t1.2.0', 'ceks': 'cis-eks-t1.2.0', 'cv1': 'cis-v1.23-t1.0.1'}
    format_list = {'pp': 'pretty-printer', 'json': 'json --format-version v2', 'html': 'html',
                   'prom': 'prometheus', 'pdf': 'pdf'}
    log_level_list = ["debug", "info", "success", "warning", "error", "fatal"]
    
    def __init__(self):
        super().__init__()    
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._resource = ""
        self._framework = "mitre"
        self._format = "html"
        self._log_level = None
    
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
        
    # Getter and Setter for resource
    def get_resource(self):
        return self._resource
    
    def set_resource(self, value):
        if value in self.resource_list:
            self._resource = value
        else:
            print("ERROR: Faulty scan resource provided.")
            return
    
    # Getter and Setter for framework
    def get_framework(self):
        return self._framework
    
    def set_framework(self, value):
        if value in self.framework_list:
            self._framework = value
    
    # Getter and Setter for format
    def get_out_format(self):
        return self._format
    
    def set_out_format(self, value):
        if value in self.format_list:
            self._format = value
    
    # Getter and Setter for log_level
    def get_log_level(self):
        return self._log_level
    
    def set_log_level(self, value):
        if value in self.log_level_list:
            self._log_level = value

    def get_env_dict(self):
        ret = [
            ["ip", self.get_ip()],
            ["subnet",  self.get_subnet()],
            ["resource",  self.get_resource()],
            ["framework",  self.get_framework()],           
            ["log_level", self.get_log_level()],
            ["format",  self.get_out_format()],
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "resource", "framework", "log_level", "format"]
        res = variable
        if res in options:
            res = "_" + res
        return res
    