from testing.testing import Testing

class ResourceHijacking(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Ressource Hijacking"
        self.mitre_tactic = "TA0040"
        self.mitre_technique = "T1496"
        self.microsoft_technique = "MS-TA9039"
        
    def run_attack(self):
        if self.check_install_kubectl():   
            pass

    def cleanup(self):
        pass

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass