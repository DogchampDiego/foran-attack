import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

import os
import subprocess

from environment.global_const import GlobalVariables


class Demonstrator(Menu):
    def __init__(self,folder_path=GlobalVariables.get_instance().get_base_dir() + "automation/scripts/generated"):
        super().__init__()
        helper.handle_globals(MenuState.DEMONSTRATOR,MenuState.DEMONSTRATOR)

        
        self.default_path = GlobalVariables.get_instance().get_base_dir() +  "automation/scripts/default"
        self.files = self.list_default_files()

        self.default_script_len = len(self.files)

        self.folder_path = folder_path
        self.list_files()



    def back(self):
        self.global_var.pop_menu_tree()
        from menu.startmenu.start import Start
        return Start()

    def handle_user_input(self, user_input):
        if int(user_input.strip())<=len(self.files) and int(user_input.strip())>0:
            self.run_script(int(user_input.strip()))
        else:
            print("Enter a valid Number")
        return self

    def list_files(self):
        if os.path.exists(self.folder_path):
            files = os.listdir(self.folder_path)
            for file in files:
               self.files.append(file)
        else:
            print(f"The folder '{self.folder_path}' does not exist.")
    
    def list_default_files(self):
        temp = []
        if os.path.exists(self.default_path):
            files = os.listdir(self.default_path)
            for file in files:
               temp.append(file)
        else:
            print(f"The folder '{self.default_path}' does not exist.")
        return temp

    def run_script(self,user_input):
        try:
            if user_input == 0:
                print("Enter a valid Number")
                return self
            if user_input>= 0 and user_input <= self.default_script_len:
                path = self.default_path+"/"+self.files[(user_input-1)]
            if user_input>= 0 and user_input > self.default_script_len:
                path = self.folder_path+"/"+self.files[(user_input-1)]
            subprocess.run(['bash', path], check=True)
            print("Shell script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the shell script: {e}")
        except FileNotFoundError:
            print("The shell script file was not found.")
        return self

    def print_menu_basic(self):
        print("\nExisting Templates:")
        for key, value in self.create_file_dict().items():
            print(f"{key}: {value}")

    def create_file_dict(self):
        return {str(i + 1): value for i, value in enumerate(self.files)}