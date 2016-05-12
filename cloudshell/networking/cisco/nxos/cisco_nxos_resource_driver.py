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
    def ApplyConnectivityChanges(self, context, request):
        handler = inject.instance('handler')
        response = handler.apply_connectivity_changes(request)
        handler.logger.info('finished applying connectivity changes response is:\n{0}'.format(str(response)))
        return response

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