import json

import help.helper as helper

class Environment:
    def __init__(self):
        self._ip = helper.get_ip_address()
        self._subnet = None
        self._file_format = None
        self._file_output_raw = None
        self._file_output_parsed = None
        self._command = None
        self._tool_name = None
        self._tool_version = None
        self._timestamp_start = None
        self._timestamp_end = None
        self._attack_location = None
        self._perspective = None
        self._attack_phase = None
        self._oran_component = None
        self._result_code = None
        self._hostname = helper.detect_hostname()
        self._cve = None
        self._mitre = None
        self._pod_deployment = False

    # Getter and setter methods
    def get_timestamp_start(self):
        return self._timestamp_start

    def set_timestamp_start(self, timestamp):
        self._timestamp_start = timestamp
    
    def get_timestamp_end(self):
        return self._timestamp_end

    def set_timestamp_end(self, timestamp):
        self._timestamp_end = timestamp

    def get_file_format(self):
        return self._file_format

    def set_file_format(self, file_format):
        self._file_format = file_format

    def get_file_output_raw(self):
        return self._file_output_raw

    def set_file_output_raw(self, file_output_raw):
        self._file_output_raw = file_output_raw

    def get_file_output_parsed(self):
        return self._file_output_parsed

    def set_file_output_parsed(self, file_output_parsed):
        self._file_output_parsed = file_output_parsed

    def get_command(self):
        return self._command

    def set_command(self, command):
        self._command = command

    def get_tool_name(self):
        return self._tool_name

    def set_tool_name(self, tool_name):
        self._tool_name = tool_name

    def get_tool_version(self):
        return self._tool_version

    def set_tool_version(self, tool_version):
        self._tool_version = tool_version

    def get_attack_location(self):
        return self._attack_location

    def set_attack_location(self, attack_location):
        self._attack_location = attack_location

    def get_perspective(self):
        return self._perspective

    def set_perspective(self, perspective):
        self._perspective = perspective

    def get_attack_phase(self):
        return self._attack_phase

    def set_attack_phase(self, attack_phase):
        self._attack_phase = attack_phase

    def get_oran_component(self):
        return self._oran_component

    def set_oran_component(self, oran_component):
        self._oran_component = oran_component

    def get_result_code(self):
        return self._result_code

    def set_result_code(self, result_code):
        self._result_code = result_code

    def get_hostname(self):
        return self._hostname

    def set_hostname(self, hostname):
        self._hostname = hostname

    def get_ip(self):
        return self._ip

    def set_ip(self, ip):
        self._ip = ip

    def get_pod_deployment(self):
        return self._pod_deployment

    def set_pod_deployment(self, pod_deployment):
        self._pod_deployment = pod_deployment
        
    # Method to convert to JSON
    def to_json_all(self):
        data = {
            "ip": self.get_ip(),
            "timestamp_start": self.get_timestamp_start(),
            "timestamp_end": self.get_timestamp_start(),
            "file_format": self.get_file_format(),
            "file_output_raw": self.get_file_output_raw(),
            "file_output_parsed": self.get_file_output_parsed(),
            "command": self.get_command(),
            "tool_name": self.get_tool_name(),
            "tool_version": self.get_tool_version(),
            "attack_location": self.get_attack_location(),
            "perspective": self.get_perspective(),
            "attack_phase": self.get_attack_phase(),
            "oran_component": self.get_oran_component(),
            "result_code": self.get_result_code(),
            "hostname": self.get_hostname(),
            "pod_deployment": self.get_pod_deployment()
        }
        return data
    
    def to_json(self,output = False):
        data = {}
        for attr_name, attr_value in self.__dict__.items():
            # Remove the underscore prefix from the attribute name
            key = attr_name.lstrip('_')
            if output:
                if attr_value is not None:
                    data[key] = attr_value
            else:
                if attr_value is not None and attr_name not in ("_file_output_raw", "_file_output_parsed"):
                    if attr_name == "_timestamp_start" or attr_name == "_timestamp_end":
                        attr_value= attr_value.strftime("%Y-%m-%d %H:%M:%S")
                    data[key] = attr_value
        return data

    def set_variable_from_input(self, user_input):
        variable, value = user_input.split(" ", 1)

        new_var = self.translate_variable(variable)
        if hasattr(self, new_var):
            setattr(self, new_var, value)
            return True
        else:
            return False

    def set_variable_to_default(self,var):
        if hasattr(self, var):
            setattr(self, var, None)
            return True
        else:
            return False

    def translate_variable(self, variable):
        variable_mapping = {
            "timestamp_start": "_timestamp_start",
            "timestamp_end": "_timestamp_end",
            "ip": "_ip",
            "subnet": "_subnet",
            "file_format": "_file_format",
            "file_output_raw": "_file_output_raw",
            "file_output_parsed": "_file_output_parsed",
            "command": "_command",
            "tool_name": "_tool_name",
            "tool_version": "_tool_version",
            "attack_location": "_attack_location",
            "perspective": "_perspective",
            "attack_phase": "_attack_phase",
            "oran_component": "_oran_component",
            "result_code": "_result_code",
            "hostname": "_hostname",
            "cve":"_cve",
            "tactic":"_tactic",
            "mitre_technique":"_mitre_technique",
            "microsoft_technique":"_microsoft_technique",
            "pod_deployment":"_pod_deployment"
        }
        
        return variable_mapping.get(variable.lower(), "error")
    
    def get_cve(self):
        return self._cve

    def set_cve(self, cve):
        self._cve = cve

    def get_mitre(self):
        return self._mitre

    def set_mitre(self, mitre):
        self._mitre = mitre