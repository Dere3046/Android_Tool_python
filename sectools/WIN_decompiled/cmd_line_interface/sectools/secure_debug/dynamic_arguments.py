
from typing import List
from cmd_line_interface.base_defines import KWARGS_ACTION, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_STORE_TRUE, XMLInfo, get_cmd_arg
from cmd_line_interface.basecmdline import update_cmdline_arg
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import AUTHORITY, GENERATE, ROOT_CERTIFICATE_HASH_GROUP, SERIAL_NUMBER
from cmd_line_interface.sectools.metadata import DEPENDS_NOT_FORCED, DEPENDS_ON
from cmd_line_interface.sectools.secure_debug import defines
from cmd_line_interface.sectools.secure_debug.defines import ALL_FLAGS, OEM_FLAG_PREFIX, QTI_TEST_ROOT_CERTIFICATE_HASH, SECURE_DEBUG_NAME, SECURE_DEBUG_NON_SECURE_FLAGS_GROUP, SECURE_DEBUG_SECURE_FLAGS_GROUP
from common.data.data import version_string_to_tuple
from common.parser.debug_policy_elf.defines import DebugOption, OEM_DESIGNATED_FLAG_INDICES
from profile.defines import SCHEMA_VERSION_1_5
from profile.schema.scale_profile import Profile, get_supported_debug_options

def _get_profile_debug_options(security_profile = None):
    if not security_profile.debugging or security_profile.debugging.legacy:
        raise RuntimeError(f'''Security Profile does not support {SECURE_DEBUG_NAME} features.''')
    if None(security_profile.schema_version) < SCHEMA_VERSION_1_5:
        version = security_profile.debugging.legacy.debug_policy_revisions.default_debug_policy_revision
        security_profile.debugging.legacy.supported_debug_options = get_supported_debug_options(version)
    return (lambda .0: [ DebugOption(option.id, option.requires_serial_bind, debug_bits_string_to_ints(option.bits), option.description) for option in .0 ])(security_profile.debugging.legacy.supported_debug_options.debug_option)


def debug_option_id_to_argument(option_id = None):
    return get_cmd_arg(option_id).lower()


def debug_bits_string_to_ints(bits = None):
    return list(map(int, bits.split(',')))


def update_secure_debug_profile_arguments(security_profile = None):
    parsed_profile = security_profile.parsed_xml
    debug_options = _get_profile_debug_options(parsed_profile)
    (secure_flags_key,) = filter((lambda k: k[0] == SECURE_DEBUG_SECURE_FLAGS_GROUP), defines.SECURE_DEBUG.keys())
    (non_secure_flags_key,) = filter((lambda k: k[0] == SECURE_DEBUG_NON_SECURE_FLAGS_GROUP), defines.SECURE_DEBUG.keys())
    defines.SECURE_DEBUG[secure_flags_key] = []
    defines.SECURE_DEBUG[non_secure_flags_key] = []
    for debug_option in debug_options:
        if debug_option.requires_serial_bind:
            defines.SECURE_DEBUG[secure_flags_key].append(([
                debug_option_id_to_argument(debug_option.option_id)], {
                KWARGS_HELP: debug_option.description,
                KWARGS_DEFAULT: False,
                KWARGS_ACTION: KWARGS_STORE_TRUE }, {
                DEPENDS_NOT_FORCED: [
                    SECURITY_PROFILE],
                DEPENDS_ON: [
                    GENERATE,
                    SERIAL_NUMBER] }))
            continue
        defines.SECURE_DEBUG[non_secure_flags_key].append(([
            debug_option_id_to_argument(debug_option.option_id)], {
            KWARGS_HELP: debug_option.description,
            KWARGS_DEFAULT: False,
            KWARGS_ACTION: KWARGS_STORE_TRUE }, {
            DEPENDS_NOT_FORCED: [
                SECURITY_PROFILE],
            DEPENDS_ON: [
                GENERATE] }))
    if not defines.SECURE_DEBUG[secure_flags_key]:
        update_cmdline_arg(defines.SECURE_DEBUG, ALL_FLAGS, {
            DEPENDS_ON: [
                GENERATE] }, **('metadata_kwargs',))
    defines.security_profile_debug_options = debug_options + (lambda .0: [ DebugOption(f'''{OEM_FLAG_PREFIX}{i}''', False, [
i], '') for i in .0 ])(OEM_DESIGNATED_FLAG_INDICES)
    (root_cert_hash_group_key,) = filter((lambda k: k[0] == ROOT_CERTIFICATE_HASH_GROUP), defines.SECURE_DEBUG.keys())
    if not parsed_profile.debugging.legacy.qti_image_id:
        defines.SECURE_DEBUG[root_cert_hash_group_key] = list(filter((lambda x: x[0] != [
QTI_TEST_ROOT_CERTIFICATE_HASH]), defines.SECURE_DEBUG[root_cert_hash_group_key]))
        (authority_key,) = filter((lambda k: k[0] == AUTHORITY), defines.SECURE_DEBUG.keys())
        del defines.SECURE_DEBUG[authority_key]
        return None

