from tools.badpods.BadpodsEnv import BadpodsEnv
from tools.badpods.BadpodsWrapper import BadpodsWrapper
from tools.base_classes.args_base import Args

from tools.base_classes.pod_deployment import DeployInPod

from environment.global_const import GlobalVariables

class BadpodsArgs(Args):

    def __init__(self):
        super().__init__()
        self.global_var = GlobalVariables.get_instance()
        self.local_env = BadpodsEnv()
        self.badpods_wrapper = BadpodsWrapper(self.local_env)
        self.row = [
            ["launch", "Launch current config: " + self.local_env.get_resource() + " access " + self.local_env.get_access_scope()],
            ["clean", "Remove all BadPods"],
            ["status", "Show status of BadPods"],
            ["verbose", "Show verbose information of BadPods (YAML)"],
            ["pod-everything", "Launch " + self.local_env.get_resource() + " access everything-allowed"],
            ["pod-everything-revshell", "Launch " + self.local_env.get_resource() + " access everything-allowed and reverse shell"],
            ["pod-priv-and-hostpid", "Launch " + self.local_env.get_resource() + " access priv-and-hostpid"],
            ["pod-priv", "Launch " + self.local_env.get_resource() + " access priv"],
            ["pod-hostpath", "Launch " + self.local_env.get_resource() + " access hostpath"],
            ["pod-hostpid", "Launch " + self.local_env.get_resource() + " access hostpid"],
            ["pod-hostnetwork", "Launch " + self.local_env.get_resource() + " access hostnetwork"],
            ["pod-hostipc", "Launch " + self.local_env.get_resource() + " access hostipc"],
            ["pod-nothing", "Launch " + self.local_env.get_resource() + " access nothing-allowed"],
            ["resource", "List available resources"],
            ["access-scope", "List available access scopes"],
            ["type", "List available types"],
        ]
       
    def handle_args(self, args, param = None):

        if param:
            for param_value in param:
                # Each param_value would look like "key=value"
                param, value = param_value.split("=", 1)
                
                if param == "ip":
                    self.local_env.set_ip(value)
                if param == "subnet":
                    self.local_env.set_subnet(value)
                if param == "type":
                    self.local_env.set_type(value)
                if param == "access_scope":
                    self.local_env.set_access_scope(value)
                if param == "resource_path":
                    self.local_env.set_resource_path(value)
                if param == "resource":
                    self.local_env.set_resource(value)
                if param == "base_path":
                    self.local_env.set_base_path(value)
                if param == "revshell_port":
                    self.local_env.set_revshell_port(value)
                if param == "revshell_ip": 
                    self.local_env.set_revshell_ip(value)
                
        try:
            if args == "launch":
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch())
                self.parse_output = True
            elif args == "clean":
                self.badpods_wrapper._execute_command(self.badpods_wrapper.clean())
                self.parse_output = False
                return
            elif args == "status":
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.status())
                self.parse_output = False
                return
            elif args == "verbose":
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.status_verbose())
                self.parse_output = False
                return
            elif args == "pod-everything":
                # Launch pod with everything-allowed access
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("exec", "everything-allowed", "pod"))
                self.parse_output = True
            elif args == "pod-everything-revshell":
                # Launch pod with everything-allowed access and reverse shell
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("revshell", "everything-allowed", "pod"))
                self.parse_output = True
            elif args == "pod-priv-and-hostpid":
                # Launch pod with priv-and-hostpid access
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("exec", "priv-and-hostpid", "pod"))
                self.parse_output = True
            elif args == "pod-priv":
                # Launch pod with privileged access
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("exec", "priv", "pod"))
                self.parse_output = True
            elif args == "pod-hostpath":
                # Launch pod with hostpath access
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("exec", "hostpath", "pod"))
                self.parse_output = True
            elif args == "pod-hostpid":
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("exec", "hostpid", "pod"))
                self.parse_output = True    
            elif args == "pod-hostnetwork":
                # Launch pod with hostnetwork access
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("exec", "hostnetwork", "pod"))
                self.parse_output = True
            elif args == "pod-hostipc":
                # Launch pod with hostipc access
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("exec", "hostipc", "pod"))
                self.parse_output = True
            elif args == "pod-nothing":
                # Launch pod with nothing-allowed access
                self.out = self.badpods_wrapper._execute_command(self.badpods_wrapper.launch_custom("exec", "nothing-allowed", "pod"))
                self.parse_output = True
            elif args == "resource":
                # List available resources
                print(self.local_env.resoure_list)
                self.parse_output = False
                return
            elif args == "access-scope":
                # List available access scopes
                print(self.local_env.access_scope_list)
                self.parse_output = False
                return
            elif args == "type":
                # List available types
                print(self.local_env.type_list)
                self.parse_output = False
                return
            elif args == "help":
                # Show help information
                self.table.print_table(self.column, self.row)
                self.parse_output = False
                return
            elif args == "options":
                # Show help information
                self.table.print_table(self.column, self.local_env.get_env_dict())
                self.parse_output = False
                return
            else:
                return None, None, None, False
        except Exception as e:
            print(e)
            return None, None, None, False

        return self.out, self.badpods_wrapper.final_command, self.local_env, self.parse_output
