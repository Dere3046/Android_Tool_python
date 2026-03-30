
from collections import namedtuple
from contextlib import suppress
from functools import partial
from itertools import chain
from operator import attrgetter, contains, itemgetter
from typing import Any, NamedTuple, cast
from cmd_line_interface.sectools.cmd_line_common.defines import QTI, SECURITY_PROFILE, SOC_LIFECYCLE_STATE
from cmd_line_interface.sectools.tme_secure_debug.defines.defines import ASSERT_QTI_OWNERSHIP
from cmd_line_interface.sectools.tme_secure_debug.defines.image_inputs import DEC
from cmd_line_interface.sectools.tme_secure_debug.defines.test_signing import ENABLE_TEST_SIGNED
from common.data.data import and_separated, comma_separated_string, plural_s, unhexlify2
from common.data.defines import SHA_DESCRIPTION_TO_SIZE
from common.logging.logger import log_debug
from common.parser.tme.dpr.validation_utils import get_cmd_arg_by_consumed_tme_tag_name, verify_array, verify_bit_array, verify_debug_options_for_qti
from common.parser.tme.tme_parser.defines import AUTHORIZED_DEBUG_OPTIONS_PATH, AUTHORIZED_DEBUG_VECTOR_PATH, CHIP_UNIQUE_IDENTIFIER_PATH, DEBUG_ENTITLEMENT_PATH, DEBUG_OPTIONS_PATH, DEBUG_POLICY_DATA_PATH, DEBUG_VECTOR_PATH, DEC_CHIP_CONSTRAINTS_PATH, DP_CHIP_CONSTRAINTS_PATH, ENTITLEMENT_CERTIFICATE_PATH, FINGERPRINT_HASH_VALUE_PATH, INSTANTIATION_CONSTRAINTS_PATH, OEM_BATCH_KEY_HASH_PATH, OEM_RC_HASH_PATH, SIGNATURE_PATH, TEST_SIGNED_IMAGE_HASH_LIST_PATH, TEST_SIGNED_IMAGE_VECTOR_PATH
from common.parser.tme.tme_parser.exceptions import ProtocolParsingError
from common.parser.tme.tme_parser.tme import TME, get_selections_for_tag, get_selections_for_tag_extended
from core.tme_secure_debug.augmented_inspect import DESCRIBE_OEM_DP, DESCRIBE_OEM_DPR, DESCRIBE_QTI_DP, DESCRIBE_QTI_DPR, describe

class TMEItemError(RuntimeError):
    
    def __init__(self = None, tag_name = None, *args):
        self.tag_name = [
            tag_name] if isinstance(tag_name, str) else tag_name
    # WARNING: Decompyle incomplete

    
    def __str__(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class DPRValidationOptions(NamedTuple):
    allow_unsigned: bool = False
    skip_validation: bool = False
    allow_delegate_key_in_oem_dpr: bool = False


def validate_dpr(dpr = None, options = None):
    '''
    Verifies the Debug Policy Request (DPR).
    Checks the Debug Policy (SvcDebugPolicy/DebugPolicyData) against the
    DEC (SvcDebugPolicy/EntitlementCertificate/Entitlements/DebugEntitlement) within the DPR.

    [Miguel Jun 25 2020] Here are the mappings:

        In general, a DP can request zero or more authorized debug capabilities but not more. If DP exceeds what it
            is authorized then DP will fail.
        DEC.AuthorizedDebugVector authorizes DP.DebugVector
        DEC.AuthorizedDebugOptions authorizes DP.Options
        DEC.AuthorizedTestSignedImageVector authorizes DP.TestSignedImageVector

        On Instantiation Constraints, they map almost one to one to Chip Constraints with a couple of exceptions:
        IS_NONCE_BOUND is not applicable to DP, only applicable to AuthenticatedDebugRequest
        IS_QTI_OWNERSHIP_ASSERTION_BOUND maps to DP.DebugOptions.ASSERT_QTI_OWNERSHIP and use to designate a DP as QTI
            issued vs OEM issued
        IS_ENT_FINGERPRINT_BOUND maps to DP.EntitlementFingerprint
        DEC.PublicKey being present as the constraint for DP signature required.

        The Instantiation Constraint specifies which chip constraints must be set in the DP instantiation
            (e.g. IS_OEM_ID_BOUND means that DP must be bound to an OEM_ID value).
    '''
    if options.skip_validation:
        log_debug('Skipping DPR validation.')
        return None
    if None(dpr) not in (DESCRIBE_QTI_DPR, DESCRIBE_OEM_DPR):
        raise RuntimeError(f'''Expecting a DPR, but {describe(dpr)} is provided.''')
    if not None.is_item(DEBUG_ENTITLEMENT_PATH):
        raise RuntimeError('The DPR is invalid, missing a DEC.')
    with None(KeyError):
        constraints = dpr.get_item(INSTANTIATION_CONSTRAINTS_PATH)
        exclusives = list(filter(partial(contains, [
            'IS_FEAT_ID_BOUND',
            'IS_JTAG_ID_BOUND',
            'IS_SOC_HW_VERSION_BOUND']), constraints))
        if len(exclusives) > 1:
            raise RuntimeError(f'''The DEC is invalid. Only one of the following Instantiation Constraints should be present: {comma_separated_string(exclusives)}. Consider providing a different DEC via {DEC}.''')
        None(None, None, None)
# WARNING: Decompyle incomplete


def apply_implicit_chip_constraints_from_dec(dpr = None):
    '''
    That is possible that DP may not set any Chip Constraints, and DEC has it. That way, the target will
    respect the Constraints from the DEC. However, other logic (e.g., ELF gen) relies on the chip constraints from DP,
    not DEC. To make it explicit, copy the DEC constraints. The copy only possible if DP misses a constraint at all.
    '''
    dp_paths = []
    dec_paths = []
    for prefix, var in {
        DEC_CHIP_CONSTRAINTS_PATH: dec_paths,
        DP_CHIP_CONSTRAINTS_PATH: dp_paths }.items():
        var.extend(set(map(itemgetter(0), dpr.get_items_under_path(prefix))))
    for path in dec_paths:
        if path not in dp_paths:
            dpr.set_item(f'''{DP_CHIP_CONSTRAINTS_PATH}{path}''', dpr.get_item(DEC_CHIP_CONSTRAINTS_PATH + path))
            log_debug(f'''Copied DEC Chip Constraint to DP: {path}.''')


def validate_and_apply_tme_limits(dpr_or_dpr = None, limits = None):
    '''
    Uses the Security Profile data to verify and fix (if necessary) TME fields according to given target limits.
    Note: The main use case is the DPR/DP processing, however the function is generic and can be used for any standard
    TME structure.
    @param dpr_or_dpr - TME object that may be modified. Can be DPR or DP.
    @param limits - the Security Profile limits section.
    '''
    object_type = describe(dpr_or_dpr)
# WARNING: Decompyle incomplete

