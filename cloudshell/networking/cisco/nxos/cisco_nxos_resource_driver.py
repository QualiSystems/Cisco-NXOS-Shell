# __author__ = 'CoYe'

# from cloudshell.shell.core.driver_builder_wrapper import DriverFunction
# from cloudshell.networking.resource_driver.networking_generic_resource_driver import networking_generic_resource_driver
#
# class cisco_generic_nxos_resource_driver(networking_generic_resource_driver):
#     @DriverFunction(extraMatrixRows={"resource": ["User", "Password", "Enable Password", "Console Server IP Address",
#                                                   "Console User", "Console Password", "Console Port", "Connection Type",
#                                                   "SNMP Version", "SNMP Read Community", "SNMP V3 User", "SNMP V3 Password",
#                                                   "SNMP V3 Private Key"]})
#     def Init(self, matrixJSON):
#         self.handler_name = 'nxos'
#         networking_generic_resource_driver.Init(self, matrixJSON)
#         print self.handler_name
#
# if __name__ == '__main__':
#
#     data_json = str("""{
#             "resource" : {
#                     "ResourceAddress": "192.168.42.235",
#                     "User": "root",
#                     "Password": "Password1",
#                     "Console User": "",
#                     "Console Password": "",
#                     "Console Server IP Address": "",
#                     "CLI Connection Type": "",
#                     "Enable Password": "cisco",
#                     "Console Port": "",
#                     "Connection Type": "auto",
#                     "SNMP Community": "stargate",
#                     "SNMP Version": "2",
#                     "SNMP Password": "Password1",
#                     "SNMP User": "QUALI",
#                     "SNMP Private Key": "Live4lol",
#                     "SNMP V3 User": "",
#                     "SNMP V3 Password": "",
#                     "SNMP V3 Private Key": "",
#                     "SNMP Read Community": "stargate"
#                 }
#             }""")
#     resource_driver = cisco_generic_nxos_resource_driver('77', data_json)
#     # resource_driver.Add_VLAN(data_json, '192.168.42.235/0/24', '34', 'trunk', '')
#     resource_driver.GetInventory(data_json)

__author__ = "shms"

from cloudshell.shell.core.driver_bootstrap import DriverBootstrap
from cloudshell.shell.core.context.context_utils import context_from_args
import cisco_nxos_configuration as config
import inject


class CiscoNXOSDriver:
    def __init__(self):
        bootstrap = DriverBootstrap()
        bootstrap.add_config(config)
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
    @inject.params(context='context')
    def simple_command(self, context, command):
        # ss = 'dsd'
        # for i in range(0, int(command)):
        #     logger.info('Resource: ' + context.resource.name)
        #     time.sleep(1)
        # return logger.log_path
        # cli = CliService()
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
        result = handler.discover_snmp()
        # return handler.normalize_output(result)
        return result

    @context_from_args
    @inject.params(logger='logger', context='context')
    def load_firmware(self, context, remote_host, file_path):
        """
        Upload and updates firmware on the resource
        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.update_firmware(remote_host=remote_host, file_path=file_path)
        handler.disconnect()
        handler._logger.info(result_str)

    @context_from_args
    @inject.params(logger='logger', context='context')
    def save(self, context, folder_path, configuration_type):
        """
        Backup configuration
        :return: success string with saved file name
        :rtype: string
        """
        handler = inject.instance("handler")

        result_str = handler.backup_configuration(destination_host=folder_path,
                                                  source_filename=configuration_type)
        return handler.normalize_output(result_str)

    @context_from_args
    @inject.params(logger='logger', context='context')
    def restore(self, context, path, config_type, restore_method='Override'):
        """
        Restore configuration
        :return: success string
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.restore_configuration(source_file=path, config_type=config_type, clear_config=restore_method)
        handler._logger.info(result_str)

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
    @inject.params(logger='logger', context='context')
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
        handler._logger.info(result_str)

    @context_from_args
    @inject.params(logger='logger', context='context')
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
        handler._logger.info(result_str)

    @context_from_args
    @inject.params(logger='logger', context='context')
    def send_custom_config_command(self, context, command):
        handler = inject.instance("handler")
        result_str = handler.sendConfigCommand(cmd=command)
        return handler.normalize_output(result_str)

    def reset_driver(self, context):
        self.initialize(context)

    def shutdown(self, context):
        pass