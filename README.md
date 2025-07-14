# Introduction
**Clusterforce** is a versatile security tool designed for assessing and testing the security posture of Kubernetes clusters. It provides both a **Graphical User Interface (GUI)** and a **Command-Line Interface (CLI)** to execute various attack tools and test cases. The tool is particularly useful for penetration testing, and vulnerability assessment in Kubernetes environments.

## Key Features:
- **GUI and CLI Support**: Clusterforce offers both a user-friendly GUI for interactive usage and a CLI for automated or scripted operations.
- **Attack Tools**: It includes a wide range of pre-configured attack tools such as **Nmap**, **KubeHunter**, **Redkube**, **KDigger**, and more, which can be executed at both the **cluster** and **pod** levels.
- **Test Cases**: Clusterforce implements test cases based on the **Kubernetes Threat Matrix**, covering various tactics like **Initial Access**, **Execution**, **Persistence**, **Privilege Escalation**, **Defense Evasion**, **Credential Access**, **Discovery**, **Lateral Movement** and **Impact**
- **Playbook Execution**: Users can execute predefined playbooks for automated testing and attack simulations.
- **Pod Deployment**: Attacks can be executed directly from within Kubernetes pods, with options to configure privileged access and service accounts.
- **Global and Tool-Specific Variables**: Users can set global and tool-specific variables to customize attack parameters.

# Table of Contents

1. [Clusterforce GUI](#clusterforce-gui)
   - [User Manual](#user-manual)
     - [General Commands](#general)
     - [Tool Specific Commands](#tool-specific)
   - [Example Usage](#example-usage)
     - [Setting Variables](#setting-variables)
     - [Campaign](#campaign)
     - [Execute Attack](#execute-attack)

2. [Clusterforce CLI](#clusterforce-cli)
   - [Before CLI Usage](#before-cli-usage)
   - [User Manual](#user-manual-1)
   - [Example Usage](#example-usage-1)
     - [Attack Tool](#attack-tool)
     - [Testcases](#testcases)

3. [Implemented Attack Tools and Testcases](#implemented-attack-tools-and-testcases)
   - [Attack Tools](#attack-tools)
   - [Testcases](#testcases-1)

# Clusterforce GUI

## User Manual

### General
- `?` or `help`: Show User Manual
- `exit`: Exit Tool
- `back`: Navigate back to the previous menu
- `clear`: Clear the screen
- `end`: Exit current Menu State to Start Menu
- `show`: Display global variables
- `template`: Create a Template with all Tool Attack Commands previous entered
- `campaign <ACTION>`: 
  - `info`: Display information about the campaign
  - `start`: Start the campaign
  - `end`: End the campaign
- `setg <VAR-NAME> <VALUE>`: Set a global variable with the specified name and value

### Tool Specific
- `set <VAR-NAME> <VALUE>`: Set tool-specific values with the specified name and value
- `options`: Display tool-specific variables
- `menu`: Show predefined methods specific for the tool.

---

**Note**: Replace `<VAR-NAME>` and `<VALUE>` with the actual variable name and value you want to set.

---

## Example Usage 

### Setting  Variables
To set a global variable, use the following command:
```plaintext
# Set Tool Variable 'Port' to 80
set port 80
# Set Globale Variable 'IP' to 10.0.0.1
setg ip 10.0.0.1
```

### Campaign
Start, end or get info about campaign:
```plaintext
# Start Campaign
campaign start
# End Campaign
campaign end
# Info Campaign
campaign info
```

### Execute Attack
```plaintext
# Display predefined Methods
(Start/Tools/Nmap)>> menu
Method         | Description                                                       
---------------+-------------------------------------------------------------------
--help or help | View the help menu                                                
agg            | Scan using the flags -sS (SYN) -sV (Version) -sC (Scripts) -O (OS)
syn            | SYN scan (SYN flag)                            
con            | TCP connect scan (SYN/SYN-ACK/ACK)                                
udp            | UDP scan                                                          
null           | Null scan (no flags set)                                          
fin            | FIN scan (FIN flag)                                               
version        | TCP Version detection

# Execute the predefined 'syn' Method
(Start/Tools/Nmap)>> syn
Starting Nmap 7.80 ( https://nmap.org ) at 2023-10-25 11:46 UTC
...
```


# Clusterforce CLI

## Before CLI Usage

The attack tools have to be installed via the GUI first. 

1. Enter the GUI and navigate to the menu entry **'Tools'**.
2. Choose the tool you want to install.
3. After installation, you can leave the GUI and execute the tool via **CLI**.

## User Manual
```plaintext
usage: attack [--tool TOOL-NAME] [--attack ATTACK] [--param [PARAM]]

Clusterforce:

optional arguments:
  -h, --help         show this help message and exit
  -t , --tool        specify Tool Name.
  -a , --attack      specify the Attack from the Tool.
  -p , --param       specify Parameter, which should be set for the Attack.
  -v , --value       specify the Value for the Parameter.
  -pb , --playbook   specify the Name of the Playbook to execute.
  -n , --number      specify the Number of the Playbook to execute.

display available Tools:
  attack --tool help

display Tool Attacks:
  attack --tool [TOOL-NAME] --attack help --pod_deployment [TRUE/FALSE] --pod_specs [pod_priviliged=TRUE/FALSE] --pod_specs [service_account=evil-admin/default]

display available Playbooks:
  attack --playbook help                 

run Playbook:
  attack --playbook [PLAYBOOK-NAME]
  attack --playbook [generated/default] --number [NUMBER]

```

## Example Usage
### Attack Tool 

To execute the attack tool, which are shown in the Table **Attack Tools** below of this File, use the following command:
```bash
attack --tool kdigger 
       --attack dig 
       -p buckets=apiresources 
       --pod_deployment True 
       --pod_specs pod_priviliged=True 
       --pod_specs service_account=evil-admin 
```      

- Use `--param` or `-p` to specify tool-specific parameters, like the example `[buckets=apiresources]`.
- If the `--pod_deployment` parameter is not specified, the attack tool will be executed at the **cluster level**.
- To run the attack tool from inside a pod, set `--pod_deployment True`.
- When `--pod_deployment True` is set:
  - The pod is created with the default setting of `pod_priviliged=False`.
  - The default service account used will be `default`.
- To run the deployed pod with priviledge rights set --pod_specs  `[pod_priviliged=True ]`
- To run the deployed pod with a priviledge service account set --pod_specs  `[service_account=evil-admin]`

- The attack tools which can be run from inside a pod are listed below:
  - Kdigger
  - Kuberhunter
  - Nmap
  - Flightsim                                      
```

### Testcases
To execute the testcases, which are shown in the Table **Testcases** below of this File, use the following command:
```bash
attack --testcase kubernetes 
       --tactic privilege_escalation 
       --technique privileged_container
```    
- `--testcase`: Specifies the testcase to execute. The only testcases implemented are for, **kubernetes**.
- `--tactic`: Defines the tactic used, such as **privilege_escalation**.
- `--technique`: Specifies the technique, for example, **privileged_container**.


# Implemented Attack Tools and Testcases

## Attack Tools
| Attack Tool          | Attack Type                           | Description                                                                                                                                                                                                 | Component / Service | Context          |
|----------------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|------------------|
| Nmap                 | Aggresive Scan                        | TCP Syn Scan with Version Detection, Nmap Default Scripts and OS fingerprinting                                                                                                                             | Pod, Cluster        | Port to execute from within Pod |
| Nmap                 | Port Scan - TCP SYN                   | Run TCP SYN Scan                                                                                                                                                                                            | Pod, Cluster        | Port to execute from within Pod |
| Nmap                 | Port Scan - TCP Connect               | Run TCP connect scan (SYN/SYN-ACK/ACK)                                                                                                                                                                      | Pod, Cluster        | Port to execute from within Pod |
| Nmap                 | Port Scan - UDP                       | Run UDP scan                                                                                                                                                                                                | Pod, Cluster        | Port to execute from within Pod |
| Nmap                 | Port Scan - Null Scan                 | Run Null scan (no flags set)                                                                                                                                                                                | Pod, Cluster        | Port to execute from within Pod |
| Nmap                 | Port Scan - Fin Scan                  | Run FIN scan                                                                                                                                                                                                | Pod, Cluster        | Port to execute from within Pod |
| Nmap                 | Service Enumeration and Version Detection (TCP) | Detect running services and their according versions                                                                                                                                                        | Pod, Cluster        | Port to execute from within Pod |
| Kubehunter           | Remote Scan                           | Scans vulnerabilities (Passive and Active)                                                                                                                                                                  | Cluster / Outside (Remote) | - |
| Kubehunter           | Interface Scan / Pod Scan / CIDR Scan | Scans vulnerabilities on all network interfaces / Scans vulnerabilities from inside a pod / Scans vulnerabilities a specified range (/24)                                                                    | Cluster / Pod / Cluster | - |
| Redkube              | Privileged containers                 | Get pods with privileged containers                                                                                                                                                                         | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Root Containers                       | Get pods with containers running as root                                                                                                                                                                    | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Sys Admin Container                   | Get pods with containers including system admin capability                                                                                                                                                  | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Sensitive keys from configmaps        | Get all configmaps with sensitive details in keys                                                                                                                                                           | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Sensitive configmaps values           | Get all configmaps with sensitive details in values                                                                                                                                                         | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Sensitive containers environment variables | Get containers with sensitive details in env                                                                                                                                                                | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Steal container mounted Token         | Get the kubernetes token mounted by default                                                                                                                                                                 | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Kubernetes API Communication          | Test communication to the kubernetes API server                                                                                                                                                             | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Scan Cluster Secrets                  | List all kubernetes cluster secrets                                                                                                                                                                         | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Scan Load Balancer                    | Get load balancers                                                                                                                                                                                          | Pod, Cluster        | Port to execute from within Pod |
| Redkube              | Scan External IP                      | Get external IP's of all nodes                                                                                                                                                                              | Cluster             | - |
| Redkube              | Scan Network Policies                 | Get all network policies                                                                                                                                                                                    | Cluster             | - |
| Redkube              | Scan Cluster Admins                   | Get cluster admin role binding                                                                                                                                                                              | Cluster             | - |
| Redkube              | Scan Roles                            | Get roles with secrets access, Get roles with configmaps access                                                                                                                                             | Cluster             | - |
| Redkube              | No Limit Container                    | Get pods with containers without resources limits                                                                                                                                                           | Cluster             | - |
| Redkube              | Container Images                      | Get all containers images                                                                                                                                                                                   | Cluster             | - |
| Redkube              | Wildcard Resources                    | Get cluster roles with wildcard resources, Get roles with wildcard resources                                                                                                                                | Cluster             | - |
| Redkube              | Persistent volume                     | Get persistent volume claims                                                                                                                                                                                | Cluster             | - |
| Redkube              | Persistent stealth Pod                | Creates a stealth pod in the kube-system namespace                                                                                                                                                          | Cluster             | - |
| KDigger              | Scan Admission Controller             | Scans the admission controller chain by creating default with dry run specific pods to find what is prevented or not                                                                                         | Pod                 | Port to execute from within Pod |
| KDigger              | Scan API Resources                    | Discovers the available APIs of the cluster                                                                                                                                                                 | Pod                 | Port to execute from within Pod |
| KDigger              | Scan Authorization of APIs            | Checks your API permissions with the current context or the available token                                                                                                                                  | Pod                 | Port to execute from within Pod |
| KDigger              | Read cgroups                          | Reads the /proc/self/cgroup files that can leak information under cgroups v1                                                                                                                                | Pod                 | Port to execute from within Pod |
| KDigger              | Scan Devices                          | Shows the list of devices available in the container                                                                                                                                                        | Pod                 | Port to execute from within Pod |
| KDigger              | Scan information about container      | Retrieves hints that the process is running inside a typical container                                                                                                                                      | Pod                 | Port to execute from within Pod |
| KDigger              | Scan Environment                      | Checks the presence of Kubernetes related environment variables                                                                                                                                             | Pod                 | Port to execute from within Pod |
| KDigger              | Scan Mount                            | Shows all mounted devices in the container                                                                                                                                                                  | Pod                 | Port to execute from within Pod |
| KDigger              | Scan Node                             | Retrieves various information in /proc about the current host                                                                                                                                               | Pod                 | Port to execute from within Pod |
| KDigger              | PID Namespace                         | Analyses the PID namespace of the container in the context of Kubernetes                                                                                                                                    | Pod                 | Port to execute from within Pod |
| KDigger              | Scan Token                            | Checks for the presence of a service account token in the filesystem                                                                                                                                        | Pod                 | Port to execute from within Pod |
| KDigger              | Scan Version                          | Dumps the API server version information                                                                                                                                                                    | Pod                 | Port to execute from within Pod |
| Stratus Red Team     | Credential Access - Secretes          | Dump All Secrets                                                                                                                                                                                            | Pod, Cluster        | Port to execute from within Pod |
| Stratus Red Team     | Credential Access - Tokens            | Steal Pod Service Account Token                                                                                                                                                                             | Pod, Cluster        | Port to execute from within Pod |
| Stratus Red Team     | Persistence - ClusterRole             | Create Admin ClusterRole                                                                                                                                                                                    | Pod, Cluster        | Port to execute from within Pod |
| Stratus Red Team     | Persistence - Certificate             | Create Client Certificate Credential                                                                                                                                                                        | Pod, Cluster        | Port to execute from within Pod |
| Stratus Red Team     | Persistence - Token                   | Create Long-Lived Token                                                                                                                                                                                     | Pod, Cluster        | Port to execute from within Pod |
| Stratus Red Team     | Privilege Escalation - ClusterRole    | Create Admin ClusterRole                                                                                                                                                                                    | Pod, Cluster        | Port to execute from within Pod |
| Stratus Red Team     | Privilege Escalation - HostPath Mount | Container breakout via hostPath volume mount                                                                                                                                                                | Pod                 | Port to execute from within Pod |
| Stratus Red Team     | Privilege Escalation - Node/proxy     | Privilege escalation through node/proxy permissions                                                                                                                                                         | Pod, Cluster        | Port to execute from within Pod |
| Stratus Red Team     | Privilege Escalation - Pod            | Run a Privileged Pod                                                                                                                                                                                        | Pod, Cluster        | Port to execute from within Pod |
| Badpods              | General                               | Create Kubernetes resource with certain access-scope                                                                                                                                                        | Cluster             | - |
| Badpods              | Resources                             | pod, cronjob, daemonset, deployment, job, replicaset, replicationcontroller, statefulset                                                                                                                    | Cluster             | - |
| Badpods              | Access scopes                         | everything-allowed, priv-and-hostpid, priv, hostpath, hostpid, hostnetwork, hostipc, nothing-allowed                                                                                                        | Cluster             | - |
| Badpods              | Standard creation or reverse-shell    | Standard creation or Reverse-shell                                                                                                                                                                          | Cluster             | - |
| Rakkess              | View cluster                          | View access-matrix on cluster level                                                                                                                                                                         | Cluster             | - |
| Rakkess              | View namespace                        | View access-matrix on namespace level                                                                                                                                                                       | Pod, Cluster        | - |
| Rakkess              | View resource                         | View access-matrix on resource level                                                                                                                                                                        | Pod, Cluster        | - |
| Rakkess              | Impersonate user                      | Impersonate a specific user                                                                                                                                                                                 | Pod, Cluster        | - |
| Rakkess              | Impersonate group                     | Impersonate a specific group                                                                                                                                                                                | Pod, Cluster        | - |
| Rakkess              | Impersonate service-account           | Impersonate a service account in the format \<namespace\>:\<sa-name\>                                                                                                                                      | Pod, Cluster        | - |
| CDK                  | Information Gathering                 | OS Basic Info, Available Capabilities, Available Linux Commands, Mounts, Net Namespace, Sensitive ENV, Sensitive Process, Sensitive Local Files, Kube-proxy Route Localnet(CVE-2020-8558), DNS-Based Service Discovery | Pod | - |
| CDK                  | Discovery                             | K8s Api-server Info, K8s Service-account Info, Cloud Provider Metadata API                                                                                                                                  | Pod                 | - |
| CDK                  | Escaping                              | docker-runc CVE-2019-5736, containerd-shim CVE-2020-15257, docker.sock PoC (DIND attack), docker.sock RCE, Docker API(2375) RCE, Device Mount Escaping, LXCFS Escaping, Cgroups Escaping, Abuse Unprivileged User Namespace Escaping CVE-2022-0492, Procfs Escaping, Ptrace Escaping PoC, Rewrite Cgroup(devices.allow), Read arbitrary file from host system (CAP_DAC_READ_SEARCH) | Pod | - |
| CDK                  | Discovery                             | K8s Component Probe, Dump Istio Sidecar Meta, Dump K8s Pod Security Policies                                                                                                                                | Pod                 | - |
| CDK                  | Remote Control                        | Reverse Shell, Kubelet Exec                                                                                                                                                                                 | Pod                 | - |
| CDK                  | Credential Access                     | Registry BruteForce, Access Key Scanning, Etcd Get K8s Token, Dump K8s Secrets, Dump K8s Config                                                                                                             | Pod                 | - |
| CDK                  | Privilege Escalation                  | K8s RBAC Bypass                                                                                                                                                                                             | Pod                 | - |
| CDK                  | Persistence                           | Deploy WebShell, Deploy Backdoor Pod, Deploy Shadow K8s api-server, K8s MITM Attack (CVE-2020-8554), Deploy K8s CronJob                                                                                     | Pod                 | - |
| Flightsim            | Cleartext                             | Generates random cleartext traffic to an Internet service operated by AlphaSOC                                                                                                                              | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Dga                                   | Simulates DGA traffic using random labels and top-level domains                                                                                                                                             | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Imposter                              | Generates DNS traffic to a list of imposter domains                                                                                                                                                         | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Irc                                   | Connects to a random list of public IRC servers                                                                                                                                                             | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Miner                                 | Generates Stratum mining protocol traffic to known cryptomining pools                                                                                                                                       | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Oast                                  | Simulates out-of-band application security testing (OAST) traffic                                                                                                                                           | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Scan                                  | Performs a port scan of random RFC 5737 addresses using common TCP ports                                                                                                                                    | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Sink                                  | Connects to known sinkholed destinations run by security researchers                                                                                                                                        | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Spambot                               | Resolves and connects to random Internet SMTP servers to simulate a spam bot                                                                                                                                | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | SSH-exfil                             | Simulates an SSH file transfer to a service running on a non-standard SSH port                                                                                                                              | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | SSH-transfer                          | Simulates an SSH file transfer to a service running on an SSH port                                                                                                                                          | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Telegram-bot                          | Generates Telegram Bot API traffic using a random or provided token                                                                                                                                         | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Tunnel-dns                            | Generates DNS tunneling requests to *.sandbox.alphasoc.xyz                                                                                                                                                  | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | Tunnel-icmp                           | ICMP tunneling traffic to an Internet service operated by AlphaSOC                                                                                                                                          | Pod, Cluster        | Port to execute from within Pod |
| Flightsim            | C2 communication                      | Generates both DNS and IP traffic to a random list of known C2 destinations                                                                                                                                 | Pod, Cluster        | Port to execute from within Pod |
| HackerContainer      | Container with hacker tools           | Includes tools like coreutils, iputils, unzip, net-tools, openssl, htop, curl, wget, docker, kubectl, amicontained, python2, python3, helm V2, helm V3, git, nmap, zmap, masscan, audit2rbac, nikto, proxychains-ng, netcat, capsh, kubesec, awscli, whois, tcpdump, cfssl, Amass, wordlists, rockyou.txt, gobuster, kubectl-who-can, etcdctl, redis-cli, psql, mysql-client, testssl.sh, scapy, LinEnum.sh, unix-privesc-check, Linux_Exploit_Suggester, postenum, docker-bench-security, kube-bench, truffleHog, gitleaks, bind-tools, lynis, tldr.sh, pwnchart, kubeaudit, popeye, hadolint, conftest, kube-hunter, kubeletctl, mongo | Pod | Incorporate container into pod |
| MTKPI                | Pod with offensive capabilities       | Includes tools like botb, kubeletctl, kubesploit agent, CDK, peirates, traitor, ctrsploit, kdigger, kubectl, linuxprivchecker, deepce, helm, kube-hunter, kube-bench, DDexec, kubetcd                                                                                     | Pod                 | - |
## Testcases
The Testcases are implement based on the [Kubernetes Thread Matrix](https://kubernetes-threat-matrix.redguard.ch/)
| **Initial Access**       | **Tool Name**                    | **Description**                                                                                                                                                       |
|--------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1                        | Kubeconfig file                 | Get a kubeconfig file from somewhere (in this case the default config (/root). Use the kubeconfig file to show all pods.                                           |

| **Execution**            | **Tool Name**                    | **Description**                                                                                                                                                       |
|--------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2                        | New container                   | Create a pod.                                                                                                                                                        |
| 3                        | Exec into Container             | See (Execution) bash/cmd in container.                                                                                                                               |
| 4                        | bash/cmd in container           | Create a pod that includes the nginx container image. Execute bash in the container.                                                                                |
| 5                        | SSH server running inside container | Create a pod with a running SSH Server. Exec into Container with bash.                                                                                                |

| **Persistence**          | **Tool Name**                    | **Description**                                                                                                                                                       |
|--------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 7                        | Writable hostPath mount         | Create a pod with a container that uses a hostPath volume. Output the host system’s file system.                                                                    |
| 8                        | Kubernetes CronJob              | Create a CronJob which adds an SSH key to the authorized_keys file.                                                                                                  |

| **Privilege Escalation**  | **Tool Name**                    | **Description**                                                                                                                                                       |
|--------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 10                       | Cluster-admin binding           | Create a new ServiceAccount evil-admin. Create a new RoleBinding that binds evil-admin to the cluster-admin role. Check permissions for evil-admin service account. |
| 12                       | Disable Namespacing             | Create Container with specs: hostNetwork: true, hostPID: true, hostIPC: true, privileged: true, hostPath: /. Execute into container and verify access via chroot.    |

| **Defense Evasion**      | **Tool Name**                    | **Description**                                                                                                                                                       |
|--------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 14                       | Delete k8s events               | Delete the Kubernetes events in all namespaces.                                                                                                                      |
| 15                       | Pod / container name similarity | List all Pods in kube-system namespace. Deploy a Pod with a similar name to an existing coredns pod.                                                                |

| **Credential Access**    | **Tool Name**                    | **Description**                                                                                                                                                       |
|--------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 17                       | Access container service account | Create a pod with the ServiceAccount secret-reader. Output the `/var/run/secrets/kubernetes.io/serviceaccount/token`.                                                |
| 18                       | Applications credentials in config files | Create a pod with a sensitive environment variable: `name: POSTGRES_PASSWORD, value: "mysecretpassword"`. List the value of the pod.                               |

| **Discovery**            | **Tool Name**                    | **Description**                                                                                                                                                       |
|--------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 19                       | Network mapping                 | Deploy `naabu` in a container. Scan `10.42.0.0/24` from inside the container. Output the result by accessing the container logs.                                     |

| **Lateral Movement**     | **Tool Name**                    | **Description**                                                                                                                                                       |
|--------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 20                       | Cluster internal networking     | Create `secret` namespace. Deploy the `web` Pod. Deploy the `web-secret-only` Pod. Create a Service for `web-secret-only`. Create `test-namespace`. Deploy `test-pod`. Test communication between `test-pod` and `web`. |

