
from copy import deepcopy
from typing import Any
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_ID, SECURITY_PROFILE
from common.crypto.openssl.defines import ALGORITHM_ECDSA_USER_FACING, ALGORITHM_RSA_USER_FACING
from common.logging.logger import log_debug
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from core.profile_validator.defines import UIE
from profile.defines import ANY, JTAG_IDS, PRODUCT_SEGMENT_IDS, SCHEMA_STRUCTURE, SOC_FEATURE_IDS, SOC_HW_VERSIONS
from profile.schema import Authenticator, EncryptionFeatures, EncryptionFormat, HashTableSegmentProperties, Image, ImageFormat, ImageFormats, LicenseManagerSegmentProperties, MBNProperties, PlatformBindings, Profile, SignatureFormat, SignatureFormats, SigningFeatures, SupportedEncryptionFormats, TMEELFProperties, VouchSegmentProperties
from profile.utils import filter_elements, verify_profile_elements
FormatToResolve = EncryptionFormat | SignatureFormat | SigningFeatures | MBNProperties | HashTableSegmentProperties | VouchSegmentProperties | LicenseManagerSegmentProperties
DictToResolve = dict[(str, tuple[(list[str], str)])]

def resolve_platform_bindings(parsed_profiles = None, schema_member = None):
    profile_platform_bindings = deepcopy(parsed_profiles[0].platform_binding_values)
    verify_profile_elements(filter_elements(vars(profile_platform_bindings)), schema_member.keys(), 'platform_binding_values', 'resolve_platform_bindings')
    for parsed_profile in parsed_profiles[1:]:
        parsed_platform_bindings = parsed_profile.platform_binding_values
        verify_profile_elements(filter_elements(vars(parsed_platform_bindings)), schema_member.keys(), 'platform_binding_values', 'resolve_platform_bindings')
        for platform_binding in (SOC_HW_VERSIONS, JTAG_IDS, SOC_FEATURE_IDS, PRODUCT_SEGMENT_IDS):
            if getattr(profile_platform_bindings, platform_binding) and getattr(parsed_platform_bindings, platform_binding):
                for value in getattr(parsed_platform_bindings, platform_binding).value:
                    value_found = False
                    for profile_value in getattr(profile_platform_bindings, platform_binding).value:
                        if value.valueOf_ == profile_value.valueOf_ and value.variant != profile_value.variant:
                            getattr(profile_platform_bindings, platform_binding).value.append(value)
                            value_found = True
                    if not value_found:
                        getattr(profile_platform_bindings, platform_binding).value.append(value)
                continue
            setattr(profile_platform_bindings, platform_binding, None)
    return profile_platform_bindings


def resolve_authenticator(authenticators = None, encrypt = None, schema_member = None):
    for authenticator in authenticators:
        verify_profile_elements(filter_elements(vars(authenticator)), schema_member.keys(), f'''Authenticator {authenticator.id}''', 'resolve_authenticator')
    resolved_authenticator = deepcopy(authenticators[0])
    resolved_authenticator.supported_image_formats = resolve_supported_image_formats(authenticators, schema_member['supported_image_formats'])
    if resolved_authenticator.supported_oem_signing_features:
        resolved_authenticator.supported_oem_signing_features = resolve_supported_signing_features(authenticators, AUTHORITY_OEM, schema_member['supported_oem_signing_features'])
    if resolved_authenticator.supported_qti_signing_features:
        resolved_authenticator.supported_qti_signing_features = resolve_supported_signing_features(authenticators, AUTHORITY_QTI, schema_member['supported_qti_signing_features'])
    if encrypt:
        if resolved_authenticator.supported_oem_encryption_features:
            resolved_authenticator.supported_oem_encryption_features = resolve_supported_encryption_features(authenticators, AUTHORITY_OEM, schema_member['supported_oem_encryption_features'])
        if resolved_authenticator.supported_qti_encryption_features:
            resolved_authenticator.supported_qti_encryption_features = resolve_supported_encryption_features(authenticators, AUTHORITY_QTI, schema_member['supported_qti_encryption_features'])
    supported_image_format_ids = (lambda .0: [ supported_image_format.id for supported_image_format in .0 ])(resolved_authenticator.supported_image_formats.image_format)
    if not supported_image_format_ids:
        raise RuntimeError(f'''There is no image_format that is supported by Security Profiles provided via {SECURITY_PROFILE}.''')
    if None.default_image_format not in supported_image_format_ids:
        resolved_authenticator.default_image_format = resolved_authenticator.supported_image_formats.image_format[0]
    return resolved_authenticator


def resolve_supported_image_formats(authenticators = None, schema_member = None):
    resolved_image_formats = deepcopy(authenticators[0].supported_image_formats)
    verify_profile_elements(filter_elements(vars(resolved_image_formats)), schema_member.keys(), f'''supported_image_formats for authenticator {authenticators[0].id}''', 'resolve_supported_image_formats')
    for authenticator in authenticators[1:]:
        verify_profile_elements(filter_elements(vars(authenticator.supported_image_formats)), schema_member.keys(), f'''supported_image_formats for authenticator {authenticator.id}''', 'resolve_supported_image_formats')
        image_formats = authenticator.supported_image_formats.image_format
        resolved_image_formats.image_format = resolve_image_formats(resolved_image_formats.image_format, image_formats, schema_member['image_format'])
    return resolved_image_formats


def not_candidates_for_resolution(primary_image_format = None, secondary_image_format = None):
    if primary_image_format.file_type == 'ELF':
        if (bool(primary_image_format.hash_table_segment_properties) != bool(secondary_image_format.hash_table_segment_properties) and bool(primary_image_format.vouch_segment_properties) != bool(secondary_image_format.vouch_segment_properties) and bool(primary_image_format.license_manager_segment_properties) != bool(secondary_image_format.license_manager_segment_properties) or primary_image_format.elf_properties.contains_preamble != secondary_image_format.elf_properties.contains_preamble) and primary_image_format.file_type == 'MBN':
            pass
    return primary_image_format.mbn_properties.mbn_version != secondary_image_format.mbn_properties.mbn_version


def resolve_image_formats(primary_image_formats = None, secondary_image_formats = None, schema_member = None):
    resolved_image_formats = []
# WARNING: Decompyle incomplete


def resolve_alignment(primary_feature = None, secondary_feature = None, feature_string = None, error_str = ('primary_feature', Any, 'secondary_feature', Any, 'feature_string', str, 'error_str', str, 'return', str | None)):
    primary_alignment = getattr(primary_feature, feature_string)
    secondary_alignment = getattr(secondary_feature, feature_string)
    if bool(primary_alignment) != bool(secondary_alignment):
        if not primary_alignment:
            pass
        resolved_alignment = secondary_alignment
        return resolved_alignment
    if None is None and secondary_alignment is None:
        resolved_alignment = ANY
        return resolved_alignment
    if None != ANY and secondary_alignment != ANY:
        if int(primary_alignment, 16) != int(secondary_alignment, 16):
            raise RuntimeError(f'''Security Profiles provided via {SECURITY_PROFILE} do not have a common value for {error_str}.''')
        resolved_alignment = None
        return resolved_alignment
    resolved_alignment = primary_alignment if None == ANY else secondary_alignment
    return resolved_alignment


def resolve_phy_addr(primary_phy_addr = None, secondary_phy_addr = None, feature_string = None):
    if primary_phy_addr != ANY and secondary_phy_addr != ANY and int(primary_phy_addr, 16) != int(secondary_phy_addr, 16):
        raise RuntimeError(f'''Security Profiles provided via {SECURITY_PROFILE} do not have a common value for phy_addr in the {feature_string}.''')
    if None != ANY:
        return primary_phy_addr


def resolve_image_format(primary_format = None, secondary_format = None, schema_member = None):
    primary_format_copy = deepcopy(primary_format)
    error = f'''Security Profiles provided via {SECURITY_PROFILE} do not have a common value for'''
    if primary_format_copy.file_type == 'MBN':
        for image_format in (primary_format_copy, secondary_format):
            verify_profile_elements(filter_elements(vars(image_format.mbn_properties)), schema_member['mbn_properties'].keys(), f'''mbn_properties for image format {image_format.id}''', 'resolve_image_format')
        metadata = { }
        if primary_metadata_versions = primary_format_copy.mbn_properties.mbn_metadata_versions:
            metadata['mbn_metadata_versions'] = (primary_metadata_versions.supported_mbn_metadata_versions.value, primary_metadata_versions.default_mbn_metadata_version)
        if primary_common_metadata_versions = primary_format_copy.mbn_properties.mbn_common_metadata_versions:
            metadata['mbn_common_metadata_versions'] = (primary_common_metadata_versions.supported_mbn_common_metadata_versions.value, primary_common_metadata_versions.default_mbn_common_metadata_version)
        if metadata:
            primary_format_copy.mbn_properties = resolve_default_and_supported_valued_features(metadata, primary_format_copy.mbn_properties, secondary_format.mbn_properties, schema_member['mbn_properties'])
        return primary_format_copy
    for image_format in (None, secondary_format):
        verify_profile_elements(filter_elements(vars(image_format.elf_properties)), schema_member['elf_properties'].keys(), f'''elf_properties for image format {image_format.id}''', 'resolve_image_format')
        verify_profile_elements(filter_elements(vars(image_format.elf_properties.elf_class)), schema_member['elf_properties']['elf_class'].keys(), f'''elf_class in the elf_properties for image format {image_format.id}''', 'resolve_image_format')
    primary_format_classes = primary_format_copy.elf_properties.elf_class.supported_elf_classes.value
    secondary_format_classes = secondary_format.elf_properties.elf_class.supported_elf_classes.value
    primary_default_class = primary_format_copy.elf_properties.elf_class.default_elf_class
    secondary_default_class = secondary_format.elf_properties.elf_class.default_elf_class
    (primary_format_copy.elf_properties.elf_class.supported_elf_classes.value, primary_format_copy.elf_properties.elf_class.default_elf_class) = resolve_default_and_supported_values(primary_format_classes, secondary_format_classes, primary_default_class, secondary_default_class, 'elf_class')
    primary_format_copy.elf_properties.load_segment_filesz_multiple = resolve_alignment(primary_format_copy.elf_properties, secondary_format.elf_properties, 'load_segment_filesz_multiple', f'''load_segment_filesz_multiple for image format with id {primary_format_copy.id}''')
    if primary_format_copy.hash_table_segment_properties:
        for image_format in (primary_format_copy, secondary_format):
            verify_profile_elements(filter_elements(vars(image_format.hash_table_segment_properties)), schema_member['hash_table_segment_properties'].keys(), f'''hash_table_segment_properties for image format {image_format.id}''', 'resolve_image_format')
        for feature in ('hash_table_segment_version', 'hash_pages'):
            if getattr(primary_format_copy.hash_table_segment_properties, feature) != getattr(secondary_format.hash_table_segment_properties, feature):
                raise RuntimeError(f'''{error} {feature} for image format with id {primary_format_copy.id}.''')
            primary_format_copy.hash_table_segment_properties.hash_table_segment_alignment = resolve_alignment(primary_format_copy.hash_table_segment_properties, secondary_format.hash_table_segment_properties, 'hash_table_segment_alignment', f'''hash_table_segment_alignment for image format with id {primary_format_copy.id}''')
            hash_algorithms = primary_format_copy.hash_table_segment_properties.segment_hash_algorithms
            placements = primary_format_copy.hash_table_segment_properties.hash_table_segment_placements
            segment_properties = {
                'segment_hash_algorithms': (hash_algorithms.supported_segment_hash_algorithms.value, hash_algorithms.default_segment_hash_algorithm),
                'hash_table_segment_placements': (placements.supported_hash_table_segment_placements.value, placements.default_hash_table_segment_placement) }
            if metadata_versions = primary_format_copy.hash_table_segment_properties.hash_table_segment_metadata_versions:
                segment_properties['hash_table_segment_metadata_versions'] = (metadata_versions.supported_hash_table_segment_metadata_versions.value, metadata_versions.default_hash_table_segment_metadata_version)
        if common_metadata_versions = primary_format_copy.hash_table_segment_properties.hash_table_segment_common_metadata_versions:
            segment_properties['hash_table_segment_common_metadata_versions'] = (common_metadata_versions.supported_hash_table_segment_common_metadata_versions.value, common_metadata_versions.default_hash_table_segment_common_metadata_version)
        primary_properties = primary_format_copy.hash_table_segment_properties
        secondary_properties = secondary_format.hash_table_segment_properties
        properties_string = 'hash_table_segment_properties'
        primary_format_copy.hash_table_segment_properties = resolve_default_and_supported_valued_features(segment_properties, primary_properties, secondary_properties, schema_member[properties_string])
    if primary_format_copy.vouch_segment_properties:
        for image_format in (primary_format_copy, secondary_format):
            verify_profile_elements(filter_elements(vars(image_format.vouch_segment_properties)), schema_member['vouch_segment_properties'].keys(), f'''vouch_segment_properties for image format {image_format.id}''', 'resolve_image_format')
        image_format_string = f'''image format with id {primary_format_copy.id}'''
        if primary_format_copy.vouch_segment_properties.vouch_segment_version != secondary_format.vouch_segment_properties.vouch_segment_version:
            raise RuntimeError(f'''{error} vouch_segment_version for {image_format_string}.''')
        primary_format_copy.vouch_segment_properties.phy_addr = primary_format_copy.hash_table_segment_properties.hash_table_segment_common_metadata_versions(primary_format_copy.vouch_segment_properties.phy_addr, secondary_format.vouch_segment_properties.phy_addr, f'''vouch_segment_properties of {image_format_string}''')
        primary_format_copy.vouch_segment_properties.vouch_segment_alignment = resolve_alignment(primary_format_copy.vouch_segment_properties, secondary_format.vouch_segment_properties, 'vouch_segment_alignment', f'''vouch_segment_alignment for image format with id {primary_format_copy.id}''')
        primary_format_copy.vouch_segment_properties.max_entry_count = min(primary_format_copy.vouch_segment_properties.max_entry_count, secondary_format.vouch_segment_properties.max_entry_count)
        hash_algorithms = primary_format_copy.vouch_segment_properties.vouch_segment_hash_algorithms
        placements = primary_format_copy.vouch_segment_properties.vouch_segment_placements
        segment_properties = {
            'vouch_segment_hash_algorithms': (hash_algorithms.supported_vouch_segment_hash_algorithms.value, hash_algorithms.default_vouch_segment_hash_algorithm),
            'vouch_segment_placements': (placements.supported_vouch_segment_placements.value, placements.default_vouch_segment_placement) }
        primary_properties = primary_format_copy.vouch_segment_properties
        secondary_properties = secondary_format.vouch_segment_properties
        properties_string = 'vouch_segment_properties'
        primary_format_copy.vouch_segment_properties = resolve_default_and_supported_valued_features(segment_properties, primary_properties, secondary_properties, schema_member[properties_string])
    if primary_format_copy.license_manager_segment_properties:
        for image_format in (primary_format_copy, secondary_format):
            verify_profile_elements(filter_elements(vars(image_format.license_manager_segment_properties)), schema_member['license_manager_segment_properties'].keys(), f'''license_manager_segment_properties for image format {image_format.id}''', 'resolve_image_format')
        if primary_format_copy.license_manager_segment_properties.license_manager_segment_version != secondary_format.license_manager_segment_properties.license_manager_segment_version:
            raise RuntimeError(f'''{error} license_manager_segment_version for image format with id {primary_format_copy.id}.''')
        primary_format_copy.license_manager_segment_properties.license_manager_segment_alignment = primary_format_copy.hash_table_segment_properties.hash_table_segment_metadata_versions(primary_format_copy.license_manager_segment_properties, secondary_format.license_manager_segment_properties, 'license_manager_segment_alignment', f'''license_manager_segment_alignment for image format with id {primary_format_copy.id}''')
        placements = primary_format_copy.license_manager_segment_properties.license_manager_segment_placements
        segment_properties = {
            'license_manager_segment_placements': (placements.supported_license_manager_segment_placements.value, placements.default_license_manager_segment_placement) }
        primary_properties = primary_format_copy.license_manager_segment_properties
        secondary_properties = secondary_format.license_manager_segment_properties
        properties_string = 'license_manager_segment_properties'
        primary_format_copy.license_manager_segment_properties = resolve_default_and_supported_valued_features(segment_properties, primary_properties, secondary_properties, schema_member[properties_string])
    return primary_format_copy


def resolve_supported_signing_features(authenticators = None, authority = None, schema_member = None):
    authority_signing_features_string = f'''supported_{authority.lower()}_signing_features'''
    error_string = f'''Security Profiles provided via {SECURITY_PROFILE} do not have a common value for'''
    if not (authority == AUTHORITY_OEM or authenticators[0].supported_oem_signing_features or authority == AUTHORITY_QTI) and authenticators[0].supported_qti_signing_features:
        raise RuntimeError(f'''Security Profiles provided via {SECURITY_PROFILE} must specify {authority} signing features for the hash or sign  operation.''')
    resolved_signing_features = None(authenticators[0], authority_signing_features_string)
    verify_profile_elements(filter_elements(vars(resolved_signing_features)), schema_member.keys(), f'''{authority_signing_features_string}''', 'resolve_supported_signing_features')
    serial_bound_features = {
        'serial_bind': resolved_signing_features.serial_bind,
        'debug': resolved_signing_features.debug,
        'uie_key_switch_enable': resolved_signing_features.uie_key_switch_enable,
        'root_revoke_activation_enable': resolved_signing_features.root_revoke_activation_enable,
        'crash_dump': resolved_signing_features.crash_dump }
    boolean_features = {
        'supports_vouch_for': resolved_signing_features.supports_vouch_for,
        'supports_root_revoke_activation_enable_as_combined': resolved_signing_features.supports_root_revoke_activation_enable_as_combined,
        'supports_oem_id_product_id_independent': resolved_signing_features.supports_oem_id_product_id_independent,
        'supports_anti_rollback_version': resolved_signing_features.supports_anti_rollback_version,
        'requires_secondary_software_id': resolved_signing_features.requires_secondary_software_id,
        'requires_feature_id': resolved_signing_features.requires_feature_id }
    enumeration_features_strings = [
        'supported_measurement_register_targets',
        'supported_soc_lifecycle_states',
        'supported_oem_lifecycle_states']
    enumeration_features = { }
    for enumeration_features_string in enumeration_features_strings:
        enumeration_features[enumeration_features_string] = getattr(resolved_signing_features, enumeration_features_string).value if getattr(resolved_signing_features, enumeration_features_string) else None
    default_and_supported_valued_features = {
        'certificate_chain_depths': (resolved_signing_features.certificate_chain_depths.supported_certificate_chain_depths.value, resolved_signing_features.certificate_chain_depths.default_certificate_chain_depth) }
    if resolved_signing_features.mrc_specs:
        default_and_supported_valued_features['mrc_specs'] = (resolved_signing_features.mrc_specs.supported_mrc_specs.value, resolved_signing_features.mrc_specs.default_mrc_spec)
    if resolved_signing_features.root_certificate_hash_algorithms:
        default_and_supported_valued_features['root_certificate_hash_algorithms'] = (resolved_signing_features.root_certificate_hash_algorithms.supported_root_certificate_hash_algorithms.value, resolved_signing_features.root_certificate_hash_algorithms.default_root_certificate_hash_algorithm)
    for authenticator in authenticators[1:]:
        if not (authority == AUTHORITY_OEM or authenticator.supported_oem_signing_features or authority == AUTHORITY_QTI) and authenticator.supported_qti_signing_features:
            raise RuntimeError(f'''Security Profiles provided via {SECURITY_PROFILE} must specify {authority} signing features for the hash or sign operation.''')
        signing_features = None(authenticator, authority_signing_features_string)
        error_information = f'''{authority_signing_features_string} for authenticator {authenticator.id}'''
        verify_profile_elements(filter_elements(vars(signing_features)), schema_member.keys(), error_information, 'resolve_supported_signing_features')
        for feature, feature_object in boolean_features.items():
            signing_features_bool = getattr(signing_features, feature)
            if feature_object:
                pass
            boolean_features[feature] = signing_features_bool
            setattr(resolved_signing_features, feature, boolean_features[feature])
        for feature, feature_object in serial_bound_features.items():
            verify_profile_elements(filter_elements(getattr(signing_features, feature).__dict__), schema_member[feature].keys(), f'''{feature} of the {error_information}''', 'resolve_supported_signing_features')
            if feature_object.supported:
                pass
            feature_object.supported = getattr(signing_features, feature).supported
            getattr(resolved_signing_features, feature).supported = feature_object.supported
            if feature_object.supports_single_serial:
                pass
            feature_object.supports_single_serial = getattr(signing_features, feature).supports_single_serial
            getattr(resolved_signing_features, feature).supports_single_serial = feature_object.supports_single_serial
            if feature_object.supports_multi_serials:
                pass
            feature_object.supports_multi_serials = getattr(signing_features, feature).supports_multi_serials
            getattr(resolved_signing_features, feature).supports_multi_serials = feature_object.supports_multi_serials
        for feature, feature_object in enumeration_features.items():
            if feature_object and getattr(signing_features, feature):
                verify_profile_elements(filter_elements(vars(getattr(signing_features, feature))), schema_member[feature].keys(), f'''{feature} of the {error_information}''', 'resolve_supported_signing_features')
                feature_object = get_intersection(feature_object, getattr(signing_features, feature).value)
                if not feature_object:
                    raise RuntimeError(f'''{error_string} {feature}.''')
                getattr(resolved_signing_features, feature).value = None
        if resolved_signing_features.platform_bindings.supports_multiple_soc_ver:
            pass
        resolved_signing_features.platform_bindings.supports_multiple_soc_ver = signing_features.platform_bindings.supports_multiple_soc_ver
        resolved_signing_features.platform_bindings.supported_platform_bindings.value = get_intersection(resolved_signing_features.platform_bindings.supported_platform_bindings.value, signing_features.platform_bindings.supported_platform_bindings.value)
        if not resolved_signing_features.platform_bindings.supported_platform_bindings.value:
            raise RuntimeError(f'''{error_string} supported_platform_bindings.''')
        resolved_signing_features.platform_bindings.default_platform_bindings.value = None(resolved_signing_features.platform_bindings.default_platform_bindings.value, signing_features.platform_bindings.default_platform_bindings.value)
        if not resolved_signing_features.platform_bindings.default_platform_bindings.value:
            resolved_signing_features.platform_bindings.default_platform_bindings.value = [
                sorted(resolved_signing_features.platform_bindings.supported_platform_bindings.value)[0]]
        if resolved_signing_features.mrc_specs and signing_features.mrc_specs:
            default_and_supported_valued_features['mrc_specs'] = (resolved_signing_features.mrc_specs.supported_mrc_specs.value, resolved_signing_features.mrc_specs.default_mrc_spec)
        else:
            resolved_signing_features.mrc_specs = None
        if resolved_signing_features.root_certificate_hash_algorithms and signing_features.root_certificate_hash_algorithms:
            default_and_supported_valued_features['root_certificate_hash_algorithms'] = (resolved_signing_features.root_certificate_hash_algorithms.supported_root_certificate_hash_algorithms.value, resolved_signing_features.root_certificate_hash_algorithms.default_root_certificate_hash_algorithm)
        else:
            resolved_signing_features.root_certificate_hash_algorithms = None
        for profile_member in default_and_supported_valued_features:
            if getattr(signing_features, profile_member):
                verify_profile_elements(filter_elements(vars(getattr(signing_features, profile_member))), schema_member[profile_member].keys(), f'''{profile_member} of the {error_information}''', 'resolve_supported_signing_features')
        resolved_signing_features = resolve_default_and_supported_valued_features(default_and_supported_valued_features, resolved_signing_features, signing_features, schema_member)
        resolved_signing_features.signature_formats.signature_format = resolve_signature_formats(resolved_signing_features.signature_formats, signing_features.signature_formats, authority_signing_features_string, schema_member['signature_formats'])
        signature_formats_ids = []
        default_signature_format = resolved_signing_features.default_signature_format
        for signature_format in resolved_signing_features.signature_formats.signature_format:
            signature_formats_ids.append(signature_format.id)
        if default_signature_format not in signature_formats_ids:
            resolved_signing_features.default_signature_format = resolved_signing_features.signature_formats.signature_format[0].id
    return resolved_signing_features


def resolve_signature_formats(primary_signature_formats = None, secondary_signature_formats = None, authority_signing_features_string = None, schema_member = ('primary_signature_formats', SignatureFormats, 'secondary_signature_formats', SignatureFormats, 'authority_signing_features_string', str, 'schema_member', dict[(str, dict)], 'return', list[SignatureFormat])):
    common_signature_format_found = False
    resolved_signature_formats = []
# WARNING: Decompyle incomplete


def resolve_signature_format(primary_format = None, secondary_format = None, schema_member = None):
    default_and_supported_valued_features = {
        'signature_hash_algorithms': (primary_format.signature_hash_algorithms.supported_signature_hash_algorithms.value, primary_format.signature_hash_algorithms.default_signature_hash_algorithm) }
    if primary_format.signature_algorithm == ALGORITHM_ECDSA_USER_FACING:
        default_and_supported_valued_features |= {
            'ecdsa_curves': (primary_format.ecdsa_curves.supported_ecdsa_curves.value, primary_format.ecdsa_curves.default_ecdsa_curve) }
    elif primary_format.signature_algorithm == ALGORITHM_RSA_USER_FACING:
        default_and_supported_valued_features |= {
            'exponents': (primary_format.exponents.supported_exponents.value, primary_format.exponents.default_exponent),
            'key_sizes': (primary_format.key_sizes.supported_key_sizes.value, primary_format.key_sizes.default_key_size),
            'rsa_paddings': (primary_format.rsa_paddings.supported_rsa_paddings.value, primary_format.rsa_paddings.default_rsa_padding) }
    for signature_format in (primary_format, secondary_format):
        verify_profile_elements(filter_elements(vars(signature_format)), schema_member.keys(), f'''Signature format {signature_format.id}''', 'resolve_signature_format')
        for profile_member in default_and_supported_valued_features:
            verify_profile_elements(filter_elements(vars(getattr(signature_format, profile_member))), schema_member[profile_member].keys(), f'''{profile_member} in signature format {signature_format.id}''', 'resolve_signature_format')
    primary_format = resolve_default_and_supported_valued_features(default_and_supported_valued_features, primary_format, secondary_format, schema_member)
    return primary_format


def resolve_supported_encryption_features(authenticators = None, authority = None, schema_member = None):
    authority_encryption_features_string = f'''supported_{authority.lower()}_encryption_features'''
    resolved_encryption_features = getattr(authenticators[0], authority_encryption_features_string)
    for authenticator in authenticators[1:]:
        encryption_features = getattr(authenticator, authority_encryption_features_string)
        if not encryption_features:
            raise RuntimeError(f'''Security Profiles provided via {SECURITY_PROFILE} do not support {authority} encryption.''')
        None(filter_elements(vars(resolved_encryption_features)), schema_member.keys(), f'''{authority_encryption_features_string} for authenticator {authenticator.id}''', 'resolve_supported_encryption_features')
        resolved_encryption_features.supported_encryption_formats.encryption_format = resolve_encryption_formats(resolved_encryption_features.supported_encryption_formats, encryption_features.supported_encryption_formats, authority_encryption_features_string, schema_member['supported_encryption_formats'])
        default_encryption_format = resolved_encryption_features.default_encryption_format
        encryption_formats_ids = (lambda .0: [ encryption_format.id for encryption_format in .0 ])(resolved_encryption_features.supported_encryption_formats.encryption_format)
        if default_encryption_format not in encryption_formats_ids:
            resolved_encryption_features.default_encryption_format = resolved_encryption_features.supported_encryption_formats.encryption_format[0].id
    return resolved_encryption_features


def resolve_encryption_formats(primary_encryption_formats = None, secondary_encryption_formats = None, authority_encryption_features_string = None, schema_member = ('primary_encryption_formats', SupportedEncryptionFormats, 'secondary_encryption_formats', SupportedEncryptionFormats, 'authority_encryption_features_string', str, 'schema_member', dict[(str, dict)], 'return', list[EncryptionFormat])):
    common_encryption_format_found = False
    resolved_encryption_formats = []
    for None in secondary_encryption_formats.encryption_format:
        secondary_encryption_format = None
# WARNING: Decompyle incomplete


def resolve_tme_elf_properties(elf_properties = None, schema_member = None):
    primary_elf_properties = elf_properties[0]
    verify_profile_elements(filter_elements(vars(primary_elf_properties)), schema_member.keys(), 'tme_elf_properties', 'resolve_tme_elf_properties')
    verify_profile_elements(filter_elements(vars(primary_elf_properties.elf_classes)), schema_member['elf_classes'].keys(), 'elf_classes in the tme_elf_properties', 'resolve_tme_elf_properties')
    for secondary_elf_properties in elf_properties[1:]:
        verify_profile_elements(filter_elements(vars(secondary_elf_properties)), schema_member.keys(), 'tme_elf_properties', 'resolve_tme_elf_properties')
        verify_profile_elements(filter_elements(vars(secondary_elf_properties.elf_classes)), schema_member['elf_classes'].keys(), 'elf_classes in the tme_elf_properties', 'resolve_tme_elf_properties')
        primary_elf_properties.phy_addr = resolve_phy_addr(primary_elf_properties.phy_addr, secondary_elf_properties.phy_addr, 'tme_elf_properties')
        primary_format_classes = primary_elf_properties.elf_classes.supported_elf_classes.value
        secondary_format_classes = secondary_elf_properties.elf_classes.supported_elf_classes.value
        primary_default_class = primary_elf_properties.elf_classes.default_elf_class
        secondary_default_class = secondary_elf_properties.elf_classes.default_elf_class
        (primary_elf_properties.elf_classes.supported_elf_classes.value, primary_elf_properties.elf_classes.default_elf_class) = resolve_default_and_supported_values(primary_format_classes, secondary_format_classes, primary_default_class, secondary_default_class, 'tme_elf_properties elf_class')
        primary_elf_properties.dpr_segment_alignment = resolve_alignment(primary_elf_properties, secondary_elf_properties, 'dpr_segment_alignment', 'dpr_segment_alignment')
    return primary_elf_properties


def get_intersection(primary_list = None, secondary_list = None):
    if ANY in primary_list and ANY not in secondary_list:
        intersection = secondary_list
        return intersection
    if None in secondary_list and ANY not in primary_list:
        intersection = primary_list
        return intersection
    intersection = None(set(primary_list) & set(secondary_list))
    return intersection


def resolve_default_and_supported_values(primary_supported_values, secondary_supported_values = None, primary_default = None, secondary_default = None, feature = ('primary_supported_values', list[str], 'secondary_supported_values', list[str], 'primary_default', str, 'secondary_default', str, 'feature', str, 'return', tuple[(list[str], str)])):
    error = f'''Security Profiles provided via {SECURITY_PROFILE} do not have a common value for'''
    primary_supported_values = get_intersection(primary_supported_values, secondary_supported_values)
    if not primary_supported_values:
        raise RuntimeError(f'''{error} {feature}.''')
    if None != secondary_default:
        primary_default = primary_supported_values[0]
    return (primary_supported_values, primary_default)


def resolve_default_and_supported_valued_features(default_and_supported_valued_features = None, primary_format = None, secondary_format = None, schema_member = ('default_and_supported_valued_features', DictToResolve, 'primary_format', FormatToResolve, 'secondary_format', FormatToResolve, 'schema_member', dict[(str, dict)], 'return', FormatToResolve)):
    for supported_values, default_value in default_and_supported_valued_features.items():
        for member_format in (primary_format, secondary_format):
            if getattr(member_format, feature):
                verify_profile_elements(filter_elements(vars(getattr(member_format, feature))), schema_member[feature].keys(), feature, 'resolve_default_and_supported_valued_features')
        if getattr(primary_format, feature):
            supported_feature = 'supported_' + feature
            secondary_supported_values = getattr(getattr(secondary_format, feature), supported_feature).value
            secondary_default_value = getattr(getattr(secondary_format, feature), 'default_' + feature[:-1])
            default_and_supported_valued_features[feature] = resolve_default_and_supported_values(supported_values, secondary_supported_values, default_value, secondary_default_value, supported_feature)
            getattr(getattr(primary_format, feature), supported_feature).value = default_and_supported_valued_features[feature][0]
            setattr(getattr(primary_format, feature), 'default_' + feature[:-1], default_and_supported_valued_features[feature][1])
    return primary_format


def resolve_image_formats_from_image_list(image_entries = None, authenticator_entries = None, schema_member = None):
    verify_profile_elements(filter_elements(vars(image_entries[0])), schema_member['image'], f'''Image entry {image_entries[0].id}''', 'resolve_image_formats_from_image_list')
    schema_authenticator = SCHEMA_STRUCTURE['profile']['authentication']['authenticators']['authenticator']
    schema_image_format = schema_authenticator['supported_image_formats']['image_format']
    primary_image_format = None
    processed_idx = None
    error = f'''Cannot resolve image format for {IMAGE_ID} {image_entries[0].id}.'''
    for idx, image_entry in enumerate(image_entries):
        if image_entry.image_format:
            for image_format in authenticator_entries[idx].supported_image_formats.image_format:
                if image_entry.image_format == image_format.id:
                    primary_image_format = image_format
                
                processed_idx = idx
# WARNING: Decompyle incomplete


def resolve_image_entries_from_image_list(image_entries = None, schema_member = None, resolving_multi_image = None):
    verify_profile_elements(filter_elements(vars(image_entries[0])), schema_member['image'], f'''Image entry {image_entries[0].id}''', 'resolve_image_entries_from_image_list')
    sw_id = int(image_entries[0].sw_id, 16)
    authenticator_oem = bool(image_entries[0].authenticator_oem)
    authenticator_qti = bool(image_entries[0].authenticator_qti)
    compression_format = image_entries[0].compression_format
    qti_vouch_for_disallowed = image_entries[0].qti_vouch_for_disallowed
    oem_vouch_for_disallowed = image_entries[0].oem_vouch_for_disallowed
    for idx, image in enumerate(image_entries[1:]):
        verify_profile_elements(filter_elements(vars(image)), schema_member['image'], f'''Image entry {image.id}''', 'resolve_image_entries_from_image_list')
        if int(image.sw_id, 16) != sw_id:
            id_string = 'Multi Image' if resolving_multi_image else f'''{IMAGE_ID} {image.id}'''
            raise RuntimeError(f'''Software ID for {id_string} must be identical across all Security Profiles provided via {SECURITY_PROFILE}.''')
        if None != bool(image.authenticator_oem) or authenticator_qti != bool(image.authenticator_qti):
            raise RuntimeError(f'''Cannot authenticate with {IMAGE_ID} {image.id}''')
        if None.compression_format or image.compression_format != compression_format:
            image_entries[0].compression_format = None
        if not image.qti_vouch_for_disallowed is None or qti_vouch_for_disallowed is None:
            image_entries[0].qti_vouch_for_disallowed = ''
        if not image.oem_vouch_for_disallowed is None or oem_vouch_for_disallowed is None:
            image_entries[0].oem_vouch_for_disallowed = ''

