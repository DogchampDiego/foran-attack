from testing.testing_args import TestingArgs

from testing.kubernetes.persistence.backdoor_container import BackdoorContainer
from testing.kubernetes.persistence.writeable_hostpath import WriteableHostpath
from testing.kubernetes.persistence.kubernetes_cronjob import KubernetesCronJob

class PersistenceArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["backdoor_container", "Backdoor container"],
            ["writeable_hostpath", "Writeable hostpath"],
            ["kubernetes_cronjob", "Kubernetes cronjob"]
        ]
    
    def handle_testcase_tactic(self, technique):
        if technique == "backdoor_container":
            BackdoorContainer().run_testcase()
        elif technique == "writeable_hostpath":
            WriteableHostpath().run_testcase()
        elif technique == "kubernetes_cronjob":
            KubernetesCronJob().run_testcase()
        else:
            print("Invalid technique")