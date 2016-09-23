from unittest import TestCase
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails
from cloudshell.networking.cisco.nxos import cisco_nxos_configuration
from cloudshell.shell.core import context_utils
import inject
from mock import Mock
import types
import mock
from cloudshell.networking.cisco.nxos.cisco_nxos_resource_driver import CiscoNXOSDriver


class CiscoNXOSDriverUnitTest(TestCase):
    CONTEXT = ResourceCommandContext()
    CONTEXT.resource = ResourceContextDetails()
    CONTEXT.resource.name = 'Nexus_driver'
    CONTEXT.reservation = ReservationContextDetails()
    CONTEXT.reservation.reservation_id = 'id'

    def setUp(self):
        config = cisco_nxos_configuration

        handler_mock = Mock()
        cisco_nxos_configuration.HANDLER_CLASS = lambda: handler_mock
        logger_mock = Mock()
        config.GET_LOGGER_FUNCTION = lambda: logger_mock

        def test_bindings(binder):
            binder.bind('cli_service', Mock())

        self.driver = CiscoNXOSDriver()

    def test_initialize(self):
        #Arrange
        self.driver.initialize = Mock()
        #Act
        result = self.driver.initialize()
        #Assert
        self.assertTrue(result, 'Finished initializing')

    def test_simple_command(self):
        #Arrange
        command = 'test command'
        context_utils.get_resource_name = lambda: 'true'

        #Act
        with mock.patch('cloudshell.networking.cisco.cisco_run_command_operations.CiscoRunCommandOperations') as mocked_class:
            mocked_class.run_custom_command = mock.MagicMock(return_value="show ver output")

        result = self.driver.run_custom_command(self.CONTEXT, command)
        #Assert
        self.assertTrue(mocked_class.run_custom_command.called)

    def test_get_inventory(self):
        #Arrange
        # print(type(self.driver))
        # handler = Mock()
        handler = inject.instance('handler')
        handler.discover_snmp = Mock()
        logger = inject.instance('logger')
        logger.info = Mock()
        context = Mock(spec=AutoLoadCommandContext)
        context.resource = Mock()
        context.resource.name = Mock(return_value="resource name")
        #Act
        self.driver.get_inventory(context)
        #Assert
        self.assertTrue(handler.discover_snmp.called)
        pass

    def test_load_firmware(self):
        #Arrange
        handler = inject.instance('handler')
        handler.update_firmware = Mock()
        context = Mock(spec=AutoLoadCommandContext)
        context.resource = Mock()
        context.resource.name = Mock(return_value="resource name")
        remote_host = Mock(return_value="127.0.0.1")
        file_path = Mock(return_value="/tmp/file")
        #Act
        self.driver.load_firmware(context, remote_host, file_path)
        #Assert
        self.assertTrue(handler.update_firmware.called)

    def test_save(self):
        #Arrange
        handler = inject.instance('handler')
        handler.save_configuration = Mock()
        context = Mock(spec=AutoLoadCommandContext)
        context.resource = Mock()
        context.resource.name = Mock(return_value="resource name")
        folder_path = Mock(return_value="test_folder")
        configuration_type = Mock(return_value="running")
        #Act
        self.driver.save(context, folder_path, configuration_type)
        #Assert
        self.assertTrue(handler.save_configuration.called)
        pass

    def test_restore(self):
        #Arrange
        handler = inject.instance('handler')
        handler.restore_configuration = Mock()
        context = Mock(spec=AutoLoadCommandContext)
        context.resource = Mock()
        context.resource.name = Mock(return_value="resource name")
        path = Mock(return_value="test_folder")
        configuration_type = Mock(return_value="running")
        restore_method = Mock(return_value="append")
        #Act
        self.driver.restore(context, path, configuration_type, restore_method)
        #Assert
        self.assertTrue(handler.restore_configuration.called)

    def test_send_custom_command(self):
        #Arrange
        cli = inject.instance("cli_service")
        cli.send_command = Mock()
        context = Mock(spec=AutoLoadCommandContext)
        context.resource = Mock()
        context.resource.name = Mock(return_value="resource name")
        command = Mock(return_value="sample command")
        #Act
        self.driver.send_custom_command(context, command)
        #Assert
        self.assertTrue(cli.send_command.called)
        pass

    def test_add_vlan(self):
        #Arrange
        handler = inject.instance('handler')
        handler.add_vlan = Mock()
        context = Mock(spec=AutoLoadCommandContext)
        context.resource = Mock()
        context.resource.name = Mock(return_value="resource name")
        ports = 0
        vlan_range = "500-1000"
        port_mode = 'trunk'
        additional_info = "info"
        #Act
        self.driver.add_vlan(context, ports, vlan_range, port_mode, additional_info)
        #Assert
        self.assertTrue(handler.add_vlan.called)

    def test_remove_vlan(self):
        #Arrange
        handler = inject.instance('handler')
        handler.remove_vlan = Mock()
        context = Mock(spec=AutoLoadCommandContext)
        context.resource = Mock()
        context.resource.name = Mock(return_value="resource name")
        ports = 0
        vlan_range = "500-1000"
        port_mode = 'trunk'
        additional_info = "info"
        #Act
        self.driver.remove_vlan(context, ports, vlan_range, port_mode, additional_info)
        #Assert
        self.assertTrue(handler.remove_vlan.called)

    def test_send_custom_config_command(self):
        #Arrange
        handler = inject.instance('handler')
        handler.sendConfigCommand = Mock()
        context = Mock(spec=AutoLoadCommandContext)
        context.resource = Mock()
        context.resource.name = Mock(return_value="resource name")
        command = Mock(return_value="test command")
        #Act
        self.driver.send_custom_config_command(context, command)
        #Assert
        self.assertTrue(handler.sendConfigCommand.called)