
import json
import tempfile
from itertools import chain
from operator import methodcaller
from os.path import relpath, sep
from pathlib import Path
from typing import Any, Callable, Type
from filelock import SoftFileLock
import profile
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.auto_close_image_type import ImageWithPath
from cmd_line_interface.sectools.cmd_line_common.base_defines import ENCRYPTION_MODE, LOCAL, PLUGIN, QTI, SIGNATURE_FORMAT, TEST
from cmd_line_interface.sectools.cmd_line_common.defines import FUSE_BLOWER_IMAGES, HASH, IMAGE_ID, INFILE, OUTFILE, SECURITY_PROFILE, SIGN, VALIDATE
from cmd_line_interface.sectools.secure_image.defines import COMPRESS, COMPRESSED_OUTFILE, DATA_ENCRYPTION_KEY, DEVICE_PUBLIC_KEY, ENCRYPT, ENCRYPTED_SEGMENT_INDEX, ENCRYPTION_FORMAT, FEATURE_ID, L1_KEY, L2_KEY, L3_KEY, OUTFILE_RECORD, PIL_SPLIT, PIL_SPLIT_OUTDIR, PLUGIN_ENCRYPTER, PLUGIN_ENCRYPTER_ARGS, ROOT_KEY_TYPE, SECURE_IMAGE_NAME, VOUCH_FOR, DEVICE_PRIVATE_KEY, DEVICE_NONCE
from common.data.data import a_or_an, and_separated, numbered_string, plural_s, unhexlify2
from common.logging.logger import QuietError, log_debug, log_info, log_warning
from common.parser.elf.defines import INT_TO_ELFCLASS
from common.parser.elf.elf import ELF
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import ENCRYPTED_THEN_SIGNED, QBEC_VERSION_2, SIGNED_THEN_ENCRYPTED
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.parser.hash_segment.hash_segment_utils import validate_software_id
from common.parser.mbn.mbn import MBN
from common.parser.mdt_with_hash_segment.mdt_with_hash_segment import MDTWithHashTableSegment
from common.parser.multi_image.defines import MULTI_IMAGE, MULTI_IMAGE_DESCRIPTION_ALGO
from common.parser.multi_image.multi_image import MultiImage
from common.parser.sec_elf_with_hash_segment.sec_elf_with_hash_segment import SecELFWithHashTableSegment
from common.parser.utils import get_compressed_data, get_parsed_image
from common.utils import is_macos, write_cmdline_file
from core.core_interfaces.core_security_profile_validator_interface import CoreSecurityProfileValidatorInterface
from core.core_interfaces.core_specific_profile_consumer_interface import CoreSpecificProfileConsumerInterface
from core.core_interfaces.device_restrictions_consumer import DeviceRestrictions, DeviceRestrictionsConsumer
from core.hash_sign_core import HashSignCore, log_info_wrap
from core.profile_validator.defines import ENCRYPTED_THEN_SIGNED as ENCRYPTED_THEN_SIGNED_STRING, SIGNED_THEN_ENCRYPTED as SIGNED_THEN_ENCRYPTED_STRING, UIE
from core.profile_validator.validate import validate_authentication
from core.secure_image.encrypter.qbec.local.block_encryption.block_encrypter import BlockEncrypter
from core.secure_image.encrypter.qbec.local.segment_encryption.segment_encrypter import SegmentEncrypter
from core.secure_image.encrypter.qbec.plugin.qbec_plugin_encrypter import QBECPluginEncrypter
from core.secure_image.encrypter.uie.local.local_encrypter import LocalEncrypter
from core.secure_image.encrypter.uie.plugin.plugin_encrypter import UIEPluginEncrypter
from core.secure_image.encrypter.uie.test.test_encrypter import TestEncrypter
from core.secure_image.encrypter.uie.uie_encrypter import UIEEncrypter
from core.secure_image.encrypter.utils import get_key_management_feature_id, get_qbec_encrypter_class, validate_key_arguments_against_encryption_type
from core.secure_image.encryption_order_utils import get_order_of_operations, validate_infile_type_against_current_operations
from core.secure_image.secure_image_device_restrictions import SecureImageDeviceRestrictions
from core.secure_image.validate.validate import get_fuse_blower_images_mismatches
from profile.defines import ANY, SCHEMA_STRUCTURE
from profile.profile_core import SecurityProfile
from profile.schema import Profile
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
