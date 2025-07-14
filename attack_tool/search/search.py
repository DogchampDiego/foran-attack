import subprocess

class CveSearchSploitWrapper:
    def __init__(self):
        self.tool_path = 'cve_searchsploit'

    def install_tool(self):
        subprocess.call(["bash", "search/install_search.sh"])

    def check_installed(self):
        command = "command -v cve_searchsploit"
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.returncode == 0

    def search_exploits(self, cve_id):
        command = self.tool_path +" "+ cve_id
        print(command)
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        if process.returncode != 0:
            print(f"An error occurred: {process.stderr}")
            return None

        return process.stdout
