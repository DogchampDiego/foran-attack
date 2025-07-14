import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.redkube.redkube import RedKube
from tools.flightsim.Flightsim import Flightsim
from tools.stratusred.Stratusred import Stratusred

class Exfiltration(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.EXFILTRATION,MenuState.EXFILTRATION)
        self.command_mapping = {
            "1": self.flightsim,
            "2": self.stratusred,
            "3": self.red_kube,
        }
        GlobalVariables.get_instance().get_env().set_attack_phase("Exfiltration")
        
    def back(self):
        self.global_var.pop_menu_tree()
        GlobalVariables.get_instance().get_env().set_variable_to_default("_attack_phase")
        from menu.startmenu.attackphase import AttackPhase
        return AttackPhase()
    
    # InputHandle Methods
    def red_kube(self):
        return RedKube()
    
    def flightsim(self):
        return Flightsim()
    
    def stratusred(self):
        return Stratusred()
    