
from typing import NamedTuple
from cmd_line_interface.base_defines import AutoCloseFileType, DYNAMIC_HELP_PLURAL, KWARGS_ACTION, KWARGS_CHOICES, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_NARGS, KWARGS_READ_BINARY, KWARGS_STORE_TRUE, KWARGS_TYPE
from cmd_line_interface.basecmdline import CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.defines import QTI
from cmd_line_interface.sectools.metadata import CONSUMES, INCOMPATIBLE_WITH
from common.parser.tme.tme_parser.defines import DEBUG_OPTIONS_PATH, DEBUG_POLICY_DATA_PATH, OEM_CRASH_DUMP_PUBLIC_KEY_PATH
from common.parser.tme.tme_parser.tme import get_selections_for_tag
from common.utils import is_multi_bit
DEBUG_OPTIONS_GROUP = 'Debug Options'
DEBUG_OPTIONS_GROUP_HELP = f'''Additional debug and subsystem-specific debug {DYNAMIC_HELP_PLURAL}'''
IP_SCAN_DUMP_POLICY_GROUP = 'IP Scan Dump Policy'
QAD_DUMP_POLICY_GROUP = 'QAD Dump Policy'
OEM_CRASH_DUMP_PUBLIC_KEY = '--oem-crash-dump-public-key'
PERMANENT_UNLOCK = '--permanent-unlock'
PERSIST_ON_RESET = '--persist-on-reset'
DISABLE_SYSTEM_WATCHDOG = '--disable-system-watchdog'
ALLOW_SYSTEM_WATCHDOG_ACCESS = '--allow-system-watchdog-access'
CRASH_DUMP = '--crash-dump'
OEM_CRASH_DUMP_PUBLIC_KEY_HELP = 'File path of public key used to encrypt crash dumps.'
PERSIST_ON_RESET_HELP = 'Allows debug policy updates to the debug vector to persist on soft reset. This option helps JTAG enablement in APPS or TME subsystem as early as the first line of Boot ROM code.'
DISABLE_SYSTEM_WATCHDOG_HELP = 'Disables the system watchdog for global STOP_ON_FAIL support.'
ALLOW_SYSTEM_WATCHDOG_ACCESS_HELP = 'Allows the APPS Secure and AOP subsystems to access system watchdog registers for selective STOP_ON_FAIL support.'
CRASH_DUMP_VECTOR_HELP = 'Used in conjunction with Debug Options to enable crash dump for a specific subsystem.'
TME_DEBUG_OPTIONS_GROUP: CMDLineGroup = [
    ([
        OEM_CRASH_DUMP_PUBLIC_KEY], {
        KWARGS_HELP: OEM_CRASH_DUMP_PUBLIC_KEY_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }, {
        INCOMPATIBLE_WITH: [
            QTI],
        CONSUMES: [
            OEM_CRASH_DUMP_PUBLIC_KEY_PATH] }),
    ([
        PERSIST_ON_RESET], {
        KWARGS_HELP: PERSIST_ON_RESET_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        CONSUMES: [
            DEBUG_OPTIONS_PATH] }),
    ([
        DISABLE_SYSTEM_WATCHDOG], {
        KWARGS_HELP: DISABLE_SYSTEM_WATCHDOG_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        CONSUMES: [
            DEBUG_OPTIONS_PATH] }),
    ([
        ALLOW_SYSTEM_WATCHDOG_ACCESS], {
        KWARGS_HELP: ALLOW_SYSTEM_WATCHDOG_ACCESS_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        CONSUMES: [
            DEBUG_OPTIONS_PATH] }),
    ([
        CRASH_DUMP], {
        KWARGS_NARGS: '+',
        KWARGS_HELP: CRASH_DUMP_VECTOR_HELP,
        KWARGS_CHOICES: sorted(get_selections_for_tag('CrashDumpVector')) }, {
        CONSUMES: [
            f'''{DEBUG_POLICY_DATA_PATH}/CrashDumpVector'''] })]

class TMEVectorOption(NamedTuple):
    description: str = '\n    Represents options for TME vector objects, including DebugVector, IPScanDumpPolicyVector, and QADDumpPolicyVector.\n    '
    enabled_if_crash_dump_vector: object = None


def debug_vector_id_to_argument(option_id = None):
    '''Defines the naming conversion from the debug vector option id to the CMD argument.'''
    return f'''--debug-{option_id}'''.replace('_', '-').lower()


def ip_scan_dump_id_to_argument(option_id = None):
    '''Defines the naming conversion from the IP scan dump option id to the CMD argument.'''
    return f'''--ip-scan-dump-{option_id}'''.replace('_', '-').lower()


def qad_dump_id_to_argument(option_id = None):
    '''Defines the naming conversion from the QAD dump option id to the CMD argument.'''
    return f'''--qad-dump-{option_id}'''.replace('_', '-').lower()


def get_bit_shifted_value(bits = None, cmdline_value = None):
    start_idx = min(map(int, bits.split(':'))) if is_multi_bit(bits) else int(bits)
    return int(cmdline_value) << start_idx

