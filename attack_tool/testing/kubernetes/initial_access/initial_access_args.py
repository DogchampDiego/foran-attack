from testing.testing_args import TestingArgs

from testing.kubernetes.initial_access.kubeconfig import Kubeconfig
from testing.kubernetes.initial_access.exposed_sensitive_interfaces import ExposeSensitiveInterfaces

class InitialAccessArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["kubeconfig", "Download kubeconfig file from Kubernetes cluster"],
            ["exposed_sensitive_interfaces", "Expose sensitive interfaces"]
        ]
        
    def handle_testcase_tactic(self, technique):
        if technique == "kubeconfig":
            Kubeconfig().run_testcase()
        elif technique == "exposed_sensitive_interfaces":
            #ExposeSensitiveInterfaces().run_testcase()
            print("TODO")
        else:
            print("Invalid technique")
            