from cisco_nxos_handler import CiscoNXOSHandler

__author__ = 'shms'

HANDLER_CLASS = CiscoNXOSHandler

DEFAULT_PROMPT = '.*[#>]\s*$'
ENABLE_PROMPT = '.*# *$'
CONFIG_MODE_PROMPT = '\(config.*\)# *$'