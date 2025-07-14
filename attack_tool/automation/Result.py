class Result:
    def __init__(self, options, command, toolame, version, hostname, resultcode):
        self._options = options
        self._command = command
        self._toolame = toolame
        self._version = version
        self._hostname = hostname
        self._resultcode = resultcode

    def get_options(self):
        return self._options

    def set_options(self, options):
        self._options = options

    def get_command(self):
        return self._command

    def set_command(self, command):
        self._command = command

    def get_toolame(self):
        return self._toolame

    def set_toolame(self, toolame):
        self._toolame = toolame

    def get_version(self):
        return self._version

    def set_version(self, version):
        self._version = version

    def get_hostname(self):
        return self._hostname

    def set_hostname(self, hostname):
        self._hostname = hostname

    def get_resultcode(self):
        return self._resultcode

    def set_resultcode(self, resultcode):
        self._resultcode = resultcode

    def __eq__(self, other):
        if isinstance(other, Result):
            return (
                self._options == other._options and
                self._command == other._command and
                self._toolame == other._toolame and
                self._version == other._version and
                self._hostname == other._hostname and
                self._resultcode == other._resultcode
            )
        return False

    def __str__(self):
        return f"Options: {self._options}, Command: {self._command}, Toolame: {self._toolame}, Version: {self._version}, Hostname: {self._hostname}, Result Code: {self._resultcode}"