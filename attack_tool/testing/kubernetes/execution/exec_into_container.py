from testing.testing import Testing

class ExecIntoContainer(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Exec into Container"
        self.mitre = "T1610"
        
    def cleanup(self):
        pass

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass