from environment.global_const import GlobalVariables
from help.file_name_generator import gen_file_name
from tools.base_classes.wrapper_base import Wrapper

class KubescapeWrapper(Wrapper):

    def __init__(self, env):
        self.command = 'kubescape'
        self.sudo = True
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = env

    def help(self):
        cmd = ['--help']
        return cmd
        
    def scan(self):
        cmd = ['scan']
        return self._generate_command(cmd)

    def scan_framework_mitre(self):
        cmd = ['scan', 'framework']
        self.env.set_framework('mitre')
        return self._generate_command(cmd, framework=True)

    def scan_framework_nsa(self):
        cmd = ['scan', 'framework']
        self.env.set_framework('nsa')
        return self._generate_command(cmd, framework=True)
    
    def scan_workload(self):
        cmd = ['scan', '--exclude-namespaces', 'kube-system']
        return self._generate_command(cmd) 

    def _generate_command(self, cmd, resource=False, framework=False, output=False, verbose=True, log_level=False):
        if framework and "framework" in cmd:
            cmd.append(self.env.get_framework())
        if resource:
            cmd.append(self.env.get_resource())
        if verbose:
            cmd.extend(['--verbose'])
        if log_level:
            cmd.extend(['--logger', self.env.get_log_level()])
        if output:
            cmd.extend(self._add_output_format(self.env.get_out_format()))
        return cmd

    def _add_output_format(self, output):
        res = ''
        if output == 'json':
            res = self._output_format_helper(output, 'json')
        elif output == 'pp':
            res = self._output_format_helper(output, 'txt')
        elif output in self.env.format_list:
            res = self._output_format_helper(output, self.env.format_list[output])
        else:
            print("ERROR: Output format not supported.")
            return
        return res

    def _output_format_helper(self, format='json', extension='json'):
        path = 'reports/kubescape/'
        file_name = gen_file_name('kubescape', format, extension)
        output_params = (['--format', self.env.format_list[format], '--output', path + file_name])
        return output_params
