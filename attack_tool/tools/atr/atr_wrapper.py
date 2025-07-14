import subprocess
import help.helper as help

class ATRWrapper:
    def __init__(self):

        if help.check_python_interpreter != "error":
            self.command = help.check_python_interpreter()
            self.command = self.command + ' /opt/tools/red-kube/main.py'
        self.final_command = None
    # Info
    def help(self):
        cmd = self.command + " -h"
        return self._execute_command(cmd)
        
    def show_tactics (self):
        cmd = self.command + " --show_tactics"
        return self._execute_command(cmd)
    
    def run_attack(self, mode,tactic):
        cmd = self.command + " --mode " + mode + " --tactic " + tactic + " --cleanup"
        return self._execute_command(cmd)
    
    # Helper
    def __methodnames__(self):
         return [method_name for method_name in dir(ATRWrapper) if callable(getattr(ATRWrapper, method_name)) and not method_name.startswith("_")]
    
    def _execute_command(self, cmd):
        output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(output.stdout)
        self.final_command = cmd
        return output 