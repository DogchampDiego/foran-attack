import json

class KubehunterParser:
    def __init__(self):
        self.data = None
        self.mapping = {
            "generalsensitiveinformation": {"TA0001": ""},  # Intial Access
            "exposedsensitiveinterfaces": {"TA0001": ["T1133", "MS-TA9005"]},  # Intial Access
            "mountserviceprincipal": {"TA0006": ["T1552.001", "MS-TA9026"]},  # Credential Access
            "listk8ssecrets": {"TA0006": ["T1552.007", "MS-TA9025"]},  # Credential Access
            "accesscontainerserviceaccount": {"TA0006": ["T1528", "MS-TA9016"]},  # Credential Access
            "accessk8sapiserver": {"TA0007": ["T1613", "MS-TA9029"]},  # Discovery
            "accesskubeletapi": {"TA0007": ["T1613", "MS-TA9030"]},  # Discovery
            "accessk8sdashboard": {"TA0007": ""},  # Discovery
            "instancemetadataapi": {"TA0007": ["T1552.005", "MS-TA9033"]},  # Discovery
            "execintocontainer": {"TA0002": ["T1609", "MS-TA9006"]},  # Execution
            "sidecarinjection": {"TA0002": ["T1610", "MS-TA9011"]},  # Execution
            "newcontainer": {"TA0002": ["T1610", "MS-TA9008"]},  # Execution
            "generalpersistence": {"TA0003": ""},  # Persistence
            "hostpathmountprivilegeescalation": {"TA0004": ["T1611", "MS-TA9013"]},  # Privilege Escalation
            "privilegedcontainer": {"TA0004": ["T1610", "MS-TA9018"]},  # Privilege Escalation
            "clusteradminbinding": {"TA0004": ["T1078.003", "MS-TA9019"]},  # Privilege Escalation
            "arppoisoning": {"TA0008": ["T1557", "MS-TA9036"]},  # Lateral Movement
            "corednspoisoning": {"TA0008": ["T1557", "MS-TA9035"]},  # Lateral Movement
            "datadestruction": {"TA0040": ["T1485", "MS-TA9038"]},  # Impact
            "generaldefenseevasion": {"TA0005": ""},  # Defense Evasion
            "connectfromproxyserver": {"TA0005": ["T1090", "MS-TA9024"]},  # Defense Evasion
            "KHV022":{"TA0004":"","CVE":"CVE-2018-1002105"}, # Privelege Escalation // CVEPrivilegeEscalationCategory
            "KHV023":{"TA0040":[["T1498", "T1499"],"MS-TA9040"],"CVE":"CVE-2019-1002100"}, # Impact DoS Attack // CVEDenialOfServiceTechnique
            "KHV024":{"TA0040":[["T1498", "T1499"],"MS-TA9040"],"CVE":"CVE-2019-9512"}, # Impact DoS Attack // CVEDenialOfServiceTechnique
            "KHV025":{"TA0040":[["T1498", "T1499"],"MS-TA9040"],"CVE":"CVE-2019-9514"}, # Impact DoS Attack // CVEDenialOfServiceTechnique
            "KHV026":{"TA0004":"","CVE":"CVE-2019-11247"}, # Privelege Escalation // CVEPrivilegeEscalationCategory
            "KHV027":{"TA0002":"","CVE":"CVE-2019-11246"}, # Execution Remote Code // CVERemoteCodeExecutionCategory
            "KHV028":{"TA0002":"","CVE":"CVE-2019-1002101"}, # Execution Remote Code // CVERemoteCodeExecutionCategory
            "KHV003":{"TA0007":["T1552.005","MS-TA9033"],"CVE":"CVE-2021-27075"},
        }

    def get_info(self, input_key):
        if input_key in self.mapping:
            item = self.mapping[input_key]
            if isinstance(item, dict):
                ta_number = list(item.keys())[0]
                ta_values = item[ta_number]
                if isinstance(ta_values, list):
                    ta_value1, ta_value2 = ta_values[0], ta_values[1]
                else:
                    ta_value1, ta_value2 = None, None
                cve_identifier = item.get("CVE", None)
                return (ta_number,ta_value1, ta_value2, cve_identifier)
            elif isinstance(item, list):
                ta_number = item[0] 
                ta_values = item[1:]
                ta_value1, ta_value2 = ta_values[0], ta_values[1]
                cve_identifier = None
                return (ta_number,ta_value1, ta_value2, cve_identifier)
            else:
                ta_number = input_key
                ta_value1, ta_value2 = None, None
                cve_identifier = None
                return (ta_number,ta_value1, ta_value2, cve_identifier)
        return None
    #({ta_number: [ta_value1, ta_value2]}, cve_identifier)
    def set_data(self, data):
        self.data = json.loads(data)

    def parse_vulnerabilities(self):
        vulnerabilities = self.data.get("vulnerabilities", [])
        val = set()
        for vulnerability in vulnerabilities:
            subcategory = None

            if vulnerability.get("category"):
                if len(self.split_and_clean(vulnerability.get("category")))==2:
                    subcategory = self.split_and_clean(vulnerability.get("category"))[1].replace(" ", "").lower()
            
            val.add(self.get_info(subcategory))

        mitre = []
        cve = []
        for item in val:
            ta_number, ta_value1, ta_value2, cve_identifier = item
            mitre.append({ta_number: [ta_value1, ta_value2]})
            cve.append(cve_identifier)        
        return mitre, cve

    def split_and_clean(self,user_input):       
        return [part.strip() for part in user_input.split("//")]