import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

from menu.mitre_tactics.privilege_escalation import PrivilegeEscalation 
from menu.mitre_tactics.defense_evasion import DefenseEvasion
from menu.mitre_tactics.persistence import Persistence
from menu.mitre_tactics.execution import Execution
from menu.mitre_tactics.discovery import Discovery
from menu.mitre_tactics.credential_access import CredentialAccess
from menu.mitre_tactics.initial_access import InitialAccess
from menu.mitre_tactics.lateral_movement import LateralMovement
from menu.mitre_tactics.collection import Collection
from menu.mitre_tactics.impact import Impact
from menu.mitre_tactics.reconnaissance import Reconnaissance
from menu.mitre_tactics.command_control import CommandControl
from menu.mitre_tactics.exfiltration import Exfiltration

class AttackPhase(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.ATTACK_PHASE,MenuState.ATTACK_PHASE)
        self.command_mapping = {
            "1": self.reconnaissance,
            "2": self.initial_access,
            "3": self.execution,
            "4": self.persistence,
            "5": self.privilege_escalation,
            "6": self.defense_evasion,
            "7": self.credential_access,
            "8": self.discovery,
            "9": self.lateral_movement,
            "10": self.collection,
            "11": self.command_control,
            "12": self.exfiltration,
            "13": self.impact,
        }

        
    def back(self):
        self.global_var.pop_menu_tree()
        from menu.startmenu.start import Start
        return Start()
    
    # InputHandle Methods
    def reconnaissance(self):
        return Reconnaissance()
    
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
    
    def command_control(self):
        return CommandControl()
    
    def exfiltration(self):
        return Exfiltration()

    def impact(self):
        return Impact()
    