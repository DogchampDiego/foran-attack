from environment.global_const import GlobalVariables
from tools.base_classes.wrapper_base import Wrapper

class FlightsimWrapper(Wrapper):

    def __init__(self, env):
        self.command = 'flightsim'
        self.sudo = True
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env

    def _init(self):
        pass

    def help(self):
        cmd = ['--help']	
        return cmd
    
    def list(self):
        cmd = ['get']
        return self._generate_command(cmd)
    
    def run_custom(self, module):
        cmd = ['run']
        if module == None or module == "":
            self.env.set_module("")
        else:
            self.env.set_module(module)
        return self._generate_command(cmd, dry=self.env.get_dry(), fast=self.env.get_fast(), interface=self.env.get_interface())

    def _generate_command(self, cmd, dry=False, fast=False, interface=False):
        if  'get' in cmd:
            cmd.append(self.env.get_element() + ':' + self.env.get_category())
        if 'run' in cmd and dry:
            cmd.append('--dry')
        # reduce sleep intervals between simulation events
        if 'run' in cmd and fast:
            cmd.append('--fast')
        # network interface or local IP address to use
        if 'run' in cmd and interface:
            cmd.append('--iface')
            cmd.append(self.env.get_ip())
        if 'run' in cmd:
            cmd.append(self.env.get_module())
        return cmd