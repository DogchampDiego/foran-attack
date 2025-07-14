from testing.testing import Testing
import time

class ApplicationCredentialsConfigurationFile(Testing):
    def __init__(self):
        super().__init__()
        self.mitre_tactic = "TA0006"
        self.mitre_technique = "T1552"
        self.microsoft_technique = "MS-TA9027"
        
        self.name = "Applications credentials in configuration files"
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "postgres-db-pod"
            },
            "spec": {
                "containers": [
                    {
                        "image": "postgres",
                        "name": "postgres-db-pod",
                        "env": [
                            {
                                "name": "POSTGRES_PASSWORD",
                                "value": "FORANisFUN"
                            }
                        ]
                    }
                ]
            }
        }
        
    def run_attack(self):
        if self.check_install_kubectl():   
            # Creating Pod postgres-db-pod
            print("# Creating Pod postgres-db with sensitive environment variables configured (Password)...")
            self.kubectl_create_file("postgres-db-pod.yaml", self.pod)
            self.kubectl_apply("postgres-db-pod.yaml")
        
            while not self.kubectl_is_pod_ready("postgres-db-pod"):
                time.sleep(1)
            
            print("# Show sensitive environment variables of the container...")
            output, error = self.kubectl_describe("pod", "postgres-db-pod")
            print(output)
            password = self.extract_postgres_password(output)
            print(f"# POSTGRES_PASSWORD: {password}")
            
            if self.error:
                print("An Error has occured: " + error)
            else:
                self.output["env_variables"] = output
                self.output["password"] = password

            # Cleanup
            self.cleanup()

    def extract_postgres_password(self, describe_output):
        lines = describe_output.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("POSTGRES_PASSWORD:"):
                return line.split(":", 1)[1].strip()
        return None
    
    def cleanup(self):
        # Delete Pod privilege-pod
        print("\n# Deleting Pod postgres-db-pod...")
        self.kubectl_delete("postgres-db-pod")
        
        print("\n# Deleting postgres-db-pod.yaml...")
        self.delete_file("postgres-db-pod.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass