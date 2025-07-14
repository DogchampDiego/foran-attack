import ipaddress
from environment.global_const import GlobalVariables
import re
from database.mongo_db_handler import MongoDBWrapper as db
from help.helper import get_current_timestamp
from help.table import Table

class Campaign:
    _instance = None  # Stores the reference to the singleton instance
    
    def __init__(self):
        self.name = None
        self.id = None
        self.start_date = None
        self.end_date = None
        self.description = None
        self.targets = []
        self.global_var = GlobalVariables.get_instance()
        self.db = db(self.global_var.get_base_dir() + "database/config.ini")
        self.table = Table()
        self.menu = [
            ["campaign info", "Show current campaign infos"],
            ["campaign start", "Start a campaign"],
            ["campaign end", "End a campaign"],
        ]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def set_id(self, id):
        self.id = id
    
    def get_id(self):
        return self.id

    def set_start_date(self, start_date):
        self.start_date = start_date

    def get_start_date(self):
        return self.start_date

    def set_end_date(self, end_date):
        self.end_date = end_date

    def get_end_date(self):
        return self.end_date

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_targets(self, targets):
        self.targets = targets

    def get_targets(self):
        return self.targets

    def parse_targets(self, targets):
        res = True
        validated_targets = []

        for target in targets:
            # Check valid IP address
            try:
                ip = ipaddress.ip_address(target)
                validated_targets.append(ip)
            except ValueError:
                res = False
                print(f"Invalid IP address: {target}")

            # Check valid domain 
            if re.match(r"^[a-zA-Z0-9.-]+$", target):
                validated_targets.append(target)
        return validated_targets, res
    
    def database_insert(self):
        # connect
        self.db.connect_db("collection-campaign")
        
        # insert campaing into database
        self.id = self.db.insert_document(self.to_json())
        print("Campaign ID: ", self.id)
        print("Campaign:", self.to_json())
        
        self.db.close_connection() 
    
    def to_json(self):
        campaign_dict = {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "targets": self.targets
        }
        return campaign_dict
    
    def start(self):
        error = False
        # Dialogue to request user input
        self.start_date = get_current_timestamp()
        self.name = input("Enter the name of the campaign: ")
        self.description = input("Enter a description for the campaign: ")
        targets_input = input("Enter a list of targets (IPs or domains) separated by commas: ")
        self.targets = [target.strip() for target in targets_input.split(",")]
        
        #self.targets, error = self.parse_targets(tmp_targets)
        #if error:
        #    print("Invalid input. Aborting camapaign creation.")
        #    return
        if self.name:
            print("Creating Campaign...")
            self.database_insert()
            print("Campaign created successfully.")
        else:
            print("\nCampaign not created, please set provide a valid name")
            self.description= None
            self.targets=[]
            self.start_date = None
            self.end_date = None

    def print_menu(self):
        if self.name:
            header = ["Parameter","Value"]
            self.table.print_table(header,self.get_info())
        else:
            print("\nPlease start a campaign to see the info")

    def print_command(self):
        print("\nThe commands to use are the following:")

        header = ["Parameter","Value"]
        self.table.print_table(header,self.menu)

    def get_info(self):
        return [
            ["name", self.get_name()],
            ["start_date",  self.get_start_date()],
            ["targets", self.get_targets()],
            ["description", self.get_description()]
        ]

    def end(self):
        # connect
        self.db.connect_db("collection-campaign")

        # update DB
        self.end_date = get_current_timestamp()
        
        if self.db.update_document(self.id,"end_date",self.end_date) == 1:
            print("\nCampaign ended successfully.")
            #clean
            self.id = None
            self.ip = None
            self.name = None
            self.start_date = None
            self.end_date = None
            self.description= None
            self.targets=[]
        else:
            print("Something went wrong...")

        #close
        self.db.close_connection() 
    
    def __str__(self):
        return f"Campaign Name: {self.name}\nStart Date: {self.start_date}\nEnd Date: {self.end_date}\nDescription: {self.description}\nTargets: {', '.join(self.targets)}"

