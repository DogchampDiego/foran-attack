import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

import tools.mtkpi.mtkpi as mtkpi
import tools.hackercontainer.HackerContainer as hackercontainer

class Container(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.CONTAINER,MenuState.CONTAINER)
        self.command_mapping = {
            "1": self.mtkpi,
            "2": self.hackercontainer,
        }

    def back(self):
        self.global_var.pop_menu_tree()
        from menu.startmenu.start import Start
        return Start()
    
    # InputHandle Methods
    def mtkpi(self):
        return mtkpi.MTKPI()
    
    def hackercontainer(self):  
        hackercontainer.HackerContainer()
        return Container()