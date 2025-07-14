from testing.testing_args import TestingArgs

from testing.kubernetes.execution.bash_cmd_in_container import BashCmdContainer
from testing.kubernetes.execution.new_container import NewContainer
from testing.kubernetes.execution.application_exploit import ApplicationExploit
from testing.kubernetes.execution.ssh_inside_container import SSHServerContainer
from testing.kubernetes.execution.sidecar_injection import SidecarInjection
from testing.kubernetes.execution.exec_into_container import ExecIntoContainer
from testing.kubernetes.execution.exec_command_in_container import ExecCommandContainer

class ExecutionArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["bash_cmd_in_container", "Run a bash command in a container"],
            ["new_container", "Create a new container"],
            ["application_exploit", "Exploit an application"],
            ["ssh_inside_container", "SSH into a container"],
            ["sidecar_injection", "Inject a sidecar container"],
            ["exec_into_container", "Exec into a container"],
            ["exec_command_in_container", "Exec command in a container (add --value ssh/nslookup/curl)"]
        ]
    
    def handle_testcase_tactic(self, technique, case=None):
        if technique == "bash_cmd_in_container":
            BashCmdContainer().run_testcase()
        elif technique == "new_container":
            NewContainer().run_testcase()
        elif technique == "application_exploit":
            ApplicationExploit().run_testcase()
        elif technique == "ssh_inside_container":
            SSHServerContainer().run_testcase()
        elif technique == "sidecar_injection":
            SidecarInjection()
        elif technique == "exec_into_container":
            BashCmdContainer().run_testcase()
        elif technique == "exec_command_in_container":
            if case:
                ExecCommandContainer().run_testcase(case)
            else:
                print("Please specify what to execute: (SSH/NSLOOKUP/CURL)")
        else:
            print("Invalid technique")