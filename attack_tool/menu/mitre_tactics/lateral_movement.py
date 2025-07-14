import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter
from tools.redkube.redkube import RedKube
from tools.kdigger.kdigger import KDigger
from tools.cdk.Cdk import Cdk

from testing.kubernetes.lateral_movement.cluster_internal_networking import ClusterInternalNetworking
from testing.kubernetes.lateral_movement.core_dns_poisoning import CoreDNSPoisoning



class LateralMovement(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.LATERAL_MOVEMENT,MenuState.LATERAL_MOVEMENT)
        
        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.cdk,
                "2": self.kubehunter,
                "3": self.kdigger,
            }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.cluster_internal_networking,
                "2": self.coreDNS_spoisoning,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Lateral Movement")
    
    def back(self):
        self.global_var.pop_menu_tree()
        GlobalVariables.get_instance().get_env().set_variable_to_default("_attack_phase")
        if self.global_var.get_menu_tree()[-1] == MenuState.ATTACK_PHASE:
            from menu.startmenu.attackphase import AttackPhase
            return AttackPhase()
        elif self.global_var.get_menu_tree()[-1] == MenuState.KUBERNETES:
            from menu.testing.kubernetes import Kubernetes
            return Kubernetes()

    # InputHandle Methods Phase
    def kubehunter(self):
        return Kubehunter()
    
    def red_kube(self):
        return RedKube()
    
    def kdigger(self):
        return KDigger()
    
    def cdk(self):
        return Cdk()

    # InputHandle Methods Test
    def cluster_internal_networking(self):
        ClusterInternalNetworking().run_testcase()
        return LateralMovement()
    
    def coreDNS_spoisoning(self):
        CoreDNSPoisoning().run_testcase()
        return LateralMovement()
