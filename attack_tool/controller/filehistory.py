from prompt_toolkit.history import FileHistory

class ConditionalFileHistory(FileHistory):
    def __init__(self, filename, save_condition=False):
        super().__init__(filename)
        self.save_condition = save_condition

    def append_string(self, string):
        if self.save_condition:
            super().append_string(string)
            self.save_condition = False
            
    def set_save_condition(self, condition):
        self.save_condition = condition
