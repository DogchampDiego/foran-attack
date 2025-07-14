from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class KubehunterEnv(LocalEnv):
    def __init__(self):
        super().__init__()
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._log_level = None
        self._active_mode = None
        self._quick = None
        self._report = "json"
        self._mapping = False
        self._statistics = False
        self._subnet = "/24"
    
    # Getter and Setter for local_ip
    def get_ip(self):
        return self._ip
    
    def set_ip(self, value):
        self._ip = value
    
    # Getter and Setter for log_level
    def get_log_level(self):
        return self._log_level
    
    def set_log_level(self, value):
        self._log_level = value
    
    # Getter and Setter for active_mode
    def get_active_mode(self):
        return self._active_mode
    
    def set_active_mode(self, value):
        self._active_mode = value
    
    # Getter and Setter for quick
    def get_quick(self):
        return self._quick
    
    def set_quick(self, value):
        self._quick = value
    
    # Getter and Setter for report
    def get_report(self):
        return self._report
    
    def set_report(self, value):
        self._report = value
    
    # Getter and Setter for mapping
    def get_mapping(self):
        return self._mapping
    
    def set_mapping(self, value):
        self._mapping = value
    
    # Getter and Setter for statistics
    def get_statistics(self):
        return self._statistics
    
    def set_statistics(self, value):
        self._statistics = value

     # Getter and Setter for subnet
    def get_subnet(self):
        return self._subnet
    
    def set_subnet(self, value):
        self._subnet = value

    def get_env_dict(self):
        ret = [
            ["IP", self.get_ip()],
            ["LOG_LEVEL", self.get_log_level()],
            ["ACTIVE_MODE",  self.get_active_mode()],
            ["QUICK", self.get_quick()],
            ["REPORT",  self.get_report()],
            ["MAPPING",  self.get_mapping()],
            ["STATISTICS", self.get_statistics()],
            ["SUBNET",  self.get_subnet()]
        ]
        return ret

    def translate_variable(self, variable):
        variable_mapping = {
            "ip": "_ip",
            "log_level": "_log_level",
            "active_mode": "_active_mode",
            "quick": "_quick",
            "report": "_report",
            "mapping": "_mapping",
            "statistics": "_statistics",
            "subnet": "_subnet"
        } 
        
        return variable_mapping.get(variable.lower(), "error")