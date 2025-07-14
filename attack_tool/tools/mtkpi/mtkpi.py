import subprocess

import help.helper as helper
from controller.filehistory import ConditionalFileHistory
from state.menu_state import MenuState
from tools.base_classes.tool_base import Tool
from tools.mtkpi.mtpki_env import MTKPIEnv
from tools.mtkpi.mtkpi_wrapper import MTKPIWrapper

class MTKPI(Tool):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.MTKPI, MenuState.MTKPI)

        # Wrapper and Environment Variables
        self.local_env = MTKPIEnv()
        self.wrapper = MTKPIWrapper(self.local_env)

        # Set Tool Name / Tool Version
        self.name = "MTKPI"

        # Command Mapping
        self.command_mapping = {
            "start": self.handle_start,
            "exec": self.handle_exec,
            "command": self.handle_exec_custom
        }
        
        self.command_mapping_db_ignore_db = {
            "clean": self.handle_clean,
            "status": self.handle_status,
            "verbose": self.handle_status_verbose,
        }
        
        # Prompt
        self.history = ConditionalFileHistory(self.global_var.get_base_dir() + "history/.mtkpi_history")
        self.add_corrections()
        self.add_completer()
        self.show_menu = False

        self.column = ["Method", "Description"]
        self.row = [
            ["start", "Start MTKPI pod"],
            ["clean", "Remove MTKPI pod"],
            ["status", "Show status of MTKPI pod"],
            ["exec", "Launch bash shell into pod"],
            ["command", "Execute custom command in pod"],
            ["verbose", "Show verbose information of MTKPI pod (YAML)"]
        ]
        
        # Set the attack phase in menu prompt
        common_elements = set(self.global_var.get_menu_tree()).intersection(set(helper.get_menu_phase()))  
        if common_elements:
            phase = next(iter(common_elements))
            self.env.set_attack_phase(phase.name.lower().capitalize())

    def check_installed(self):
        try:
            cmd = ['ls', self.local_env.get_base_path()]
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"MTKPI not installed.")
            return False
        
    def install_tool(self):
        path = self.global_var.get_base_dir() + "tools/mtkpi/install_mtkpi.sh"
        print("Installation script path MTKPI: ", path)
        subprocess.run(["sudo", "chmod", "+x", path], check=True)
        print(f"Script '{path}' is now executable.")
        subprocess.call(["bash", path, self.global_var.get_tool_non_bin_dir(), self.global_var.get_base_dir()])

    def tool_version(self):
        return "No version available."

    # InputHandle Methods
    def handle_start(self):
        return self.wrapper._execute_command(self.wrapper.start())
    
    def handle_status(self):
        return self.wrapper._execute_command(self.wrapper.status())
    
    def handle_status_verbose(self):
        return self.wrapper._execute_command(self.wrapper.status_verbose())
    
    def handle_clean(self):
        return self.wrapper._execute_command(self.wrapper.clean())
    
    def handle_exec(self):
        return self.wrapper._execute_command(self.wrapper.exec())
    
    # TODO Parse command passed via menu to wrapper (check controller for user_input)
    def handle_exec_custom(self):
        return self.wrapper._execute_command(self.wrapper.exec_custom(self.user_raw))
    
    def add_completer(self):
        self.completer.words.append("clean")
        self.completer.words.append("exec")
        self.completer.words.append("status")
        self.completer.words.append("start")
        self.completer.words.append("exit")
        self.completer.words.append("back")
        self.completer.words.append("verbose")
        self.completer.words.append("command")

    def add_corrections(self):
        self.corrections = {
            "k": "apply -f",
            "get": self.local_env.get_resource_path()
        }
        
        