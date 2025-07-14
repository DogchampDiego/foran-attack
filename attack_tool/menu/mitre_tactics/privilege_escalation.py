import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter
from tools.redkube.redkube import RedKube
from tools.kdigger.kdigger import KDigger
from tools.stratusred.Stratusred import Stratusred
from tools.rakkess.Rakkess import Rakkess
from tools.cdk.Cdk import Cdk
from tools.badpods.Badpods import Badpods


from testing.kubernetes.privilege_escalation.cluster_admin_binding import ClusterAdminBinding
from testing.kubernetes.privilege_escalation.disable_namespacing import DisableNamespacing
from testing.kubernetes.privilege_escalation.privileged_container import PrivilegedContainer

class PrivilegeEscalation(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.PRIVILEGE_ESCALATION,MenuState.PRIVILEGE_ESCALATION)

        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.stratusred,
                "2": self.rakkess,
                "3": self.cdk,
                "4": self.badpods,
                "5": self.kubehunter,
                "6": self.red_kube,
                "7": self.kdigger,
            }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.privileged_container,
                "2": self.cluster_admin_binding,
                "3": self.disable_namespacing,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Privilege Escalation")

    
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
    
    def stratusred(self):
        return Stratusred()
    
    def rakkess(self):
        return Rakkess()
    
    def badpods(self):
        return Badpods()

    # InputHandle Methods Test
    def privileged_container(self):
        PrivilegedContainer().run_testcase()
        return PrivilegeEscalation()
    
    def cluster_admin_binding(self):
        ClusterAdminBinding().run_testcase()
        return PrivilegeEscalation()
    
    def disable_namespacing(self):
        DisableNamespacing().run_testcase()
        return PrivilegeEscalation()