from abc import ABC, abstractmethod
import re
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from controller.wordcompleter import CustomWordCompleter

import help.helper as helper
from environment.global_const import GlobalVariables
from state.menu_state import MenuState
from help.table import Table

from database.mongo_db_handler import MongoDBWrapper as db
from controller.filehistory import ConditionalFileHistory
from automation.Template import Template
from automation.Result import Result
from campaign.Campaign import Campaign


# Abstract Base Class for Tool Classes
class Tool(ABC):
    def __init__(self):

        # For Promp Appearance
        self.custom_style = Style.from_dict({'prompt': 'red'})
        self.completer = CustomWordCompleter(
            [
                "end",
                "exit",
                "back",
                "clear",
            ],
            ignore_case=True,
        )
        self.corrections = {
            "bakc": "back",
            "claer": "clear",
            "clera": "clear",
            "exti": "exit",
            "edn": "end",
        }
        self.history = ConditionalFileHistory("")
        #Show Menu
        self.show_menu = True
        # Table output
        self.table = Table()
        self.row = None
        self.column = None

        # Global Variable Instance
        self.global_var = GlobalVariables.get_instance()
        self.global_env = self.global_var.get_env()
        self.user_raw = ""

        # Template
        self.template = Template().get_instance()
        # Output muss noch in env class gehandelt werden
        self.out = None
        # DB 
        self.db =  db(self.global_var.get_base_dir() + "database/config.ini")
        self.database = None
        self.collection = None
        # Commands
        self.command_mapping = None
        # Campaign
        self.campaign = Campaign.get_instance()

        # Parser
        self.parser = None
        self.parse_out = None
        
    def handle_user_input(self, user_input):
        self.user_raw = user_input.strip()
        if user_input.strip() == "menu":
            self.menu()
        elif re.search(r'\bset\b', user_input):
            self.set_local(user_input)
        elif user_input.strip()  == "options" or user_input.strip() == "":
            self.settings()
        else:
            if user_input.strip() in self.command_mapping_db_ignore_db:
                # handle every case that should not be inserted into db
                self.out = self.command_mapping_db_ignore_db[user_input]()
                self.history.set_save_condition(True)
                self.history.append_string(user_input)
            else:
                try:
                    # set timestamp start
                    self.global_env.set_timestamp_start(helper.get_current_timestamp())
                    if user_input.strip() in self.command_mapping:
                        user_input=user_input.strip()
                        self.out = self.command_mapping[user_input]()
                    else:
                        # run command and get outpu
                        if self.global_env.get_pod_deployment():
                            self.out = self.wrapper.custom_scan(user_input)
                        else:    
                            self.out = self.wrapper.custom_scan(user_input)
                    if self.out:
                        # set timestamp end
                        self.global_env.set_timestamp_end(helper.get_current_timestamp())

                        # set result code
                        if self.out.return_code is not None: 
                            self.global_env.set_result_code(self.out.return_code)

                        # handle output
                        if self.out.return_code == 0:
                            # expand history
                            self.history.set_save_condition(True)
                            self.history.append_string(user_input)

                            # add to template
                            self.template.add_to_result_list(Result(self.local_env.to_json(),self.wrapper.final_command,self.global_env.get_tool_name(),self.global_env.get_tool_version(),self.global_env.get_hostname(),self.out.return_code))
                            # insert output into database
                            self.database_insert()
                        else:    
                            # print error
                            print("error:"+self.out.captured_error)
                    if self.out == None:
                        print("An error occured")
                except Exception as e:
                    # set timestamp start/end to default
                    self.global_env.set_variable_to_default(self.global_env.translate_variable("timestamp_start"))
                    self.global_env.set_variable_to_default(self.global_env.translate_variable("timestamp_end"))

                    # close db connection
                    self.db.close_connection() 

                    # print exception
                    print("Exception occured: ", e.__cause__, e.args, e.with_traceback, e.__context__)
                    print("Error: The mapped command was not successfully executed.")
        return self


    @abstractmethod
    def check_installed(self):
        pass

    @abstractmethod
    def install_tool(self):
        pass
    
    @abstractmethod
    def tool_version(self):
        pass

    def tool_name(self):
        return self.name
    
    # Set Local Metavalue        
    def set_local(self,user_input):
        ret =self.local_env.set_variable_from_input(user_input)
        if ret:
            self.history.set_save_condition(True)
            self.history.append_string(user_input)
    
    def back(self):
        # set tool name/version to default
        self.global_env.set_variable_to_default(self.global_env.translate_variable("tool_name"))
        self.global_env.set_variable_to_default(self.global_env.translate_variable("tool_version"))

        # set timestamp start/end to default
        self.global_env.set_variable_to_default(self.global_env.translate_variable("timestamp_start"))
        self.global_env.set_variable_to_default(self.global_env.translate_variable("timestamp_end"))
    
        # set timestamp start/end to default
        self.global_env.set_variable_to_default(self.global_env.translate_variable("command"))
        self.global_env.set_variable_to_default(self.global_env.translate_variable("result_code"))


        # set State
        self.global_var.pop_menu_tree()
        if self.global_var.get_menu_tree()[-1] == MenuState.TOOLS:
            from menu.startmenu.tools import Tools         
            return Tools()
        elif self.global_var.get_menu_tree()[-1] == MenuState.CONTAINER:
            from menu.startmenu.container import Container
            return Container()
        else:            
            from menu.mitre_tactics.privilege_escalation import PrivilegeEscalation 
            from menu.mitre_tactics.defense_evasion import DefenseEvasion
            from menu.mitre_tactics.persistence import Persistence
            from menu.mitre_tactics.execution import Execution
            from menu.mitre_tactics.discovery import Discovery
            from menu.mitre_tactics.credential_access import CredentialAccess
            from menu.mitre_tactics.initial_access import InitialAccess
            from menu.mitre_tactics.lateral_movement import LateralMovement
            from menu.mitre_tactics.collection import Collection
            from menu.mitre_tactics.impact import Impact
            from menu.mitre_tactics.reconnaissance import Reconnaissance
            from menu.mitre_tactics.command_control import CommandControl
            from menu.mitre_tactics.exfiltration import Exfiltration
            state = self.global_var.get_menu_tree()[-1]
            menu_dict = {
                MenuState.INITIAL_ACCESS: InitialAccess,
                MenuState.PERSISTENCE: Persistence,
                MenuState.PRIVILEGE_ESCALATION: PrivilegeEscalation,
                MenuState.DEFENSE_EVASION: DefenseEvasion,
                MenuState.DISCOVERY: Discovery,
                MenuState.CREDENTIAL_ACCESS: CredentialAccess,
                MenuState.LATERAL_MOVEMENT: LateralMovement,
                MenuState.EXECUTION: Execution,
                MenuState.COLLECTION: Collection,
                MenuState.IMPACT: Impact,
                MenuState.RECONNAISSANCE: Reconnaissance,
                MenuState.COMMAND_CONTROL: CommandControl,
                MenuState.EXFILTRATION: Exfiltration,
            }
            return menu_dict[state]()
        
    def menu(self):
        self.table.print_table(self.column,self.row)

    def settings(self):
        header = ["Parameter","Value"]
        self.table.print_table(header,self.local_env.get_env_dict())

    def print_menu_basic(self):
        if self.show_menu:
            helper.print_menu()

    def invalid_option(self):
            print("Invalid option selected.")
            return self

    def ask_install_tool_question(self):
        # Define the cursive style
        cursive_style = Style.from_dict({'prompt': 'italic'})

        # Prompt the installation question
        answer = prompt('The Tool is not installed, do you want to install it? (Yes/No) ',
                        style=cursive_style)

        # Return the user's answer
        return answer
    
    def check_requirements(self):
        if not self.check_installed():
            answer = self.ask_install_tool_question()
            if answer.lower() == 'yes' or answer.lower() == 'y':
                self.install_tool()
                return True
            else:
               print("You have to install the tool to use it!")
               return False
        else:
            return True 
    
    # help

    def parse_output(self):
        self.parser.set_data(self.out.captured_output)
        mitre, cve = self.parser.parse_vulnerabilities()

        print("------------------------")
        print("Mitre:", mitre)
        print("CVE:", cve)
        # only if exist
        self.global_env.set_cve(cve)
        self.global_env.set_mitre(mitre)


    def database_insert(self):
        if not self.global_var.get_lite_version():
            # connect
            self.db.connect_db("collection")
            # set Metavalues
            self.global_env.set_command(self.wrapper.final_command)
            self.global_env.set_file_output_raw(self.out.captured_output)
            #set insert Values

            # check if tool has parser
            #if self.parser is not None and self.parse_output is True:
            #    self.parse_output()

            metavalues = self.global_env.to_json(output=True)

            # add campaign
            if self.campaign.get_id():
                metavalues["campaign_id"]=self.campaign.get_id()
            
            
            
            # add locals 
            metavalues.update(self.local_env.to_json())
            print("Insert into DB: ",metavalues)
            id_doc = self.db.insert_document(metavalues)
            print("Inserted into DB Document: ",id_doc)
            # save id somewhere in thread class
            # close connection
            self.global_env.set_variable_to_default(self.global_env.translate_variable("file_output_raw"))
            self.db.close_connection()
        else:
            print("Ligth Version no DB used")