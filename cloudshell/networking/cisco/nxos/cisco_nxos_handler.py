__author__ = 'CoYe'

import re

from cloudshell.networking.cisco.cisco_handler_base import CiscoHandlerBase

class CiscoNXOSHandler(CiscoHandlerBase):
    def __init__(self):
        CiscoHandlerBase.__init__(self)
        self.supported_os = ['NXOS', 'NX-OS']