
from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class FlightsimEnv(LocalEnv):
    
    module_list = ["c2", "dga", "imposter", "miner", "scan", "sink", "spambot", "ssh-exfil", 
                   "ssh-transfer", "tunnel-dns", "tunnel-icmp"]

    c2_family_list = [
    "Adwind", "Agent Tesla", "Alien", "Amadey", "AndroRAT", "Anubis", "APT34", "Arkei Stealer",
    "Astaroth", "AsyncRAT", "Ave Maria", "AZORult", "BazarBackdoor", "Beta Bot", "BitRAT",
    "BlackNET RAT", "Bozok RAT", "Bumblebee", "Chrysaor", "Cobalt Strike", "Collector Stealer",
    "CryptBot", "CryptoCore", "CyberGate RAT", "DanaBot", "DarkComet", "DCRat", "DiamondFox",
    "DNSMessenger", "FormBook", "Gamaredon", "Gh0st RAT", "Grandoreiro", "Hancitor", "Houdini",
    "Hydra", "IcedID", "Imminent Monitor", "IRATA", "Kimsuky", "KPOT Stealer", "Lazarus", "Loda",
    "LokiBot", "Lu0bot", "Lu0Bot", "Lumma Stealer", "Mars Stealer", "MorphineRAT", "NanoCore RAT",
    "NetSupport Manager", "NetWire RAT", "Nitol", "njRAT", "NSO Group", "Nymaim", "Orcus RAT",
    "Oski Stealer", "Poison Ivy", "Pony", "Predator the Thief", "Prometei", "Qakbot", "QuaDream",
    "Quasar RAT", "Raccoon Stealer", "Raspberry Robin", "RedLine Stealer", "Remcos RAT",
    "RevengeRAT", "Ryuk", "ServHelper", "SharkBot", "Shlayer", "sLoad", "smokeloader",
    "Smoke Loader", "SMSspy", "SocGholish", "SpyMax", "StrongPity", "STRRAT", "SystemBC",
    "TA505", "Taurus", "Tofsee", "TrickBot", "URSNIF", "Vidar", "Vjw0rm", "XtremeRAT",
    "XWorm", "Zeus Panda", "Zloader", "ztds"]
    
    def __init__(self):
        super().__init__()    
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._element = "families"
        self._category = "c2"
        self._module = "scan"
        self._c2_family = ""
        self._num_hosts = 10
        self._dry = True
        self._fast = False
        self._interface = ""
        # Command variable
        self._command = None
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
        
    # Getter and Setter for element
    def get_element(self):
        return self._element
    
    def set_element(self, value):
        self._element = value
        
    # Getter and Setter for category
    def get_category(self):
        return self._category
    
    def set_category(self, value):
        self._category = value
        
    # Getter and Setter for module
    def get_module(self):
        return self._module
    
    def set_module(self, value):
        if value in self.module_list:
            self._module = value
        else:
            print("Module not supported.")
        
    # Getter and Setter for module_c2
    def get_c2_family(self):
        return self._c2_family
    
    def set_c2_family(self, value):
        if value in self.c2_family_list:
            self._c2_family = value
        else:
            print("C2-Family not supported.")
            
    # Getter and Setter for num_simulated_hosts
    def get_num_hosts(self):
        return self._num_hosts

    def set_num_hosts(self, value):
        self._num_hosts = value
    
    # Getter and Setter for dry
    def get_dry(self):
        return self._dry
    
    def set_dry(self, value):
        if isinstance(value, bool):
            self._dry = value
        else:
            print("Value must be boolean.")
    
    # Getter and Setter for fast
    def get_fast(self):
        return self._fast
    
    def set_fast(self, value):
        if isinstance(value, bool):
            self._fast = value
        else:
            print("Value must be boolean.")
        
    # Getter and Setter for interface
    def get_interface(self):
        return self._interface
    
    def set_interface(self, value):
        self._interface = value
        
    def get_command(self):
        return self._command

    def get_pod_name(self):
        return self._pod_name

    def set_pod_name(self, pod_name):
        self._pod_name = pod_name
        
    def get_pod_yaml(self):
        return self.yaml

    def set_pod_yaml(self, yaml):
        self._yaml = yaml
        
    def get_env_dict(self):
        ret = [
            ["ip", self.get_ip()],
            ["subnet",  self.get_subnet()],
            ["element", self.get_element()],
            ["category", self.get_category()],
            ["module", self.get_module()],
            ["c2_family", self.get_c2_family()],
            ["num_hosts", self.get_num_hosts()],
            ["dry", self.get_dry()],
            ["fast", self.get_fast()],
            ["interface", self.get_interface()],
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "element", "category", "module",
                   "c2_family", "num_hosts", "dry", "fast", "interface"]
        res = variable
        if res in options:
            res = "_" + res
        return res
    