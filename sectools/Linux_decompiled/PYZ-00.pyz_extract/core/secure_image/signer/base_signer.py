
from abc import ABC, abstractmethod
from typing import Any
import profile
from cmd_line_interface.sectools.cmd_line_common.defines import INDEPENDENT, MEASUREMENT_REGISTER_TARGET, OEM_ID, OEM_LIFECYCLE_STATE, OEM_PRODUCT_ID, PLATFORM_BINDING, PRODUCT_SEGMENT_ID, SECURITY_PROFILE, SERIAL_NUMBER, SOC_FEATURE_ID, SOC_LIFECYCLE_STATE
from cmd_line_interface.sectools.secure_image.defines import CRASH_DUMP, DISABLE, ENABLE, JTAG_DEBUG, NOP, OEM_ROOT_CERTIFICATE_HASH
from common.crypto.openssl.defines import SignatureDescription
from common.data.binary_struct import StructDynamic
from common.data.data import a_or_an, compute_zero_filled_list, hex_val
from common.data.defines import SHA_DESCRIPTION_TO_FUNCTION
from common.logging.logger import log_debug
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.v6.metadata.defines import TRUE, TRUE_BOUND
from common.parser.hash_segment.defines import HASH_SEGMENT_V3, HASH_SEGMENT_V5
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from core.base_device_restrictions import BaseDeviceRestrictions
from core.secure_image.signer.defines import DEBUG_DISABLE_V3_V5, DEBUG_ENABLE_V3_V5, DEBUG_NOP_V3_V5, NUM_SERIAL_NUMBERS, NUM_SERIAL_NUMBERS_PER_ROW, NUM_SOC_HW_VERS_PER_ROW, OU_ACTIVATION_ENABLEMENT, OU_APP_ID, OU_CRASH_DUMP, OU_DEBUG, OU_DICT, OU_HW_ID, OU_IN_USE_SOC_HW_VERSION, OU_MODEL_ID, OU_OEM_ID, OU_OEM_ID_INDEPENDENT, OU_REVOCATION_ENABLEMENT, OU_ROOT_CERT_SEL, OU_ROOT_REVOKE_ACTIVATE_ENABLE, OU_SN, OU_SOC_HW_VERSION, OU_SOC_VERS, OU_SW_ID, OU_SW_SIZE, OU_UIE_KEY_SWITCH_ENABLE, OU_USE_SERIAL_NUMBER_IN_SIGNING, get_ou_string_for_row
from profile.profile_core import SecurityProfile

class BaseSigner(ABC):
    
    def __init__(self, image, security_profile = None, device_restrictions = None, authority = None, outfile = ('',), subject = ('image', HashTableSegmentCommon | None, 'security_profile', SecurityProfile | None, 'device_restrictions', BaseDeviceRestrictions | None, 'authority', str | None, 'outfile', str | None, 'subject', str, 'return', None)):
        self.image = image
        self.security_profile = security_profile
        self.device_restrictions = device_restrictions
        self.authority = authority
        self.outfile = outfile
        self.subject = subject
        self.oem_id_independent = 0
        self.in_use_soc_hw_version = 0
        self.use_serial_number_in_signing = 0
        self.hash_to_sign = b''

    
    def sign(self = None):
        pass

    sign = None(sign)
    
    def get_number_of_certificates(self = None):
        pass

    get_number_of_certificates = None(get_number_of_certificates)
    
    def get_signature_algorithm(self = None):
        pass

    get_signature_algorithm = None(get_signature_algorithm)
    
    def get_number_of_root_certificates(self = None):
        pass

    get_number_of_root_certificates = None(get_number_of_root_certificates)
    
    def get_image_assets(self = None, hash_algorithm = None):
        pass
    # WARNING: Decompyle incomplete

    
    def retry_sign_allowed(self = None):
        return False

    retry_sign_allowed = None(retry_sign_allowed)


def construct_ou_fields(device_restrictions = None, data_size = None, hash_algorithm = None, image = ('device_restrictions', BaseDeviceRestrictions, 'data_size', int, 'hash_algorithm', str, 'image', HashTableSegmentCommon, 'return', str)):
