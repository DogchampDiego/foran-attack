
from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class RakkessEnv(LocalEnv):

    namespace_list = ["default", "all", "*", "ricinfra", "ricplt", "ricxapp"]
    verb_list = ["create", "delete", "get", "list", "patch", "update", "watch", "deletecollection", "*", "all"]
    debug_lvl_list = ["debug", "info", "warn", "error", "fatal", "panic"] 
    resource_list = ["configmap", ""]
    
    def __init__(self):
        super().__init__()
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._namespace = ""
        self._resource = ""
        self._verbs = ["all"]
        self._user = ""
        self._group = ""
        self._service_account = ""
        self._debug_level = "1"
        self._pod_name = ""
    
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
    
    # Getter and Setter for subnet
    def get_pod_name(self):
        return self._pod_name
    
    def set_pod_name(self, pod_name):
        self._pod_name = pod_name    

    # Getter and Setter for namespace
    def get_namespace(self):
        return self._namespace
    
    def set_namespace(self, value):
        self._namespace = value
    
    # Getter and Setter for resource    
    def get_resource(self):
        return self._resource
    
    def set_resource(self, value):
        self._resource = value
        
    # Getter and Setter for verbs
    def get_verbs(self):
        return self._verbs
    
    def set_verbs(self, verbs):
        for i in verbs:
            if i not in self.verb_list:
                print("ERROR: Faulty verb:", verbs[i], " provided.")
                return
        self._verbs = verbs
    
    # Getter and Setter for user
    def get_user(self):
        return self._user
    
    def set_user(self, value):
        self._user = value
    
    # Getter and Setter for group
    def get_group(self):
        return self._group
    
    def set_group(self, value):
        self._group = value
    
    # Getter and Setter for service_account
    def get_service_account(self):
        return self._service_account
    
    def set_service_account(self, value):
        self._service_account = value
    
    # Getter and Setter for debug_level
    def get_debug_level(self):
        return self._debug_level
    
    def set_debug_level(self, value):
        if value in self.debug_lvl_list:
            self._debug_level = value
        else:
            print("ERROR: Faulty debug level provided.")
            return
    
    # Getter and Setter for service_account
    def get_service_account(self):
        return self._service_account
    
    def set_service_account(self, value):
        self._service_account = value    
 
    def get_env_dict(self):
        ret = [
            ["ip", self.get_ip()],
            ["subnet",  self.get_subnet()],
            ["namespace", self.get_namespace()],
            ["resource", self.get_resource()],
            ["verbs", self.get_verbs()],
            ["user", self.get_user()],
            ["group", self.get_group()],
            ["service_account", self.get_service_account()],
            ["debug_level", self.get_debug_level()]
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "namespace", "resource", "verbs",
                   "user", "group", "service_account", "debug_level"]
        res = variable
        if res in options:
            res = "_" + res
        return res
    