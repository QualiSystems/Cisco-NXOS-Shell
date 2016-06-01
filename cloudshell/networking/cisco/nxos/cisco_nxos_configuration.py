from cisco_nxos_handler import CiscoNXOSHandler

__author__ = 'shms'

HANDLER_CLASS = CiscoNXOSHandler

DEFAULT_PROMPT = '.*[#>]\s*$'
ENABLE_PROMPT = '.*# *$'
CONFIG_MODE_PROMPT = '\(config.*\)# *$'

def send_default_actions(session):
    """Send default commands to configure/clear session outputs
    :return:
    """

    session.hardware_expect('terminal length 0', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)
    session.hardware_expect(ENTER_CONFIG_MODE_PROMPT_COMMAND, CONFIG_MODE_PROMPT)
    session.hardware_expect('no logging console', CONFIG_MODE_PROMPT)
    session.hardware_expect('exit', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)

ENTER_CONFIG_MODE_PROMPT_COMMAND = 'configure terminal'
EXIT_CONFIG_MODE_PROMPT_COMMAND = 'exit'
DEFAULT_ACTIONS = send_default_actions
