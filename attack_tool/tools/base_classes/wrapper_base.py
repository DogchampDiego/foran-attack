import subprocess
import threading

from output.output import Output
from environment.global_const import GlobalVariables

class Wrapper():
    def __init__(self):
        self.final_command = None
        self.sudo = False
     
    def _execute_command(self, cmd, sudo=False, cwd_path=None, command=True, show_output=True):  # Execute a command and return the output
        split_cmds = []
        if isinstance(cmd, list):
            for item in cmd:
                split_items = item.split()  # Split each string by spaces
                split_cmds.extend(split_items)  # Add split items to the new list
        elif isinstance(cmd, str):
            split_cmds = cmd.split()
        else:
            print("The command is neither a list nor a string.")

        if command:
            split_cmds.insert(0, self.command)
        if sudo or self.sudo:
            split_cmds.insert(0, "sudo")
        if cwd_path:
            output = subprocess.Popen(
                split_cmds,
                cwd= cwd_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        else:
            output = subprocess.Popen(
                split_cmds,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

        self.final_command = split_cmds
        if show_output:
            print(self.final_command)
        
        captured_output_lines = []
        captured_error_lines = []
        output_lock = threading.Lock()
        error_lock = threading.Lock()

        error_thread = threading.Thread(target=self._capture_output, args=(output.stderr, captured_error_lines, error_lock))
        output_thread = threading.Thread(target=self._capture_output, args=(output.stdout, captured_output_lines, output_lock))

        error_thread.start()
        output_thread.start()

        error_thread.join()
        output_thread.join()

        output.wait()

        captured_output = ''.join(captured_output_lines)
        captured_error = ''.join(captured_error_lines)

        return Output(captured_output, captured_error, output.returncode)

    def _execute_command_without_output(self, cmd, sudo=False, command=True): 
        split_cmds = []
        if isinstance(cmd, list):
            for item in cmd:
                split_items = item.split()  # Split each string by spaces
                split_cmds.extend(split_items)  # Add split items to the new list
        elif isinstance(cmd, str):
            split_cmds = cmd.split()
        else:
            print("The command is neither a list nor a string.")

        if command:
            split_cmds.insert(0, self.command)
        if sudo or self.sudo:
            split_cmds.insert(0, "sudo")

        output = subprocess.Popen(
                split_cmds,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        
        captured_output_lines = []
        captured_error_lines = []
        output_lock = threading.Lock()
        error_lock = threading.Lock()

        error_thread = threading.Thread(target=self._capture_output, args=(output.stderr, captured_error_lines, error_lock))
        output_thread = threading.Thread(target=self._capture_output, args=(output.stdout, captured_output_lines, output_lock))

        error_thread.start()
        output_thread.start()

        error_thread.join()
        output_thread.join()

        output.wait()

        captured_output = ''.join(captured_output_lines)
        captured_error = ''.join(captured_error_lines)

        return Output(captured_output, captured_error, output.returncode)

    def __methodnames__(self, class_name):
         return [method_name for method_name in dir(class_name) if callable(getattr(class_name, method_name)) and not method_name.startswith("_")]
     
    def custom_scan(self, command_values):
        return self._execute_command(command_values, self.sudo)

    def string_execute(self,cmd):
        cmd = self.command + " "+ cmd
        output = subprocess.Popen(
                cmd,
                shell= True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

        self.final_command = cmd
        print(self.final_command)
        
        captured_output_lines = []
        captured_error_lines = []
        output_lock = threading.Lock()
        error_lock = threading.Lock()

        error_thread = threading.Thread(target=self._capture_output, args=(output.stderr, captured_error_lines, error_lock))
        output_thread = threading.Thread(target=self._capture_output, args=(output.stdout, captured_output_lines, output_lock))

        error_thread.start()
        output_thread.start()

        error_thread.join()
        output_thread.join()

        output.wait()

        captured_output = ''.join(captured_output_lines)
        captured_error = ''.join(captured_error_lines)

        print("Captured Output:")
        print(captured_output)
        print("Captured Error:")
        print(captured_error)
        print("Return Code:", output.returncode)

        return Output(captured_output, captured_error, output.returncode)

    def _capture_output(self, stream, lines_list, lock):
        for line in stream:
            with lock:
                lines_list.append(line)
                print(line, end='')

    def exec_command_on_pod(self, command):
        print(f"# Executing command: {command}")
        GlobalVariables.get_instance().get_env().set_command(command)                
        try:
            print(command)
            if type(command) == list:
                command = self.command + " " + " ".join(command)

            
            print(["kubectl", "exec", "-it", self.env.get_pod_name(), "--", "/bin/bash", "-c", command])
            result=subprocess.run(["kubectl", "exec", "-it", self.env.get_pod_name(), "--", "/bin/bash", "-c", command], check=True, capture_output=True, text=True)
            print(result.stdout)
            self.final_command = command
            return Output(result.stdout, result.stderr, result.returncode)
        except Exception as e:
            print(e)
            return None
