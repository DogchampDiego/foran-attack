from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class TrivyEnv(LocalEnv):
    
    format_list = {'json': 'json', 'html': 'template --template "@contrib/html.tpl"',
                   'xml': 'template --template "@contrib/junit.tpl"'}
    scan_types = {'vuln', 'config', 'secret', 'rbac', 'license'}
    resource_list = {'cluster', 'deployment', 'configmap', 'all', 'pod', 'daemonset', 'serviceaccount', 'role', 'rolebinding', 
                'service', 'statefulset', 'replicaset', 'replicationcontroller', 'job', 'cronjob', 'networkpolicy', 'namespace', 'persistentvolume', 'persistentvolumeclaim', 'storageclass'}
    severity_list = {'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN'}
    component_list = {'infra', 'workload'}
    
    def __init__(self):
        super().__init__()
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._resource = "cluster"
        self._scan_type = "vuln"
        self._severity = ""
        self._summary = True
        self._format = "json"
        self._components = 'workload'
       
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
            print("ERROR: Faulty K8S resource provided.")
            return False
    
    # Getter and Setter for scan_type
    def get_scan_type(self):
        return self._scan_type
    
    def set_scan_type(self, value):
        if value in self.scan_types:
            self._scan_type = value
        else:
            print("ERROR: Faulty scan type provided.")
            return
    
    # Getter and Setter for severity
    def get_severity(self):
        return self._severity
    
    def set_severity(self, value):
        if value in self.severity_list:
            self._severity = value
        else:
            print("ERROR: Faulty severity value provided.")
            return
        
     # Getter and Setter for summary 
    def get_summary(self):
        return self._summary
        
    def set_summary(self, value):
        if isinstance(value, bool):
            self._summary = value
        else:
            print("ERROR: Summary can only be set to True/False.")
    
    # Getter and Setter for format
    def get_format(self):
        return self._format
    
    def set_format(self, value):
        if value in self.format_list:
            self._format = value
            
    # Getter and Setter for component
    def get_component(self):
        return self._components
    
    def set_component(self, value):
        if value in self.component_list:
            self._components = value
        else:
            print("ERROR: Faulty component provided.")
            return False
    
    def get_env_dict(self):
        ret = [
            ["ip", self.get_ip()],
            ["subnet",  self.get_subnet()],
            ["resource",  self.get_resource()],
            ["scan_type",  self.get_scan_type()],
            ["severity",  self.get_severity()],        
            ["summary", self.get_summary()],
            ["format",  self.get_format()],
            ["component",  self.get_component()]
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "resource", "scan_type", "severity", "summary", "format", "component"]
        res = variable
        if res in options:
            res = "_" + res
        return res
