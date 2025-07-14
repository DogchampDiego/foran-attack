from testing.testing import Testing

class AccessK8sAPIServer(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Access the K8s API server"
        self.mitre_tactic = "TA0007"
        self.mitre_technique = "T1613"
        self.microsoft_technique = "MS-TA9030"
    def cleanup(self):
        pass

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass