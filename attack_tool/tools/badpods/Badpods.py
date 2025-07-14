import subprocess

import help.helper as helper
from controller.filehistory import ConditionalFileHistory
from state.menu_state import MenuState
from tools.base_classes.tool_base import Tool
from tools.badpods.BadpodsEnv import BadpodsEnv
from tools.badpods.BadpodsWrapper import BadpodsWrapper

class Badpods(Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.BADPODS, MenuState.BADPODS)

        # Wrapper and Environment Variables
        self.local_env = BadpodsEnv()
        self.wrapper = BadpodsWrapper(self.local_env)

        # Set Tool Name / Tool Version
        self.name = "BadPods"

        # Command Mapping
        self.command_mapping = {
            "launch": self.handle_launch,
            "pod-everything": self.handle_launch_pod_everything,
            "pod-everything-revshell": self.handle_launch_revshell_pod_everything,
            "pod-priv-and-hostpid": self.handle_launch_pod_priv_and_hostpid,
            "pod-priv": self.handle_launch_pod_priv,
            "pod-hostpath": self.handle_launch_pod_hostpath,
            "pod-hostpid": self.handle_launch_pod_hostpid,
            "pod-hostnetwork": self.handle_launch_pod_hostnetwork,
            "pod-hostipc": self.handle_launch_pod_hostipc,
            "pod-nothing": self.handle_launch_pod_nothing,

        }
        self.command_mapping_db_ignore_db = {
            "status": self.handle_status,
            "verbose": self.handle_status_verbose,
            "clean": self.handle_clean,
            "resource": self.handle_resource,
            "access-scope": self.handle_access_scope,
            "type": self.handle_type
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.badpods_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["launch", "Launch current config: " + self.local_env.get_resource() + " access " + self.local_env.get_access_scope()],
            ["clean", "Remove all BadPods"],
            ["status", "Show status of BadPods"],
            ["verbose", "Show verbose information of BadPods (YAML)"],
            ["pod-everything", "Launch " + self.local_env.get_resource() + " access everything-allowed"],
            ["pod-everything-revshell", "Launch " + self.local_env.get_resource() + " access everything-allowed and reverse shell"],
            ["pod-priv-and-hostpid", "Launch " + self.local_env.get_resource() + " access priv-and-hostpid"],
            ["pod-priv", "Launch " + self.local_env.get_resource() + " access priv"],
            ["pod-hostpath", "Launch " + self.local_env.get_resource() + " access hostpath"],
            ["pod-hostpid", "Launch " + self.local_env.get_resource() + " access hostpid"],
            ["pod-hostnetwork", "Launch " + self.local_env.get_resource() + " access hostnetwork"],
            ["pod-hostipc", "Launch " + self.local_env.get_resource() + " access hostipc"],
            ["pod-nothing", "Launch " + self.local_env.get_resource() + " access nothing-allowed"],
            ["resource", "List available resources"],
            ["access-scope", "List available access scopes"],
            ["type", "List available types"],
        ]
        
        # Set the attack phase in menu prompt
        common_elements = set(self.global_var.get_menu_tree()).intersection(set(helper.get_menu_phase()))  
        if common_elements:
            phase = next(iter(common_elements))
            self.local_env.set_attack_phase(phase.name.lower().capitalize())

    def check_installed(self):
        try:
            cmd = ['ls', self.local_env.get_base_path()]
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"BadPods not installed.")
            return False
        
    def install_tool(self):
        path = self.global_var.get_base_dir() + "tools/badpods/install_badpods.sh"
        print("Installation script path BadPods: ", path)
        subprocess.run(["sudo", "chmod", "+x", path], check=True)
        print(f"Script '{path}' is now executable.")
        subprocess.call(["bash", path, self.global_var.get_tool_non_bin_dir(), self.global_var.get_base_dir()])
        
    def tool_version(self):
        return "No version available."

    # InputHandle Methods
    def handle_clean(self):
        return self.wrapper._execute_command(self.wrapper.clean())
    
    def handle_status(self):
        return self.wrapper._execute_command(self.wrapper.status())
    
    def handle_status_verbose(self):
        return self.wrapper._execute_command(self.wrapper.status_verbose())
    
    def handle_resource(self):
        print(self.local_env.resoure_list)
        return

    def handle_access_scope(self):
        print(self.local_env.access_scope_list)
        return
    
    def handle_type(self):
        print(self.local_env.type_list)
        return
    
    def handle_launch(self):
        return self.wrapper._execute_command(self.wrapper.launch())
    
    def handle_launch_custom(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom(
            self.env.get_type(), self.env.get_access_scope(), self.env.get_resource()))

    def handle_launch_revshell_pod_everything(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("revshell", "everything-allowed", "pod"))

    def handle_launch_pod_everything(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("exec", "everything-allowed", "pod"))
    
    def handle_launch_pod_priv_and_hostpid(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("exec", "priv-and-hostpid", "pod"))
    
    def handle_launch_pod_priv(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("exec", "priv", "pod"))
    
    def handle_launch_pod_hostpath(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("exec", "hostpath", "pod"))
    
    def handle_launch_pod_hostpid(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("exec", "hostpid", "pod"))
    
    def handle_launch_pod_hostnetwork(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("exec", "hostnetwork", "pod"))
    
    def handle_launch_pod_hostipc(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("exec", "hostipc", "pod"))
    
    def handle_launch_pod_nothing(self):
        return self.wrapper._execute_command(self.wrapper.launch_custom("exec", "nothing-allowed", "pod"))
    
    def add_completer(self):
        self.completer.words.append("clean")
        self.completer.words.append("launch")
        self.completer.words.append("type")
        self.completer.words.append("status")
        self.completer.words.append("verbose")
        self.completer.words.append("resource")
        self.completer.words.append("access-scope")
        self.completer.words.append("exec")
        self.completer.words.append("revshell")
        self.completer.words.append("everything")
        self.completer.words.append("allowed")
        self.completer.words.append("priv")
        self.completer.words.append("and")
        self.completer.words.append("hostpid")
        self.completer.words.append("hostpath")
        self.completer.words.append("hostnetwork")
        self.completer.words.append("hostipc")
        self.completer.words.append("nothing")
        self.completer.words.append("pod")
        self.completer.words.append("cronjob")
        self.completer.words.append("deamonset")
        self.completer.words.append("deployment")
        self.completer.words.append("job")
        self.completer.words.append("replicaset")
        self.completer.words.append("replicationcontroller")
        self.completer.words.append("statefulset")
        self.completer.words.append("exit")
        self.completer.words.append("back")

    def add_corrections(self):
        self.corrections = {
            "k": "apply -f",
            "get": self.local_env.get_resource_path(),
            "everything": "everything-allowed",
            "priv-": "priv-and-hostpid",
            "nothing": "nothing-allowed",
            "replication": "replicationcontroller",
        }
        
        