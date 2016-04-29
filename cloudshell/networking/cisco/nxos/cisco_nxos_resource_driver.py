__author__ = "shms"

from cisco_nxos_bootstrap import CiscoNXOSBootstrap
from cloudshell.shell.core.context.context_utils import context_from_args
import cisco_nxos_configuration as driver_config
import inject


class CiscoNXOSDriver:
    def __init__(self, config=None, bindings=None):
        bootstrap = CiscoNXOSBootstrap()
        bootstrap.add_config(driver_config)
        if config:
            bootstrap.add_config(config)
        if bindings:
            bootstrap.add_bindings(bindings)
        bootstrap.initialize()
        # self.config = inject.instance('config')

    @context_from_args
    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        return 'Finished initializing'

    # Destroy the driver session, this function is called everytime a driver instance is destroyed
    # This is a good place to close any open sessions, finish writing to log files
    def cleanup(self):
        pass

    @context_from_args
    def simple_command(self, command):
        handler = inject.instance("handler")
        logger = inject.instance("logger")
        out = handler.send_command('show ver')
        logger.info('Command completed ' + out)
        return out

    @context_from_args
    def get_inventory(self, context):
        """
        Return device structure with all standard attributes
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        logger = inject.instance("logger")
        logger.info(context.resource.__dict__)
        result = handler.discover_snmp()
        # return handler.normalize_output(result)
        return result

    @context_from_args
    @inject.params(context='context')
    def load_firmware(self, context, remote_host, file_path):
        """
        Upload and updates firmware on the resource
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.update_firmware(remote_host=remote_host, file_path=file_path)
        handler.disconnect()
        return result_str

    @context_from_args
    @inject.params(context='context')
    def save(self, context, folder_path, configuration_type):
        """
        Backup configuration
        :return: success string with saved file name
        :rtype: string
        """
        handler = inject.instance("handler")

        result_str = handler.backup_configuration(custom_destination_host=folder_path,
                                                  source_filename=configuration_type)
        return result_str

    @context_from_args
    @inject.params(context='context')
    def restore(self, context, path, config_type, restore_method='Override'):
        """
        Restore configuration
        :return: success string
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.restore_configuration(source_file=path, config_type=config_type, clear_config=restore_method)
        return result_str

    @context_from_args
    def send_custom_command(self, context, command):
        """
        Send custom command
        :return: result
        :rtype: string
        """
        cli = inject.instance("cli_service")
        result_str = cli.send_command(command)
        return result_str

    @context_from_args
    @inject.params(context='context')
    def add_vlan(self, context, ports, vlan_range, port_mode, additional_info):
        """
        Assign vlan or vlan range to the certain interface
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.add_vlan(port_list=ports,
                                      vlan_range=vlan_range.replace(' ', ''),
                                      port_mode=port_mode,
                                      additional_info=additional_info)
        return result_str

    @context_from_args
    @inject.params(context='context')
    def remove_vlan(self, context, ports, vlan_range, port_mode, additional_info):
        """
        Remove vlan or vlan range from the certain interface
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.remove_vlan(port_list=ports,
                                         vlan_range=vlan_range, port_mode=port_mode,
                                         additional_info=additional_info)
        return result_str

    @context_from_args
    @inject.params( context='context')
    def send_custom_config_command(self, context, command):
        handler = inject.instance("handler")
        result_str = handler.sendConfigCommand(cmd=command)
        return result_str

    def reset_driver(self, context):
        self.initialize(context)

    def shutdown(self, context):
        pass