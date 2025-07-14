import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.nmap.Nmap import Nmap
from tools.kubescape.Kubescape import Kubescape
from tools.trivy.Trivy import Trivy
from tools.rakkess.Rakkess import Rakkess
from tools.cdk.Cdk import Cdk

from testing.kubernetes.discovery.nerwork_mapping import NetworkMapping

class Discovery(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.DISCOVERY,MenuState.DISCOVERY)

        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.nmap,
                "2": self.kubescape,
                "3": self.trivy,
                "4": self.rakkess,
                "5": self.cdk,
            }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.access_the_k8s_API_server,
                "2": self.network_mapping,
                "3": self.instance_metadata_API,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Discovery")

    def back(self):
        self.global_var.pop_menu_tree()
        GlobalVariables.get_instance().get_env().set_variable_to_default("_attack_phase")
        if self.global_var.get_menu_tree()[-1] == MenuState.ATTACK_PHASE:
            from menu.startmenu.attackphase import AttackPhase
            return AttackPhase()
        elif self.global_var.get_menu_tree()[-1] == MenuState.KUBERNETES:
            from menu.testing.kubernetes import Kubernetes
            return Kubernetes()
    
    # InputHandle Methods
    def nmap(self):
        return Nmap()
    
    def kubescape(self):
        return Kubescape()
    
    def trivy(self):
        return Trivy()
    
    def rakkess(self):
        return Rakkess()
    
    def cdk(self):
        return Cdk()
    
    # InputHandle Methods Test
    def access_the_k8s_API_server(self):
        return Discovery()
    
    def network_mapping(self):
        NetworkMapping().run_testcase()
        return Discovery()
    
    def instance_metadata_API(self):
        return Discovery()
