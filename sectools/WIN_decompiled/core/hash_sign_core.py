
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator
import profile
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.base_defines import LOCAL, PLUGIN, PLUGIN_SIGNER, QTI, ROOT_KEY, SECURITY_PROFILE, SIGNATURE_FORMAT, SIGNING_MODE, TEST
from cmd_line_interface.sectools.cmd_line_common.defines import ATTEST_CERTIFICATE_SUBJECT, CA_CERTIFICATE, CA_KEY, CERTIFICATE_CHAIN_DEPTH, DUMP, HASH, INDEPENDENT, INFILE, INSPECT, OUTFILE, PLATFORM_BINDING, PLUGIN_SIGNER_ARGS, ROOT_CERTIFICATE, ROOT_CERTIFICATE_COUNT, ROOT_CERTIFICATE_INDEX, SEGMENT_HASH_ALGORITHM, SIGN, VERIFY_ROOT
from cmd_line_interface.sectools.secure_image.defines import CLIENT_ID, ENCRYPT, LIBRARY_ID, PERSIST_SECTIONS
from common.crypto.openssl.defines import ALGORITHM_ECDSA_USER_FACING, CURVE_SECP384R1, RS_48_49, SIGNATURE_DESCRIPTION_TO_SIZE
from common.crypto.openssl.openssl import convert_certificate_chain_to_format, extract_signature_format, get_all_r_s_sizes, get_signature_information, get_text_from_certificate, get_unsupported_r_s_sizes_in_signing_assets_text, verify_certificate_chain, verify_signature
from common.data.base_parser import BaseParser, DumpInterface
from common.data.certificate import validate_certificate_chain_depth, validate_root_certificate_count_against_mrc_spec
from common.data.data import ordinal, plural_s, version_string_to_tuple
from common.data.defines import SHA_SIZE_TO_DESCRIPTION, ZI_HASH_ALGORITHMS
from common.logging.logger import QuietError, log_debug, log_info
from common.parser.debug_policy_elf_with_hash_segment.debug_policy_elf_with_hash_segment import DebugPolicyELFWithHashTableSegment
from common.parser.elf.elf import ELF
from common.parser.elf_preamble_with_hash_segment.elf_preamble_with_hash_segment import ELFPreambleWithHashTableSegment
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.v6.hash_table_segment_header import HashTableSegmentHeaderV6
from common.parser.elf_with_hash_segment.v7.hash_table_segment_header import HashTableSegmentHeaderV7
from common.parser.hash_segment.defines import ATTESTATION, AUTHORITY_OEM, AUTHORITY_QTI, ROOT
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.parser.hash_segment.hash_segment_utils import check_rch_algorithm_uniformity, get_inactive_rch_algorithms
from common.parser.license_manager.license_manager import LicenseManager
from common.parser.mbn.mbn import MBN
from common.parser.mbn.v6.mbn_header import MBNHeaderV6
from common.parser.mbn.v7.mbn_header import MBNHeaderV7
from common.parser.parser_security_profile_validator_interface import ParserSecurityProfileValidatorInterface
from common.parser.sec_elf_with_hash_segment.sec_elf_with_hash_segment import SecELFWithHashTableSegment
from common.parser.tme_elf_with_hash_segment.tme_elf_with_hash_segment import TMEELFWithHashTableSegment
from common.parser.utils import get_parsed_image
from core.base_device_restrictions import BaseDeviceRestrictions
from core.core_interface import CoreInterface
from core.core_interfaces.core_security_profile_validator_interface import CoreSecurityProfileValidatorInterface
from core.core_interfaces.core_specific_profile_consumer_interface import CoreSpecificProfileConsumerInterface
from core.core_interfaces.device_restrictions_consumer import DeviceRestrictionsConsumer
from core.profile_validator.defines import COMMON_METADATA_0_1
from core.secure_image.signer.base_signer import BaseSigner
from core.secure_image.signer.local.local_signer import LocalSigner
from core.secure_image.signer.plugin.plugin_signer import PluginSigner
from core.secure_image.signer.test.test_signer import TestSigner
from core.secure_image.signer.utils import validate_signature_and_certificate_format_supported, verify_signature_format_supported
from profile.profile_core import SecurityProfile
from profile.schema import ImageFormat
nonpublic_match_signing_mode: Callable[([
    Any,
    Any,
    Any,
    Any], Any)] | None = None
nonpublic_match_encryption_mode: Callable[([
    Any,
    Any,
    Any], Any)] | None = None
# WARNING: Decompyle incomplete
