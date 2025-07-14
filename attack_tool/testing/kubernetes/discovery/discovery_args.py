from testing.testing_args import TestingArgs

from testing.kubernetes.discovery.nerwork_mapping import NetworkMapping

class DiscoveryArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["network_mapping", "Network Mapping"]
        ]
    
    def handle_testcase_tactic(self, technique):
        if technique == "network_mapping":
            NetworkMapping().run_testcase()
        else:
            print("Invalid technique")