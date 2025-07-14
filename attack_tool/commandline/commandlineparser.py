import argparse
import textwrap
from tools.kubehunter.kubehunter_args import KubehunterArgs as kubehunter
from tools.kubehunter.kubehunter_parser import KubehunterParser

from tools.redkube.redkube_args import RedKubeArgs as redkube
from tools.kdigger.kdigger_args import kdiggerArgs as kdigger

from tools.nmap.nmap_args import NmapArgs as nmap
from tools.stratusred.stratus_red_args import StratusArgs as stratusred

from tools.badpods.badpods_args import BadpodsArgs as badpods
from tools.flightsim.flightsim_args import FlightsimArgs as flightsim


from environment.global_const import GlobalVariables
from database.mongo_db_handler import MongoDBWrapper
import help.helper as helper
from help.table import Table

from testing.kubernetes.initial_access.initial_access_args import InitialAccessArgs
from testing.kubernetes.execution.execution_args import ExecutionArgs
from testing.kubernetes.persistence.persistence_args import PersistenceArgs
from testing.kubernetes.privilege_escalation.privilege_escalation_args import PrivilegeEscalationArgs
from testing.kubernetes.defense_evasion.defense_evasion_args import DefenseEvasionArgs
from testing.kubernetes.credential_access.credential_access_args import CredentialAccessArgs
from testing.kubernetes.discovery.discovery_args import DiscoveryArgs
from testing.kubernetes.lateral_movement.lateral_movement_args import LateralMovementArgs
from testing.kubernetes.collection.collection_args import CollectionArgs
from testing.kubernetes.impact.impact_args import ImpactArgs


import os
import subprocess
import shutil
import subprocess
from output.output import Output

class CommandLineParser:
    def __init__(self):
        # Parser
        self.parser = argparse.ArgumentParser(description='Clusterforce:', prog='attack',
                                              formatter_class=argparse.RawDescriptionHelpFormatter, 
                                              usage= """attack [--tool [TOOL-NAME]] [--attack [ATTACK]] [--param [PARAM]], \n       attack [--playbook [PLAYBOOK-NAME]] [--number [NUMBER]], \n       attack [--testcase TESTCASE] [--tactic [TACTIC-NAME]] [--technique [TECHNIQUE-NAME]], \n       attack [--help]
                                              """,
                                              epilog=textwrap.dedent('''\
                                                  display available Tools:
                                                    attack --tool help
                                                                                        
                                                  display Tool Attacks:
                                                    attack --tool [TOOL-NAME] --attack help

                                                  display available Playbooks:
                                                    attack --playbook help                 

                                                  run Playbook:
                                                    attack --playbook [PLAYBOOK-NAME]
                                                    attack --playbook [generated/default/pytest] --number [NUMBER]
                                                                       
                                                  display available Tests:
                                                    attack --testcase help
                                                    attack --testcase [TESTCASE] --tactic help
                                                    attack --testcase [TESTCASE] --tactic [TACTIC-NAME] --technique help  
                                                    attack --testcase [TESTCASE] --tactic [execution] --technique [exec_command_in_container]  (--value [SSH/NSLOOKUP/CURL])
                                                                     
                                                 usage Light version :
                                                    attack --testcase or --playbook or --tool and --light_version          
                                                  '''))
        
        self.parser.add_argument('-t', '--tool', metavar='', help='specify Tool Name.')
        self.parser.add_argument('-a', '--attack', metavar='', help='specify the Attack from the Tool.')
        self.parser.add_argument('-p', '--param', metavar='key=value', action='append', help='specify Parameters and Values as key=value.')
        self.parser.add_argument('-pb', '--playbook', metavar='', help='specify the Name of the Playbook to execute.')
        self.parser.add_argument('-n', '--number', metavar='', help='specify the Number of the Playbook to execute.')
        self.parser.add_argument('-tc', '--testcase', metavar='', help='specify the Name of the Testcase to execute.')
        self.parser.add_argument('--tactic', metavar='', help='specify the Tactic Name.')
        self.parser.add_argument('--value', metavar='', help='specify the command used in conainer')
        self.parser.add_argument('--technique', metavar='', help='specify the Technique Name.')
        self.parser.add_argument('--light_version', metavar='', help='specify if Tool gets used in light mode (No DB needed)')
        self.parser.add_argument('--pod_deployment', metavar='', help='specify if Tool should be executed inside a container')
        self.parser.add_argument('--pod_specs', metavar='key=value', action='append', help='specify [pod_priviliged=True/False, service_account="NAME"]')


        self.args = self.parser.parse_args()
        
        # Globales
        self.global_var = GlobalVariables.get_instance()
        self.global_env = GlobalVariables.get_instance().get_env()
        self.local_env = None
        self.parse_output = False

        # Database
        self.db =  MongoDBWrapper(self.global_var.get_base_dir() + "database/config.ini")
        self.database = None
        self.collection = None

        # Parser
        self.parser = None

        self.wrapper = None

        # Table
        self.table = Table()
        self.header_tools = ["Tool", "Description"]
        self.row_tools = [
            ["Kubehunter",  "Imitated view of hunting for Information from outside the cluster"],
            ["Redkube",  "Run kubectl commands to find weaknesses inside the cluster"],
            ["Nmap",  "Scan IP to find weaknesses"],
            ["Kdigger",  "Run buckets with dig to find weaknesses inside the cluster"],
        ]
        self.header_test = ["Testcase", "Description"]
        self.row_test = [
            ["Kubernetes",  "Testcases based on the Kubernetes Thread Matrix"],
            ["Open RAN",  "Testcases specific for Open RAN Components"],
        ]
        self.header_test_tactic = ["Tactic", "Description"]
        self.row_test_tactic = [
            ["Initial_Access", "Gain foothold within network"],
            ["Execution", "Execute adversary-controlled code"],
            ["Persistence", "Maintain access across restarts"],
            ["Privilege_Escalation", "Gain higher-level permissions"],
            ["Defense_Evasion", "Avoid detection and security software"],
            ["Credential_Access", "Steal account credentials"],
            ["Discovery", "Gain knowledge about the system"],
            ["Lateral_Movement", "Access and control remote systems"],
            ["Collection", "Gather information from target networks"],
            ["Impact", "Manipulate or destroy systems and data"],
        ]

        # Path
        self.path = self.global_var.get_base_dir() + "automation/scripts/"

        # Files
        self.files_default =  self.get_files("default")
        self.files_generated =  self.get_files("generated")
        self.files_general =  self.get_files("general")

        # Tactics
        self.kubernetes_tactics = ["initial_access", "execution", "persistence", "privilege_escalation", "defense_evasion", "credential_access", "discovery", "lateral_movement", "collection", "impact"]
        self.oran_tactics = []

        # Output
        self.out = Output(None,None,None) 
        self.final_command = None
    
        # Priv specs
        self.sa_account_value = None
        self.privpod_value = None
    
    def get_options(self):
        return self.args

    def handle_tool(self):
        # set timestamp start
        self.global_env.set_timestamp_start(helper.get_current_timestamp())

        if self.args.pod_deployment:
            self.global_env.set_pod_deployment(True)
            # Iterate through the list to find and extract the values
            if self.args.pod_specs is not None and self.args.pod_deployment:
                for param in self.args.pod_specs:
                    if 'pod_priviliged' in param:
                        self.privpod_value = param.split('=')[1]  # Extract value after '='
                    elif 'service_account' in param:
                         self.sa_account_value = param.split('=')[1]  # Extract value after '='

        # handle tool attack
        if self.args.tool == 'kubehunter':       
            self.kubehunter = kubehunter()
            if self.args.pod_specs is not None or self.args.pod_deployment:
                print("Kubehunter can only be executed from cluster or deployed as pod via its '--attack pod_scan'")
                return
            if self.args.attack == "help" or self.args.attack == "options":
                self.kubehunter.handle_args(self.args.attack)
                return
            self.parser = KubehunterParser()
            if self.args.param is None:
                self.out, self.final_command, self.local_env, self.parse_output = self.kubehunter.handle_args(self.args.attack)
            else:
                self.out, self.final_command, self.local_env, self.parse_output = self.kubehunter.handle_args(self.args.attack, self.args.param)
        elif self.args.tool == 'redkube':
            self.redkube = redkube()
            if self.args.pod_specs is not None or self.args.pod_deployment:
                print("Redkube can only be executed from cluster.")
                return
            if self.args.attack == "help"or self.args.attack == "options":
                self.redkube.handle_args(self.args.attack)
                return
            if self.args.param is None:
                self.out, self.final_command, self.local_env, self.parse_output = self.redkube.handle_args(self.args.attack)
            else:
                self.out, self.final_command, self.local_env, self.parse_output = self.redkube.handle_args(self.args.attack, self.args.param)
        elif self.args.tool == 'nmap':
            self.nmap = nmap()
            if self.args.attack == "help" or self.args.attack == "options":
                self.nmap.handle_args(self.args.attack)
                return
            if self.args.param is None:
                self.out, self.final_command, self.local_env, self.parse_output = self.nmap.handle_args(self.args.attack)
            else:
                self.out, self.final_command, self.local_env, self.parse_output = self.nmap.handle_args(self.args.attack, self.args.param)
        elif self.args.tool == 'kdigger':
            if self.args.pod_specs is not None and self.args.pod_deployment:
                if self.privpod_value is None and  self.sa_account_value is None:
                    print("The specified values are wrong.")
                    return
                self.kdigger = kdigger(self.privpod_value,self.sa_account_value)
            if self.args.attack == "help" or self.args.attack == "delete_pod" or self.args.attack == "options" or self.args.attack == "options_dig":
                self.kdigger.handle_args(self.args.attack)
                return

            if self.args.param is None:
                self.out, self.final_command, self.local_env, self.parse_output = self.kdigger.handle_args(self.args.attack)
            else:
                
                self.out, self.final_command, self.local_env, self.parse_output = self.kdigger.handle_args(self.args.attack, self.args.param)
        elif self.args.tool == 'stratusred':
            self.stratusred = stratusred()
            if self.args.attack == "help" or self.args.attack == "list" or self.args.attack == "clean" or self.args.attack == "cur" or self.args.attack == "list-persist" or self.args.attack == "options":
                self.stratusred.handle_args(self.args.attack)
                return

            if self.args.param is None:
                self.out, self.final_command, self.local_env, self.parse_output = self.stratusred.handle_args(self.args.attack)
            else:
                self.out, self.final_command, self.local_env, self.parse_output = self.stratusred.handle_args(self.args.attack, self.args.param)
        elif self.args.tool == 'badpods':
            self.badpods = badpods()
            if self.args.attack == "help" or self.args.attack == "clean" or self.args.attack == "status" or self.args.attack == "verbose" or self.args.attack == "type" or self.args.attack == "options" or self.args.attack == "access-scope" or self.args.attack == "resource":
                self.badpods.handle_args(self.args.attack)
                return
            if self.args.param is None:
                self.out, self.final_command, self.local_env, self.parse_output = self.badpods.handle_args(self.args.attack)
            else:
                self.out, self.final_command, self.local_env, self.parse_output = self.badpods.handle_args(self.args.attack, self.args.param)
        elif self.args.tool == 'flightsim':
            
            if self.args.pod_specs is not None and self.args.pod_deployment:
                if self.privpod_value is None and  self.sa_account_value is None:
                    print("The specified values are wrong.")
                    return
                self.flightsim = flightsim(self.privpod_value,self.sa_account_value)
            else:
                self.flightsim = flightsim()
            if self.args.attack == "help" or self.args.attack == "options" or self.args.attack == "run --help" or self.args.attack == "list":
                self.flightsim.handle_args(self.args.attack)
                return
  
            if self.args.param is None:
                self.out, self.final_command, self.local_env, self.parse_output = self.flightsim.handle_args(self.args.attack)
            else:
                self.out, self.final_command, self.local_env, self.parse_output = self.flightsim.handle_args(self.args.attack, self.args.param)
        else:
            print("Specify the Tool Name with --tool TOOLNAME.")

        if self.out is None and self.final_command is None and self.local_env is None and self.parse_output is False:
            print("Error while executing the Attack, please check the Tool and Attack Name.")
            return


        # set timestamp end
        self.global_env.set_timestamp_end(helper.get_current_timestamp())

        # set result code
        if self.out.return_code is not None: 
            self.global_env.set_result_code(self.out.return_code)

        if self.out.return_code == 0:
            if not self.global_var.get_instance().get_lite_version():
                GlobalVariables.get_instance().get_env().set_tool_name(self.args.tool)
                self.database_insert()
            else:
                print("No DB insert due to usage of light version")
        else:
            print("Specify the Attack to execute.")

    def run_playbook(self):

        # set timestamp start
        self.global_env.set_timestamp_start(helper.get_current_timestamp())

        # Make Playbook Name Lowercase
        self.args.playbook = self.args.playbook.lower()

        files = []
        # Set Path 
        if self.args.playbook.startswith("demo") or self.args.playbook.startswith("default"):
            self.path = self.path + "default/"
            files = self.files_default.copy()

        if self.args.playbook.startswith("template") or self.args.playbook.startswith("generated"):
            self.path = self.path + "generated/"
            files = self.files_generated.copy()

        if self.args.playbook.startswith("general") or self.args.playbook.startswith("general"):
            self.path = self.path + "general/"
            files = self.files_general.copy()

        # Set Filename
        if self.args.number:
            try:
                if int(self.args.number) > 0 and int(self.args.number) <= len(files):
                    self.path = self.path + files[int(self.args.number) - 1]
                else:
                    print(f"Error: The number '{self.args.number}' is not in the range of the available Playbooks.")
                    return
            except Exception as e:
                print(f"Error: {e}")
        else:
            self.path = self.path + self.args.playbook

        try:
            # Execute Playbook and capture the result, including the return code
            result = subprocess.run(
                ['bash', self.path], 
                check=False,  # Do not raise an exception automatically on a non-zero return code
                stdout=subprocess.PIPE,  # Capture standard output
                stderr=subprocess.PIPE,  # Capture standard error
                text=True  # Output will be captured as a string
            )

            if result.returncode == 0 and not self.global_var.get_instance().get_lite_version():
                # set timestamp end
                print(f"Script output:\n{result.stdout}")
                self.out.captured_output = result.stdout
                self.global_env.set_timestamp_end(helper.get_current_timestamp())
                self.database_insert() 
            elif result.returncode == 0 and self.global_var.get_instance().get_lite_version():
                print(f"Script output:\n{result.stdout}")
            elif result.returncode != 0:
                print("An Error occured during Script execution")
                print(f"Script error: {result.stderr}")

        except Exception as e:
            print(f"Error executing the shell script: {e}")

    def handle_testcase(self):
        if self.args.testcase == "help":
            self.kubehunter.handle_args(self.args.attack)
            return
        if self.args.testcase.lower() == "kubernetes":
            if self.args.tactic == "help":
                self.print_testcase_tactic_help()
            elif self.args.tactic.lower() in self.kubernetes_tactics and self.args.technique:
                # Execute Testcase
                if self.args.tactic.lower() == "initial_access":
                    if self.args.technique == "help":
                        InitialAccessArgs().print_testcases()
                    else:
                        InitialAccessArgs().handle_testcase_tactic(self.args.technique)
                elif self.args.tactic.lower() == "execution":
                    if self.args.technique == "help":
                        ExecutionArgs().print_testcases()
                    else:
                        ExecutionArgs().handle_testcase_tactic(self.args.technique, self.args.value)
                elif self.args.tactic.lower() == "persistence":
                    if self.args.technique == "help":
                        PersistenceArgs().print_testcases()
                    else:
                        PersistenceArgs().handle_testcase_tactic(self.args.technique)
                elif self.args.tactic.lower() == "privilege_escalation":
                    if self.args.technique == "help":
                        PrivilegeEscalationArgs().print_testcases()
                    else:
                        PrivilegeEscalationArgs().handle_testcase_tactic(self.args.technique)
                elif self.args.tactic.lower() == "defense_evasion":
                    if self.args.technique == "help":
                        DefenseEvasionArgs().print_testcases()
                    else:
                        DefenseEvasionArgs().handle_testcase_tactic(self.args.technique)
                elif self.args.tactic.lower() == "credential_access":
                    if self.args.technique == "help":
                        CredentialAccessArgs().print_testcases()
                    else:
                        CredentialAccessArgs().handle_testcase_tactic(self.args.technique)
                elif self.args.tactic.lower() == "discovery":
                    if self.args.technique == "help":
                        DiscoveryArgs().print_testcases()
                    else:
                        DiscoveryArgs().handle_testcase_tactic(self.args.technique)
                elif self.args.tactic.lower() == "lateral_movement":
                    if self.args.technique == "help":
                        LateralMovementArgs().print_testcases()
                    else:
                        LateralMovementArgs().handle_testcase_tactic(self.args.technique)
                elif self.args.tactic.lower() == "collection":
                    if self.args.technique == "help":
                        CollectionArgs().print_testcases()
                    else:
                        CollectionArgs().handle_testcase_tactic(self.args.technique)
                elif self.args.tactic.lower() == "impact":
                    if self.args.technique == "help":
                        ImpactArgs().print_testcases()
                    else:
                        ImpactArgs().handle_testcase_tactic(self.args.technique)
        elif self.args.testcase.lower() == "open ran":
            if self.args.tactic == "help":
                print("TODO")
            if self.args.tactic in self.oran_tactics and self.args.technique == "help":
                print("TODO")
        else:
            print("Specify the Testcase Name with --testcase TESTCASE-NAME and --tactic TACTIC-NAM and --technique TECHNIQUE-NAME to execute a Testcase.")

    def show_playbooks(self):
        # Debug if no files are available
        if not self.files_default and not self.files_generated and not self.files_general:
            print("Create Templates via Clusterforce to list!")
            
        # Print Folder Names
        if self.files_default:
            print("Default Playbooks:")
            for index, file in enumerate(self.files_default):
                print(f"{index+1}. {file}")

        if self.files_generated:
            print("\nGenerated Playbooks:")
            for index, file in enumerate(self.files_generated):
                print(f"{index+1}. {file}")

        if self.files_general:
            print("\nGeneral Playbooks:")
            for index, file in enumerate(self.files_general):
                print(f"{index+1}. {file}")

    def get_files(self, folder_name):

        ret = []
        # Get Folder Names
        folder_path = os.path.join(self.path, folder_name)

        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            if files:
                if folder_name == "default":
                    ret.extend(files)
                if folder_name == "generated":
                    ret.extend(files)
                if folder_name == "general":
                    ret.extend(files)
        else:
            print(f"The folder '{folder_path}' does not exist.")
            
        return ret

    def print_tool_help(self):
        self.table.print_table(self.header_tools, self.row_tools)

    def print_testcase_help(self):
        self.table.print_table(self.header_test, self.row_test)
        
    def print_testcase_tactic_help(self):
        self.table.print_table(self.header_test_tactic, self.row_test_tactic)
    
    def handle_attack(self):
        print('Specify the Tool Name with --tool TOOLNAME to execute a attack.')
        
    def database_insert(self):
        # connect
        try:
            print("")
            self.db.connect_db("collection")
            
            # set Metavalues
            if self.final_command:
                self.global_env.set_command(self.final_command)
            
            self.global_env.set_file_output_raw(self.out.captured_output)

            # check if tool has parser
            if self.parser is not None and self.parse_output is True:
                self.parser.set_data(self.out.captured_output)
                mitre, cve = self.parser.parse_vulnerabilities()
                self.global_env.set_cve(cve)
                self.global_env.set_mitre(mitre)

            metavalues = self.global_env.to_json(output=True)
            
            # add locals 
            if self.local_env:
                metavalues.update(self.local_env.to_json())

            if metavalues["command"] and isinstance(metavalues["command"], str):
                # Convert to String
                metavalues["command"] = metavalues["command"].split()

            print(metavalues)
            id_doc = self.db.insert_document(metavalues)
            print("Inserted into DB Document: ",id_doc)
            # save id somewhere in thread class

            # close connection
            self.global_env.set_variable_to_default(self.global_env.translate_variable("file_output_raw"))
            self.db.close_connection()
        except Exception as e:
            print(e)

    
    def check_command(self, command):
        return shutil.which(command) is not None


    def check_and_install(self):

        # Check if nslookup is installed
        if not self.check_command("nslookup"):
            print("nslookup is not installed. Running install_nslookup.sh...")
            subprocess.run(["bash", "install_nslookup.sh"], check=True)
        else:
            print("nslookup is already installed.")

        # Check if curl is installed
        if not self.check_command("curl"):
            print("curl is not installed. Running install_curl.sh...")
            subprocess.run(["bash", "install_curl.sh"], check=True)
        else:
            print("curl is already installed.")

        # Check if ssh is installed
        if not self.check_command("ssh"):
            print("ssh is not installed. Running install_ssh.sh...")
            subprocess.run(["bash", "install_ssh.sh"], check=True)
        else:
            print("ssh is already installed.")
