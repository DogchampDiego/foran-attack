import socket
import sys
from datetime import datetime

from colorama import Fore, Style

from environment.global_const import GlobalVariables
from state.menu_state import MenuState

import random

import subprocess
# Banner

tool_banner = """
 ██████╗██╗     ██╗   ██╗███████╗████████╗███████╗██████╗ ███████╗ ██████╗ ██████╗  ██████╗███████╗
██╔════╝██║     ██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
██║     ██║     ██║   ██║███████╗   ██║   █████╗  ██████╔╝█████╗  ██║   ██║██████╔╝██║     █████╗  
██║     ██║     ██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  
╚██████╗███████╗╚██████╔╝███████║   ██║   ███████╗██║  ██║██║     ╚██████╔╝██║  ██║╚██████╗███████╗
 ╚═════╝╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
---------------------------------------------------------------------------------------------------
""".rstrip("\n")


# Options for the Menu
OPTIONS_BASE = {
    'START': {
        '1': 'Attack Phases',
        '2': 'Tools',
        '3': 'Demonstrator (One-Click Attack)',
        '4': 'Environment',
        '5': 'Reporting',
        '6': 'Config',
        '7': 'Container',
        '8': 'Testing',
    },
    'ATTACK_PHASE': {
        '1': 'Reconnaissance',
        '2': 'Initial Access',
        '3': 'Execution',
        '4': 'Persistence',
        '5': 'Privilege Escalation',
        '6': 'Defense Evasion',
        '7': 'Credential Access',
        '8': 'Discovery',
        '9': 'Lateral Movement',
        '10': 'Collection',
        '11': 'Command and Control',
        '12': 'Exfiltration',
        '13': 'Impact',
    },
    'TOOLS': {
        '1': 'Kubehunter',
        '2': 'Nmap',
        '3': 'Kubescape',
        '4': 'Trivy',
        '5': 'Red-Kube',
        '6': 'Stratus-Red-Team',
        '7': 'KDigger',
        '8': 'Rakkess',
        '9': 'CDK',
        '10': 'Flightsim',
        '11': 'HackerContainer',
        '12': 'BadPods',
        '13': 'MTKPI',
    },
    'REPORTING': {
        '1': 'Option 1',
        '2': 'Option 2',
        '3': 'Option 3',
    },
    'DEMONSTRATOR': {
        '1': 'Option 1',
        '2': 'Option 2',
        '3': 'Option 3',
    },
    'ENVIRONMENT': {
        '1': 'Option 1',
        '2': 'Option 2',
        '3': 'Option 3',
    },
    'CONFIG': {
        '1': 'Option 1',
        '2': 'Option 2',
        '3': 'Option 3',
    },
    'CONTAINER': {
        '1': 'Mtkpi',
        '2': 'HackerContainer',
    },
    'TESTING': {
        '1': 'Kubernetes',
        '2': 'Open-RAN',
    },
}

OPTIONS_ATTACK = {
    'RECONNAISSANCE': {
        '1': 'Nmap',
        '2': 'Kubescape',
        '3': 'Trivy',
        '4': 'CDK',
        '5': 'Red-Kube',
        '6': 'KDigger',
    },
    'INITIAL_ACCESS': {
        'PHASE':{
            '1': 'Kubehunter',
            '2': 'KDigger',
        },
        'TEST':{
            '1': 'Kubeconfig'
        }
    },
    'EXECUTION': {
        'PHASE':{
            '1': 'Stratus-Red-Team',
            '2': 'CDK',
            '3': 'Kubehunter',
            '4': 'KDigger',
            '5': 'BadPods',
        },
        'TEST':{
            '1': "Exec into Container",
            '2': "New Container",
            '3': "SSH-Server running in inside Container",
            '4': 'bash/cmd in container',
        }
    },
    'PERSISTENCE': {
        'PHASE':{
            '1': 'Stratus-Red-Team',
            '2': 'BadPods',
            '3': 'CDK',
            '4': 'Kubehunter',
            '5': 'Red-Kube',
            '6': 'KDigger',
        },
        'TEST':{
            '1': "Backdoor Container",
            '2': "Writable hostPath mount",
            '3': "Kubernetes CronJob",
        }
    },
    'PRIVILEGE_ESCALATION': {
        'PHASE':{
            '1': 'Stratus-Red-Team',
            '2': 'Rakkess',
            '3': 'CDK',
            '4': 'BadPods',
            '5': 'Kubehunter',
            '6': 'Red-Kube',
            '7': 'KDigger',
        },
        'TEST':{
            '1': "Privileged Container",
            '2': "Cluster-admin binding",
            '3': "Disable Namespacing",
        }
    },
    'DEFENSE_EVASION': {
        'PHASE':{
            '1': 'BadPods',
            '2': 'Kubehunter',
            '3': 'Red-Kube',
            '4': 'KDigger',
        },
        'TEST':{
            '1': "Delete k8s events",
            '2': "Pod / container name similarity",
            '3': "Clear Container logs",
        }  
    },
    'CREDENTIAL_ACCESS': {
        'PHASE':{
            '1': 'Stratus-Red-Team',
            '2': 'CDK',
            '3': 'Kubehunter',
            '4': 'Red-Kube',
            '5': 'KDigger',
        },
        'TEST':{
            '1': "List K8s secrets",
            '2': "Access container service account",
            '3': "Applications credentials in configuration files",
        }
    },
    'DISCOVERY': {
        'PHASE':{
            '1': 'Nmap',
            '2': 'Kubescape',
            '3': 'Trivy',
            '4': 'Rakkess',
            '5': 'CDK',
        },
        'TEST':{
            '1': "Network mapping",
        }
    },
    'LATERAL_MOVEMENT': {
        'PHASE':{
            '1': 'CDK',
            '2': 'Kubehunter',
            '3': 'KDigger',
        },
        'TEST':{
            '1': "Cluster internal networking",
            '2': "CoreDNS Poisoning",
        }
    },
    'COLLECTION': {
        'PHASE':{
            '1': 'Stratus-Red-Team',
            '2': 'CDK',
            '3': 'Kubehunter',
            '4': 'Red-Kube',
            '5': 'KDigger',
        },
        'TEST':{
            '1': "No Test available",
        }
    },
    'COMMAND_CONTROL': {
        '1': 'Flightsim',
        '2': 'Red-Kube',
        '3': 'KDigger',
    },
    'EXFILTRATION': {
        '1': 'Flightsim',
        '2': 'Stratus-Red-Team',
        '3': 'Red-Kube',
    },
    'IMPACT': {
        'PHASE':{
            '1': 'Kubehunter',
        },
        'TEST':{
            '1': "Data Destruction",
        }
    },
}

OPTIONS_TESTING = {
    'KUBERNETES': {
        '1': 'Initial Access',
        '2': 'Execution',
        '3': 'Persistence',
        '4': 'Privilege Escalation',
        '5': 'Defense Evasion',
        '6': 'Credential Access',
        '7': 'Discovery',
        '8': 'Lateral Movement',
        '9': 'Collection',
        '10': 'Impact',
    },
    'OPENRAN': {
        '1': 'Option 1',
        '2': 'Option 2',
        '3': 'Option 3',
    },

}


TOOLS = {
    'KUBEHUNTER': {
        '1': 'menu',
    },
    'KUBESCAPE': {
        '1': 'menu',
    },
    'NMAP': {
        '1': 'menu',
    },
    'TRIVY': {
        '1': 'menu',
    },
    'REDKUBE': {
        '1': 'menu',
    },
    'STRATUSREDTEAM': {
        '1': 'menu',
    },
    'KDIGGER': {
        '1': 'menu',
    },
    'RAKKESS': {
        '1': 'menu',
    },
    'CDK': {
        '1': 'menu',
    },
    'FLIGHTSIM': {
        '1': 'menu',
    },
    'BADPODS': {
        '1': 'menu',
    },
    'MTKPI': {
        '1': 'menu',
    },
}

result_code= {
        '101': 'OK',
        '201': 'ERROR',
        '301': 'SOMETHING WENT WRONG',
    }


# Print the menu with the OPTIONS dict
def print_menu():
    print()
    state = GlobalVariables.get_instance().get_menu_state()
    key = state.name
    if state.value <=10:
        sub_menu = OPTIONS_BASE[key]
    elif state.value >= 11 and state.value <=19:
        sub_menu = OPTIONS_TESTING[key]
    elif state.value >= 20 and state.value <=32:
        sub_menu = OPTIONS_ATTACK[key]
    elif state.value >=40 and state.value <=60:
        sub_menu = TOOLS[key]

    print(f"Menu options for {Fore.RED}{key}{Style.RESET_ALL}:")

    if 'PHASE' in sub_menu and  'TEST' in sub_menu:
        if GlobalVariables.get_instance().get_menu_tree()[-2] == MenuState.ATTACK_PHASE:
            sub_menu = sub_menu["PHASE"]
        if GlobalVariables.get_instance().get_menu_tree()[-2] == MenuState.KUBERNETES:
            sub_menu = sub_menu["TEST"]

    for option_key, option_value in sub_menu.items():
        print(f"{option_key}: {option_value}")


def handle_globals(menu_state,menu_tree):
    GlobalVariables.get_instance().set_menu_state(menu_state)
    if menu_tree.value not in [e.value for e in GlobalVariables.get_instance().get_menu_tree()]:
        GlobalVariables.get_instance().add_menu_tree(menu_tree)

def print_banner():
    print(Fore.RED + tool_banner + Style.RESET_ALL)

def create_cursor():
    list = GlobalVariables.get_instance().get_menu_tree()
    names = [enum.name.capitalize() for enum in list]
    return f"({'/'.join(names)})>> "
    
    
# Metadata Methods
def detect_hostname():
    return socket.gethostname()

def detect_hostip():
    try:     
        # Get the IP address using gethostbyname
        ip_address = socket.gethostbyname(detect_hostname())
        return ip_address
    except Exception as e:
        return str(e)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_current_timestamp():
    timestamp = datetime.utcnow()
    return timestamp

def get_menu_phase():
    start_state = MenuState.INITIAL_ACCESS
    end_state = MenuState.IMPACT

    menu_states = []
    for state in MenuState:
        if start_state.value <= state.value <= end_state.value:
            menu_states.append(state)

    return menu_states

def check_python_interpreter():
    executable = sys.executable

    if "python3" in executable:
        return "python3"
    elif "python" in executable:
        return "python3"
    else:
        return "error"

def regex_ip_port(text):
    import re

    final_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b'
    ip_port = re.findall(final_pattern, text)
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ip = re.findall(ip_pattern, text)

    return ip_port, ip


def create_service_account_and_binding():
    service_account_name = "evil-admin"
    namespace = "default"
    cluster_role_binding_name = "evil-admin-binding"
    cluster_role = "cluster-admin"

    # Create the ServiceAccount
    create_sa_cmd = [
        "kubectl", "create", "serviceaccount", service_account_name, 
        "--namespace", namespace
    ]

    try:
        subprocess.run(create_sa_cmd, check=True)
        print(f"ServiceAccount '{service_account_name}' created in namespace '{namespace}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating ServiceAccount: {e}")

    # Create the ClusterRoleBinding
    create_crb_cmd = [
        "kubectl", "create", "clusterrolebinding", cluster_role_binding_name, 
        "--serviceaccount", f"{namespace}:{service_account_name}", 
        "--clusterrole", cluster_role
    ]

    try:
        subprocess.run(create_crb_cmd, check=True)
        print(f"ClusterRoleBinding '{cluster_role_binding_name}' created for ServiceAccount '{service_account_name}' with cluster-admin role.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating ClusterRoleBinding: {e}")


def delete_service_account_and_binding(service_account_name="evil-admin", namespace="default", cluster_role_binding_name="evil-admin-binding"):
    # Delete the ClusterRoleBinding
    delete_crb_cmd = [
        "kubectl", "delete", "clusterrolebinding", cluster_role_binding_name
    ]

    try:
        subprocess.run(delete_crb_cmd, check=True)
        print(f"ClusterRoleBinding '{cluster_role_binding_name}' deleted.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting ClusterRoleBinding: {e}")

    # Delete the ServiceAccount
    delete_sa_cmd = [
        "kubectl", "delete", "serviceaccount", service_account_name,
        "--namespace", namespace
    ]

    try:
        subprocess.run(delete_sa_cmd, check=True)
        print(f"ServiceAccount '{service_account_name}' deleted from namespace '{namespace}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting ServiceAccount: {e}")


def get_modified_pod_name():
    # Run kubectl command to list all pod names in the default namespace
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", "default", "-o", "jsonpath={.items[*].metadata.name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Check if the command was successful
    if result.returncode != 0:
        return f"Error retrieving pods: {result.stderr.strip()}"

    # Get the pod names from the command output
    pod_names = result.stdout.strip().split()

    # Check if there are any pods available
    if not pod_names:
        return "No pods found in the default namespace."

    # Select a random pod name
    random_pod_name = random.choice(pod_names)

    # Modify the last character of the selected pod name
    last_char = random_pod_name[-1]
    if last_char.isdigit():  # If the last character is a digit
        new_char = str((int(last_char) + 1) % 10)  # Increment digit cyclically
    else:  # If it's not a digit, assume it's an ASCII letter and increment cyclically
        new_char = chr((ord(last_char) + 1 - ord('a')) % 26 + ord('a'))

    # Create the modified pod name
    modified_name = random_pod_name[:-1] + new_char

    return modified_name