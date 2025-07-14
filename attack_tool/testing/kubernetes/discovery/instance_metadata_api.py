from testing.testing import Testing

class InstanceMetadataAPI(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Instance metadata API"
        self.mitre_tactic = "TA0007"
        self.mitre_technique = "T1552.005"
        self.microsoft_technique = "MS-TA9033"
    def cleanup(self):
        pass

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass