
from contextlib import suppress
from typing import List, Optional
from cmd_line_interface.sectools.cmd_line_common.defines import SECURITY_PROFILE
from cmd_line_interface.sectools.tme_secure_debug.defines import defines
from cmd_line_interface.sectools.tme_secure_debug.defines.image_inputs import DEC
from common.data.data import comma_separated_string, hexlify2
from common.data.defines import SHA_DESCRIPTION_TO_FUNCTION, SHA_SIZE_TO_DESCRIPTION
from common.parser.tme.dpr.dpr import DPR
from common.parser.tme.dpr.validations import DPRValidationOptions, TMEItemError, apply_implicit_chip_constraints_from_dec, validate_and_apply_tme_limits
from common.parser.tme.tme_parser.defines import FINGERPRINT_HASH_VALUE_PATH
from common.parser.tme.tme_parser.tme import TME
from core.tme_secure_debug.augmented_inspect import DESCRIBE_OEM_DP, DESCRIBE_QTI_DP, describe

def generate_dpr(dp = None, dec_bytes = None, dpr_validation_options = None):
    '''Assembles the debug policy out of generated DP and provided DEC.'''
    pass
# WARNING: Decompyle incomplete


def add_tme_common_hash(tme, hash_val = None, hash_property = None, algorithm_property = None, allowed_algorithms = (None, False), hash_append = ('tme', TME, 'hash_val', str, 'hash_property', str, 'algorithm_property', str, 'allowed_algorithms', Optional[List], 'hash_append', Optional[bool], 'return', str)):
    '''There are multiple hash accepting tags in TME. Generalize it in a single function.'''
    hash_val = hash_val[2:]
    hash_algorithm = SHA_SIZE_TO_DESCRIPTION[len(hash_val) // 2]
    if allowed_algorithms and hash_algorithm not in allowed_algorithms:
        is_dp = describe(tme) in (DESCRIBE_OEM_DP, DESCRIBE_QTI_DP)
        raise TMEItemError(f'''SvcDebugPolicy/{hash_property.strip('/')}''' if is_dp else hash_property, f'''{hash_algorithm} hash algorithm is not supported. The supported hash algorithm{'s are' if len(allowed_algorithms) > 1 else ' is'} {comma_separated_string(allowed_algorithms, 'and', **('final_separator',))}.''')
# WARNING: Decompyle incomplete

