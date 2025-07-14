from testing.testing_args import TestingArgs

class CollectionArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = []
    
    def handle_testcase_tactic(self, technique):
        print("No Testcases available for the Tactic Collection.")