from environment.global_const import GlobalVariables
from help.file_name_generator import gen_file_name
from tools.base_classes.wrapper_base import Wrapper

class CdkWrapper(Wrapper):

    def __init__(self, env):
        self.command = 'cdk'
        self.sudo = True
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env

    def help(self):
        cmd = ['--help']	
        return cmd
    
    def _init(self):
        pass
    
    def list_exploits(self):
        cmd = ['run', '--list']
        return self._generate_command(cmd)
    
    def evaluate(self):
        cmd = ['evaluate']
        return self._generate_command(cmd)
    
    def evaluate_full(self):
        cmd = ['evaluate']
        return self._generate_command(cmd, full=True)
    
    def tool(self, tool, tool_args):
        cmd = ['']
        if tool in self.env.tool_list:
            self.env.set_tool(tool)
            cmd.append(self.env.get_tool())
            cmd.append(tool_args)
        else:
            print("ERROR: Tool not supported.")
            return
        return self._generate_command(cmd)
    
    def exploit(self, exploit, exploit_args):
        cmd = ['run']
        if exploit in self.env.exploit_list:
            self.env.set_exploit(exploit)
            cmd.append(self.env.get_exploit())
            cmd.append(exploit_args)
        else:   
            print("ERROR: Exploit not supported.")
            return
        return self._generate_command(cmd)
    
    def auto_escape(self, cmd_on_target):
        cmd = ['auto-escape', cmd_on_target]
        return self._generate_command(cmd)
    
    def _generate_command(self, cmd, full=False, tool=False):
        if 'evaluate' in cmd and full:
            cmd.append('--full')
        if  'tool' in cmd:
            pass
        return cmd