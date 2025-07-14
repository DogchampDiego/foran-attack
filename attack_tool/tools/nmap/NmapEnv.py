from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class NmapEnv(LocalEnv):
    
    format_list = {'normal': '-oN', 'xml': '-oX', 'grep': '-oG', 'all': '-oA',
                   'scriptkiddie': '-oS', 'list': '-oL'}
    scan_list = {'-sS', '-sT', '-sU', '-sN', '-sF', '-sA'}
    speed_list = {"-T0", "-T1", "-T2", "-T3", "-T4", "-T5"}
    port_list = ["-p 443,2379,6666,4194,6443,8443,8080,10250,10255,10256,9099,6782-6784,30000-32767,44134", "-p-"]

    def __init__(self):
        super().__init__()
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._ports = ""
        self._scan_type = "-sS"
        self._version = ""
        self._script = ""
        self._custom_script = "/usr/share/nmap/scripts/kubernetes-info.nse"
        self._os = ""
        self._noping = "-Pn"
        self._speed = "-T4"
        self._agg = ""
        self._verbose = "-vv"
        self._format = "xml"

        # env
        self._pod_name = None
        self._yaml = None
   
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
    
    def get_ports(self):
        return self._ports

    def set_ports(self, new_ports):
        if new_ports == "k8s":
            self._ports = self.port_list[0]
        elif new_ports == "all":
            self._ports = self.port_list[1]
        elif new_ports != "" and len(new_ports) > 0:
                self._ports = "-p" + new_ports
        else:
            print("ERROR: Faulty port range provided.")
            return

    def get_scan_type(self):
        return self._scan_type

    def set_scan_type(self, new_scan_type):
        if new_scan_type in self.scan_list:
            self._scan_type = new_scan_type
        else:
            print("ERROR: Faulty scan type provided.")
            return

    def get_version(self):
        return self._version

    def set_version(self):
         self._version = "-sV"

    def get_script(self):
        return self._script

    def set_script(self):
        self._script = "-sC"
    
    def get_custom_script(self):
        return "--script=" + self._custom_script + " -d"
    
    def set_custom_script(self, new_script):
        self._custom_script = new_script

    def get_os(self):
        return self._os

    def set_os(self):
        self._os = "-O"

    def get_noping(self):
        return self._noping

    def set_noping(self):
        self._noping = "-Pn"

    def get_speed(self):
        return self._speed

    def set_speed(self, new_speed):
        if new_speed in self.speed_list:
            self._speed = new_speed
        else:
            print("ERROR: Faulty speed value provided.")
            return

    def get_agg(self):
        return self._agg

    def set_agg(self):
        self._agg = "-A"

    def get_verbose(self):
        return self._verbose

    def set_verbose(self):
        self._verbose = "-vv"

    def get_format(self):
        return self._format

    def set_format(self, new_format):
        if new_format in self.format_list:
            self._format = self.format_list[new_format]
        else:
            print("ERROR: Output format not supported.")
            return
        
    def get_env_dict(self):
        ret = [
            ["ip", self.get_ip()],
            ["subnet",  self.get_subnet()],
            ["ports",  self.get_ports()],
            ["scan_type",  self.get_scan_type()],
            ["version",  self.get_version()],           
            ["script", self.get_script()],
            ["custom_script", self.get_custom_script()],
            ["os",  self.get_os()],
            ["noping",  self.get_noping()],
            ["speed",  self.get_speed()],
            ["agg",  self.get_agg()],           
            ["verbose", self.get_verbose()],
            ["format",  self.get_format()],
            ["pod_name",  self.get_pod_name()],
            ["yaml",  self.get_pod_yaml()],
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "ports", "scan_type", "version", "script",
                   "custom_script", "os", "noping", "speed", "agg", "verbose", 
                   "format","pod_name","yaml"]
        res = variable
        if res in options:
            res = "_" + res
        return res
    
    def get_pod_name(self):
        return self._pod_name

    def set_pod_name(self, pod_name):
        self._pod_name = pod_name
        
    def get_pod_yaml(self):
        return self.yaml

    def set_pod_yaml(self, yaml):
        self._yaml = yaml
