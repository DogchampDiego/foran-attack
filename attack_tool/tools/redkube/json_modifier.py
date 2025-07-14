import json
import os
import re

class JSONModifier:
    def __init__(self, pod_name, namespace, api_server, token):
        # Initialize instance variables
        self.POD_NAME = pod_name
        self.NAMESPACE = namespace
        self.API_SERVER = api_server
        self.TOKEN = token

    def remove_entry(self, json_file_path, key, value):
        """
        Removes an entry from the JSON file where the key-value pair matches.

        :param json_file_path: Path to the JSON file.
        :param key: The key to match (e.g., 'id' or 'name').
        :param value: The value of the key to match for deletion.
        """
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"{json_file_path} does not exist.")

        # Read the JSON data from the file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Find the entry to remove
        entry_found = False
        for entry in data:
            if entry.get(key) == value:
                data.remove(entry)
                entry_found = True
                break

        if not entry_found:
            raise ValueError(f"No entry found with {key} = {value}.")

        # Write the modified data back to the file using sudo
        temp_file_path = "/tmp/temp_json_file.json"
        with open(temp_file_path, 'w') as temp_file:
            json.dump(data, temp_file, indent=4)

        # Use sudo to overwrite the original file
        os.system(f"sudo mv {temp_file_path} {json_file_path}")

        print(f"Entry with {key} = {value} removed from {json_file_path} successfully.")

    def update(self, pod_name=None, namespace=None, api_server=None, token=None):
        """
        Update all instance variables. If a parameter is None, it will not be updated.
        
        :param pod_name: New pod name.
        :param namespace: New namespace.
        :param api_server: New API server.
        :param token: New token.
        """
        if pod_name is not None:
            self.set_pod_name(pod_name)
        if namespace is not None:
            self.set_namespace(namespace)
        if api_server is not None:
            self.set_api_server(api_server)
        if token is not None:
            self.set_token(token)

    def update_json_with_class_vars(self, json_file_path):
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"{json_file_path} does not exist.")

        # Read the JSON data from the file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        # Iterate over the JSON objects and modify where args is True
        for entry in data:
            if entry.get("args") == True:
                # Replace the placeholders in the command with instance variables
                entry["command"] = self.replace_args_in_command(entry["command"])
                # Set args to False
                entry["args"] = False

                # Remove the arg_list field if it exists
                if "arg_list" in entry:
                    del entry["arg_list"]

        # Write the modified data back to the file using sudo
        temp_file_path = "/tmp/temp_json_file.json"
        with open(temp_file_path, 'w') as temp_file:
            json.dump(data, temp_file, indent=4)

        # Use sudo to overwrite the original file
        os.system(f"sudo mv {temp_file_path} {json_file_path}")

    def replace_args_in_command(self, command):
        # Replace placeholders in the command with instance variables
        
        for var_name, var_value in vars(self).items():
            placeholder = f"${{{var_name}}}"
            if var_name in command:
                if var_name == "POD_NAME":
                    value = self.get_pod_name()
                if var_name == "NAMESPACE":
                    value = self.get_namespace()
                if var_name == "API_SERVER":
                    value = self.get_api_server()
                if var_name == "TOKEN":
                        value = self.get_token()
                command = re.sub(rf'\${var_name}', value, command)  # ${VAR} format
                command = command.replace(placeholder, value)  # ${VAR_NAME} format
        return command
    

      # Getter and Setter methods (as defined earlier)
    def get_pod_name(self):
        return self.POD_NAME

    def set_pod_name(self, pod_name):
        self.POD_NAME = pod_name

    def get_namespace(self):
        return self.NAMESPACE

    def set_namespace(self, namespace):
        self.NAMESPACE = namespace

    def get_api_server(self):
        return self.API_SERVER

    def set_api_server(self, api_server):
        self.API_SERVER = api_server

    def get_token(self):
        return self.TOKEN

    def set_token(self, token):
        self.TOKEN = token

