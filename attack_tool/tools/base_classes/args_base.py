from help.table import Table
import help.helper as helper

class Args():
    def __init__(self):
        self.out = None
        self.name = None
        self.parse_output = False
        self.table = Table()
        self.column = ["Method", "Description"]
        
    def split_key(self, string):
        str = string.split('][')
        return self.remove_brackets(str)

    def split_value(self, string):
        split = string.split('][')
        for i in range(len(split)):
            if ',' in split[i]:
                split[i] = split[i].split(',')
                split[i] = self.remove_brackets(split[i])
            else:
                split[i] = split[i].replace(']', '')
                split[i] = split[i].replace('[', '')
        return split

    def remove_brackets(self, string):
        return [item.replace('[', '').replace(']', '') for item in string]

    def string_to_dict(self, keys, values):
        ret = dict(zip(keys, values))
        for key in ret:
            if ret[key] == "True":
                ret[key] = True
                print(type(ret[key]))
            if ret[key] == "False":
                ret[key] = False
            if ret[key] == "None":
                ret[key] = None
        return ret
    
    def create_admin_role(self):
        helper.create_service_account_and_binding()