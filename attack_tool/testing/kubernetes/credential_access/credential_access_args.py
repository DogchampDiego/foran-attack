from testing.testing_args import TestingArgs

from testing.kubernetes.credential_access.list_k8s_secrets import ListK8sSecrets
from testing.kubernetes.credential_access.application_credentials_configuration_file import ApplicationCredentialsConfigurationFile

class CredentialAccessArgs(TestingArgs):
    def __init__(self):
        super().__init__()
        self.row = [
            ["list_k8s_secrets", "List K8s Secrets"],
            ["application_credentials_configuration_file", "Application Credentials Configuration File"],
            ["access_container_service_account", "Access Container Service Account"]
        ]
    
    def handle_testcase_tactic(self, technique):
        if technique == "list_k8s_secrets":
            ListK8sSecrets("List K8s secrets").run_testcase()
        elif technique == "access_container_service_account":
            ListK8sSecrets("Access Container Service Account").run_testcase()
        elif technique == "application_credentials_configuration_file":
            ApplicationCredentialsConfigurationFile().run_testcase()
        else:
            print("Invalid technique")
            return
