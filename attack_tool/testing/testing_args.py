from abc import ABC, abstractmethod
from help.table import Table

class TestingArgs(ABC):
    def __init__(self):
        self.table = Table()
        self.row = []
        self.header = ["Technique", "Description"]
        
    @abstractmethod
    def handle_testcase_tactic(self, technique):
        pass

    def print_testcases(self):
        self.table.print_table(self.header, self.row)