class Template:
    _instance = None 

    def __init__(self):
        self._result_list = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_result_list(self):
        return self._result_list

    def empty_result_list(self):
        self._result_list = []

    def add_to_result_list(self, item):
        self._result_list.append(item)
        return self._adjacent_duplicates()

    def toString(self):
        return ', '.join(map(str, self._result_list))

    def _adjacent_duplicates(self):
        if len(self._result_list) < 2:
            return False

        for i in range(len(self._result_list) - 1):
            if self._result_list[i].__eq__(self._result_list[i + 1]):
                del self._result_list[i + 1]
                return True

        return False
