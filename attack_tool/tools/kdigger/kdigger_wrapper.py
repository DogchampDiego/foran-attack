import json
from tools.base_classes.wrapper_base import Wrapper

class KdiggerWrapper(Wrapper):
    def __init__(self,env):
        self.command = "kdigger"
        self.env = env
        self.sudo = False
        
    def help(self, command):
        return self.exec_command_on_pod(f"kdigger {command} --help")

    def help_base(self):
        return self.exec_command_on_pod(f"kdigger --help")

    def show_buckets(self):
        return self.exec_command_on_pod(f"kdigger ls")

    def dig(self):
        cmd = ["kdigger","dig"]
        
        if self.env.get_buckets():
            cmd.extend([self.env.get_buckets()])
            
            if self.env.get_buckets() == "admission":
                cmd.append("--admission-create")
            if self.env.get_namespace():
                cmd.extend(["-n", self.env.get_namespace()])
            if self.env.get_side_effects() or self.env.get_buckets() == "admission" or  self.env.get_buckets() == "syscalls":
                cmd.append("--side-effects")
            if self.env.get_kubeconfig():
                cmd.extend(["--kubeconfig", self.env.get_kubeconfig()])
            cmd.extend(["--output", self.env.get_output_format()])
            return self.exec_command_on_pod(" ".join(cmd))
        else:
            print("You need to set a bucket! Use 'buckets' to see all buckets available")
            return None
        
    def dig_all(self):
        return self.exec_command_on_pod("kdigger dig all")

    def generate_pod_template(self):
        cmd = ["kdigger", "gen"]

        if self.env.get_name():
            cmd.append(self.env.get_name())
        if self.env.get_gen_all():
            cmd.append("--all")
        if self.env.get_gen_command():
            cmd.extend(["--command"] + self.env.get_gen_command())
        if self.env.get_gen_fuzz_container():
            cmd.append("--fuzz-container")
        if self.env.get_gen_fuzz_init():
            cmd.append("--fuzz-init")
        if self.env.get_gen_fuzz_pod():
            cmd.append("--fuzz-pod")
        if self.env.get_gen_hostnetwork():
            cmd.append("--hostnetwork")
        if self.env.get_gen_hostpath():
            cmd.append("--hostpath")
        if self.env.get_gen_hostpid():
            cmd.append("--hostpid")
        if self.env.get_namespace():
            cmd.extend(["-n", self.env.get_namespace()])
        if self.env.get_gen_privileged():
            cmd.append("--privileged")
        if self.env.get_gen_tolerations():
            cmd.append("--tolerations")
            
        cmd.extend(["--image", self.env.get_gen_image()])
        cmd.extend(["--output", self.env.get_output_format()])

        return self.exec_command_on_pod(" ".join(cmd))