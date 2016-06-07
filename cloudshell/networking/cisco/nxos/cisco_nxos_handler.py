__author__ = 'CoYe'

import re

from cloudshell.networking.cisco.cisco_handler_base import CiscoHandlerBase

class CiscoNXOSHandler(CiscoHandlerBase):
    def __init__(self):
        CiscoHandlerBase.__init__(self)
        self.supported_os = ['NXOS', 'NX-OS']

    def _check_replace_command(self):
        return True

    def configure_replace(self, source_filename, timeout=600, vrf=None):
        if not source_filename:
            raise Exception('Cisco NXOS', 'Must pass source file name to replace configuration')
        back_up = 'bootflash:backup-sc'
        startup = 'startup-config'

        self._backup_startup_config(back_up, startup, vrf)
        self._replace_startup_config_with(source_filename, vrf)
        self.reload(retries=19, sleep_timeout=30)
        self._replace_startup_config_with(back_up, vrf)

    def _backup_startup_config(self, back_up, startup, vrf):
        if not self.copy(source_file=startup, destination_file=back_up, vrf=vrf):
            raise Exception('Cisco NXOS', 'Could not backup startup-config, check if bootflash has enough free space')

    def _replace_startup_config_with(self, source_filename, vrf):
        sc = 'startup-config'

        if not self.copy(source_file=source_filename, destination_file=sc, vrf=vrf):
            raise Exception('Cisco NXOS', 'Failed to replace startup config, detailed information in logs')

