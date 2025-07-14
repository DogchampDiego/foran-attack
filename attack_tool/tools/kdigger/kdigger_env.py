from tools.base_classes.local_env_base import LocalEnv

class KDiggerEnv(LocalEnv):
    def __init__(self):
        super().__init__()
        
        # Default flag values for dig
        self._kubeconfig = None
        self._side_effects = False
        self._buckets = None
        self._all_buckets = False

        # Default flag values for gen
        self._name = None
        self._gen_all = False
        self._gen_command = None
        self._gen_fuzz_container = False
        self._gen_fuzz_init = False
        self._gen_fuzz_pod = False
        self._gen_hostnetwork = False
        self._gen_hostpath = False
        self._gen_hostpid = False
        self._gen_image = "busybox"
        self._gen_privileged = False
        self._gen_tolerations = False

        # Global flags
        self._output_format = "human"  # Default to "human"
        self._width = 140  # Default width
        self._namespace = None

        # Command variable
        self._command = None
        self._pod_name = None
        self._yaml = None

    # Getter and setter methods for flags related to 'dig' command
    def get_kubeconfig(self):
        return self._kubeconfig

    def set_kubeconfig(self, kubeconfig):
        self._kubeconfig = kubeconfig

    def get_side_effects(self):
        return self._side_effects

    def set_side_effects(self, side_effects):
        self._side_effects = side_effects

    def get_buckets(self):
        return self._buckets

    def set_buckets(self, buckets):
        self._buckets = buckets

    def get_buckets_all(self):
        return self.get_buckets_all

    def set_buckets_all(self, buckets_all):
        self.get_buckets_all = buckets_all

    # Getter and setter methods for flags related to 'gen' command
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_gen_all(self):
        return self._gen_all

    def set_gen_all(self, gen_all):
        self._gen_all = gen_all

    def get_gen_command(self):
        return self._gen_command

    def set_gen_command(self, gen_command):
        self._gen_command = gen_command

    def get_gen_fuzz_container(self):
        return self._gen_fuzz_container

    def set_gen_fuzz_container(self, gen_fuzz_container):
        self._gen_fuzz_container = gen_fuzz_container

    def get_gen_fuzz_init(self):
        return self._gen_fuzz_init

    def set_gen_fuzz_init(self, gen_fuzz_init):
        self._gen_fuzz_init = gen_fuzz_init

    def get_gen_fuzz_pod(self):
        return self._gen_fuzz_pod

    def set_gen_fuzz_pod(self, gen_fuzz_pod):
        self._gen_fuzz_pod = gen_fuzz_pod

    def get_gen_hostnetwork(self):
        return self._gen_hostnetwork

    def set_gen_hostnetwork(self, gen_hostnetwork):
        self._gen_hostnetwork = gen_hostnetwork

    def get_gen_hostpath(self):
        return self._gen_hostpath

    def set_gen_hostpath(self, gen_hostpath):
        self._gen_hostpath = gen_hostpath

    def get_gen_hostpid(self):
        return self._gen_hostpid

    def set_gen_hostpid(self, gen_hostpid):
        self._gen_hostpid = gen_hostpid

    def get_gen_image(self):
        return self._gen_image

    def set_gen_image(self, gen_image):
        self._gen_image = gen_image

    def get_gen_privileged(self):
        return self._gen_privileged

    def set_gen_privileged(self, gen_privileged):
        self._gen_privileged = gen_privileged

    def get_gen_tolerations(self):
        return self._gen_tolerations

    def set_gen_tolerations(self, gen_tolerations):
        self._gen_tolerations = gen_tolerations

    # Getter and setter methods for global flags
    def get_output_format(self):
        return self._output_format

    def set_output_format(self, output_format):
        self._output_format = output_format

    def get_width(self):
        return self._width

    def set_width(self, width):
        self._width = width

    def get_namespace(self):
        return self._namespace

    def set_namespace(self, namespace):
        self._namespace = namespace

    def get_command(self):
        return self._command

    def get_pod_name(self):
        return self._pod_name

    def set_pod_name(self, pod_name):
        self._pod_name = pod_name
        
    def get_pod_yaml(self):
        return self.yaml

    def set_pod_yaml(self, yaml):
        self._yaml = yaml

    # Getter and setter methods for the command
    def set_command(self, command):
        available_commands = [
            "completion",
            "dig",
            "gen",
            "help",
            "ls",
            "version"
        ]
        if command in available_commands:
            self._command = command
   
    def get_env_dict(self):
        ret = [
            ["WIDTH", self.get_width()],
            ["NAMESPACE", self.get_namespace()],
            ["COMMAND", self.get_command()],
            ["OUTPUT_FORMAT", self.get_output_format()]
        ]
        return ret

    def get_env_dict_dig(self):
        ret = [
            ["KUBECONFIG", self.get_kubeconfig()],
            ["SIDE_EFFECTS", self.get_side_effects()],
            ["BUCKETS", self.get_buckets()],
        ]
        return ret

    def get_env_dict_gen(self):
        ret = [
            ["NAME", self.get_name()],
            ["GEN_ALL", self.get_gen_all()],
            ["GEN_COMMAND", self.get_gen_command()],
            ["GEN_FUZZ_CONTAINER", self.get_gen_fuzz_container()],
            ["GEN_FUZZ_INIT", self.get_gen_fuzz_init()],
            ["GEN_FUZZ_POD", self.get_gen_fuzz_pod()],
            ["GEN_HOSTNETWORK", self.get_gen_hostnetwork()],
            ["GEN_HOSTPATH", self.get_gen_hostpath()],
            ["GEN_HOSTPID", self.get_gen_hostpid()],
            ["GEN_IMAGE", self.get_gen_image()],
            ["GEN_PRIVILEGED", self.get_gen_privileged()],
            ["GEN_TOLERATIONS", self.get_gen_tolerations()],
        ]
        return ret

    def translate_variable(self, variable):
        variable_mapping = {
            "kubeconfig": "_kubeconfig",
            "namespace": "_namespace",
            "buckets": "_buckets",
            "name": "_name" ,
            "side_effects": "_side_effects",
            "gen_all": "_gen_all",
            "gen_command": "_gen_command",
            "gen_fuzz_container": "_gen_fuzz_container",
            "gen_fuzz_init": "_gen_fuzz_init",
            "gen_fuzz_pod": "_gen_fuzz_pod",
            "gen_hostnetwork": "_gen_hostnetwork",
            "gen_hostpath": "_gen_hostpath",
            "gen_hostpid": "_gen_hostpid",
            "gen_image": "_gen_image",
            "gen_privileged": "_gen_privileged",
            "gen_tolerations": "_gen_tolerations",
            "output_format": "_output_format",
            "width": "_width",
            "command": "_command",
            "_pod_name": "pod_name",
            "_yaml":"yaml"

        }
        
        return variable_mapping.get(variable.lower(), "error")