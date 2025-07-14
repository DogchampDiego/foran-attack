from environment.global_const import GlobalVariables
from tools.base_classes.local_env_base import LocalEnv

class RedKubeEnv(LocalEnv):
    def __init__(self):
        super().__init__()
        self._mode = "passive"
        self._pod_name="redkube-pod"
        self._namespace="default"
        self._api_server=None
        self._token=None


    # Getters
    def get_mode(self):
        return self._mode

    def get_pod_name(self):
        return self._pod_name

    def get_namespace(self):
        return self._namespace

    def get_api_server(self):
        return self._api_server

    def get_token(self):
        return self._token

    def get_role(self):
        return self._role

    # Setters
    def set_mode(self, mode):
        self._mode = mode

    def set_pod_name(self, pod_name):
        self._pod_name = pod_name

    def set_namespace(self, namespace):
        self._namespace = namespace

    def set_api_server(self, api_server):
        self._api_server = api_server

    def set_token(self, token):
        self._token = token

    def set_role(self, role):
        self._role = role

    def get_env_dict(self):
        # Create a list of lists with environment variable names and their corresponding values
        ret = [
            ["MODE (passive|active|all)", self.get_mode()],
            ["POD_NAME", "redkube-pod"],
            ["NAMESPACE", "default"],
            ["API_SERVER", self._api_server],
            ["TOKEN", "Default Token from redkube-pod"]
        ]
        return ret


    def translate_variable(self, variable):
        variable_mapping = {
            "mode": "_mode",
            "pod_name": "_pod_name",
            "namespace": "_namespace",
            "api_server": "_api_server",
            "token": "_token"
        }

        return variable_mapping.get(variable.lower(), "error")


    