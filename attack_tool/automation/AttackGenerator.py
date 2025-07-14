from automation.Template import Template
from automation.Result import Result
from help.file_name_generator import get_timestamp
from environment.global_const import GlobalVariables


class AttackGenerator:

    def __init__(self):
        self.script_name = "template_attack_script-" + get_timestamp() + ".sh"
        self.template = Template().get_instance()
        self.results = self.template.get_result_list()
        self.commands = []
    
    def gen_script_name(self):
        self.script_name = "template_attack_script-" + get_timestamp() + ".sh"
    
    def get_commands(self):
        for res in self.results:
            if res.get_resultcode() == 0:
                self.commands.append(res.get_command())
    
    def clean(self):
        self.template.empty_result_list()
        self.commands = []
    
    def generate_script(self):
        if self.template.get_result_list():
            self.gen_script_name()
            self.get_commands()
            with open(GlobalVariables.get_instance().get_base_dir() + "automation/scripts/generated/" + self.script_name, 'w') as script_file:
                script_file.write("#!/bin/bash\n")
                for cmd in self.commands:
                    cmd = " ".join(cmd)
                    script_file.write(cmd + "\n")
                script_file.write("echo 'Attack automation completed.'\n")
                script_file.close()
            self.clean()
        else:
            print("\nUse Commands first to create a template")
