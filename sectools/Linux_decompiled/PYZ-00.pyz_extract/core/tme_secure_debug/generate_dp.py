
from collections import namedtuple
from functools import reduce
from itertools import groupby
from math import ceil
from operator import attrgetter, itemgetter, or_
from struct import pack, unpack
from typing import Callable
import profile
from cmd_line_interface.base_defines import get_cmd_member
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import OEM_ID, OEM_LIFECYCLE_STATE, OEM_PRODUCT_ID, OEM_TEST_ROOT_CERTIFICATE_HASH, PLATFORM_BINDING, QTI, SERIAL_NUMBER, SOC_LIFECYCLE_STATE, VARIANT
from cmd_line_interface.sectools.secure_image.defines import OEM_ROOT_CERTIFICATE_HASH
from cmd_line_interface.sectools.tme_secure_debug.defines import defines
from cmd_line_interface.sectools.tme_secure_debug.defines.debug_options import ALLOW_SYSTEM_WATCHDOG_ACCESS, CRASH_DUMP, DISABLE_SYSTEM_WATCHDOG, OEM_CRASH_DUMP_PUBLIC_KEY, PERSIST_ON_RESET, debug_vector_id_to_argument, get_bit_shifted_value, ip_scan_dump_id_to_argument, qad_dump_id_to_argument
from cmd_line_interface.sectools.tme_secure_debug.defines.defines import ASSERT_QTI_OWNERSHIP
from cmd_line_interface.sectools.tme_secure_debug.defines.device_restrictions import OEM_BATCH_KEY_HASH
from cmd_line_interface.sectools.tme_secure_debug.defines.subsystem_debug_options import get_supported_subsystem_debug_options
from cmd_line_interface.sectools.tme_secure_debug.defines.test_signing import ENABLE_TEST_SIGNED
from common.crypto.openssl.defines import CURVE_ASN1_TO_NORMALIZED_ASN1_NIST, CURVE_NORMALIZED_ASN1_TO_ASN1
from common.crypto.openssl.openssl import get_x_y_from_ecdsa_public_key2
from common.data.data import and_separated, hexlify2, plural_s
from common.parser.tme.dpr.validations import TMEItemError
from common.parser.tme.tme_parser.defines import OEM_CRASH_DUMP_PUBLIC_KEY_PATH
from common.parser.tme.tme_parser.tme import TME
from core.platform_binding_utilities import get_security_profile_platform_binding_values
from core.tme_secure_debug.enable_test_signed import _add_test_signed_image_vector, add_enable_test_signed
from core.tme_secure_debug.generate_dpr import add_tme_common_hash
from profile.defines import JTAG_IDS, SOC_FEATURE_IDS, SOC_HW_VERSIONS

def generate_dp(parsed_args = None):
    debug_policy = TME(defines.security_profile_data['tme_version'], **('version',))
    if parsed_args.get(OEM_ID):
        debug_policy.DebugPolicyData.ChipConstraints.OemIdentifier = parsed_args.get(OEM_ID)
    if parsed_args.get(OEM_PRODUCT_ID):
        debug_policy.DebugPolicyData.ChipConstraints.OemProductIdentifier = parsed_args.get(OEM_PRODUCT_ID)
    if parsed_args.get(SOC_LIFECYCLE_STATE):
        debug_policy.DebugPolicyData.ChipConstraints.SocLifeCycleState = parsed_args.get(SOC_LIFECYCLE_STATE).replace('-', '_')
    if parsed_args.get(SERIAL_NUMBER):
        SerialNumber = namedtuple('SerialNumber', 'product_id, serial_number, cmd_value')
        serial_numbers = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(parsed_args.get(SERIAL_NUMBER))
        unique_product_ids = set(map(attrgetter('product_id'), serial_numbers))
        if 1 != len(unique_product_ids):
            grouped = sorted((lambda .0: [ list(g) for _, g in .0 ])(groupby(sorted(serial_numbers, attrgetter('product_id'), **('key',)), attrgetter('product_id'), **('key',))), len, **('key',))
            raise RuntimeError(f'''All serial numbers have to be of the same Product ID. Provided serial numbers contain the following Product IDs: {and_separated(map(hex, unique_product_ids))}. Check the following serial number{plural_s(grouped[0])}: {and_separated(map(attrgetter('cmd_value'), grouped[0]))}''')
        debug_policy.DebugPolicyData.ChipConstraints.ChipUniqueIdentifier.ProductIdentifier = None[-1].product_id
        debug_policy.DebugPolicyData.ChipConstraints.ChipUniqueIdentifier.SerialNumber = list(set(map(attrgetter('serial_number'), serial_numbers)))
    if parsed_args.get(PLATFORM_BINDING):
        _add_platform_bindings(parsed_args, debug_policy)
    for arg, tme_flag in {
        ALLOW_SYSTEM_WATCHDOG_ACCESS: 'ALLOW_SYSTEM_WATCHDOG_ACCESS',
        DISABLE_SYSTEM_WATCHDOG: 'DISABLE_SYSTEM_WATCHDOG',
        PERSIST_ON_RESET: 'PERSIST_ON_RESET',
        QTI: ASSERT_QTI_OWNERSHIP }.items():
        if parsed_args.get(arg):
            debug_options = debug_policy.DebugPolicyData.DebugOptions
            if isinstance(debug_options, list):
                debug_options.append(tme_flag)
                continue
            debug_policy.DebugPolicyData.DebugOptions = [
                tme_flag]
    if parsed_args.get(CRASH_DUMP):
        debug_policy.DebugPolicyData.CrashDumpVector = parsed_args.get(CRASH_DUMP)
    if parsed_args.get(OEM_LIFECYCLE_STATE):
        debug_policy.DebugPolicyData.ChipConstraints.OemLifeCycleState = parsed_args.get(OEM_LIFECYCLE_STATE)
    if defines.security_profile_data:
        _add_subsystem_debug_options(parsed_args, debug_policy)
        _add_debug_vector(parsed_args, debug_policy)
        _add_dump_policy_vector(parsed_args, debug_policy, 'ip_scan_dump_policy_vector', 'scan_dump_ip', ip_scan_dump_id_to_argument, 'DebugIPScanDumpPolicyVector')
        _add_dump_policy_vector(parsed_args, debug_policy, 'qad_dump_policy_vector', 'qad', qad_dump_id_to_argument, 'DebugQADDumpPolicyVector')
    if parsed_args.get(ENABLE_TEST_SIGNED):
        add_enable_test_signed(parsed_args, debug_policy)
    _add_test_signed_image_vector(parsed_args, debug_policy)
    if parsed_args.get(OEM_ROOT_CERTIFICATE_HASH):
        add_tme_common_hash(debug_policy, parsed_args.get(OEM_ROOT_CERTIFICATE_HASH), 'DebugPolicyData/ChipConstraints/OemRcHash/HashArray', 'DebugPolicyData/ChipConstraints/OemRcHash/HashAlgorithmIdentifier', defines.security_profile_data['supported_oem_rch_algorithms']['value'], **('hash_property', 'algorithm_property', 'allowed_algorithms'))
    if parsed_args.get(OEM_BATCH_KEY_HASH):
        add_tme_common_hash(debug_policy, parsed_args.get(OEM_BATCH_KEY_HASH), 'DebugPolicyData/ChipConstraints/OemBatchKeyHash/HashArray', 'DebugPolicyData/ChipConstraints/OemBatchKeyHash/HashAlgorithmIdentifier', defines.security_profile_data['supported_oem_rch_algorithms']['value'], **('hash_property', 'algorithm_property', 'allowed_algorithms'))
    if parsed_args.get(OEM_TEST_ROOT_CERTIFICATE_HASH):
        hash_algorithms = []
        for hash_val in parsed_args.get(OEM_TEST_ROOT_CERTIFICATE_HASH):
            allowed_algorithms = defines.security_profile_data['supported_oem_rch_algorithms']['value']
            hash_algorithms.append(add_tme_common_hash(debug_policy, hash_val, 'DebugPolicyData/OemTestRootCaHashValues/HashArray', 'DebugPolicyData/OemTestRootCaHashValues/HashAlgorithmIdentifier', allowed_algorithms, True, **('hash_property', 'algorithm_property', 'allowed_algorithms', 'hash_append')))
        if len(set(hash_algorithms)) > 1:
            raise RuntimeError(f'''The hashes provided via {OEM_TEST_ROOT_CERTIFICATE_HASH} must be of the same hash algorithm. However, the provided hashes are {and_separated(sorted(set(hash_algorithms)))} hashes.''')
        if None.get(OEM_CRASH_DUMP_PUBLIC_KEY):
            _add_oem_crash_dump_public_key(parsed_args.get(OEM_CRASH_DUMP_PUBLIC_KEY), debug_policy)
    return debug_policy


def _add_oem_crash_dump_public_key(key = None, debug_policy = None):
    pass
# WARNING: Decompyle incomplete


def _add_subsystem_debug_options(parsed_args = None, debug_policy = None):
    selected_debug_options = None((lambda i = None: if get_cmd_member(i.arg) in vars(parsed_args):
passvars(parsed_args)[get_cmd_member(i.arg)]), get_supported_subsystem_debug_options(defines.security_profile_data))
    for k, g in groupby(sorted(selected_debug_options, attrgetter('subsystem'), **('key',)), attrgetter('subsystem'), **('key',)):
        val = reduce(or_, map((lambda x: 1 << x.bit), g), 0)
        subsystem_debug_options = debug_policy.DebugPolicyData.SubsystemDebugOptions
        subsystem_option = {
            'SubsysIdentifier': k,
            'SubsysDebugOptions': hex(val) }
        if isinstance(subsystem_debug_options, list):
            subsystem_debug_options.append(subsystem_option)
            continue
        debug_policy.DebugPolicyData.SubsystemDebugOptions = [
            subsystem_option]


def _add_debug_vector(parsed_args = None, debug_policy = None):
    all_debug_vector_args = list(map((lambda x: (get_cmd_member(debug_vector_id_to_argument(x.id)), 1 << x.bit, x.enabled_if_crash_dump_vector)), defines.security_profile_data['debug_vector']['debug_vector_option']))
    selected_options = None(None((lambda i = None: if i[0] in vars(parsed_args):
passvars(parsed_args)[i[0]]), all_debug_vector_args))
    if parsed_args.get(CRASH_DUMP):
        for selected_options in parsed_args.get(CRASH_DUMP):
            crash_dump = None
    val = reduce(or_, map(itemgetter(1), selected_options), 0)
    debug_policy.DebugPolicyData.DebugVector = hexlify2(val.to_bytes(ceil(val.bit_length() / 8), 'little', False, **('length', 'byteorder', 'signed'))) if selected_options else ''


def _add_dump_policy_vector(parsed_args, debug_policy, vector_name = None, item_name = None, arg_name_function = None, attr_name = ('parsed_args', NamespaceWithGet, 'debug_policy', TME, 'vector_name', str, 'item_name', str, 'arg_name_function', Callable[([
    str], str)], 'attr_name', str, 'return', None)):
    if vector_name in defines.security_profile_data:
        relevant_args = None(None((lambda x = None: (get_cmd_member(arg_name_function(x.id)), x.bits)), defines.security_profile_data[vector_name][item_name]))
        if selected_options = None(None((lambda i = None: parsed_args.get(i[0])), relevant_args)):
            val = None(None, (lambda .0 = None: [ get_bit_shifted_value(selected_option[1], parsed_args.get(selected_option[0])) for selected_option in .0 ])(selected_options), 0)
            formatted_val = hexlify2(val.to_bytes(ceil(val.bit_length() / 8), 'little', False, **('length', 'byteorder', 'signed')))
            setattr(debug_policy.DebugPolicyData, attr_name, formatted_val)
            return None
        return None(None((lambda i = None: parsed_args.get(i[0])), relevant_args))


def _add_platform_bindings(parsed_args = None, debug_policy = None):
    pass
# WARNING: Decompyle incomplete

