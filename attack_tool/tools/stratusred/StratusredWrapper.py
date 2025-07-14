from environment.global_const import GlobalVariables
from tools.base_classes.wrapper_base import Wrapper

class StratusredWrapper(Wrapper):

    def __init__(self, env):
        self.command = 'stratus'
        self.sudo = False
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env

    def help(self):
        cmd = ['--help']	
        return cmd
    
    def _init(self, platform, tactic):
        if platform in self.env.platform_list and platform != None:
            self.env.set_platform(platform)
        if tactic in self.env.tactic_list and tactic != None:
            self.env.set_tactic(tactic)
    
    def clean(self):
        cmd = ['cleanup --force --all']
        return self._generate_command(cmd)
    
    def list(self, platform, tactic):
        cmd = ['list']
        self._init(platform, tactic)
        if tactic != None:
            cmd.append('--mitre-attack-tactic')
            cmd.append(tactic)
        return self._generate_command(cmd, tactic=True)
    
    def detonate(self, platform, tactic, technique, clean=True):
        cmd = ['detonate']
        self._init(platform, tactic)
        self.env.set_technique(technique)
        cmd.append(self._generate_technique(self.env.get_tactic(), self.env.get_technique()))
        return self._generate_command(cmd, cleanup=clean)
    
    def show(self, platform, tactic, technique):
        cmd = ['show']
        self._init(platform, tactic)
        self.env.set_technique(technique)
        cmd.append(self._generate_technique(self.env.get_tactic(), self.env.get_technique()))
        return self._generate_command(cmd)

    def _generate_command(self, cmd, tactic=False, cleanup=False):
        if  'list' in cmd:
            cmd.append('--platform')
            cmd.append(self.env.get_platform())
        if 'detonate' in cmd and cleanup:
            cmd.append('--cleanup')
        return cmd

    def _generate_technique(self, tactic, technique):
        if tactic in self.env.tactic_list and technique in self.env.technique_list:
            technique = 'k8s.' + tactic + '.' + technique
            print("Generate technique: " + technique)
            return technique
        else:
            print("ERROR: Faulty tactic or technique provided.")
            return
        
    def cred_secrets(self):
        cmd = ['detonate']
        self._init('kubernetes', 'credential-access')
        self.env.set_technique('dump-secrets')
        cmd.append(self._generate_technique(self.env.get_tactic(), self.env.get_technique()))
        return self._generate_command(cmd, cleanup=True)
    
    def persist_client_cert(self):
        cmd = ['detonate']
        self._init('kubernetes', 'persistence')
        self.env.set_technique('create-client-certificate')
        cmd.append(self._generate_technique(self.env.get_tactic(), self.env.get_technique()))
        return self._generate_command(cmd, cleanup=True)
    
    def privesc_privileged_pod(self):
        cmd = ['detonate']
        self._init('kubernetes', 'privilege-escalation')
        self.env.set_technique('privileged-pod')
        cmd.append(self._generate_technique(self.env.get_tactic(), self.env.get_technique()))
        return self._generate_command(cmd, cleanup=True)