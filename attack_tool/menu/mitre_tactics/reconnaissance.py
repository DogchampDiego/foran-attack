import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

from environment.global_const import GlobalVariables
from tools.redkube.redkube import RedKube
from tools.kdigger.kdigger import KDigger
from tools.nmap.Nmap import Nmap
from tools.kubescape.Kubescape import Kubescape
from tools.trivy.Trivy import Trivy
from tools.cdk.Cdk import Cdk

class Reconnaissance(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.RECONNAISSANCE,MenuState.RECONNAISSANCE)
        self.command_mapping = {
            "1": self.nmap,
            "2": self.kubescape,
            "3": self.trivy,
            "4": self.cdk,
            "5": self.red_kube,
            "6": self.kdigger,
        }
        GlobalVariables.get_instance().get_env().set_attack_phase("Reconnaissance")

    
    def back(self):
        self.global_var.pop_menu_tree()
        GlobalVariables.get_instance().get_env().set_variable_to_default("_attack_phase")
        from menu.startmenu.attackphase import AttackPhase
        return AttackPhase()
    
    
    # InputHandle Methods
    def red_kube(self):
        return RedKube()

    def kdigger(self):
        return KDigger()
    
    def nmap(self):
        return Nmap()
    
    def kubescape(self):
        return Kubescape()
    
    def trivy(self):
        return Trivy()
    
    def cdk(self):
        return Cdk()