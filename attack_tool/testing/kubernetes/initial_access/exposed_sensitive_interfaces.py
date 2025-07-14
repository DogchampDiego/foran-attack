from testing.testing import Testing

class ExposeSensitiveInterfaces(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Exposed sensitive interfaces"
        self.mitre = "T1190"
    def cleanup(self):
        pass

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass
    
    def run_attack(self):
        self.check_install_kubectl()
        