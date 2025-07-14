class LocalEnv():
    def __init__(self):
        pass
    
    def set_variable_from_input(self, user_input):
        command, variable, value = user_input.split(" ", 2)
        new_var = self.translate_variable(variable)

        if command == "set" and hasattr(self, new_var):
            setattr(self, new_var, value)
            return True
        else:
            return False

    def to_json(self):
        data = {}
        for attr_name, attr_value in self.__dict__.items():
            key = attr_name.lstrip('_')
            if attr_value is not None:
                data[key] = attr_value

        return data
    