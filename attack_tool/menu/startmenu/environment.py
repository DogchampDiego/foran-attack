import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

class Environment(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.ENVIRONMENT, MenuState.ENVIRONMENT)
        self.command_mapping = {
            "1": self.todo,
            "2": self.todo,
            "3": self.todo,
        }
        
    def back(self):
        self.global_var.pop_menu_tree()
        from menu.startmenu.start import Start
        return Start()

    # InputHandle Methods
    def todo(self):
        return Environment()
