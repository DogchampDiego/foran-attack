import re
import subprocess
from controller.filehistory import ConditionalFileHistory
import help.helper as helper
from state.menu_state import MenuState
from tools.kubescape.KubescapeEnv import KubescapeEnv

from tools.kubescape.KubescapeWrapper import KubescapeWrapper
from tools.base_classes.tool_base import Tool

class Kubescape(Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.KUBESCAPE,MenuState.KUBESCAPE)

        # Wrapper and Environment Variables
        self.local_env = KubescapeEnv()
        self.wrapper = KubescapeWrapper(self.local_env)
        
        # Set Tool Name / Tool Version
        self.name = "Kubescape"

        # Command Mapping
        self.command_mapping = {
            "scan" : self.handle_scan,
            "mitre": self.handle_scan_framework_mitre,
            "nsa": self.handle_scan_framework_nsa,
            "workload": self.hand_scan_workload
        }
        
        self.command_mapping_db_ignore_db = {
            "--help": self.handle_help,
            "help": self.handle_help,
            "-h": self.handle_help,
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.kubescape_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["--help or help", "View the help menu"],
            ["scan", "Scan all resources in the cluster"],
            ["mitre",  "Scan running cluster against MITRE framework"],
            ["nsa",  "Scan running cluster against NSA framework"],
            ["workload",  "Scan running workloads (except namespace kube-system)"]
        ]

    def check_installed(self):
        try:
            cmd = ['kubescape', 'version']
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except FileNotFoundError:
            return False
    
    def install_tool(self):
        path = self.global_var.get_base_dir() + "tools/kubescape/install_kubescape.sh"
        subprocess.run(["sudo", "chmod", "+x", path], check=True)
        print(f"Script '{path}' is now executable.")
        subprocess.call(["bash", path, self.global_var.get_tool_dir(), self.global_var.get_base_dir()])

    def tool_version(self):
        cmd = ['kubescape', 'version']
        version_raw = subprocess.check_output(cmd).decode("utf-8").strip()
        matches = re.findall(r'v\d+\.\d+\.\d+', version_raw)
        return matches[0]

    # InputHandle Methods
    def handle_help(self):
        return self.wrapper._execute_command(self.wrapper.help())

    def handle_scan(self):
        return self.wrapper._execute_command(self.wrapper.scan())

    def handle_scan_framework_mitre(self):
        return self.wrapper._execute_command(self.wrapper.scan_framework_mitre())

    def handle_scan_framework_nsa(self):
        return self.wrapper._execute_command(self.wrapper.scan_framework_nsa())
    
    def hand_scan_workload(self):
        return self.wrapper._execute_command(self.wrapper.scan_workload())
    
    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("scan")
        self.completer.words.append("framework")
        self.completer.words.append("mitre")
        self.completer.words.append("nsa")
        self.completer.words.append("workload")

    def add_corrections(self):
        self.corrections = {
            "scan": " ".join(self.wrapper.scan()),
            "mitre": " ".join(self.wrapper.scan_framework_mitre()),
            "nsa": " ".join(self.wrapper.scan_framework_nsa()),
            "scann": "scan",
            "verbose": "scan",
            "sacn": "scan",
            "csan": "scan",
            "scann": "scan",
            "scna": "scan",
            "sscan": "scan",
            "sac": "scan",
            "sca": "scan",
            "h": "help",
            "hepl": "help",
            "helpp": "help",
            "heelp": "help",
            "helep": "help",
            "helps": "help",
            "framwork": "framework",
            "frameork": "framework",
            "frmaework": "framework",
            "frameowrk": "framework",
            "frakmework": "framework"
        }
        