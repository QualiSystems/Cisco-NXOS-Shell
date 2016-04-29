__author__ = 'shms'

from cloudshell.shell.core.driver_bootstrap import DriverBootstrap

class CiscoNXOSBootstrap(DriverBootstrap):

    def configuration(self, binder):
        """Binding for handler"""
        binder.bind_to_provider('handler', self._config.HANDLER_CLASS)
