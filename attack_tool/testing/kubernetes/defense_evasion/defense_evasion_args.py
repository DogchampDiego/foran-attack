from testing.testing_args import TestingArgs

from testing.kubernetes.defense_evasion.delete_k8s_events import DeleteK8sEvents
from testing.kubernetes.defense_evasion.pod_container_name_similarity import PodContainerNameSimilarity
from testing.kubernetes.defense_evasion.clear_container_logs import ClearContainerLogs

class DefenseEvasionArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["delete_k8s_events", "Delete K8s Events"],
            ["pod_container_name_similarity", "Pod Container Name Similarity"],
            ["clear_container_logs", "Clear Container Logs"]
        ]
    
    def handle_testcase_tactic(self, technique):
        if technique == "delete_k8s_events":
            DeleteK8sEvents().run_testcase()
        elif technique == "pod_container_name_similarity":
            PodContainerNameSimilarity().run_testcase()
        elif technique == "clear_container_logs":
            ClearContainerLogs().run_testcase()
        else:
            print("Invalid technique")