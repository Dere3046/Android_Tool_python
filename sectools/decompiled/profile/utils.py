
import re
from io import StringIO
from typing import Any, Iterable
from cmd_line_interface.sectools.cmd_line_common.defines import INFILE, SECURITY_PROFILE
from common.crypto.openssl.defines import ALGORITHM_ECDSA_USER_FACING, ALGORITHM_RSA_USER_FACING
from common.crypto.openssl.openssl import SignatureFormat
from common.data.data import comma_separated_string
from common.parser.elf.defines import ELFCLASS_TO_INT
from profile.defines import ANY, UNKNOWN
from profile.schema import HashTableSegmentProperties, ImageFormat, LicenseManagerSegmentProperties, MBNProperties, SignatureFormat as ProfileSignatureFormat, VouchSegmentProperties

def filter_elements(elements = None):
    filter_prefixes = [
        'gds_',
        'ns_prefix',
        'nsprefix',
        'original_tagname_',
        'parent_object_']
    return None((lambda .0 = None: pass# WARNING: Decompyle incomplete
)(list(elements.keys())))


def verify_profile_elements(parsed_profile_elements = None, schema_elements = None, object_name = None, function_name = ('parsed_profile_elements', Iterable, 'schema_elements', Iterable, 'object_name', str, 'function_name', str, 'return', None)):
    unrecognized_elements = set(parsed_profile_elements) - set(schema_elements)
    if unrecognized_elements:
        unrecognized_elements_string = comma_separated_string(list(unrecognized_elements), 'and', **('final_separator',))
        member_string = 'unrecognized members' if len(unrecognized_elements) > 1 else 'an unrecognized member'
        raise RuntimeError(f'''{object_name} contains {member_string} {unrecognized_elements_string}. To support new members, update SCHEMA_STRUCTURE dictionary and {function_name} accordingly.''')


def compare_objects(primary_buffer, secondary_buffer = None, primary_object = None, secondary_object = None, error_string = ('primary_buffer', StringIO, 'secondary_buffer', StringIO, 'primary_object', Any, 'secondary_object', Any, 'error_string', str, 'return', None)):
    primary_object.export(primary_buffer, 0, '', **('namespacedef_',))
    secondary_object.export(secondary_buffer, 0, '', **('namespacedef_',))
    if primary_buffer.getvalue() != secondary_buffer.getvalue():
        raise RuntimeError(error_string)


def compare_authentication_image_format(parsed_image_format = None, profile_image_format = None):
    match = False
    image_elf = getattr(parsed_image_format, 'elf_properties', None)
    profile_elf = getattr(profile_image_format, 'elf_properties', None)
    image_hash_table_segment = getattr(parsed_image_format, 'hash_table_segment_properties', None)
    profile_hash_table_segment = getattr(profile_image_format, 'hash_table_segment_properties', None)
    image_vouch_segment = getattr(parsed_image_format, 'vouch_segment_properties', None)
    profile_vouch_segment = getattr(profile_image_format, 'vouch_segment_properties', None)
    image_lm_segment = getattr(parsed_image_format, 'license_manager_segment_properties', None)
    profile_lm_segment = getattr(profile_image_format, 'license_manager_segment_properties', None)
    image_mbn = getattr(parsed_image_format, 'mbn_properties', None)
    profile_mbn = getattr(profile_image_format, 'mbn_properties', None)
    if image_elf:
        if profile_elf and ELFCLASS_TO_INT[image_elf.elf_class] in profile_elf.elf_class.supported_elf_classes.value and bool(image_elf.contains_preamble) == profile_elf.contains_preamble:
            match = True
        if bool(profile_hash_table_segment) != bool(image_hash_table_segment):
            match = False
        elif image_hash_table_segment and profile_hash_table_segment:
            if match:
                pass
            match = compare_hash_table_segment_properties(image_hash_table_segment, profile_hash_table_segment)
        elif match:
            pass
        match = True
        if bool(profile_vouch_segment) != bool(image_vouch_segment):
            match = False
        elif image_vouch_segment and profile_vouch_segment:
            if match:
                pass
            match = compare_vouch_segment_properties(image_vouch_segment, profile_vouch_segment)
        elif match:
            pass
        match = True
        if bool(profile_lm_segment) != bool(image_lm_segment):
            match = False
            return match
        if match and profile_lm_segment:
            if match:
                pass
            match = compare_license_manager_segment_properties(image_lm_segment, profile_lm_segment)
            return match
        if match:
            pass
        match = True
        return match
    if None and profile_mbn and compare_mbn_properties(image_mbn, profile_mbn):
        match = True
    return match


def compare_hash_table_segment_properties(image = None, profile = None):
    if image.hash_table_segment_version == profile.hash_table_segment_version:
        pass
    match = image.hash_pages == profile.hash_pages
    profile_placements = profile.hash_table_segment_placements.supported_hash_table_segment_placements.value
    if ANY not in profile_placements:
        if UNKNOWN in image.hash_table_segment_placements:
            raise RuntimeError(f'''The placement of the Hash Table Segment in {INFILE} is not supported by Security Profiles provided via {SECURITY_PROFILE}.''')
        if None:
            pass
        match = bool(set(image.hash_table_segment_placements).intersection(set(profile_placements)))
    if profile.hash_table_segment_alignment != ANY:
        if match:
            pass
        match = image.hash_table_segment_alignment == int(profile.hash_table_segment_alignment, 16)
    segment_hash_algorithms = profile.segment_hash_algorithms.supported_segment_hash_algorithms.value
    if match:
        pass
    match = None((lambda .0 = None: for hash_algorithm in .0:
hash_algorithm in segment_hash_algorithms + [
'NA'])(image.segment_hash_algorithms))
    if image.hash_table_segment_metadata_versions and profile.hash_table_segment_metadata_versions:
        profile_versions = profile.hash_table_segment_metadata_versions.supported_hash_table_segment_metadata_versions.value
        if match:
            pass
        match = bool(set(image.hash_table_segment_metadata_versions).intersection(set(profile_versions)))
    if image.hash_table_segment_common_metadata_versions and profile.hash_table_segment_common_metadata_versions:
        common_metadata_versions = profile.hash_table_segment_common_metadata_versions
        profile_versions = common_metadata_versions.supported_hash_table_segment_common_metadata_versions.value
        if match:
            pass
        match = bool(set(image.hash_table_segment_common_metadata_versions).intersection(set(profile_versions)))
    return match


def compare_vouch_segment_properties(image = None, profile = None):
    segment_hash_algorithms = profile.vouch_segment_hash_algorithms.supported_vouch_segment_hash_algorithms.value
    if image.vouch_segment_version == profile.vouch_segment_version and image.max_entry_count <= profile.max_entry_count:
        pass
    match = bool(set(image.vouch_segment_hash_algorithms).intersection(set(segment_hash_algorithms)))
    profile_placements = profile.vouch_segment_placements.supported_vouch_segment_placements.value
    if ANY not in profile_placements:
        if UNKNOWN in image.vouch_segment_placements:
            raise RuntimeError(f'''The placement of the Multi Image segment in {INFILE} is not supported by Security Profiles provided via {SECURITY_PROFILE}.''')
        if None:
            pass
        match = bool(set(image.vouch_segment_placements).intersection(set(profile_placements)))
    if profile.vouch_segment_alignment != ANY:
        if match:
            pass
        match = image.vouch_segment_alignment == int(profile.vouch_segment_alignment, 16)
    if profile.phy_addr != ANY:
        if match:
            pass
        match = image.phy_addr == int(profile.phy_addr, 16)
    return match


def compare_license_manager_segment_properties(image = None, profile = None):
    profile_placements = profile.license_manager_segment_placements.supported_license_manager_segment_placements
    match = image.license_manager_segment_version == profile.license_manager_segment_version
    if ANY not in profile_placements.value:
        if UNKNOWN in image.license_manager_segment_placements:
            raise RuntimeError(f'''The placement of the License Manager segment in {INFILE} is not supported by Security Profiles provided via {SECURITY_PROFILE}.''')
        if None:
            pass
        match = set(image.license_manager_segment_placements).intersection(set(profile_placements.value))
    if profile.license_manager_segment_alignment != ANY:
        if match:
            pass
        match = image.license_manager_segment_alignment == int(profile.license_manager_segment_alignment, 16)
    return match


def compare_mbn_properties(image = None, profile = None):
    match = image.mbn_version == profile.mbn_version
    if image.mbn_metadata_versions and profile.mbn_metadata_versions:
        profile_versions = profile.mbn_metadata_versions.supported_mbn_metadata_versions.value
        if match:
            pass
        match = set(image.mbn_metadata_versions).intersection(set(profile_versions))
    if image.mbn_common_metadata_versions and profile.mbn_common_metadata_versions:
        profile_versions = profile.mbn_common_metadata_versions.supported_mbn_common_metadata_versions.value
        if match:
            pass
        match = set(image.mbn_common_metadata_versions).intersection(set(profile_versions))
    return match


def compare_legacy_debugging_format(image, profile):
    if image.debug_policy_revisions in profile.debug_policy_revisions.supported_debug_policy_revisions.value:
        pass
    match = image.phy_addr == int(profile.phy_addr, 16)
    if match:
        pass
    match = ELFCLASS_TO_INT[image.elf_class] in profile.elf_class.supported_elf_classes.value
    profile_placements = profile.debug_policy_segment_placements.supported_debug_policy_segment_placements.value
    if ANY not in profile_placements:
        if match:
            pass
        match = set(image.debug_policy_segment_placements).intersection(set(profile_placements))
    if profile.debug_policy_segment_alignment != ANY:
        if match:
            pass
        match = image.debug_policy_segment_alignment == int(profile.debug_policy_segment_alignment, 16)
    return match


def compare_fuse_blowing_format(image, profile):
    if profile.sec_elf_properties:
        profile_elf = profile.sec_elf_properties
        image_elf = image.sec_elf_properties
        if image_elf.sec_dat_segment_versions in profile_elf.sec_dat_segment_versions.supported_sec_dat_segment_versions.value:
            pass
        match = image_elf.phy_addr == int(profile_elf.phy_addr, 16)
        if match:
            pass
        match = ELFCLASS_TO_INT[image_elf.elf_class] in profile_elf.elf_class.supported_elf_classes.value
        profile_placements = profile_elf.sec_dat_segment_placements.supported_sec_dat_segment_placements.value
        if ANY not in profile_placements:
            if match:
                pass
            match = set(image_elf.sec_dat_segment_placements).intersection(set(profile_placements))
        if profile_elf.sec_dat_segment_alignment != ANY:
            if match:
                pass
            match = image_elf.sec_dat_segment_alignment == int(profile_elf.sec_dat_segment_alignment, 16)
        if image_elf.fuse_version and profile_elf.fuse_version:
            if match:
                pass
            match = image_elf.fuse_version == profile_elf.fuse_version
        return match
    match = None
    return match


def get_ids_for_format(signature_format = None, get_default = None):
    format_ids = []
    format_id = signature_format.signature_algorithm
    default_hash_algorithm = signature_format.signature_hash_algorithms.default_signature_hash_algorithm
    supported_hash_algorithms = signature_format.signature_hash_algorithms.supported_signature_hash_algorithms.value
    if format_id == ALGORITHM_ECDSA_USER_FACING:
        if get_default:
            curve = signature_format.ecdsa_curves.default_ecdsa_curve
            format_ids.append(f'''{format_id}-{default_hash_algorithm}-{curve}''')
            return format_ids
        for hash_algorithm in None:
            for curve in signature_format.ecdsa_curves.supported_ecdsa_curves.value:
                format_ids.append(f'''{format_id}-{hash_algorithm}-{curve}''')
        return format_ids
    if None == ALGORITHM_RSA_USER_FACING:
        if get_default:
            key_size = signature_format.key_sizes.default_key_size
            padding = signature_format.rsa_paddings.default_rsa_padding
            exponent = signature_format.exponents.default_exponent
            format_ids.append(f'''{format_id}-{default_hash_algorithm}-KEY{key_size}-{padding}-EXP{exponent}''')
            return format_ids
        for hash_algorithm in None:
            for key_size in signature_format.key_sizes.supported_key_sizes.value:
                for padding in signature_format.rsa_paddings.supported_rsa_paddings.value:
                    for exponent in signature_format.exponents.supported_exponents.value:
                        format_ids.append(f'''{format_id}-{hash_algorithm}-KEY{key_size}-{padding}-EXP{exponent}''')
        return format_ids
    None.append(format_id)
    return format_ids


def get_signature_format_from_id(signature_format_id = None):
    pass
# WARNING: Decompyle incomplete

