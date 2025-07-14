import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter
from tools.kdigger.kdigger import KDigger
from tools.cdk.Cdk import Cdk
from tools.stratusred.Stratusred import Stratusred
from tools.badpods.Badpods import Badpods

from testing.kubernetes.execution.bash_cmd_in_container import BashCmdContainer
from testing.kubernetes.execution.new_container import NewContainer
from testing.kubernetes.execution.application_exploit import ApplicationExploit
from testing.kubernetes.execution.ssh_inside_container import SSHServerContainer
from testing.kubernetes.execution.sidecar_injection import SidecarInjection

class Execution(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.EXECUTION,MenuState.EXECUTION)

        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.stratusred,
                "2": self.cdk,
                "3": self.kubehunter,
                "4": self.kdigger,
                "5": self.badpods,
        }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.exec_container,
                "2": self.new_container,
                #"3": self.rce,
                "3": self.ssh_inside_container,
                #"5": self.side_car_injection,
                "4": self.bash_shell,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Execution")
        
    def back(self):
        self.global_var.pop_menu_tree()
        GlobalVariables.get_instance().get_env().set_variable_to_default("_attack_phase")
       
        if self.global_var.get_menu_tree()[-1] == MenuState.ATTACK_PHASE:
            from menu.startmenu.attackphase import AttackPhase
            return AttackPhase()
        elif self.global_var.get_menu_tree()[-1] == MenuState.KUBERNETES:
            from menu.testing.kubernetes import Kubernetes
            return Kubernetes()

    # InputHandle Methods Phase
    def kubehunter(self):
        return Kubehunter()
    
    def kdigger(self):
        return KDigger()
    
    def cdk(self):
        return Cdk()
    
    def stratusred(self):
        return Stratusred()
    
    def badpods(self):
        return Badpods()
    
    # InputHandle Methods Test
    def exec_container(self):
        BashCmdContainer().run_testcase()
        return Execution()
    
    def new_container(self):
        NewContainer().run_testcase()
        return Execution()
    
    def rce(self):
        ApplicationExploit().run_testcase()
        return Execution()
    
    def ssh_inside_container(self):
        SSHServerContainer().run_testcase()
        return Execution()
    
    def side_car_injection(self):
        SidecarInjection().run_testcase()
        return Execution()
    
    def bash_shell(self):
        BashCmdContainer().run_testcase()
        return Execution()