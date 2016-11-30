#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from cloudshell.networking.cisco.cisco_command_actions import delete_file, copy, override_running, reload_device
from cloudshell.networking.cisco.flow.cisco_restore_flow import CiscoRestoreFlow


class CiscoNXOSRestoreFlow(CiscoRestoreFlow):
    STARTUP_LOCATION = "nvram:startup_config"
    BACKUP_STARTUP_LOCATION = "bootflash:backup-sc"

    def __init__(self, cli_handler, logger):
        super(CiscoNXOSRestoreFlow, self).__init__(cli_handler, logger)

    def execute_flow(self, path, configuration_type, restore_method, vrf_management_name):
        """ Execute flow which save selected file to the provided destination

        :param path: the path to the configuration file, including the configuration file name
        :param restore_method: the restore method to use when restoring the configuration file.
                               Possible Values are append and override
        :param configuration_type: the configuration type to restore. Possible values are startup and running
        :param vrf_management_name: Virtual Routing and Forwarding Name
        """

        if "-config" not in configuration_type:
            configuration_type += "-config"

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
            copy_action_map = self._prepare_action_map(path, configuration_type)
            if "startup" in configuration_type:
                if restore_method == "override":
                    del_action_map = OrderedDict({
                        "[Dd]elete [Ff]ilename ": lambda session, logger: session.send_line(configuration_type,
                                                                                            logger)})
                    delete_file(session=enable_session, logger=self._logger,
                                path=self.STARTUP_LOCATION, action_map=del_action_map)
                    copy(session=enable_session, logger=self._logger, source=path,
                         destination=configuration_type, vrf=vrf_management_name,
                         action_map=copy_action_map)
                else:
                    copy(session=enable_session, logger=self._logger, source=path,
                         destination=configuration_type, vrf=vrf_management_name,
                         action_map=copy_action_map)

            elif "running" in configuration_type:
                if restore_method == "override":
                    copy(session=enable_session,
                         logger=self._logger,
                         source=self.STARTUP_LOCATION,
                         destination=self.BACKUP_STARTUP_LOCATION,
                         vrf=vrf_management_name,
                         action_map=copy_action_map)
                    copy(session=enable_session, logger=self._logger, source=path,
                         destination=self.STARTUP_LOCATION, vrf=vrf_management_name,
                         action_map=copy_action_map)
                    reload_device(session=enable_session, logger=self._logger, timeout=500)
                    copy(session=enable_session,
                         logger=self._logger,
                         source=self.BACKUP_STARTUP_LOCATION,
                         destination=self.STARTUP_LOCATION,
                         vrf=vrf_management_name,
                         action_map=copy_action_map)
                else:
                    copy(session=enable_session, logger=self._logger, source=path,
                         destination=configuration_type, vrf=vrf_management_name,
                         action_map=copy_action_map)
