import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter
from tools.kdigger.kdigger import KDigger


from testing.kubernetes.initial_access.kubeconfig import Kubeconfig

class InitialAccess(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.INITIAL_ACCESS,MenuState.INITIAL_ACCESS)

        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.kubehunter,
                "2": self.kdigger,
            }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.kubeconfig,
                #"2": self.expose_sensitive_interfaces,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Initial Access")
        
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
    
    def kdigger(self):
        return KDigger()
    
    # InputHandle Methods Test
    def kubeconfig(self):
        # Run Attack and return to InitialAccess
        Kubeconfig().run_testcase()
        
        return InitialAccess()

    def expose_sensitive_interfaces(self):
        return InitialAccess()
    

