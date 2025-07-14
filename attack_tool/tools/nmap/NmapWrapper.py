from environment.global_const import GlobalVariables
from tools.base_classes.wrapper_base import Wrapper

from help.file_name_generator import gen_file_name

class NmapWrapper(Wrapper):

    def __init__(self, nmap_env):
        self.command = 'nmap'
        self.sudo = True
        self.global_env = GlobalVariables.get_instance().get_env()
        self.env = nmap_env

    def help(self):
        cmd = ['--help']	
        return cmd

    def scan_syn(self):
        self.env.set_scan_type("-sS")
        return self._generate_command()

    def scan_con(self):
        self.env.set_scan_type("-sT")
        return self._generate_command()

    def scan_udp(self):
        self.env.set_scan_type("-sU")
        return self._generate_command()

    def scan_agg(self, protocol):
        if protocol == "udp":
            self.env.set_scan_type("-sU")
        else:
            self.env.set_scan_type("-sS") 
            
        return self._generate_command(agg=True)

    def scan_null(self):
        self.env.set_scan_type("-sN")
        return self._generate_command()

    def scan_fin(self):
        self.env.set_scan_type("-sF")
        return self._generate_command()

    def scan_version(self, protocol):
        if protocol == "udp":
            self.env.set_scan_type("-sU")
        else:
            self.env.set_scan_type("-sS")  
          
        return self._generate_command(version=True, os=True)
    
    
    def _generate_command(self, scan_type=True, output=False, verbose=True, noping=True, speed=True,
                          version=False, script=False, custom_script=False, os=False, agg=False, subnet=False):
        cmd = []
        if scan_type:
            cmd.append(self.env.get_scan_type())
        if version:
            self.env.set_version()
            cmd.append(self.env.get_version())
        if script:
            self.env.set_script()
            cmd.append(self.env.get_script())
        if os:
            self.env.set_os()
            cmd.append(self.env.get_os())
        if noping:
            self.env.set_noping()
            cmd.append(self.env.get_noping())
        if speed:
            cmd.append(self.env.get_speed())
        if agg:   
            self.env.set_agg()
            cmd.append(self.env.get_agg())
        if verbose:
            self.env.set_verbose()
            cmd.append(self.env.get_verbose())
        if custom_script:
            cmd.append(self.env.get_custom_script())
        
        cmd.append(self.env.get_ip())
        if subnet:
            cmd.append(self.env.get_subnet())
        
        if self.env.get_ports() != "":
            cmd.append(self.env.get_ports())

        if output:
            cur_format = self.env.get_format()
            cmd.extend(self._add_output_format(cur_format))
        return cmd

    def _add_output_format(self, output):
        if output in ['normal', 'all', 'scriptkiddie' 'list']:
            res = self._output_format_helper(output, 'txt')
        elif output == 'grep':
            res = self._output_format_helper(output, 'gnmap')
        elif output in self.env.format_list:
            res = self._output_format_helper(output, output)
        else:
            print("ERROR: Output format not supported.")
            return
        return res

    def _output_format_helper(self, output_format='xml', extension='xml'):
        path = 'reports/nmap/'
        file_name = gen_file_name('nmap', output_format, extension)
        format_param = self.env.format_list[self.env.get_format()]
        out = [format_param, path + file_name]
        return out
