import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter
from tools.redkube.redkube import RedKube
from tools.kdigger.kdigger import KDigger
from tools.badpods.Badpods import Badpods

from testing.kubernetes.defense_evasion.delete_k8s_events import DeleteK8sEvents
from testing.kubernetes.defense_evasion.pod_container_name_similarity import PodContainerNameSimilarity
from testing.kubernetes.defense_evasion.clear_container_logs import ClearContainerLogs

class DefenseEvasion(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.DEFENSE_EVASION,MenuState.DEFENSE_EVASION)
        
        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.badpods,
                "2": self.kubehunter,
                "3": self.red_kube,
                "4": self.kdigger,
        }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.delete_k8s_events,
                "2": self.pod_container_name_similarity,
                "3": self.clear_container_logs,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Defense Evasion")
        
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
    
    def badpods(self):
        return Badpods()

    # InputHandle Methods Test
    def delete_k8s_events(self):
        DeleteK8sEvents().run_testcase()
        return DefenseEvasion()
    
    def pod_container_name_similarity(self):
        PodContainerNameSimilarity().run_testcase()
        return DefenseEvasion()
    
    def clear_container_logs(self):
        ClearContainerLogs().run_testcase()
        return DefenseEvasion()