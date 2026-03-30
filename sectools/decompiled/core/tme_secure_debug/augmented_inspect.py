
from contextlib import suppress
from textwrap import indent
from cmd_line_interface.sectools.cmd_line_common.defines import INSPECT, SECURITY_PROFILE
from cmd_line_interface.sectools.tme_secure_debug.defines import TME_SECURE_DEBUG_NAME, defines
from cmd_line_interface.sectools.tme_secure_debug.defines.debug_options import TMEVectorOption
from cmd_line_interface.sectools.tme_secure_debug.defines.defines import ASSERT_QTI_OWNERSHIP
from cmd_line_interface.sectools.tme_secure_debug.defines.subsystem_debug_options import DebugOption
from common.data.data import get_enabled_bit_indices_from_byte, properties_repr, unhexlify2
from common.logging.logger import log_warning
from common.parser.tme.tme_parser.defines import DEBUG_OPTIONS_PATH
from common.parser.tme.tme_parser.tme import TME, get_selections_for_tag_extended
from common.utils import get_start_and_end_indices, is_multi_bit
TME_DEBUG_POLICY_IMAGE = 'TME Debug Policy ELF Image'
DESCRIBE_OEM_DP = 'OEM DP'
DESCRIBE_QTI_DP = 'QTI DP'
DESCRIBE_DP = 'DP'
DESCRIBE_QTI_DEC = 'QTI DEC'
DESCRIBE_OEM_DEC = 'OEM DEC'
DESCRIBE_DEC = 'DEC'
DESCRIBE_OEM_DPR = 'OEM DPR'
DESCRIBE_QTI_DPR = 'QTI DPR'
DESCRIBE_DPR = 'DPR'
DESCRIBE_IAR = 'IAR'
DESCRIBE_SLC = 'SLC'
DESCRIBE_UNKNOWN_TME = 'unknown TME structure'
DESCRIBE_EMPTY = 'empty structure'
DESCRIBE_NOT_A_TME = 'unknown format'

def describe(tme_or_data = None):
    '''Returns a string describing the TME object.'''
    if not isinstance(tme_or_data, TME):
        if not TME.is_type(tme_or_data):
            return DESCRIBE_NOT_A_TME
        tme = None(tme_or_data)
    else:
        tme = tme_or_data
    tme_type = DESCRIBE_UNKNOWN_TME
    if not tme.structure:
        tme_type = DESCRIBE_EMPTY
    if tme.structure.keys() and next(iter(tme.structure.keys())).startswith('Svc'):
        tme_type = DESCRIBE_SLC
# WARNING: Decompyle incomplete


def augmented_inspect(tme = None):
    '''Adds additional human-readable information for particular TME tags using the data from the Security Profile.'''
    lines = []
    security_profile_data = defines.security_profile_data
# WARNING: Decompyle incomplete


def inspect_debug_vector_bits(debug_vector = None, options_from_profile = None, bit_field_name = None):
    '''Accepts little endian hex string.'''
    debug_vector_val = int.from_bytes(unhexlify2(debug_vector), 'little', False, **('byteorder', 'signed'))
    options = { }
    for option in options_from_profile:
        bit_or_bit_range = getattr(option, bit_field_name)
        if isinstance(bit_or_bit_range, str) and is_multi_bit(bit_or_bit_range):
            (start, end) = get_start_and_end_indices(bit_or_bit_range)
            for bit in range(start, end + 1):
                options[bit] = option
        options[int(bit_or_bit_range)] = option
    table = [
        ('Bit', 'ID', 'Description')]
    unknown = TMEVectorOption(255, 'UNKNOWN', 'Not specified in the provided Security Profile.')
    for bit in range(debug_vector_val.bit_length()):
        if debug_vector_val & 1 << bit:
            option = options.get(bit, unknown)
            table.append((bit, option.id, option.description))
    if len(table) > 1:
        return properties_repr(table, [
            0], **('sep_rows',))


def inspect_test_signed_image_vector_bits(image_vector = None):
    '''Accepts little endian hex string.'''
    image_vector_val = int.from_bytes(unhexlify2(image_vector), 'little', False, **('byteorder', 'signed'))
    supported_software_ids = dict(get_selections_for_tag_extended('BootSubsystemSoftwareComponentIdentifier'))
    table = [
        ('Bit', 'Software ID')]
    for bit in range(image_vector_val.bit_length()):
        if image_vector_val & 1 << bit:
            table.append((bit, supported_software_ids.get(bit, 'UNKNOWN')))
    if len(table) > 1:
        return properties_repr(table, [
            0], **('sep_rows',))


def inspect_subsystem_debug_options_bits(subsystem_item = None, subsystem_debug_options_from_profile = None):
    '''Accepts subsystem debug option item.'''
    debug_options = None
    with suppress(StopIteration, KeyError):
        debug_options = None(None((lambda i = None: i['id'] == subsystem_item['SubsysIdentifier']), subsystem_debug_options_from_profile))['supported_debug_options']['debug_option']
        None(None, None, None)
# WARNING: Decompyle incomplete

