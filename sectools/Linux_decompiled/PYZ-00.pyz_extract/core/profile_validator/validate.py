
from io import StringIO
from operator import attrgetter
from typing import Any
from cmd_line_interface.sectools.cmd_line_common.defines import INDEPENDENT, MEASUREMENT_REGISTER_TARGETS, OEM_LIFECYCLE_STATES, PLATFORM_BINDINGS, PRODUCT_SEGMENT_ID, SEGMENT_HASH_ALGORITHMS, SOC_FEATURE_ID, SOC_LIFECYCLE_STATES
from cmd_line_interface.sectools.fuseblower.dynamic_arguments import compute_and_validate_multi_row_fuses
from cmd_line_interface.sectools.secure_image.defines import ROOT_KEY_TYPES
from common.crypto.openssl.defines import ALGORITHM_ECDSA_USER_FACING, ALGORITHM_RSA_USER_FACING, CERTIFICATE_CHAIN_DEPTHS, CURVE_SECP384R1, CURVE_SECP384R1_RS_48_49, PQC_SIGNATURE_ALGORITHMS, RS_48_49, SUPPORTED_SIGNATURE_ALGORITHMS
from common.data.data import a_or_an, and_separated, are_or_is, hex_val, or_separated, plural_s
from common.data.defines import NON_ZI_HASH_ALGORITHMS
from common.logging.logger import log_warning
from common.parser.debug_policy_elf.defines import SUPPORTED_DEBUG_POLICY_VERSIONS
from common.parser.defines import COMPRESSION_FORMATS
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import DATA_ENCRYPTION_SCHEME_DESCRIPTION_TO_ID, KEY_MANAGEMENT_FEATURE_DESCRIPTION_TO_ID, KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID, QBEC_VERSIONS, GCM_GCM, WRAPPED_KEY_POLICY_HEX_LEN
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI, HASH_SEGMENT_V3, HASH_SEGMENT_V5, HASH_SEGMENT_V6, HASH_SEGMENT_V7, MRC_3_0
from common.parser.multi_image.defines import MULTI_IMAGE
from common.parser.sec_dat.defines import SECDAT_VERSION_TO_REGIONS, SECDAT_VERSION_TO_REGION_TYPE_SPREADSHEET, SEC_DAT_SUPPORTED_VERSIONS, SEC_DAT_VERSION_2
from common.parser.sec_dat.sec_dat_segment import FUSE_HEADER_CLASSES
from common.parser.tme.tme_parser.grammar import TMEGrammarException, TME_GRAMMAR_VERSIONS
from common.parser.tme.tme_parser.tme import get_selections_for_tag, get_selections_for_tag_extended, validate_tag_grammar
from core.fuse_blower.defines import FEC_FUSE_SIZE
from core.fuse_blower.utils import get_start_and_end_indices, is_fec_fuse, is_multi_bit
from core.fuseblower_profile_generator.defines import OEM_VALUE_XML
from core.profile_validator.defines import COMMON_METADATA_0_1, COMMON_METADATA_VERSIONS, DEFAULT_SEGMENT_PLACEMENTS, ECDSA_CURVES, ELF_CLASSES, ENCRYPTION_ORDERS, ENCRYPTION_SPECS, ENCRYPTION_TYPES, FUSE_SEGMENTS_TYPE, HASH_ALGORITHMS, HASH_TABLE_SEGMENT_VERSIONS, LICENSE_MANAGER_SEGMENT_VERSIONS, MRC_SPECS, RSA_EXPONENTS, RSA_KEY_SIZES, RSA_PADDINGS, SUPPORTED_SEGMENT_PLACEMENTS, TME_COMMAND_VERSIONS, TME_SEQ_TEST_SIGNED_IMAGE_HASH_ALGORITHMS, UIE, V6_METADATA_VERSIONS, V7_METADATA_VERSIONS, V8_METADATA_VERSIONS, VOUCH_SEGMENT_VERSIONS
from core.tme_secure_debug.tme_signing_algorithm_details import tme_signing_algorithm_details
from profile.defines import ANY, SCHEMA_STRUCTURE
from profile.schema import EncryptionFeatures, HashTableSegmentProperties, Image, MBNProperties, SignatureFormat, SigningFeatures
from profile.schema.scale_profile import Profile
from profile.utils import filter_elements, verify_profile_elements
ERROR_STRING = 'Security Profile error: '

def _validate_unique_ids(ids = None, id_string = None):
    if repeated_ids = (lambda .0 = None: [ i for idx, i in .0 if i in ids[:idx] ])(enumerate(ids)):
        raise RuntimeError(f'''{ERROR_STRING}{id_string} must be unique within Security Profile. {and_separated(repeated_ids)} {are_or_is(repeated_ids)} repeated.''')
    return (lambda .0 = None: [ i for idx, i in .0 if i in ids[:idx] ])(enumerate(ids))


def _validate_unique_feature_entries(feature_descriptions = None, feature_description_string = None, object_string = None):
    unique = False
    primary_buffer = StringIO()
    secondary_buffer = StringIO()
    if len(feature_descriptions) > 1:
        for idx, feature_description in enumerate(feature_descriptions[:-1]):
            for other_feature_description in feature_descriptions[idx + 1:]:
                for member in filter_elements(vars(feature_description)):
                    if member != 'id':
                        primary_object = getattr(feature_description, member)
                        secondary_object = getattr(other_feature_description, member)
                        if bool(primary_object) != bool(secondary_object):
                            unique = True
                            continue
                        if primary_object and secondary_object:
                            if callable(getattr(primary_object, 'export', None)) and callable(getattr(secondary_object, 'export', None)):
                                primary_object.export(primary_buffer, 0, '', **('namespacedef_',))
                                secondary_object.export(secondary_buffer, 0, '', **('namespacedef_',))
                                if primary_buffer.getvalue() != secondary_buffer.getvalue():
                                    unique = True
                                continue
                            if getattr(feature_description, member) != getattr(other_feature_description, member):
                                unique = True
                if not unique:
                    raise RuntimeError(f'''{ERROR_STRING}{feature_description_string} must be unique within {object_string}.''')
                return None
                return None


def _validate_default_and_supported_values(feature_object, feature_string, format_object_string = None, authenticator = None, schema_member = None, feature_string_suffix_len = (None, None, 1, None), schema_enums = ('feature_object', Any, 'feature_string', str, 'format_object_string', str, 'authenticator', str | None, 'schema_member', dict[(str, dict)] | None, 'feature_string_suffix_len', int, 'schema_enums', Any | None, 'return', None)):
    feature_string_default = 'default_' + feature_string[:-feature_string_suffix_len]
    feature_string_supported = 'supported_' + feature_string
    supported_values = set(getattr(feature_object, feature_string_supported).value) - {
        'NONE'}
    authenticator_string = f''' in authenticator {authenticator}''' if authenticator else ''
    if schema_enums:
        _validate_value_supported(supported_values, schema_enums, f'''{feature_string} of {format_object_string}{authenticator_string}''')
    if ANY in supported_values:
        if len(supported_values) > 1:
            supported_values.remove(ANY)
            list_string = and_separated(list(supported_values))
            error_prefix = f'''More restrictive values, {list_string}, are''' if len(supported_values) > 1 else f'''A more restrictive value, {list_string}, is'''
            raise RuntimeError(f'''{ERROR_STRING}{error_prefix} listed as supported for {feature_string} in addition to {ANY}. A more specific value cannot be listed alongside {ANY}.''')
    if getattr(feature_object, feature_string_default) not in supported_values:
        raise RuntimeError(f'''{ERROR_STRING}The {feature_string_default} of {format_object_string}{authenticator_string} is missing from the {feature_string_supported}.''')
# WARNING: Decompyle incomplete


def _validate_value_supported(profile_values = None, schema_enums = None, information_string = None):
    if disallowed_values = sorted(set(profile_values) - set(schema_enums)):
        raise RuntimeError(f'''{ERROR_STRING}{information_string} contains unsupported value{plural_s(disallowed_values)}, {and_separated(disallowed_values)}. Supported value{plural_s(schema_enums)} {are_or_is(schema_enums)}: {and_separated(schema_enums)}.''')
    return sorted(set(profile_values) - set(schema_enums))


def _validate_mbn_or_hash_table_segment_properties(properties, image_type_string = None, image_id_string = None, authenticator_id = None, schema_member = ('properties', HashTableSegmentProperties | MBNProperties, 'image_type_string', str, 'image_id_string', str, 'authenticator_id', str, 'schema_member', dict[(str, dict)], 'return', None)):
    if image_type_string == 'MBN':
        version_string = 'mbn_version'
        metadata_versions_string = 'mbn_metadata_versions'
        common_metadata_versions_string = 'mbn_common_metadata_versions'
    else:
        version_string = 'hash_table_segment_version'
        metadata_versions_string = 'hash_table_segment_metadata_versions'
        common_metadata_versions_string = 'hash_table_segment_common_metadata_versions'
    schema_metadata_element = schema_member[metadata_versions_string]
    schema_common_metadata_element = schema_member[common_metadata_versions_string]
    metadata_versions = getattr(properties, metadata_versions_string, None)
    common_metadata_versions = getattr(properties, common_metadata_versions_string, None)
    if version = getattr(properties, version_string) not in HASH_TABLE_SEGMENT_VERSIONS:
        raise RuntimeError(f'''{ERROR_STRING}{version_string} of {image_id_string} in authenticator {authenticator_id} contains unsupported value, {version}. Supported values are: {and_separated(HASH_TABLE_SEGMENT_VERSIONS)}.''')
    if getattr(properties, version_string) in (HASH_SEGMENT_V3, HASH_SEGMENT_V5):
        if any([
            common_metadata_versions,
            metadata_versions]):
            raise RuntimeError(f'''{ERROR_STRING}image_format describing a v{version} {image_type_string} in authenticator {authenticator_id} cannot contain {metadata_versions_string} or {common_metadata_versions_string}.''')
    if version == HASH_SEGMENT_V6:
        error_prefix = f'''image_format describing a v6 {image_type_string} in authenticator {authenticator_id}'''
        if metadata_versions:
            _validate_default_and_supported_values(metadata_versions, metadata_versions_string, image_id_string, authenticator_id, schema_metadata_element, V6_METADATA_VERSIONS, **('schema_enums',))
        else:
            raise RuntimeError(f'''{ERROR_STRING}{error_prefix} must contain {metadata_versions_string}.''')
        if None:
            raise RuntimeError(f'''{ERROR_STRING}{error_prefix} cannot contain {common_metadata_versions_string}.''')
        None(filter_elements(vars(metadata_versions)), schema_metadata_element, f'''{metadata_versions_string} of {error_prefix}''', '_validate_mbn_or_hash_table_segment_properties')
    elif version == HASH_SEGMENT_V7:
        pass
    
    error_prefix = f'''v7{'v8'} {image_type_string} in authenticator {authenticator_id}'''
    if not common_metadata_versions:
        raise RuntimeError(f'''{ERROR_STRING}{error_prefix} must contain {common_metadata_versions_string}.''')
    'image_format describing a '(common_metadata_versions, common_metadata_versions_string, image_id_string, authenticator_id, schema_common_metadata_element, COMMON_METADATA_VERSIONS, **('schema_enums',))
    if metadata_versions:
        _validate_default_and_supported_values(metadata_versions, metadata_versions_string, image_id_string, authenticator_id, schema_metadata_element, V7_METADATA_VERSIONS if version == HASH_SEGMENT_V7 else V8_METADATA_VERSIONS, **('schema_enums',))
    else:
        raise RuntimeError(f'''{ERROR_STRING}{error_prefix} must contain {metadata_versions_string}.''')
    v7_v8_elements = [
        (None, schema_metadata_element, metadata_versions_string),
        (common_metadata_versions, schema_common_metadata_element, common_metadata_versions_string)]
    for element_profile, element_schema, metadata_string in v7_v8_elements:
        if element_profile:
            verify_profile_elements(filter_elements(vars(element_profile)), element_schema, f'''{metadata_string} of {error_prefix}''', '_validate_mbn_or_hash_table_segment_properties')
    if image_type_string == 'Hash Table Segment':
        common_metadatas = common_metadata_versions.supported_hash_table_segment_common_metadata_versions.value
        if COMMON_METADATA_0_1 not in common_metadatas:
            unsupported_algos = set(properties.segment_hash_algorithms.supported_segment_hash_algorithms.value) - set(NON_ZI_HASH_ALGORITHMS)
            if unsupported_algos:
                raise RuntimeError(f'''{ERROR_STRING}{error_prefix} can only contain supported_segment_hash_algorithms {and_separated(sorted(unsupported_algos))} when supported_hash_table_segment_common_metadata_versions contains {COMMON_METADATA_0_1}.''')
            if None < HASH_SEGMENT_V7 or image_type_string == 'Hash Table Segment':
                _validate_default_and_supported_values(properties.segment_hash_algorithms, 'segment_hash_algorithms', image_id_string, authenticator_id, schema_member['segment_hash_algorithms'], NON_ZI_HASH_ALGORITHMS, **('schema_enums',))
                return None
            return None
        return None


def _validate_signature_format_ecdsa(signature_format, error_message = None, schema_member = None, authenticator_id = None, information_string = ('signature_format', SignatureFormat, 'error_message', str, 'schema_member', dict[(str, dict)], 'authenticator_id', str, 'information_string', str, 'return', None)):
    if signature_format.key_sizes and signature_format.rsa_paddings or signature_format.exponents:
        raise RuntimeError(f'''{ERROR_STRING}{error_message} cannot contain key_sizes, rsa_paddings, or exponents.''')
    if not None.ecdsa_curves:
        raise RuntimeError(f'''{ERROR_STRING}{error_message} must contain ecdsa_curves.''')
    None(filter_elements(vars(getattr(signature_format, 'ecdsa_curves'))), schema_member['ecdsa_curves'].keys(), error_message, '_validate_signature_format')
    _validate_default_and_supported_values(getattr(signature_format, 'ecdsa_curves'), 'ecdsa_curves', f'''signature_format {signature_format.id}''', authenticator_id, schema_member['ecdsa_curves'], ECDSA_CURVES + [
        CURVE_SECP384R1_RS_48_49], **('schema_enums',))
    supported_ecdsa_curves = getattr(getattr(signature_format, 'ecdsa_curves'), 'supported_ecdsa_curves').value
    secp384r1_values = list(filter((lambda curve: CURVE_SECP384R1.upper() in curve), supported_ecdsa_curves))
    if not any((lambda .0: for curve in .0:
RS_48_49 in curve)(secp384r1_values)) or all((lambda .0: for curve in .0:
RS_48_49 in curve)(secp384r1_values)):
        raise RuntimeError(f'''supported_ecdsa_curves, {and_separated(supported_ecdsa_curves)}, of signature_format {signature_format.id} of {information_string} cannot contain a combination of RS-48-49 and non RS-48-49 values for ECDSA curve SECP384R1.''')
    return None


def _validate_signature_format_rsa(signature_format = None, error_message = None, schema_member = None, authenticator_id = ('signature_format', SignatureFormat, 'error_message', str, 'schema_member', dict[(str, dict)], 'authenticator_id', str, 'return', None)):
    if not signature_format.key_sizes and signature_format.rsa_paddings or signature_format.exponents:
        raise RuntimeError(f'''{ERROR_STRING}{error_message} must contain key_sizes, rsa_paddings, and exponents.''')
    if None.ecdsa_curves:
        raise RuntimeError(f'''{ERROR_STRING}{error_message} cannot contain ecdsa_curves.''')
    for feature, allowed_rsa_values in ((None, RSA_EXPONENTS), ('key_sizes', RSA_KEY_SIZES), ('rsa_paddings', RSA_PADDINGS)):
        verify_profile_elements(filter_elements(vars(getattr(signature_format, feature))), schema_member[feature].keys(), error_message, '_validate_signature_format')
        _validate_default_and_supported_values(getattr(signature_format, feature), feature, f'''signature_format {signature_format.id}''', authenticator_id, schema_member[feature], allowed_rsa_values, **('schema_enums',))


def _validate_signature_format(signature_formats, authenticator_id = None, authority = None, default_signature_format = None, schema_member = ('signature_formats', list[SignatureFormat], 'authenticator_id', str, 'authority', str, 'default_signature_format', str, 'schema_member', dict[(str, dict)], 'return', None)):
    valid_default = False
    signature_format_ids = []
    information_string = f'''supported_{authority.lower()}_signing_features for authenticator {authenticator_id}'''
    for signature_format in signature_formats:
        verify_profile_elements(filter_elements(vars(signature_format)), schema_member.keys(), f'''signature_format {signature_format.id} in the {information_string}''', '_validate_signature_format')
        signature_format_ids.append(signature_format.id)
        if default_signature_format == signature_format.id:
            valid_default = True
        if signature_format.signature_algorithm not in SUPPORTED_SIGNATURE_ALGORITHMS:
            raise RuntimeError(f'''{ERROR_STRING}signature_algorithm of the {information_string} contains unsupported value, {signature_format.signature_algorithm}. Supported values are: {and_separated(SUPPORTED_SIGNATURE_ALGORITHMS)}.''')
        signature_algorithm = None.signature_algorithm
        error_message = f'''signature_format with signature_algorithm {signature_algorithm} in the {information_string}'''
        feature = 'signature_hash_algorithms'
        verify_profile_elements(filter_elements(vars(getattr(signature_format, feature))), schema_member[feature].keys(), error_message, '_validate_signature_format')
        _validate_default_and_supported_values(getattr(signature_format, feature), feature, f'''signature_format {signature_format.id}''', authenticator_id, schema_member[feature], HASH_ALGORITHMS, **('schema_enums',))
        if signature_format.certificate_chain_depths_override:
            feature = 'certificate_chain_depths_override'
            verify_profile_elements(filter_elements(vars(getattr(signature_format, feature))), schema_member[feature].keys(), error_message, '_validate_signature_format')
            _validate_default_and_supported_values(getattr(signature_format, feature), 'certificate_chain_depths', f'''signature_format {signature_format.id}''', authenticator_id, schema_member[feature], CERTIFICATE_CHAIN_DEPTHS, **('schema_enums',))
        if signature_algorithm == ALGORITHM_ECDSA_USER_FACING:
            _validate_signature_format_ecdsa(signature_format, error_message, schema_member, authenticator_id, information_string)
        if signature_algorithm == ALGORITHM_RSA_USER_FACING:
            _validate_signature_format_rsa(signature_format, error_message, schema_member, authenticator_id)
        if signature_algorithm in PQC_SIGNATURE_ALGORITHMS:
            if signature_format.ecdsa_curves and signature_format.key_sizes and signature_format.rsa_paddings or signature_format.exponents:
                raise RuntimeError(f'''{ERROR_STRING}{error_message} cannot contain ecdsa_curves, key_sizes, rsa_paddings, or exponents.''')
            error = f'''Signature format IDs in the {information_string}'''
            _validate_unique_ids(signature_format_ids, error)
            _validate_unique_feature_entries(signature_formats, 'signature_formats', information_string)
            if not valid_default:
                raise RuntimeError(f'''{ERROR_STRING}The default_signature_format of the {information_string} is missing from the supported_signature_formats.''')
            return None


def _validate_signing_features(signing_features = None, signing_features_string = None, authenticator_id = None, schema_member = ('signing_features', SigningFeatures, 'signing_features_string', str, 'authenticator_id', str, 'schema_member', dict[(str, dict)], 'return', None)):
    information_string = f'''{signing_features_string} in authenticator {authenticator_id}'''
    verify_profile_elements(filter_elements(vars(signing_features)), schema_member.keys(), information_string, '_validate_signing_features')
    serial_bound_features = [
        'serial_bind',
        'debug',
        'uie_key_switch_enable',
        'root_revoke_activation_enable',
        'crash_dump']
    for serial_bound_feature in serial_bound_features:
        verify_profile_elements(filter_elements(vars(getattr(signing_features, serial_bound_feature))), schema_member[serial_bound_feature].keys(), f'''{serial_bound_feature} in the {information_string}''', '_validate_signing_features')
        feature_object = getattr(signing_features, serial_bound_feature)
        if not feature_object.supported:
            if feature_object.supports_single_serial or feature_object.supports_multi_serials:
                raise RuntimeError(f'''{ERROR_STRING}Signing feature {serial_bound_feature} of the {information_string} must be supported to be able to support single or multi serials.''')
            for feature, allowed_values in (('mrc_specs', MRC_SPECS), ('root_certificate_hash_algorithms', HASH_ALGORITHMS), ('certificate_chain_depths', CERTIFICATE_CHAIN_DEPTHS)):
                if getattr(signing_features, feature, None):
                    verify_profile_elements(filter_elements(vars(getattr(signing_features, feature))), schema_member[feature].keys(), f'''{feature} in the {information_string}''', '_validate_signing_features')
                    _validate_default_and_supported_values(getattr(signing_features, feature), feature, signing_features_string, authenticator_id, schema_member[feature], allowed_values, **('schema_enums',))
            if signing_features.mrc_specs:
                if not MRC_3_0 in signing_features.mrc_specs.supported_mrc_specs.value and signing_features.root_certificate_hash_algorithms:
                    raise RuntimeError(f'''{ERROR_STRING}{signing_features_string} must contain root_certificate_hash_algorithms when supported_mrc_specs contains {MRC_3_0}.''')
                mrc_specs = None(set(signing_features.mrc_specs.supported_mrc_specs.value))
                if len(mrc_specs) > 1:
                    log_warning(f'''{information_string} contains multiple supported_mrc_specs values: {and_separated(mrc_specs)}.''')
    default_platform_bindings = signing_features.platform_bindings.default_platform_bindings.value
    if len(default_platform_bindings) > 1 and INDEPENDENT in default_platform_bindings:
        default_platform_bindings.remove(INDEPENDENT)
        error_prefix = f'''More restrictive values, {and_separated(default_platform_bindings)}, are''' if len(default_platform_bindings) > 1 else f'''A more restrictive value, {and_separated(default_platform_bindings)}, is'''
        raise RuntimeError(f'''{ERROR_STRING}{error_prefix} listed as default_platform_bindings in addition to {INDEPENDENT}. A more restrictive value cannot be listed alongside {INDEPENDENT}.''')
    supported_platform_bindings = None.platform_bindings.supported_platform_bindings.value
    _validate_value_supported(supported_platform_bindings, PLATFORM_BINDINGS, f'''platform_bindings of {information_string}''')
    if missing_bindings = sorted(set(default_platform_bindings) - set(supported_platform_bindings)):
        raise RuntimeError(f'''{ERROR_STRING}The default_platform_bindings value{plural_s(missing_bindings)} {and_separated(list(missing_bindings))} of the {authenticator_id} {signing_features_string} {are_or_is(missing_bindings)} not{' a' if len(missing_bindings) == 1 else ''} supported platform binding{plural_s(missing_bindings)}.''')
    for feature_string, allowed_values in ((sorted(set(default_platform_bindings) - set(supported_platform_bindings)), MEASUREMENT_REGISTER_TARGETS), ('supported_soc_lifecycle_states', SOC_LIFECYCLE_STATES), ('supported_oem_lifecycle_states', OEM_LIFECYCLE_STATES)):
        if feature = getattr(signing_features, feature_string):
            _validate_value_supported(feature.value, allowed_values, f'''{feature_string} of {information_string}''')


def _validate_image_list(parsed_profile = None, schema_member = None):
    profile_elements = filter_elements(vars(parsed_profile.authentication.image_list))
    verify_profile_elements(profile_elements, schema_member.keys(), 'image_list', '_validate_image_list')
    image_ids = []
    image_entry_authenticator_ids = set()
    authenticator_ids = set()
    for None in parsed_profile.authentication.image_list.image:
        image = None
        authenticator_qti = image.authenticator_qti if image.authenticator_qti else None
        authenticator_oem = image.authenticator_oem if image.authenticator_oem else None
        if not authenticator_qti and authenticator_oem:
            raise RuntimeError(f'''{ERROR_STRING}Image {image.id} must have at least one of authenticator_oem or authenticator_qti.''')
        if None is not None:
            image_entry_authenticator_ids.add(authenticator_qti)
            if not None((lambda .0 = None: for authenticator in .0:
authenticator_qti == authenticator.id)(parsed_profile.authentication.authenticators.authenticator)):
                raise RuntimeError(f'''{ERROR_STRING}Authenticator entry with id {authenticator_qti} not found. ''')
            if None is not None:
                image_entry_authenticator_ids.add(authenticator_oem)
                if not None((lambda .0 = None: for authenticator in .0:
authenticator_oem == authenticator.id)(parsed_profile.authentication.authenticators.authenticator)):
                    raise RuntimeError(f'''{ERROR_STRING}Authenticator entry with id {authenticator_oem} not found. ''')
                image_format_supported = None
                for authenticator in parsed_profile.authentication.authenticators.authenticator:
                    authenticator_ids.add(authenticator.id)
                    if not authenticator.supported_image_formats or authenticator.default_image_format:
                        raise RuntimeError(f'''{ERROR_STRING}Authenticator {authenticator.id} must contain a default_image_format and supported_image_formats.''')
                    if None.id == authenticator_qti:
                        if not authenticator.supported_qti_signing_features and authenticator.supported_qti_encryption_features:
                            raise RuntimeError(f'''{ERROR_STRING}Authenticator {authenticator_qti} must contain {AUTHORITY_QTI} signing and/or {AUTHORITY_QTI} encryption features.''')
                        image_format_supported = None((lambda .0 = None: for image_format in .0:
if image.image_format:
passimage.image_format == image_format.id)(authenticator.supported_image_formats.image_format))
                    if authenticator.id == authenticator_oem:
                        if not authenticator.supported_oem_signing_features and authenticator.supported_oem_encryption_features:
                            raise RuntimeError(f'''{ERROR_STRING}Authenticator {authenticator_oem} must contain {AUTHORITY_OEM} signing and/or {AUTHORITY_OEM} encryption features.''')
                        image_format_supported = None((lambda .0 = None: for image_format in .0:
if image.image_format:
passimage.image_format == image_format.id)(authenticator.supported_image_formats.image_format))
                if not image.image_format and image_format_supported:
                    raise RuntimeError(f'''{ERROR_STRING}image_format {image.image_format} of image entry for {image.id} is not one of the supported_image_formats.''')
                if None.compression_format and image.compression_format not in COMPRESSION_FORMATS:
                    raise RuntimeError(f'''Image entry for {image.id} contains unsupported compression format {image.compression_format}. Supported compression formats are: {and_separated(COMPRESSION_FORMATS)}.''')
                if unused_authenticators = authenticator_ids - image_entry_authenticator_ids:
                    raise RuntimeError(f'''{ERROR_STRING}The following authenticators do not authenticate any image: {and_separated(sorted(unused_authenticators))}''')
                authenticator_ids - image_entry_authenticator_ids(image_ids, 'Image IDs')
                _validate_unique_feature_entries(parsed_profile.authentication.image_list.image, 'Image entries', 'image_list')
                return None


def _validate_encryption_features(encryption_features, encryption_features_string = None, authenticator_id = None, authority = None, schema_member = ('encryption_features', EncryptionFeatures, 'encryption_features_string', str, 'authenticator_id', str, 'authority', str, 'schema_member', dict[(str, dict)], 'return', None)):
    verify_profile_elements(filter_elements(vars(encryption_features)), schema_member.keys(), f'''{encryption_features_string} for authenticator {authenticator_id}''', '_validate_encryption_features')
    valid_default = False
    encryption_format_ids = []
    default_encryption_format = encryption_features.default_encryption_format
    information_string = f'''{encryption_features_string} for authenticator {authenticator_id}'''
    schema_element = schema_member['supported_encryption_formats']['encryption_format']
    uie_elements = [
        'encryption_specs',
        'root_key_types',
        'supports_encrypted_segment_indices']
    qbec_elements = [
        'version',
        'key_management_scheme',
        'key_management_feature',
        'data_encryption_scheme',
        'public_keys',
        'max_num_public_keys']
    required_qbec_elements = [
        'version',
        'key_management_scheme',
        'data_encryption_scheme']
    for None in encryption_features.supported_encryption_formats.encryption_format:
        encryption_format = None
        encryption_format_ids.append(encryption_format.id)
        if default_encryption_format == encryption_format.id:
            valid_default = True
        error_message = f'''encryption_format {encryption_format.id} in the {information_string}'''
        if encryption_format.encryption_type not in ENCRYPTION_TYPES:
            raise RuntimeError(f'''{ERROR_STRING}encryption_type of {error_message} contains unsupported value, {encryption_format.encryption_type}. Supported values are: {and_separated(ENCRYPTION_TYPES)}.''')
        if None.encryption_type == UIE:
            if missing_elements = (lambda .0 = None: [ uie_element for uie_element in .0 if getattr(encryption_format, uie_element, None) is None ])(uie_elements):
                raise RuntimeError(f'''{ERROR_STRING}{error_message} must contain {and_separated(missing_elements)}.''')
            if additional_elements = (lambda .0 = None: [ qbec_element for qbec_element in .0 if getattr(encryption_format, qbec_element, None) ])(qbec_elements):
                raise RuntimeError(f'''{ERROR_STRING}{error_message} cannot contain {or_separated(additional_elements)}.''')
            for feature, allowed_uie_values in (((lambda .0 = None: [ qbec_element for qbec_element in .0 if getattr(encryption_format, qbec_element, None) ])(qbec_elements), ENCRYPTION_SPECS), ('root_key_types', ROOT_KEY_TYPES)):
                _validate_default_and_supported_values(getattr(encryption_format, feature), feature, f'''encryption_format {encryption_format.id} in the {encryption_features_string}''', authenticator_id, schema_element[feature], allowed_uie_values, **('schema_enums',))
            encryption_elements = [
                (encryption_format, schema_element),
                (getattr(encryption_format, 'encryption_specs'), schema_element['encryption_specs']),
                (getattr(encryption_format, 'root_key_types'), schema_element['root_key_types'])]
            for element_profile, element_schema in encryption_elements:
                verify_profile_elements(filter_elements(vars(element_profile)), element_schema.keys(), f'''{encryption_features_string} of {authenticator_id}''', '_validate_encryption_features')
            continue
        if missing_elements = (lambda .0 = None: [ qbec_element for qbec_element in .0 if getattr(encryption_format, qbec_element, None) is None ])(required_qbec_elements):
            raise RuntimeError(f'''{ERROR_STRING}{error_message} must contain {and_separated(missing_elements)}.''')
        if additional_elements = (lambda .0 = None: [ uie_element for uie_element in .0 if getattr(encryption_format, uie_element, None) ])(uie_elements):
            raise RuntimeError(f'''{ERROR_STRING}{error_message} cannot contain {or_separated(additional_elements)}.''')
        for feature_string, allowed_qbec_values in (((lambda .0 = None: [ uie_element for uie_element in .0 if getattr(encryption_format, uie_element, None) ])(uie_elements), QBEC_VERSIONS), ('key_management_feature', KEY_MANAGEMENT_FEATURE_DESCRIPTION_TO_ID.keys()), ('data_encryption_scheme', DATA_ENCRYPTION_SCHEME_DESCRIPTION_TO_ID.keys())):
            if disallowed_value = getattr(encryption_format, feature_string) and disallowed_value not in allowed_qbec_values:
                raise RuntimeError(f'''{ERROR_STRING}{feature_string} of {error_message} contains unsupported value, {disallowed_value}. Supported value{plural_s(allowed_qbec_values)} {are_or_is(allowed_qbec_values)}: {and_separated(allowed_qbec_values)}.''')
            if encryption_format.key_management_scheme:
                if encryption_format.key_management_scheme.valueOf_ not in KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID:
                    raise RuntimeError(f'''{ERROR_STRING}key_management_scheme of {error_message} contains unsupported value, {encryption_format.key_management_scheme.valueOf_}. Supported value{plural_s(KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID)} {are_or_is(KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID)}: {and_separated(KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID.keys())}.''')
                if wrapped_key_policy = getattr(encryption_format, feature_string).key_management_scheme.wrapped_key_policy:
                    if encryption_format.key_management_scheme.valueOf_ == GCM_GCM:
                        if len(wrapped_key_policy) != WRAPPED_KEY_POLICY_HEX_LEN:
                            raise RuntimeError(f'''{ERROR_STRING}wrapped_key_policy of {error_message} contains unsupported value, {wrapped_key_policy}. wrapped_key_policy must contain exactly {WRAPPED_KEY_POLICY_HEX_LEN} hex characters.''')
                    raise RuntimeError(f'''{ERROR_STRING}wrapped_key_policy of {error_message} should not be present for key_management_scheme {encryption_format.key_management_scheme.valueOf_}. wrapped_key_policy is only supported for key_management_scheme {GCM_GCM}.''')
                if getattr(encryption_format, feature_string).key_management_scheme.wrapped_key_policy.key_management_scheme.valueOf_ == GCM_GCM:
                    raise RuntimeError(f'''{ERROR_STRING}key_management_scheme of {error_message} is missing a wrapped_key_policy. wrapped_key_policy is required for key_management_scheme {GCM_GCM}.''')
                if None == AUTHORITY_OEM:
                    if encryption_format.public_keys:
                        raise RuntimeError(f'''{ERROR_STRING} {error_message} must not contain public_keys.''')
                    if not None.max_num_public_keys:
                        raise RuntimeError(f'''{ERROR_STRING} {error_message} must contain max_num_public_keys.''')
                    if None.encryption_orders:
                        _validate_default_and_supported_values(getattr(encryption_format, 'encryption_orders'), 'encryption_orders', f'''encryption_format {encryption_format.id} in the {encryption_features_string}''', authenticator_id, schema_element['encryption_orders'], ENCRYPTION_ORDERS, **('schema_enums',))
        if authority == AUTHORITY_QTI:
            if not encryption_format.max_num_public_keys and encryption_format.public_keys:
                raise RuntimeError(f'''{ERROR_STRING}{error_message} must contain either max_num_public_keys or public_keys.''')
            if None.encryption_orders:
                raise RuntimeError(f'''{ERROR_STRING}{error_message} must not contain encryption_orders.''')
            encryption_elements = [
                (None, schema_element),
                (getattr(encryption_format, 'public_keys'), schema_element['public_keys'])]
            for element_profile, element_schema in encryption_elements:
                if element_profile:
                    verify_profile_elements(filter_elements(vars(element_profile)), element_schema.keys(), f'''{encryption_features_string} of {authenticator_id}''', '_validate_encryption_features')
            continue
            error = f'''Encryption format IDs in the {information_string}'''
            _validate_unique_ids(encryption_format_ids, error)
            _validate_unique_feature_entries(encryption_features.supported_encryption_formats.encryption_format, 'encryption_formats', information_string)
            if not valid_default:
                raise RuntimeError(f'''{ERROR_STRING}The default_encryption_format of the {information_string} is missing from the supported_encryption_formats.''')
            return None


def _validate_authenticators(parsed_profile = None, schema_member = None):
    authenticator_ids = []
# WARNING: Decompyle incomplete


def _image_can_be_vouched_for_by_authority(authority, image = None, vouch_for_image_formats_max_entry_count = None, vouch_for_authenticators = None, max_vouch_for_count = ('authority', str, 'image', Image, 'vouch_for_image_formats_max_entry_count', dict[(tuple[(str, str)], int)], 'vouch_for_authenticators', list[str], 'max_vouch_for_count', int, 'return', bool)):
    other_authority = AUTHORITY_QTI if authority == AUTHORITY_OEM else AUTHORITY_OEM.lower()
    if getattr(image, f'''authenticator_{other_authority}''') and getattr(image, f'''{other_authority}_vouch_for_disallowed''') is not None:
        raise RuntimeError(f'''{ERROR_STRING}{image.id} cannot contain {other_authority}_vouch_for_disallowed as it does not contain authenticator_{other_authority}.''')
    if authenticator_id = None(image, f'''authenticator_{authority.lower()}'''):
        vouch_for_count = vouch_for_image_formats_max_entry_count.get((image.image_format, authenticator_id))
        if vouch_for_count is not None:
            if max_vouch_for_count and vouch_for_count != max_vouch_for_count:
                raise RuntimeError(f'''{ERROR_STRING}Found multiple candidate image formats for {a_or_an(authority)} {MULTI_IMAGE}.''')
            return None(image, f'''authenticator_{authority.lower()}''')
        if None(image, f'''authenticator_{authority.lower()}''') in vouch_for_authenticators:
            pass
        return getattr(image, f'''{authority.lower()}_vouch_for_disallowed''') is None
    return None(image, f'''authenticator_{authority.lower()}''')


def _validate_vouch_for_max_entry_count(parsed_profile = None):
    (qti_vouch_for_count, oem_vouch_for_count) = (0, 0)
    (max_qti_vouch_for_count, max_oem_vouch_for_count) = (0, 0)
    authenticators_supporting_qti_vouch_for = []
    authenticators_supporting_oem_vouch_for = []
    vouch_for_image_formats_max_entry_count = { }
    for authenticator in parsed_profile.authentication.authenticators.authenticator:
        for image_format in authenticator.supported_image_formats.image_format:
            if image_format.vouch_segment_properties:
                vouch_for_image_formats_max_entry_count[(image_format.id, authenticator.id)] = image_format.vouch_segment_properties.max_entry_count
        if authenticator.supported_qti_signing_features and authenticator.supported_qti_signing_features.supports_vouch_for:
            authenticators_supporting_qti_vouch_for.append(authenticator.id)
        if authenticator.supported_oem_signing_features and authenticator.supported_oem_signing_features.supports_vouch_for:
            authenticators_supporting_oem_vouch_for.append(authenticator.id)
    for image in parsed_profile.authentication.image_list.image:
        if _image_can_be_vouched_for_by_authority(AUTHORITY_QTI, image, vouch_for_image_formats_max_entry_count, authenticators_supporting_qti_vouch_for, max_qti_vouch_for_count):
            qti_vouch_for_count += 1
        if (image.image_format, image.authenticator_qti) in vouch_for_image_formats_max_entry_count:
            max_qti_vouch_for_count = vouch_for_image_formats_max_entry_count[(image.image_format, image.authenticator_qti)]
        if _image_can_be_vouched_for_by_authority(AUTHORITY_OEM, image, vouch_for_image_formats_max_entry_count, authenticators_supporting_oem_vouch_for, max_oem_vouch_for_count):
            oem_vouch_for_count += 1
        if (image.image_format, image.authenticator_oem) in vouch_for_image_formats_max_entry_count:
            max_oem_vouch_for_count = vouch_for_image_formats_max_entry_count[(image.image_format, image.authenticator_oem)]
    error_string = 'The number of images that can be added to the {0} {1}, {2}, exceeds the maximum entry count {3}.'
    error = ''
    if qti_vouch_for_count > max_qti_vouch_for_count:
        error = f'''{ERROR_STRING}{error_string.format(AUTHORITY_QTI, MULTI_IMAGE, qti_vouch_for_count, max_qti_vouch_for_count)}'''
    if oem_vouch_for_count > max_oem_vouch_for_count:
        error = f'''{ERROR_STRING}{error_string.format(AUTHORITY_OEM, MULTI_IMAGE, oem_vouch_for_count, max_oem_vouch_for_count)}'''
    if vouch_for_image_formats_max_entry_count or error:
        log_warning(error)
        return None
    return None


def _validate_platform_bindings(parsed_profile = None, schema_member = None):
    platform_binding_values = filter_elements(vars(parsed_profile.platform_binding_values))
    verify_profile_elements(platform_binding_values, schema_member.keys(), 'platform_binding_values', '_validate_platform_bindings')
    for platform_binding_value in platform_binding_values:
        profile_values = getattr(parsed_profile.platform_binding_values, platform_binding_value)
        if profile_values and len((lambda .0: pass# WARNING: Decompyle incomplete
)(profile_values.value)) > 1:
            raise RuntimeError(f'''{platform_binding_value} in platform_binding_values cannot have a mixture of values with and without variants. Define variants for all of the values or for none of the values.''')
        return None


def _validate_authentication(parsed_profile = None, schema_member = None, validate_multi_image_entry_count = None):
    verify_profile_elements(filter_elements(vars(parsed_profile.authentication)), schema_member.keys(), 'authentication', '_validate_authentication')
    _validate_image_list(parsed_profile, schema_member['image_list'])
    _validate_authenticators(parsed_profile, schema_member['authenticators']['authenticator'])
    if validate_multi_image_entry_count:
        _validate_vouch_for_max_entry_count(parsed_profile)
        return None


def _validate_debugging(parsed_profile = None, schema_member = None):
    verify_profile_elements(filter_elements(parsed_profile.debugging.__dict__), schema_member.keys(), 'debugging', '_validate_debugging')
    if not parsed_profile.debugging.legacy and parsed_profile.debugging.tme:
        raise RuntimeError(f'''{ERROR_STRING}debugging must contain one of legacy or tme.''')
    if None.debugging.legacy:
        _validate_legacy(parsed_profile, schema_member['legacy'])
    if hasattr(parsed_profile.debugging, 'tme') or parsed_profile.debugging.tme:
        _validate_tme(parsed_profile, schema_member['tme'])
        return None
    return None


def _validate_legacy(parsed_profile = None, schema_member = None):
    legacy = parsed_profile.debugging.legacy
    verify_profile_elements(filter_elements(vars(legacy)), schema_member.keys(), 'legacy', '_validate_legacy')
    oem_image_id_found = False
    qti_image_id_found = False
    for image in parsed_profile.authentication.image_list.image:
        if image.id == legacy.oem_image_id:
            oem_image_id_found = True
            if image.authenticator_oem or image.authenticator_qti:
                raise RuntimeError(f'''Image entry with image id {image.id} must contain only authenticator_oem.''')
            if None.id == legacy.qti_image_id:
                qti_image_id_found = True
                if not image.authenticator_qti or image.authenticator_oem:
                    raise RuntimeError(f'''Image entry with image id {image.id} must contain both authenticator_oem and authenticator_qti.''')
                if not oem_image_id_found:
                    raise RuntimeError('The oem_image_id of legacy debugging is not one of the image_list IDs.')
                if not None.qti_image_id is not None and qti_image_id_found:
                    raise RuntimeError('The qti_image_id of legacy debugging is not one of the image_list IDs.')
                elf_classes = None.elf_class.supported_elf_classes.value
                _validate_value_supported(elf_classes, ELF_CLASSES, 'elf_class of legacy debugging')
                if legacy.elf_class.default_elf_class not in elf_classes:
                    raise RuntimeError(f'''{ERROR_STRING}The default_elf_class of legacy debugging is missing from the supported_elf_classes.''')
                default_placement = None.debug_policy_segment_placements.default_debug_policy_segment_placement
                if default_placement not in DEFAULT_SEGMENT_PLACEMENTS:
                    raise RuntimeError(f'''{ERROR_STRING}default_debug_policy_segment_placement of legacy debugging contains unsupported value, {default_placement}. Supported values are: {and_separated(DEFAULT_SEGMENT_PLACEMENTS)}.''')
                for feature_string, allowed_values in ((None, SUPPORTED_DEBUG_POLICY_VERSIONS), ('debug_policy_segment_placements', SUPPORTED_SEGMENT_PLACEMENTS)):
                    _validate_default_and_supported_values(getattr(legacy, feature_string), feature_string, 'legacy debugging', schema_member[feature_string], allowed_values, **('schema_member', 'schema_enums'))
                _validate_supported_debug_options(parsed_profile, schema_member['supported_debug_options'])
                return None


def _validate_supported_debug_options(parsed_profile = None, schema_member = None):
    supported_debug_options = parsed_profile.debugging.legacy.supported_debug_options
    verify_profile_elements(filter_elements(vars(supported_debug_options)), schema_member.keys(), 'supported_debug_options', '_validate_supported_debug_options')
    if supported_debug_options or debug_options = supported_debug_options.debug_option:
        for debug_option in debug_options:
            verify_profile_elements(filter_elements(vars(debug_option)), schema_member['debug_option'].keys(), 'debug_option', '_validate_supported_debug_options')
        if len((lambda .0: pass# WARNING: Decompyle incomplete
)(debug_options)) != len(debug_options):
            raise RuntimeError(f'''{ERROR_STRING}All legacy debug options must have a unique ID.''')
        return supported_debug_options.debug_option
    return supported_debug_options.debug_option


def _validate_tme(parsed_profile = None, schema_member = None):
    tme = parsed_profile.debugging.tme
    verify_profile_elements(filter_elements(tme.__dict__), schema_member.keys(), 'tme', '_validate_tme')
    image_id_found = False
# WARNING: Decompyle incomplete


def _validate_fuse_blowing(parsed_profile = None, schema_member = None):
    fuse_blowing = getattr(parsed_profile, 'fuse_blowing', None)
    verify_profile_elements(filter_elements(fuse_blowing.__dict__), schema_member.keys(), 'fuse_blowing', '_validate_fuse_blowing')
    allowed_fuse_versions = FUSE_HEADER_CLASSES.keys()
# WARNING: Decompyle incomplete


def validate_security_profile(parsed_profile = None, validate_multi_image_entry_count = None):
    profile_elements = filter_elements(vars(parsed_profile))
    profile_schema = SCHEMA_STRUCTURE['profile']
    verify_profile_elements(profile_elements, profile_schema.keys(), 'profile', 'validate_security_profile')
    _validate_platform_bindings(parsed_profile, profile_schema['platform_binding_values'])
    if parsed_profile.authentication:
        _validate_authentication(parsed_profile, profile_schema['authentication'], validate_multi_image_entry_count)
    if parsed_profile.debugging:
        _validate_debugging(parsed_profile, profile_schema['debugging'])
    if getattr(parsed_profile, 'fuse_blowing', None):
        _validate_fuse_blowing(parsed_profile, profile_schema['fuse_blowing'])
        return None


def validate_authentication(parsed_profile = None, tool_name = None):
    if not parsed_profile.authentication:
        raise RuntimeError(f'''Security Profile does not support {tool_name} features.''')

