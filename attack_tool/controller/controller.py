import re
from prompt_toolkit.shortcuts import clear

import help.helper as helper
from menu.startmenu.start import Start
from menu.startmenu.tools import Tools
import tools.base_classes.tool_base as tool
from environment.global_const import GlobalVariables
from state.menu_state import MenuState
from search.search import CveSearchSploitWrapper
from help.table import Table
from controller.promptinput import PromptInput
from automation.AttackGenerator import AttackGenerator
from campaign.Campaign import Campaign

import os

# Controller Class
class MenuStateMachine:
    def __init__(self):
        self.current_state = Start()
        self.global_var = GlobalVariables.get_instance()
        self.prompt = PromptInput()
        self.searchsploit = CveSearchSploitWrapper()
        self.table = Table()
        self.global_env = self.global_var.get_env()
        helper.print_banner()
        self.attack_generator = AttackGenerator()
        self.campaign = Campaign.get_instance()

    # Run Menu
    def run(self):
        try:
            while True:

                # Print Menu
                self.current_state.print_menu_basic()
            
                # Style
                self.prompt.set_style(self.current_state.custom_style)

                # Completer
                self.prompt.set_completer(self.current_state.completer)

                # Corrections
                self.prompt.set_corrections(self.current_state.corrections)

                # History
                self.prompt.set_history(self.current_state.history)

                # User Input
                user_input = self.prompt.get_input(helper.create_cursor())

                # Action
                action = self.get_action(user_input.strip())


                # Handle Input
                if user_input == "exit":
                    break
                elif user_input.strip() == "?" or user_input.strip() == "help":
                    self.user_manual()
                elif user_input.strip() == "show":
                    self.show()
                elif user_input.strip() == "show_all":
                    self.show_all()
                elif user_input.strip() == "template":
                    self.attack_generator.generate_script()
                elif re.search(r'\bcampaign\b', user_input):
                    try:
                        value = user_input.split(" ", 1)[-1].strip()
                        if value.strip() == "info":
                            self.campaign.print_menu()
                        elif value.strip() == "start":
                            self.campaign.start()
                        elif value.strip() == "end":
                            self.campaign.end()
                        else:
                            self.campaign.print_command()
                    except ValueError:
                        self.campaign.print_command()

                elif action is not None:
                    action()
                elif re.search(r'\bsetg\b', user_input):
                    if len(user_input.split())==3:
                        self.set_global(user_input)
                    else:
                        print("To set a Metavalue type 'setg variable value'")
                else:
                    new_state = self.current_state.handle_user_input(user_input)
                    # Check if new state is a Tool
                    if isinstance(new_state, tool.Tool):
                        # if the new state is a tool check if the tool is installed
                        if not new_state.check_requirements():
                            # (YES/NO) --> NO --> go back to last state
                            self.global_var.pop_menu_tree()
                            self.global_var.set_menu_state(self.global_var.get_menu_tree()[-1])
                        else:
                            self.current_state = new_state
                            # Set tool version and name
                            self.global_env.set_tool_version(self.current_state.tool_version())
                            self.global_env.set_tool_name(self.current_state.tool_name())
                        if user_input == "delete_pod":
                            try:
                                self.back()
                            except Exception as e:
                                print("delete pod failed")
                                print(e)
                    else:
                        self.current_state = new_state
                        
        except KeyboardInterrupt:
                print("\nExiting the program due to Ctrl+C")
                # Perform any cleanup or finalization here if needed
                # You can also simply omit this block if no cleanup is necessary
    
    
    # Handle User Input BACK, END, CLEAR
    def get_action(self, user_input):
        actions = {
            "back": self.back,
            "clear": self.clear,
            "end": self.end,
        }
        return actions.get(user_input)

    def back(self):
        new_state = self.current_state.back()
        self.current_state = new_state

    def clear(self):
        clear()
        helper.print_banner()

    def end(self):
        self.current_state = Start()
        self.global_var.reset_menu_tree()
        self.global_var.set_menu_state(MenuState.START)

    # Set Metavalue   
    def set_global(self,user_input):
        if user_input.split()[0] == "setg":
            if user_input.split()[1] == "light_version":
                self.global_var.set_lite_version(True)
            if user_input.split()[1] == "priv_container":
                self.global_var.set_priv_container(user_input)
            if user_input.split()[1] == "sa_account":
                self.global_var.set_priv_container(user_input)
            else:
                ret =self.global_env.set_variable_from_input(' '.join(user_input.split()[1:]))
                if ret and isinstance(self.current_state, tool.Tool):
                    self.current_state.history.set_save_condition(True)
                    self.current_state.history.append_string(user_input)

    # Show Metavalue
    def show(self):
        header = ["Parameter","Value"]
        metavalue = self.global_env.to_json()
        metavalue['light_version'] = self.global_var.get_lite_version()
        self.table.print_table(header, list(metavalue.items()))


    def show_all(self):
        header = ["Parameter","Value"]
        metavalue = self.global_env.to_json_all()
        metavalue['light_version'] = self.global_var.get_lite_version()
        metavalue['priv_container'] = self.global_var.get_priv_container()
        metavalue['sa_account'] = self.global_var.get_sa_account()
        self.table.print_table(header, list(metavalue.items()))


    # Show Manual
    def user_manual(self):
        print("\nClusterforce User Manual:")

        header = ["General","Description"]
        row = [
            ["exit", "Exit Clusterforce"],
            ["back", "Navigate back to the previous menu"],
            ["clear",  "Clear the screen"],
            ["end", "End the current session and return to the start menu"],
            ["show",  "Show set all Metavalues"],
            ["show_all",  "Show all avaiable Metavalues"],
            ["template",  "Generate a template for the executed attacks"],
            ["campaign <ACTION>",  "Start or end a Campaign or get Information [start, end, info]"],
            ["setg <VAR-NAME> <VALUE>",  "Set a environment variable with specific variable name and value"]
        ]
        self.table.print_table(header, row)
        header = ["Tool Specific","Description"]
        row = [
            ["set <VAR-NAME> <VALUE>", "Set a local variable with specific variable name and value"],
            ["options", "Display tool specific options / flags"],
            ["menu",  "Show predefined tool attack methods"],
        ]
        self.table.print_table(header, row)