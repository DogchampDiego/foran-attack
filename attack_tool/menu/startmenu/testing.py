import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

from menu.testing.kubernetes import Kubernetes

class Testing(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.TESTING, MenuState.TESTING)
        self.command_mapping = {
            "1": self.kubernetes,
            "2": self.openran,
        }
        
    def back(self):
        self.global_var.pop_menu_tree()
        from menu.startmenu.start import Start
        return Start()

    # InputHandle Methods
    def kubernetes(self):
        return Kubernetes()

    def openran(self):
        return Testing()
