import help.helper as helper

from state.menu_state import MenuState
from menu.menu_base import Menu

import tools.kubehunter.kubehunter as kubehunter
import tools.kubescape.Kubescape as kubescape
import tools.rakkess.Rakkess as rakkess
import tools.trivy.Trivy as trivy
import tools.nmap.Nmap as nmap
import tools.redkube.redkube as redkube
import tools.stratusred.Stratusred as stratusred
import tools.kdigger.kdigger as kdigger
import tools.cdk.Cdk as cdk
import tools.flightsim.Flightsim as flightsim
import tools.hackercontainer.HackerContainer as hackercontainer
import tools.badpods.Badpods as badpods
import tools.mtkpi.mtkpi as mtkpi

class Tools(Menu):
    def __init__(self):
        super().__init__()
        helper.handle_globals(MenuState.TOOLS,MenuState.TOOLS)
        self.command_mapping= {
            "1": self.kubehunter,
            "2": self.nmap,
            "3": self.kubescape,
            "4": self.trivy,
            "5": self.red_kube,
            "6": self.stratusred,
            "7": self.kdigger,
            "8": self.rakkess,
            "9": self.cdk,
            "10": self.flightsim,
            "11": self.hackercontainer,
            "12": self.badpods,
            "13": self.mtkpi
        }

    def back(self):
        self.global_var.pop_menu_tree()
        from menu.startmenu.start import Start
        return Start()

    # InputHandle Methods
    def kubehunter(self):
        return kubehunter.Kubehunter()
    def red_kube(self):
        return redkube.RedKube()
    def nmap(self):
        return nmap.Nmap()
    def kubescape(self):
        return kubescape.Kubescape()
    def trivy(self):
        return trivy.Trivy()
    def stratusred(self):
        return stratusred.Stratusred()
    def kdigger(self):
        return kdigger.KDigger()
    def rakkess(self):
        return rakkess.Rakkess()
    def cdk(self):
        return cdk.Cdk()
    def flightsim(self):
        return flightsim.Flightsim()
    def hackercontainer(self):  
        hackercontainer.HackerContainer()
        return Tools()
    def badpods(self):
        return badpods.Badpods()
    def mtkpi(self):
        return mtkpi.MTKPI()