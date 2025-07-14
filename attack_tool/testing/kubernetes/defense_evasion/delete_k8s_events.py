from testing.testing import Testing

class DeleteK8sEvents(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Delete k8s events"
        self.mitre_tactic = "TA0005"
        self.mitre_technique = "T1070"
        self.microsoft_technique = "MS-TA9022"
        
    def run_attack(self):
        if self.check_install_kubectl():   
            
            # Creating K8S Events
            print("# Deleting the Kubernetes events in all namespaces...")
            output, error = self.kubectl_delete(name = None,ressource_type="events", all=True, add_command=True)
            
            if self.error:
                print("An Error has occured: " + error)
            else:
                self.output["delete_k82_events"] = output
            
    def cleanup(self):
        pass

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass