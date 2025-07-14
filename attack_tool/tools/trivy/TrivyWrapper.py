from environment.global_const import GlobalVariables
from help.file_name_generator import gen_file_name
from tools.base_classes.wrapper_base import Wrapper

class TrivyWrapper(Wrapper):

    def __init__(self, env):
        self.command = 'trivy'
        self.sudo = True
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env

    def help(self):
        cmd = ['--help']
        return cmd

    def init(self):
        self.env.set_resource("cluster")
        self.env.set_scan_type("vuln")

    def scan_cluster(self):
        self.init()
        return self._generate_command()

    def scan_cluster_all(self):
        self.env.set_resource("cluster")
        return self._generate_command(summary=False, scan_type=False)
                                      
    def scan_cluster_vuln(self):
        self.init()
        return self._generate_command(scan_type=True)

    def scan_cluster_secret(self):
        self.env.set_resource("cluster")
        self.env.set_scan_type("secret")
        return self._generate_command(scan_type=True)

    def scan_cluster_config(self):
        self.env.set_resource("cluster")
        self.env.set_scan_type("config")
        return self._generate_command(scan_type=True)

    def scan_cluster_critical(self):
        self.init()
        self.env.set_severity("CRITICAL")
        return self._generate_command(severity=True)

    def _generate_command(self, resource=True, scan_type=True, severity=False, 
                          summary=True, quiet=True, output=False, timeout=False):
        cmd = ['k8s']
        
        if resource:
            cmd.append(self.env.get_resource())
        if scan_type:
            if scan_type == "config":
                  cmd.append('--component ', self.env.get_components())
            cmd.append('--scanners ' + self.env.get_scan_type())
        if severity and self.env.get_severity() != "":
            cmd.append("--severity " + self.env.get_severity())
        if quiet:
            cmd.append('--quiet')
        if timeout:
            cmd.append('--timeout 5m0s')
        if summary:
            cmd.append("--report summary")
        else:
            cmd.append("--report all")
        
        if output:
            out_format = self.env.get_format()
            cmd.extend(self._add_output_format(out_format))
        return cmd

    def _add_output_format(self, output='json'):
        res = ''
        if output == 'html':
            res = self._output_format_helper(output, 'html')
        elif output == 'xml':
            res = self._output_format_helper(output, 'xml')
        elif output in self.env.format_list:
            res = self._output_format_helper(output, self.env.format_list[output])
        else:
            print("ERROR: Output format not supported.")
            return
        return res

    def _output_format_helper(self, format='json', extension='json'):
        path = 'reports/trivy/'
        file_name = gen_file_name('trivy', format, extension)
        output_params = (['--format', self.env.format_list[format], '-o', path + file_name])
        return output_params