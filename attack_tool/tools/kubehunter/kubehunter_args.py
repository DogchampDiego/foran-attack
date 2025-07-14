from tools.kubehunter.kubehunter_wrapper import KubeHunterWrapper
from tools.kubehunter.kubehunter_env import KubehunterEnv
from tools.base_classes.args_base import Args
from environment.global_const import GlobalVariables

class KubehunterArgs(Args):

    def __init__(self):
        super().__init__()
        self.local_env = KubehunterEnv()
        self.kubehunter_wrapper = KubeHunterWrapper(self.local_env)
        self.row = [
            ["remote",  "Hunts for weaknesses from outside the cluster. Example to set multiple IPs: 'set ip 192.168.0.10, 192.168.0.11'"],
            ["quick_pod_scan",  "Imitated view of hunting for Information from inside a pod"],
            ["cidr",  "Hunts for weaknesses inside the cluster. You have to set specific CIDR to scan (default /24)"],
            ["interface",  "Hunts for weaknesses inside the cluster, by scanning all interfaces available"],
            ["pod_create",  "Creates a pod to scan for Information from inside the cluster"],
            ["pod_delete",  "Deletes the created pod"],
            ["pod_scan",  "Scans for Information from inside the with 'pod_deploy' created pod"],
            ["pod_safe_results",  "Writes Results from the Pod inside the Database"],
        ]

    def handle_args(self, args, param = None):

        if param:
            for param_value in param:
                # python main.py --tool kubehunter --attack remote -p ip=10.0.0.12,10.0.0.114 -p active_mode=true
                # Each param_value would look like "key=value"
                param, value = param_value.split("=", 1)

                if param == "ip" : 
                    ip_list = [ip.strip() for ip in value.split(',')]
                    ip_string_clean = ' '.join(ip_list)
                    self.local_env.set_ip(ip_string_clean)
                if param == "log_level" : 
                    self.local_env.set_log_level(value)
                if param == "active_mode": 
                    self.local_env.set_active_mode(value)
                if param == "quick": 
                    self.local_env.set_quick(value)
                if param == "report": 
                    self.local_env.set_report(value)
                if param == "mapping": 
                    self.local_env.set_mapping(value)
                if param == "statistics": 
                    self.local_env.set_statistics(value)
                if param == "subnet": 
                    self.local_env.set_subnet(value)

        # Handle the input
        try:
            if args == "remote":
                self.out = self.kubehunter_wrapper.remote_scan()
                self.parse_output = True
            elif args == "quick_pod_scan":
                self.out = self.kubehunter_wrapper.pod_scan()
                self.parse_output = True
            elif args == "cidr":
                self.out = self.kubehunter_wrapper.cidr_scan()
                self.parse_output = True
            elif args == "interface":
                self.out = self.kubehunter_wrapper.interface_scan()
                self.parse_output = True
            elif args == "pod_scan":
                out = self.kubehunter_wrapper.deploy_pod()
                print(out)
                self.out = self.kubehunter_wrapper.info_pod()
                GlobalVariables.get_instance().get_env().set_pod_deployment(True)
                self.kubehunter_wrapper.delete_pod()    
            
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

        return self.out, self.kubehunter_wrapper.final_command, self.local_env, self.parse_output
