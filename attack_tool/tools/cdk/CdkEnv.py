
from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class CdkEnv(LocalEnv):
    
    exploit_list = ["k8s-cronjob","test-poc","etcd-get-k8s-token","ak-leakage","k8s-backdoor-daemonset",
                    "lxcfs-rw-cgroup","lxcfs-rw","rewrite-cgroup-devices","docker-sock-check","docker-sock-pwn",
                    "registry-brute","abuse-unpriv-userns","k8s-secret-dump","k8s-shadow-apiserver","service-probe",
                    "k8s-mitm-clusterip","k8s-configmap-dump","reverse-shell","webshell-deploy","k8s-psp-dump",
                    "kubelet-exec","k8s-kubelet-var-log-escape","mount-disk","mount-procfs","cap-dac-read-search",
                    "shim-pwn","runc-pwn","k8s-get-sa-token","mount-cgroup","check-ptrace","docker-api-pwn","istio-check"
                    ]
    tool_list = ["vi", "ps", "nc", "ifconfig", "kcurl", "ectl", "ucurl", "probe"]
    
    def __init__(self):
        super().__init__()    
        self._ip = GlobalVariables.get_instance().get_env().get_ip()
        self._subnet = "/24"
        self._exploit = ""
        self._tool = ""
        self._pod_name = None
    
    
    # Getter and Setter for local_ip
    def get_ip(self):
        return self._ip
    
    def set_ip(self, value):
        self._ip = value
        
    # Getter and Setter for subnet
    def get_subnet(self):
        return self._subnet
    
    def set_subnet(self, value):
        self._subnet = value
        
    # Getter and Setter for exploit
    def get_exploit(self):
        return self._exploit
    
    def set_exploit(self, value):
        self._exploit = value
        
    # Getter and Setter for tool
    def get_tool(self):
        return self._tool
    
    def set_tool(self, value):
        if value in self.tool_list:
            self._tool = value
        else:
            print("ERROR: Faulty tool provided.")
            return

    def get_env_dict(self):
        ret = [
            ["ip", self.get_ip()],
            ["subnet",  self.get_subnet()],
            ["exploit", self.get_exploit()],
            ["tool", self.get_tool()]
        ]
        return ret

    def translate_variable(self, variable):
        options = ["ip", "subnet", "exploit", "tool"]
        res = variable
        if res in options:
            res = "_" + res
        return res
    
    def get_pod_name(self):
        return self._pod_name

    def set_pod_name(self, pod_name):
        self._pod_name = pod_name
