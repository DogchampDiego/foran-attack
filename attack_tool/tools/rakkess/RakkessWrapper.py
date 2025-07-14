from environment.global_const import GlobalVariables
from tools.base_classes.wrapper_base import Wrapper

class RakkessWrapper(Wrapper):

    def __init__(self, env):
        self.command = 'rakkess'
        self.sudo = False
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env

    def help(self):
        cmd = ['--help']
        return cmd
    
    def _init(self):
        self.env.set_namespace('all')
    
    def cluster(self):
        cmd = ['']
        self._init()
        return cmd
    
    def resource(self):
        cmd = ['resource configmaps']
        temp = self.env.get_resource()
        if temp in self.env.resource_list:
            self.env.set_resource(temp)
            cmd.append(temp)
            cmd.append("--namespace")
            cmd.append("all")
        else:
            print("ERROR: Resource not supported.")
            return
        return cmd
    
    def namespace(self):
        cmd = ['--namespace', self.env.get_namespace()]
        return cmd
    
    
    def user(self):
        cmd = ['--as', self.env.get_user()]
        if self.env.get_namespace():
            cmd.append("--namespace")
            cmd.append(self.env.get_namespace())
        return cmd
 
    def sa(self):
        cmd = ['--sa', self.env.get_service_account()]
        if self.env.get_namespace():
            cmd.append("--namespace")
            cmd.append(self.env.get_namespace())
        return cmd

