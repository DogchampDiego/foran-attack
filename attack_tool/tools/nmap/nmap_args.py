from tools.nmap.NmapWrapper import NmapWrapper
from tools.nmap.NmapEnv import NmapEnv
from tools.base_classes.args_base import Args

class NmapArgs(Args):

    def __init__(self):
        super().__init__()
        self.local_env = NmapEnv()
        self.nmap_wrapper = NmapWrapper(self.local_env)
        self.row = [
            ["help", "View the help menu"],
            ["agg", "Scan using the flags -sS (SYN) -sV (Version) -sC (Scripts) -O (OS)"],
            ["syn", "SYN scan (SYN flag)"],
            ["k8s", "SYN scan with k8s ports and script"],
            ["con", "TCP connect scan (SYN/SYN-ACK/ACK)"],
            ["udp", "UDP scan"],
            ["null", "Null scan (no flags set)"],
            ["fin", "FIN scan (FIN flag)"],
            ["version", "TCP Version detection"]
        ]

    def handle_args(self, args, param = None):

        if param:
            for param_value in param:
                # python main.py --tool kubehunter --attack remote -p ip=10.0.0.12,10.0.0.114 -p active_mode=true
                # Each param_value would look like "key=value"
                param, value = param_value.split("=", 1)

        
                if param =="ip":
                    self.local_env.set_ip(value)
                elif param == "subnet":
                    self.local_env.set_subnet(value)  
                elif param == "ports":
                    self.local_env.set_ports(value) 
                elif param == "scan_type":
                    self.local_env.set_scan_type(value)
                elif param == "version":
                    self.local_env.set_version(value) 
                elif param == "script":
                    self.local_env.set_script(value) 
                elif param == "custom_script":
                    self.local_env.set_custom_script(value) 
                elif param == "os":
                    self.local_env.set_os(value)
                elif param == "noping":
                    self.local_env.set_noping(value)
                elif param == "speed":
                    self.local_env.set_speed(value)
                elif param == "agg":
                    self.local_env.set_agg(value)
                elif param == "verbose":
                    self.local_env.set_verbose(value)
                elif param == "format":
                    self.local_env.set_format(value)

        # Handle the input
        
        try:
            if args == "con":  # TCP connect scan
                self.out = self.nmap_wrapper._execute_command(self.nmap_wrapper.scan_con()) 
                self.parse_output = True
            elif args == "udp":  # UDP scan
                self.out = self.nmap_wrapper._execute_command(self.nmap_wrapper.scan_udp()) 
                self.parse_output = True
            elif args == "null":  # Null scan
                self.out = self.nmap_wrapper._execute_command(self.nmap_wrapper.scan_null())
                self.parse_output = True
            elif args == "fin":  # FIN scan
                self.out = self.nmap_wrapper._execute_command(self.nmap_wrapper.scan_fin())  
                self.parse_output = True
            elif args == "syn":  # SYN scan
                self.out = self.nmap_wrapper._execute_command(self.nmap_wrapper.scan_syn())  
                self.parse_output = True
            elif args == "agg":  # Aggressive scan
                self.out = self.nmap_wrapper._execute_command(self.nmap_wrapper.scan_agg("tcp"))  
                self.parse_output = True
            elif args == "version":  # Version detection
                self.out = self.nmap_wrapper._execute_command(self.nmap_wrapper.scan_version("tcp")) 
                self.parse_output = True
            elif args == "k8s":  # k8s detection
                self.local_env.set_scan_type("-sS")
                self.local_env.set_ports("k8s")
                self.local_env.set_custom_script("/usr/share/nmap/scripts/kubernetes-info.nse")
                print("About to launch")
                self.out = self.nmap_wrapper._execute_command(
                    self.nmap_wrapper._generate_command(scan_type=True, verbose=True, custom_script=True))
                self.parse_output = True
            elif args == "help":
                self.table.print_table(self.column, self.row)
                return 
            elif args == "options":
                self.table.print_table(self.column, self.local_env.get_env_dict())
                return 
            else:
                return None, None, None, False
        except Exception as e:
            print(e)
            return None, None, None, False

        return self.out, self.nmap_wrapper.final_command, self.local_env, self.parse_output