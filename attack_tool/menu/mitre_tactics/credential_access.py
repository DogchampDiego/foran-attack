import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu
from environment.global_const import GlobalVariables

from tools.kubehunter.kubehunter import Kubehunter
from tools.redkube.redkube import RedKube
from tools.kdigger.kdigger import KDigger
from tools.stratusred.Stratusred import Stratusred
from tools.cdk.Cdk import Cdk

from testing.kubernetes.credential_access.list_k8s_secrets import ListK8sSecrets
from testing.kubernetes.credential_access.application_credentials_configuration_file import ApplicationCredentialsConfigurationFile

class CredentialAccess(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.CREDENTIAL_ACCESS,MenuState.CREDENTIAL_ACCESS)

        if self.global_var.get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            self.command_mapping = {
                "1": self.stratusred,
                "2": self.cdk,
                "3": self.kubehunter,
                "4": self.red_kube,
                "5": self.kdigger,
            }
        elif self.global_var.get_menu_tree()[-2] == MenuState.KUBERNETES:
            self.command_mapping = {
                "1": self.list_k8s_secrets,
                "2": self.access_container_service_account,
                "3": self.applications_credentials_in_configuration_files,
            }
        GlobalVariables.get_instance().get_env().set_attack_phase("Credential Access")
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
    
    # InputHandle Methods Test
    def list_k8s_secrets(self):
        ListK8sSecrets("List K8s secrets").run_testcase()
        return CredentialAccess()

    def access_container_service_account(self):
        ListK8sSecrets("Access Container Service Account").run_testcase()
        return CredentialAccess()

    def applications_credentials_in_configuration_files(self):
        ApplicationCredentialsConfigurationFile().run_testcase()
        return CredentialAccess()    
