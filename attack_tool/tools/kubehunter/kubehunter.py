import help.helper as helper
from state.menu_state import MenuState
from tools.base_classes.tool_base import Tool
import subprocess

from controller.filehistory import ConditionalFileHistory
from tools.kubehunter.kubehunter_wrapper import KubeHunterWrapper
from tools.kubehunter.kubehunter_env import KubehunterEnv
from tools.kubehunter.kubehunter_parser import KubehunterParser

class Kubehunter(Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.KUBEHUNTER,MenuState.KUBEHUNTER)

        # Wrapper and Metadata Variables
        self.local_env = KubehunterEnv()
        self.wrapper = KubeHunterWrapper(self.local_env)
        self.parser = KubehunterParser()

        # Set Tool Name / Tool Version
        self.name = "kubehunter"

        # Command Mapping
        self.command_mapping = {
            "remote": self.handle_remote,
            "quick_pod_scan": self.handle_pod,
            "cidr": self.handle_cidr,
            "interface": self.handle_interface,
        }
        self.command_mapping_db_ignore_db = {
            "--help": self.handle_help,
            "--list": self.handle_list,
            "list": self.handle_list,
            "pod_scan": self.handle_pod_scan,
        }

        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.prompt_history_kubehunter")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False  

        # self.custom_style = Style.from_dict({'prompt': 'blue'})
        self.column = ["Method", "Description"]
        self.row = [
            ["--help", "Show all available commands"],
            ["--list or list", "Displays all tests in kubehunter (add --active flag to see active tests)"],
            ["remote",  "Hunts for weaknesses from outside the cluster. You have to specify the IP addresses to scan. Example to set multiple IPs: 'set ip 192.168.0.10, 192.168.0.11'"],
            ["quick_pod_scan", "Imitated view of hunting for Information from inside a pod"],
            ["pod_scan",  "Scans for Information from inside a pod"],
            ["cidr",  "Hunts for weaknesses inside the cluster. You have to set specific CIDR to scan (default /24)"],
            ["interface",  "Hunts for weaknesses inside the cluster, by scanning all interfaces available"]
        ]

    # Abstract Methods
    def check_installed(self):
        try:
            # Run the kubehunter command with the `--help` flag to check if it is installed
            subprocess.check_output(['kube-hunter', '--help'])
            return True
        except FileNotFoundError:
            return False
    
    def install_tool(self):
        subprocess.call(["bash", self.global_var.get_base_dir() + "tools/kubehunter/install_kubehunter.sh",self.global_var.get_base_dir(),self.global_var.get_tool_dir()])
        
    def tool_version(self):
        return "0.6.8"

    # InputHandle Methods
    def handle_help(self):
        return self.wrapper.help()

    def handle_list(self):
        return self.wrapper.list()

    def handle_remote(self):
        self.parse_output = True
        return self.wrapper.remote_scan()

    def handle_pod(self):
        self.parse_output = True
        return self.wrapper.pod_scan()

    def handle_cidr(self):
        self.parse_output = True
        return self.wrapper.cidr_scan()

    def handle_interface(self):
        self.parse_output = True
        return self.wrapper.interface_scan()

    def handle_pod_deploy(self):
        return self.wrapper.deploy_pod()
    
    def handle_pod_delete(self):
        return self.wrapper.delete_pod()
    
    def handle_pod_scan(self):
        self.parse_output = False
        return self.wrapper.scan_pod()

    def pod_safe_results(self):
        self.database_insert()
        return None

    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("list")
        self.completer.words.append("remote")
        self.completer.words.append("pod")
        self.completer.words.append("cidr")
        self.completer.words.append("interface")

    def add_corrections(self):
        self.corrections["--hepl"] = "--help"
        self.corrections["hepl"] = "help"
        self.corrections["--lits"] = "list"
        self.corrections["lits"] = "list"
        self.corrections["remoet"] = "remote"
        self.corrections["pdo"] = "pod"
        self.corrections["cird"] = "cidr"
        self.corrections["interfaec"] = "interface"