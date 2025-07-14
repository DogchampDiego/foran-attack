import subprocess
from controller.filehistory import ConditionalFileHistory
import help.helper as helper
from state.menu_state import MenuState

from tools.trivy.TrivyEnv import TrivyEnv
from tools.trivy.TrivyWrapper import TrivyWrapper
from tools.base_classes.tool_base import Tool

class Trivy(Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.TRIVY,MenuState.TRIVY)

        # Wrapper and Environment Variables
        self.local_env = TrivyEnv()
        self.wrapper = TrivyWrapper(self.local_env)

        # Set Tool Name / Tool Version
        self.name = "Trivy"

        # Command Mapping
        self.command_mapping = {
            "cluster": self.handle_scan_cluster,
            "full": self.handle_scan_cluster_all,
            "vuln": self.handle_scan_cluster_vuln,
            "secret" : self.handle_scan_cluster_secret,
            "config": self.handle_scan_cluster_config,
            "critical": self.handle_scan_cluster_critical
        }
        
        self.command_mapping_db_ignore_db = {
            "help": self.handle_help,
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.trivy_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["help", "View the help menu"],
            ["cluster", "Scan Full Cluster for Vulnerabilities (Summary Output)"],
            ["full", "Scan Full Cluster with all Scanners (Full Output)"],
            ["vuln",  "Scan Vulnerabilities"],
            ["secret",  "Scan Secrets"],
            ["config",  "Scan Misconfigurations"],
            ["critical",  "Scan using all Scanners with Critical Severity"],
        ]

    def check_installed(self):
        try:
            cmd = ['trivy', 'version']
            subprocess.check_output(cmd)
            return True
        except FileNotFoundError:
            return False
    
    def install_tool(self):
        subprocess.call(["bash", self.global_var.get_base_dir() + "tools/trivy/install_trivy.sh"])
        
    def tool_version(self):
        cmd = ['trivy', 'version']
        return subprocess.check_output(cmd).decode("utf-8").split(" ")[1].strip()

    # InputHandle Methods
    def handle_help(self):
        return self.wrapper._execute_command(self.wrapper.help())

    def handle_scan_cluster(self):
        return self.wrapper._execute_command(self.wrapper.scan_cluster())
    
    def handle_scan_cluster_all(self):
        return self.wrapper._execute_command(self.wrapper.scan_cluster_all())

    def handle_scan_cluster_vuln(self):
        return self.wrapper._execute_command(self.wrapper.scan_cluster_vuln())

    def handle_scan_cluster_secret(self):
        return self.wrapper._execute_command(self.wrapper.scan_cluster_secret())

    def handle_scan_cluster_config(self):
        return self.wrapper._execute_command(self.wrapper.scan_cluster_config())

    def handle_scan_cluster_critical(self):
        return self.wrapper._execute_command(self.wrapper.scan_cluster_critical())
    
    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("cluster")
        self.completer.words.append("vuln")
        self.completer.words.append("critical")
        self.completer.words.append("config")
        self.completer.words.append("secret")
        self.completer.words.append("full")

    def add_corrections(self):
        self.corrections = {
            "cluster": " ".join(self.wrapper.scan_cluster()),
            "vuln": " ".join(self.wrapper.scan_cluster_vuln()),
            "secret": " ".join(self.wrapper.scan_cluster_secret()),
            "config": " ".join(self.wrapper.scan_cluster_config()),
            "critical": " ".join(self.wrapper.scan_cluster_critical()),
            "full": " ".join(self.wrapper.scan_cluster_all()),
            "cluser": "cluster",
            "cluste": "cluster",
            "clusetr": "cluster",
            "clustr": "cluster",
            "hepl": "help",
            "helpp": "help",
            "heelp": "help",
            "helep": "help",
            "helps": "help"
        }
        