class Output():
    def __init__(self, captured_output, captured_error, return_code):
        self.captured_output = captured_output
        self.captured_error = captured_error
        self.return_code = return_code

    def get_captured_output(self):
        return self._captured_output

    def get_captured_error(self):
        return self._captured_error

    def get_return_code(self):
        return self._return_code

    def set_captured_output(self, captured_output):
        self._captured_output = captured_output

    def set_captured_error(self, captured_error):
        self._captured_error = captured_error

    def set_return_code(self, return_code):
        self._return_code = return_code

