
from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class StratusredEnv(LocalEnv):
    
    tactic_list = {'credential-access', 'persistence', 'exfiltration', 'discovery', 'defense-evasion', 
                   'impact', 'execution', 'initial-access', 'privilege-escalation'}
    technique_list = {'dump-secrets', 'steal-serviceaccount-token', 'create-admin-clusterrole', 'create-client-certificate',
                      'create-token', 'hostpath-volume', 'nodes-proxy', 'privileged-pod'}
    platform_list = ["aws", "gcp", "kubernetes"]
    
    def __init__(self):
        super().__init__()    
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._platform = "kubernetes"
        self._tactic = "credential-access"
        self._technique = "dump-secrets"
    
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
    def get_platform(self):
        return self._platform
    
    def set_platform(self, value):
        if value in self.platform_list:
            self._platform = value
        else:
            print("ERROR: Faulty platform provided.")
            return
    
        # Getter and Setter for resource
    def get_tactic(self):
        return self._tactic
    
    def set_tactic(self, value):
        if value in self.tactic_list:
            self._tactic = value
        else:
            print("ERROR: Faulty tactic provided.")
            return
    
    def get_technique(self):
        return self._technique
    
    def set_technique(self, value):
        if value in self.technique_list:
            self._technique = value
        else:
            print("ERROR: Faulty technique provided.")
            return
 
    def get_env_dict(self):
        ret = [
            ["ip", self.get_ip()],
            ["subnet",  self.get_subnet()],
            ["platform", self.get_platform()],
            ["tactic", self.get_tactic()],
            ["technique", self.get_technique()]
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "platform", "tactic", "technique"]
        res = variable
        if res in options:
            res = "_" + res
        return res
    