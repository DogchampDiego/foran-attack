import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

from menu.startmenu.attackphase import AttackPhase
from menu.startmenu.tools import Tools
from menu.startmenu.demonstrator import Demonstrator
from menu.startmenu.environment import Environment
from menu.startmenu.reporting import Reporting
from menu.startmenu.config import Config
from menu.startmenu.container import Container
from menu.startmenu.testing import Testing

class Start(Menu):

    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.START,MenuState.START)
        self.command_mapping = {
            "1": self.attack_phase,
            "2": self.tools,
            "3": self.demonstrator,
            "4": self.environment,
            "5": self.reporting,
            "6": self.config,
            "7": self.container,
            "8": self.testing,
        }
        
    def back(self):
        print("Cant go back further back!")
        return self
    
    # InputHandle Methods
    def attack_phase(self):
        return AttackPhase()
    def tools(self):
        return Tools()
    def demonstrator(self):
        return Demonstrator()
    def environment(self):
        return Environment()
    def reporting(self):
        return Reporting()
    def config(self):
        return Config()
    def container(self):
        return Container()
    def testing(self):
        return Testing()
    