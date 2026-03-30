
from inspect import getmembers, getmodule, isclass
from io import StringIO
from types import ModuleType
from typing import Any, Callable, Iterable, Type, TypeVar
from cmd_line_interface.sectools.cmd_line_common.defines import PRODUCT_SEGMENT_ID
from common.data.data import and_separated, plural_s, tuple_to_version_string, version_string_to_tuple, were_or_was
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_VERSION_TO_OPTIONS
from common.parser.hash_segment.defines import MRC_3_0, MRC_SPEC_TO_LEGACY_MAX_ROOT_CERTIFICATE_COUNT
from core.profile_validator.defines import METADATA_VERSION_3_0, UIE
from profile.defines import SCHEMA_VERSIONS, SCHEMA_VERSION_1_0, SCHEMA_VERSION_1_1, SCHEMA_VERSION_1_2, SCHEMA_VERSION_1_3, SCHEMA_VERSION_1_4, SCHEMA_VERSION_1_5, SCHEMA_VERSION_1_6, SCHEMA_VERSION_1_7, SCHEMA_VERSION_1_8, SCHEMA_VERSION_PARSER_SCHEMA_LOCATION
from profile.schema import Profile
from profile.schema.v1_0.profile_parser import authentication as AuthenticationV10, platform_binding_values as PlatformBindingsV10, profile as ProfileV10, soc_hw_ver as SoCHWVerV10
from profile.schema.v1_1.profile_parser import authentication as AuthenticationV11, debugging as DebuggingV11, jtag_id as JTAGIDV11, jtag_ids, platform_binding_values as PlatformBindingsV11, profile as ProfileV11, soc_feature_id as SoCFeatureIDV11, soc_feature_ids, soc_hw_version, soc_hw_versions
from profile.schema.v1_2.profile_parser import debugging as DebuggingV12, profile as ProfileV12
from profile.schema.v1_3.profile_parser import authentication as AuthenticationV13, authenticator as AuthenticatorV13, authenticators as AuthenticatorsV13, encryption_features as EncryptionFeaturesV13, image_format as ImageFormatV13, image_formats as ImageFormatsV13, platform_binding_values as PlatformBindingValues13, platform_bindings as PlatformBindingV13, profile as ProfileV13, signing_features as SigningFeaturesV13
from profile.schema.v1_4.profile_parser import authentication as AuthenticationV14, authenticator as AuthenticatorV14, authenticators as AuthenticatorsV14, debugging as DebuggingV14, default_platform_bindings, encryption_features as EncryptionFeaturesV14, encryption_format as EncryptionFormatV14, image_format as ImageFormatV14, legacy as LegacyDebuggingV14, platform_binding_values as PlatformBindingValues14, platform_bindings as PlatformBindingsV14, profile as ProfileV14, signing_features as SigningFeaturesV14, supported_encryption_formats
from profile.schema.v1_5.profile_parser import debugging as DebuggingV15, legacy as LegacyV15, legacy_debug_option, legacy_supported_debug_options, profile as ProfileV15
from profile.schema.v1_6.profile_parser import authentication as AuthenticationV16, authenticator as AuthenticatorV16, authenticators as AuthenticatorsV16, oem_rch_algorithms as OemRchAlgorithms, profile as ProfileV16, signing_features as SigningFeaturesV16
from profile.schema.v1_7.profile_parser import authentication as AuthenticationV17, authenticator as AuthenticatorV17, authenticators as AuthenticatorsV17, profile as ProfileV17, root_certificate_hash_algorithms as RootCertificateHashAlgorithms, signing_features as SigningFeaturesV17, supported_root_certificate_hash_algorithms as SupportedRootCertificateHashAlgorithms
from profile.schema.v1_8.profile_parser import key_management_scheme as KeyManagementSchemeV18, profile as ProfileV18
GenericClass = TypeVar('GenericClass')
QBEC_CONSTRUCTOR_ARGS = [
    'version',
    'public_keys',
    'key_management_feature',
    'key_management_scheme',
    'data_encryption_scheme',
    'max_num_public_keys',
    'id',
    'encryption_type']
V17_AUTHENTICATOR_CONSTRUCTOR_ARGS = [
    'supported_image_formats.image_format.elf_properties.load_segment_filesz_multiple',
    'supported_oem_encryption_features.supported_encryption_formats.encryption_format.public_keys.value.hw_context',
    'supported_oem_encryption_features.supported_encryption_formats.encryption_format.public_keys.value.bsve',
    'supported_oem_encryption_features.supported_encryption_formats.encryption_format.encryption_orders',
    'supported_qti_encryption_features.supported_encryption_formats.encryption_format.public_keys.value.hw_context',
    'supported_qti_encryption_features.supported_encryption_formats.encryption_format.public_keys.value.bsve',
    'supported_qti_encryption_features.supported_encryption_formats.encryption_format.encryption_orders']
V18_NEW_MEMBERS = [
    'authentication.image_list.image.alternate_authenticators_oem',
    'authentication.image_list.image.alternate_authenticators_qti',
    'authentication.authenticators.authenticator.supported_oem_signing_features.supports_hybrid_signing',
    'authentication.authenticators.authenticator.supported_qti_signing_features.supports_hybrid_signing',
    'debugging.tme.debug_vector.debug_vector_option.incompatible_with',
    'debugging.tme.subsystems.subsystem.supported_debug_options.debug_option.incompatible_with',
    'debugging.tme.ip_scan_dump_policy_vector.scan_dump_ip.incompatible_with',
    'debugging.tme.qad_dump_policy_vector.qad.incompatible_with',
    'fuse_blowing.fuse_regions.fuse_region.allow_blow_random',
    'authentication.authenticators.authenticator.supported_oem_encryption_features.supported_encryption_formats.encryption_format.key_management_scheme.wrapped_key_policy',
    'authentication.authenticators.authenticator.supported_qti_encryption_features.supported_encryption_formats.encryption_format.key_management_scheme.wrapped_key_policy',
    'authentication.authenticators.authenticator.supported_image_formats.image_format.hash_table_segment_properties.hash_table_segment_filesz_multiple',
    'authentication.authenticators.authenticator.supported_oem_signing_features.signature_formats.signature_format.certificate_chain_depths_override',
    'authentication.authenticators.authenticator.supported_qti_signing_features.signature_formats.signature_format.certificate_chain_depths_override',
    'authentication.authenticators.authenticator.supported_oem_signing_features.mrc_specs.max_root_certificate_count',
    'authentication.authenticators.authenticator.supported_qti_signing_features.mrc_specs.max_root_certificate_count']
ALL_MODULES: list[ModuleType] = []
# WARNING: Decompyle incomplete
