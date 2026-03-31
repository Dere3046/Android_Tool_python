
from contextlib import suppress
from itertools import groupby
from operator import attrgetter, itemgetter
from typing import Callable
from cmd_line_interface.base_defines import COMPATIBLE, KWARGS_ACTION, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_STORE_TRUE, KWARGS_TYPE, OPTIONAL, XMLInfo, max_val_hex_type
from cmd_line_interface.sectools.cmd_line_common.defines import INSPECT, QTI, SECURITY_PROFILE
from cmd_line_interface.sectools.metadata import CONSUMES, DEPENDS_NOT_FORCED, DEPENDS_ON
from cmd_line_interface.sectools.tme_secure_debug.defines import TME_SECURE_DEBUG_NAME, defines
from cmd_line_interface.sectools.tme_secure_debug.defines.debug_options import DEBUG_OPTIONS_GROUP, DEBUG_OPTIONS_GROUP_HELP, IP_SCAN_DUMP_POLICY_GROUP, QAD_DUMP_POLICY_GROUP, debug_vector_id_to_argument, ip_scan_dump_id_to_argument, qad_dump_id_to_argument
from cmd_line_interface.sectools.tme_secure_debug.defines.subsystem_debug_options import get_supported_subsystem_debug_options
from cmd_line_interface.sectools.tme_secure_debug.defines.test_signing import QTI_TEST_SIGNED_IMAGES_GROUP, software_image_id_to_cmd_argument_name
from common.data.data import version_string_to_tuple
from common.parser.tme.tme_parser.defines import DEBUG_POLICY_DATA_PATH, DEBUG_VECTOR_PATH, TEST_SIGNED_IMAGE_VECTOR_PATH
from common.parser.tme.tme_parser.tme import get_selections_for_tag_extended
from common.utils import is_multi_bit, maximum_bits_value
from profile.schema import Profile

def security_profile_process(profile = None):
    '''Processes the Security Profile and returns TME consumable dict.'''
    given_version = float(profile.parsed_xml.schema_version)
    if given_version < 1.2:
        raise RuntimeError(f'''The TME Secure Debug requires Security Profile version 1.2; the provided version is {given_version}. Verify {SECURITY_PROFILE} command line argument.''')
    if not None.parsed_xml.debugging or profile.parsed_xml.debugging.tme:
        raise RuntimeError(f'''Security Profile does not support {TME_SECURE_DEBUG_NAME} features.''')
    
    def attribute_converter(obj = None):
        '''Convert object attributes to nested dictionary.'''
        if hasattr(obj, '__dict__'):
            res = { }
            for k, v in vars(obj).items():
                if not v is not None and k.endswith('_'):
                    if k in ('debug_vector_option', 'debug_option', 'scan_dump_ip', 'qad'):
                        res[k] = v
                        continue
                    res[k] = (lambda .0 = None: [ attribute_converter(i) for i in .0 ])(v) if isinstance(v, list) else attribute_converter(v)
            return res
        res = None
        return res

    resolved_tme_features = profile.parsed_xml.debugging.tme
    ret = attribute_converter(resolved_tme_features)
    cmd_version = version_string_to_tuple(resolved_tme_features.command_version)
    ret.update({
        'cmd_version_major': hex(cmd_version[0]),
        'cmd_version_minor': hex(cmd_version[1]) })
    return ret


def update_tme_security_profile_arguments(security_profile = None):
    '''
    Updates/adds arguments based on the Security Profile. Should be called after the first pass of the cmdline parser
    detects cmdline argument --security-profile.
    '''
    defines.security_profile_data = security_profile_process(security_profile[0])
    with suppress(KeyError):
        for subsystem, g in groupby(get_supported_subsystem_debug_options(defines.security_profile_data), attrgetter('subsystem')):
            subsystem_title = subsystem.replace('_SS_MSID', '').replace('_', ' ')
            defines.TME_SECURE_DEBUG[f'''{subsystem_title} Subsystem Debug Options'''] = (lambda .0: [ ([
i.arg], {
KWARGS_HELP: i.help,
KWARGS_DEFAULT: False,
KWARGS_ACTION: KWARGS_STORE_TRUE }, {
DEPENDS_NOT_FORCED: [
SECURITY_PROFILE],
CONSUMES: [
f'''{DEBUG_POLICY_DATA_PATH}/SubsystemDebugOptions'''] }) for i in .0 ])(g)
        None(None, None, None)
# WARNING: Decompyle incomplete


def set_security_profile_data_for_inspect(security_profiles = None):
    for security_profile in security_profiles:
        processed_security_profile = security_profile_process(security_profile)
        if soc_hw_versions = security_profile.parsed_xml.platform_binding_values.soc_hw_versions:
            for value in soc_hw_versions.value:
                soc_hw_version = value.valueOf_.lower()
                if soc_hw_version in defines.soc_vers_security_profile_data:
                    raise RuntimeError(f'''Multiple Security Profiles contain the same soc_hw_version, {value.valueOf_}. Provide Security Profiles with distinct soc_hw_version values when performing the {INSPECT} operation.''')
                defines.soc_vers_security_profile_data[soc_hw_version] = security_profile.parsed_xml.platform_binding_values.soc_hw_versions

