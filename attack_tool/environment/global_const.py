import os
import sys
from state.menu_state import MenuState
from environment.environment_base import Environment
        
import json

class GlobalVariables:
    _instance = None

    @staticmethod
    def get_instance():
        if not GlobalVariables._instance:
            GlobalVariables._instance = GlobalVariables()
        return GlobalVariables._instance

    def __init__(self):
        self.menu_state = MenuState.START
        self.menu_tree = []
        self.env = Environment()
        self.lite_version = False
        self.priv_container = False
        self.sa_account = "default"
        self.base_dir, self.tool_dir, self.tool_non_bin_dir, self.master_host = self._init_config()

    def _init_config(self):
        # Open and read the config file        
        main_path = os.path.dirname(__file__)
        main_dir = os.path.dirname(main_path)

        with open(main_dir + '/config.json', 'r') as file:
            config_data = json.load(file)

        base_dir = config_data.get('BASE_DIR')
        tool_dir = config_data.get('TOOL_DIR')
        tool_non_bin = config_data.get('TOOL_NON_BIN_DIR')
        master_host = config_data.get('MASTER_HOST')
        return base_dir, tool_dir, tool_non_bin, master_host
    
    def get_base_dir(self):
        return self.base_dir
    
    def get_tool_dir(self):
        return self.tool_dir

    def get_tool_non_bin_dir(self):
        return self.tool_non_bin_dir
    
    def get_master_host(self):
        return self.master_host

    def get_menu_state(self):
        return self.menu_state

    def set_menu_state(self, value):
        self.menu_state = value
    
    def get_menu_tree(self):
        return self.menu_tree

    def add_menu_tree(self, value):
        self.menu_tree.append(value)

    def pop_menu_tree(self):
        self.menu_tree.pop()

    def reset_menu_tree(self):
        self.menu_tree = self.menu_tree[:1]

    def get_env(self):
        return self.env

    def set_env(self, env):
        self.env = env

    def get_lite_version(self):
        return self.lite_version
    
    def set_lite_version(self, lite_version):
        self.lite_version = lite_version
        
    def get_priv_container(self):
        return self.priv_container
    
    def set_priv_container(self, priv_container):
        self.priv_container = bool(priv_container)
            
    def get_sa_account(self):
        return self.sa_account
    
    def set_sa_account(self, sa_account):
        self.sa_account = sa_account

    # Method to convert to JSON
    def to_json_all(self):
        data = {
            "menu_state": self.menu_state,
            "lite_version": self.lite_version,
        }
        return data