from testing.testing_args import TestingArgs

from testing.kubernetes.impact.data_destruction import DataDestruction

class ImpactArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["data_destruction", "Data Destruction"]
        ]
    
    def handle_testcase_tactic(self, technique):
        if technique == "data_destruction":
            DataDestruction().run_testcase()
        else:
            print("Invalid technique")