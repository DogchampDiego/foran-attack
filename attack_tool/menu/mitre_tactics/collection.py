import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter
from tools.redkube.redkube import RedKube
from tools.kdigger.kdigger import KDigger
from tools.stratusred.Stratusred import Stratusred
from tools.cdk.Cdk import Cdk

class Collection(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.COLLECTION,MenuState.COLLECTION)
    
        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.stratusred,
                "2": self.cdk,
                "3": self.kubehunter,
                "4": self.red_kube,
                "5": self.kdigger,
            }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.todo,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Collection")
        
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
    
    def red_kube(self):
        return RedKube()
    
    def kdigger(self):
        return KDigger()

    def stratusred(self):
        return Stratusred()
    
    def cdk(self): 
        return Cdk()
    
    # InputHandle Methods Test
    def todo(self):
        return Collection()