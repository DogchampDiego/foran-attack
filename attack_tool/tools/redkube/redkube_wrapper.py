from tools.base_classes.wrapper_base import Wrapper
from environment.global_const import GlobalVariables
import help.helper as help
class RedKubeWrapper(Wrapper):
    def __init__(self,env):
        if help.check_python_interpreter != "error":
            self.command = help.check_python_interpreter()
        self.sudo = False
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env
        self.cwd = GlobalVariables.get_instance().get_tool_non_bin_dir() + "red-kube"
        self.main = "main.py"

    # Info
    def help(self):
        cmd = [self.main,'-h']

        return self._execute_command(cmd,False,cwd_path=self.cwd)
        
    def show_tactics (self):
        cmd = [self.main,'--show_tactics']
        return self._execute_command(cmd,False,cwd_path=self.cwd)
    
    def run_attack(self,tactic):
        if self.env.get_mode() == "passive":
            print("For active mode use 'set mode active'")
        if self.env.get_mode() == "active":
            print("For passive mode use 'set mode passive'")
        cmd = [self.main,'--mode', self.env.get_mode(), '--tactic',tactic]
        
        return self._execute_command(cmd,False,cwd_path=self.cwd)
    