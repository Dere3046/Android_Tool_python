
import hashlib
from abc import ABC, abstractmethod
from typing import Any
from six import int2byte
from cmd_line_interface.sectools.cmd_line_common.defines import INFILE, SECURITY_PROFILE
from cmd_line_interface.sectools.secure_image.defines import FEATURE_ID
from common.crypto import crypto_cbc
from common.crypto.openssl import openssl
from common.data.data import comma_separated_string
from common.logging.logger import log_info
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment, extract_encryption_spec_versions
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.v1_2.l2_associated_data import L2AssociatedDataV12
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.defines import ROOT_KEY_TYPE_DESCRIPTION_TO_INT, ROOT_KEY_TYPE_INT_TO_DESCRIPTION
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.defines import KEY_PAYLOAD_SIZE
from common.parser.elf_with_hash_segment.uie_encryption_parameters.uie_encryption_parameters import UIEEncryptionParameters
from core.secure_image.encrypter.base_encrypter import BaseEncrypter
from profile.profile_core import SecurityProfile
from profile.schema import EncryptionFormat

class UIEEncrypter(ABC, BaseEncrypter):
    
    def __init__(self = None, parsed_image = None, security_profile = None, encryption_format = None, feature_id = None, root_key_type = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def get_encryption_spec_versions(self = None):
        pass

    get_encryption_spec_versions = None(get_encryption_spec_versions)
    
    def get_encryption_parameters(self = None, authority = None):
        pass

    get_encryption_parameters = None(get_encryption_parameters)
    
    def create_encryption_parameters(self, l1_key = None, l2_key = None, l2_wrapped_key = None, l3_key = (None, None, None, None, None), l3_wrapped_key = ('l1_key', bytes | None, 'l2_key', bytes | None, 'l2_wrapped_key', bytes | None, 'l3_key', bytes | None, 'l3_wrapped_key', bytes | None, 'return', UIEEncryptionParameters)):
        pass
    # WARNING: Decompyle incomplete

    
    def compute_segment_iv(segment_num = None, base_iv = None):
        seg_1 = segment_num & 255
        seg_2 = segment_num >> 8 & 255
        seg_3 = segment_num >> 16 & 255
        seg_4 = segment_num >> 24 & 255
        return hashlib.sha256(base_iv + bytes(int2byte(seg_4)) + bytes(int2byte(seg_3)) + bytes(int2byte(seg_2)) + bytes(int2byte(seg_1))).digest()[16:]

    compute_segment_iv = None(compute_segment_iv)
    
    def get_indices_phdrs_of_segments_to_encrypt(self = None):
        indices_of_segments_to_encrypt = []
        phdrs_of_segments_to_encrypt = []
        for idx, phdr in enumerate(self.image.phdrs):
            if phdr.is_uie_encryptable:
                indices_of_segments_to_encrypt.append(idx)
                phdrs_of_segments_to_encrypt.append(phdr)
        return (indices_of_segments_to_encrypt, phdrs_of_segments_to_encrypt)

    
    def _encrypt(self, authority = None, indices_to_encrypt = None, _ = None, __ = ('authority', str, 'indices_to_encrypt', list[int], '_', list[AbstractPositionalData], '__', bool, 'return', UIEEncryptionParameters)):
        encryption_parameters = self.get_encryption_parameters(authority)
        self.validate_encryption_parameters(encryption_parameters, authority)
    # WARNING: Decompyle incomplete

    
    def validate_encryption_parameters(self = None, encryption_parameters = None, authority = None):
        encryption_parameters.validate_before_operation()
        l2_ad = encryption_parameters.l2_associated_data
    # WARNING: Decompyle incomplete

    __classcell__ = None

