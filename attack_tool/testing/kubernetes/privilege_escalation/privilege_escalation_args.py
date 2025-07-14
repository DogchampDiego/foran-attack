from testing.testing_args import TestingArgs

from testing.kubernetes.privilege_escalation.cluster_admin_binding import ClusterAdminBinding
from testing.kubernetes.privilege_escalation.disable_namespacing import DisableNamespacing
from testing.kubernetes.privilege_escalation.privileged_container import PrivilegedContainer

class PrivilegeEscalationArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["privileged_container", "Privileged Container"],
            ["cluster_admin_binding", "Cluster Admin Binding"],
            ["disable_namespacing", "Disable Namespacing"]
        ]
    
    def handle_testcase_tactic(self, technique):
        if technique == "privileged_container":
            PrivilegedContainer().run_testcase()
        elif technique == "cluster_admin_binding":
            ClusterAdminBinding().run_testcase()
        elif technique == "disable_namespacing":
            DisableNamespacing().run_testcase()
        else:
            print("Invalid technique")