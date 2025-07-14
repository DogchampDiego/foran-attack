import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter
from tools.redkube.redkube import RedKube
from tools.kdigger.kdigger import KDigger
from tools.stratusred.Stratusred import Stratusred
from tools.cdk.Cdk import Cdk
from tools.badpods.Badpods import Badpods


from testing.kubernetes.persistence.backdoor_container import BackdoorContainer
from testing.kubernetes.persistence.writeable_hostpath import WriteableHostpath
from testing.kubernetes.persistence.kubernetes_cronjob import KubernetesCronJob

class Persistence(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.PERSISTENCE,MenuState.PERSISTENCE)
        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
            "1": self.stratusred,
            "2": self.badpods,
            "3": self.cdk,
            "4": self.kubehunter,
            "5": self.red_kube,
            "6": self.kdigger,
        }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.backdoor_container,
                "2": self.writable_hostPath_mount,
                "3": self.kubernetes_cronJob,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Persistence")
    
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
    
    def red_kube(self):
        return RedKube()
    
    def kdigger(self):
        return KDigger()
    
    def cdk(self):
        return Cdk()
    
    def stratusred(self):
        return Stratusred()
    
    def badpods(self):
        return Badpods()
    
    # InputHandle Methods Test
    def backdoor_container(self):
        BackdoorContainer().run_testcase()
        return Persistence()
    
    def writable_hostPath_mount(self):
        WriteableHostpath().run_testcase()
        return Persistence()
    
    def kubernetes_cronJob(self):
        KubernetesCronJob().run_testcase()
        return Persistence()
