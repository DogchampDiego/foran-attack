from testing.testing_args import TestingArgs

from testing.kubernetes.lateral_movement.cluster_internal_networking import ClusterInternalNetworking
from testing.kubernetes.lateral_movement.core_dns_poisoning import CoreDNSPoisoning

class LateralMovementArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["cluster_internal_networking", "Cluster Internal Networking"],
            ["core_dns_poisoning", "Change CoreDNS config"]
        ]
    
    def handle_testcase_tactic(self, technique):
        if technique == "cluster_internal_networking":
            ClusterInternalNetworking().run_testcase()
        if technique == "core_dns_poisoning":
            CoreDNSPoisoning().run_testcase()
        else:
            print("Invalid technique")