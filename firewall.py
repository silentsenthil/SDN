'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
import csv


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''
entry = []

with open(policyFile) as f:
    next(f)
    csv_entry =  csv.reader(f, delimiter=',')
    for row in csv_entry:
        entry.append(row[1:])


class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        for pair in entry:
            m = of.ofp_match()
            m.dl_src = EthAddr(pair[0])
            m.dl_dst = EthAddr(pair[1])
            msg = of.ofp_flow_mod()
            msg.match = m
            event.connection.send(msg)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))
    
def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
