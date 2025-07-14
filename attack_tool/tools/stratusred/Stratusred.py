import subprocess
from controller.filehistory import ConditionalFileHistory
import help.helper as helper
from state.menu_state import MenuState

from tools.base_classes.tool_base import Tool
from tools.stratusred.StratusredEnv import StratusredEnv
from tools.stratusred.StratusredWrapper import StratusredWrapper

class Stratusred(Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.STRATUSRED, MenuState.STRATUSRED)

        # Wrapper and Environment Variables
        self.local_env = StratusredEnv()
        self.wrapper = StratusredWrapper(self.local_env)

        # Set Tool Name / Tool Version
        self.name = "Stratus-Red-Team"

        # Command Mapping
        self.command_mapping = {
            "cred-secrets": self.handle_detonate_cred_secrets,
            "cred-tokens": self.handle_detonate_cred_token,
            "persist-admin-clusterrole": self.handle_detonate_persist_admin_clusterrole,
            "persist-client-cert": self.handle_detonate_persist_client_cert,
            "persist-create-token": self.handle_detonate_persist_create_token,
            "privesc-hostpath": self.handle_detonate_privesc_hostpath,
            "privesc-nodeproxy": self.handle_detonate_privesc_nodeproxy,
            "privesc-privileged-pod": self.handle_detonate_privesc_privileged_pod
        }
        
        self.command_mapping_db_ignore_db = {
            "--help": self.handle_help,
            "help": self.handle_help,
            "-h": self.handle_help,
            "list": self.handle_list,
            "list-persist": self.handle_list_tactics_persist,
            "clean": self.handle_clean,
            "cur": self.handle_show,
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.stratusred_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["--help or help", "View the help menu"],
            ["list", "List all attacks"],
            ["status", "Show status of current techniques"],
            ["cur", "Show information of current technique"],
            ["show <k8s.tactic.technique>", "Show details of specific resource"],
            ["clean", "Revert detonations and clean up infrastructure"],
            ["list-persist", "List all persistence attacks"],
            ["cred-secrets", "Dump secrets of cluster"],
            ["cred-tokens", "Extract serviceaccount tokens of cluster"],
            ["persist-admin-clusterrole", "Persist with admin clusterrole"],
            ["persist-client-cert", "Persist with client certificate"],
            ["persist-create-token", "Persist with serviceaccount token"],
            ["privesc-hostpath", "Privilege escalation with hostpath volume"],
            ["privesc-nodeproxy", "Privilege escalation with nodes proxy"],
            ["privesc-privileged-pod", "Privilege escalation with privileged pod"]        
        ]

    def check_installed(self):
        cmd = ['stratus', 'version']
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            return False
        return True
    
    def install_tool(self):
        path = self.global_var.get_base_dir() + "tools/stratusred/install_stratusred.sh"
        subprocess.run(["sudo", "chmod", "+x", path], check=True)
        print(f"Script '{path}' is now executable.")
        subprocess.call(["bash", path, self.global_var.get_tool_dir(), self.global_var.get_base_dir()])

    def tool_version(self):
        cmd = ['stratus', 'version']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stderr.strip()
    
    # InputHandle Methods
    def handle_help(self):
        return self.wrapper._execute_command(self.wrapper.help())
    
    def handle_clean(self):
        return self.wrapper._execute_command(self.wrapper.clean())
    
    def handle_show(self):
        return self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), self.local_env.get_tactic(), self.local_env.get_technique()))
    
    def handle_list(self):
        return self.wrapper._execute_command(self.wrapper.list(self.local_env.get_platform(), None))
            
    # TO DO: Execute method improve string processing with lists
    def handle_list_tactics_privesc(self):
                return self.wrapper._execute_command(self.wrapper.list(self.local_env.get_platform(), "privilege-escalation"))
    
    def handle_list_tactics_persist(self):
                return self.wrapper._execute_command(self.wrapper.list(self.local_env.get_platform(), "persistence"))
    
    # TO DO: Execute method improve string processing with lists
    def handle_list_tactics_cred(self):
                return self.wrapper._execute_command(self.wrapper.list(self.local_env.get_platform(), "credential-access"))
    
    def handle_detonate_cred_secrets(self):
        self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), "credential-access", "dump-secrets"))
        return self.wrapper._execute_command(self.wrapper.detonate(
            self.local_env.get_platform(), "credential-access", "dump-secrets"))
        
    def handle_detonate_cred_token(self):
        self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), "credential-access", "steal-serviceaccount-token"))
        return self.wrapper._execute_command(self.wrapper.detonate(
            self.local_env.get_platform(), "credential-access", "steal-serviceaccount-token"))
    
    def handle_detonate_persist_admin_clusterrole(self):
        self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), "persistence", "create-admin-clusterrole"))
        return self.wrapper._execute_command(self.wrapper.detonate(
            self.local_env.get_platform(), "persistence", "create-admin-clusterrole"))
    
    def handle_detonate_persist_client_cert(self):
        self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), "persistence", "create-client-certificate"))
        return self.wrapper._execute_command(self.wrapper.detonate(
            self.local_env.get_platform(), "persistence", "create-client-certificate"))
    
    def handle_detonate_persist_create_token(self):
        self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), "persistence", "create-token"))
        return self.wrapper._execute_command(self.wrapper.detonate(
            self.local_env.get_platform(), "persistence", "create-token"))
    
    def handle_detonate_privesc_hostpath(self):
        self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), "privilege-escalation", "hostpath-volume"))
        return self.wrapper._execute_command(self.wrapper.detonate(
            self.local_env.get_platform(), "privilege-escalation", "hostpath-volume"))
        
    def handle_detonate_privesc_nodeproxy(self):
        self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), "privilege-escalation", "nodes-proxy"))
        return self.wrapper._execute_command(self.wrapper.detonate(
            self.local_env.get_platform(), "privilege-escalation", "nodes-proxy"))
    
    def handle_detonate_privesc_privileged_pod(self):
        self.wrapper._execute_command(self.wrapper.show(
            self.local_env.get_platform(), "privilege-escalation", "privileged-pod"))
        return self.wrapper._execute_command(self.wrapper.detonate(
            self.local_env.get_platform(), "privilege-escalation", "privileged-pod"))

    def add_completer(self):
        self.completer.words.append("help")
        self.completer.words.append("status")
        self.completer.words.append("list")
        self.completer.words.append("cred-secrets")
        self.completer.words.append("cred-tokens")
        self.completer.words.append("persist-admin-clusterrole")   
        self.completer.words.append("persist-client-cert")
        self.completer.words.append("persist-create-token")
        self.completer.words.append("privesc-hostpath")
        self.completer.words.append("privesc-nodeproxy")
        self.completer.words.append("privesc-privileged-pod")
        self.completer.words.append("list-persist")

    def add_corrections(self):
        self.corrections = {
            "l": "list",
            "pe": "persistance",
            "persistance": "--mitre-attack-tactic persistence",
            "h": "help",
            "hepl": "help",
            "helpp": "help",
            "heelp": "help",
            "helep": "help",
            "helps": "help"
        }
        