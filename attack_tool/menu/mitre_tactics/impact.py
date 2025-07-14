import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter

from testing.kubernetes.impact.data_destruction import DataDestruction

class Impact(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.IMPACT,MenuState.IMPACT)

        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.kubehunter,
            }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.data_destruction,
                "2": self.ddos,
                "3": self.ressource_highjacking,

            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Impact")

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
    def kubehunter(self):
        return Kubehunter()
    
    # InputHandle Methods Test
    def data_destruction(self):
        DataDestruction().run_testcase()
        return Impact()
    
    def ddos(self):
        return Impact()
    
    def ressource_highjacking(self):
        return Impact()