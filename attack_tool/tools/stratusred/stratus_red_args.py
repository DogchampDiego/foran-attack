from tools.stratusred.StratusredWrapper import StratusredWrapper
from tools.stratusred.StratusredEnv import StratusredEnv
from tools.base_classes.args_base import Args

from tools.base_classes.pod_deployment import DeployInPod

from environment.global_const import GlobalVariables

class StratusArgs(Args):

    def __init__(self):
        super().__init__()
        self.global_var = GlobalVariables.get_instance()
        self.local_env = StratusredEnv()
        self.stratus_wrapper = StratusredWrapper(self.local_env)
        self.row = [
            ["list", "List all attacks"],
            ["cur", "Show information of current technique"],
            ["show <k8s.tactic.technique>", "Show details of specific resource"],
            ["clean", "Revert detonations and clean up infrastructure"],
            ["list-persist", "List all persistence attacks"],
            ["cred-secrets", "Dump secrets of cluster"],
            ["cred-tokens", "Extract serviceaccount tokens of cluster"],
            ["persist-admin-clusterrole", "Persist with admin clusterrole"],
            ["persist-client-cert", "Persist with client certificate"],
            ["persist-create-token", "Persist with serviceaccount token"],
            ["privesc-hostpath", "Privilege escalation with hostpath volume"],
            ["privesc-nodeproxy", "Privilege escalation with nodes proxy"],
            ["privesc-privileged-pod", "Privilege escalation with privileged pod"]        
        ]

    def handle_args(self, args, param = None):

        if param:
            for param_value in param:
                # Each param_value would look like "key=value"
                param, value = param_value.split("=", 1)

                if param == "ip" : 
                    self.local_env.set_ip(value)
                if param == "subnet" : 
                    self.local_env.set_subnet(value)
                if param == "platform": 
                    self.local_env.set_platform(value)
                if param == "tactic": 
                    self.local_env.set_tactic(value)
                if param == "technique": 
                    self.local_env.set_technique(value)

        # Handle the input
        try:
            if args == "list":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.list(self.local_env.get_platform(), None))
                self.parse_output = False
                return 
            elif args == "cur":
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                    self.local_env.get_platform(), self.local_env.get_tactic(), self.local_env.get_technique()))
                self.parse_output = False
                return 
            elif args == "clean":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.clean())
                self.parse_output = False
                return
            elif args == "list-persist":
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.list(self.local_env.get_platform(), "persistence"))
                self.parse_output = False
                return
            elif args == "cred-secrets":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                     self.local_env.get_platform(), "credential-access", "dump-secrets"))
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.detonate(
                    self.local_env.get_platform(), "credential-access", "dump-secrets"))
                self.parse_output = True
            elif args == "cred-tokens":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                    self.local_env.get_platform(), "credential-access", "steal-serviceaccount-token"))
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.detonate(
                    self.local_env.get_platform(), "credential-access", "steal-serviceaccount-token"))
                self.parse_output = True
            elif args == "persist-admin-clusterrole":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                    self.local_env.get_platform(), "persistence", "create-admin-clusterrole"))
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.detonate(
                    self.local_env.get_platform(), "persistence", "create-admin-clusterrole"))
                self.parse_output = True
            elif args == "persist-client-cert":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                    self.local_env.get_platform(), "persistence", "create-client-certificate"))
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.detonate(
                    self.local_env.get_platform(), "persistence", "create-client-certificate"))
                self.parse_output = True
            elif args == "persist-create-token":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                    self.local_env.get_platform(), "persistence", "create-token"))
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.detonate(
                    self.local_env.get_platform(), "persistence", "create-token"))
                self.parse_output = True
            elif args == "privesc-hostpath":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                    self.local_env.get_platform(), "privilege-escalation", "hostpath-volume"))
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.detonate(
                    self.local_env.get_platform(), "privilege-escalation", "hostpath-volume"))
                self.parse_output = True
            elif args == "privesc-nodeproxy":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                    self.local_env.get_platform(), "privilege-escalation", "nodes-proxy"))
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.detonate(
                    self.local_env.get_platform(), "privilege-escalation", "nodes-proxy"))
                self.parse_output = True
            elif args == "privesc-privileged-pod":
                self.stratus_wrapper._execute_command(self.stratus_wrapper.show(
                    self.local_env.get_platform(), "privilege-escalation", "privileged-pod"))
                self.out = self.stratus_wrapper._execute_command(self.stratus_wrapper.detonate(
                    self.local_env.get_platform(), "privilege-escalation", "privileged-pod"))
                self.parse_output = True
            elif args == "help":
                self.table.print_table(self.column, self.row)
                return
            elif args == "options":
                self.table.print_table(self.column, self.local_env.get_env_dict())
                return 
            else:
                return None, None, None, False
        except Exception as e:
            print(e)
            return None, None, None, False

        return self.out, self.stratus_wrapper.final_command, self.local_env, self.parse_output
    