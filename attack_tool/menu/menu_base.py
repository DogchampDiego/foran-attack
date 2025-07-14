from abc import ABC, abstractmethod
from prompt_toolkit.styles import Style

import help.helper as helper
from environment.global_const import GlobalVariables
from controller.wordcompleter import CustomWordCompleter

# Abstract Base Class for Menu Classes
class Menu(ABC):
    def __init__(self):
        self.custom_style = Style.from_dict({'prompt': 'red'})
        self.prompt_symbol = helper.create_cursor()
        self.global_var = GlobalVariables.get_instance()
        self.completer = CustomWordCompleter(
            [
                "end",
                "exit",
                "back",
                "clear",
            ],
            ignore_case=True,
        )
        
        self.corrections = {
            "bakc": "back",
            "claer": "clear",
            "clera": "clear",
            "exti": "exit",
            "edn": "end",
        }
        self.history = None
        self.command_mapping = None
        
    # Abstract Methods
    def handle_user_input(self, user_input):
        return self.command_mapping.get(user_input, self.invalid_option)()
    
    @abstractmethod
    def back(self):
        pass

    def invalid_option(self):
        print("Invalid option selected.")
        return self
    
    def print_menu_basic(self):
        helper.print_menu()
