import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables


from menu.mitre_tactics.initial_access import InitialAccess
from menu.mitre_tactics.execution import Execution
from menu.mitre_tactics.persistence import Persistence
from menu.mitre_tactics.privilege_escalation import PrivilegeEscalation
from menu.mitre_tactics.defense_evasion import DefenseEvasion
from menu.mitre_tactics.credential_access import CredentialAccess
from menu.mitre_tactics.discovery import Discovery
from menu.mitre_tactics.lateral_movement import LateralMovement
from menu.mitre_tactics.collection import Collection
from menu.mitre_tactics.impact import Impact


class Kubernetes(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.KUBERNETES,MenuState.KUBERNETES)
        self.command_mapping = {
            "1": self.initial_access,
            "2": self.execution,
            "3": self.persistence,
            "4": self.privilege_escalation,
            "5": self.defense_evasion,
            "6": self.credential_access,
            "7": self.discovery,
            "8": self.lateral_movement,
            "9": self.collection,
            "10": self.impact,
        }
        
    def back(self):
        self.global_var.pop_menu_tree()
        from menu.startmenu.testing import Testing
        return Testing()
    
    # InputHandle Methods
    def initial_access(self):
        return InitialAccess()
    
    def execution(self):
        return Execution()
    
    def persistence(self):
        return Persistence()
    
    def privilege_escalation(self):
        return PrivilegeEscalation()
    
    def defense_evasion(self):
        return DefenseEvasion()
    
    def credential_access(self):
        return CredentialAccess()
    
    def discovery(self):
        return Discovery()
    
    def lateral_movement(self):
        return LateralMovement()
    
    def collection(self):
        return Collection()
    
    def impact(self):
        return Impact()
    
    