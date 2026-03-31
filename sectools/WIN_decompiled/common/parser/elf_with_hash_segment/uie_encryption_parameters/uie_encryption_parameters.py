
from typing import Any, TypeAlias, cast, Type
from common.crypto import crypto_ccm, ecies
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.binary_struct import StructBase
from common.data.data import properties_repr
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf_with_hash_segment.uie_encryption_parameters.info_header import InfoHeader
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.defines import L2_AD_MAJOR_VERSION_1, L2_AD_MAJOR_VERSION_2, L2_AD_MINOR_VERSION_0, L2_AD_MINOR_VERSION_1, L2_AD_MINOR_VERSION_2
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.l2_associated_data import L2AssociatedData
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.v1_0.l2_associated_data import L2AssociatedDataV10
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.v1_1.l2_associated_data import L2AssociatedDataV11
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.v1_2.l2_associated_data import L2AssociatedDataV12
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.v2_0.l2_associated_data import L2AssociatedDataV20
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l3_associated_data.l3_associated_data import L3AssociatedData
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.defines import EPS_MAJOR_VERSION_1, EPS_MAJOR_VERSION_2, EPS_MINOR_VERSION_0, ROOT_KEY_TYPE_DESCRIPTION, ROOT_KEY_TYPE_OTP_OEM
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.b0 import B0
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.base_iv import BaseIV
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.l2_key_payload import L2KeyPayload
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.l2_mac import L2KeyMAC
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.l3_key_payload import L3KeyPayload
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.l3_mac import L3KeyMAC
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.section_header import SectionHeaderV1
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v2_0.b0 import B0ECIESAD
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v2_0.l2_key_payload import L2KeyPayloadECIESAD
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v2_0.l2_mac import L2KeyMACECIES
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v2_0.section_header import SectionHeaderV2
SECTION_HEADER_CLASSES: dict[(tuple[(int, int)], Type[SectionHeaderV1 | SectionHeaderV2])] = {
    (EPS_MAJOR_VERSION_2, EPS_MINOR_VERSION_0): SectionHeaderV2,
    (EPS_MAJOR_VERSION_1, EPS_MINOR_VERSION_0): SectionHeaderV1 }
BO_CLASSES: dict[(tuple[(int, int)], Type[B0 | B0ECIESAD])] = {
    (EPS_MAJOR_VERSION_2, EPS_MINOR_VERSION_0): B0ECIESAD,
    (EPS_MAJOR_VERSION_1, EPS_MINOR_VERSION_0): B0 }
L2AssociatedDataClassType: TypeAlias = L2AssociatedDataV10 | L2AssociatedDataV12
ASSOCIATED_DATA_CLASSES: dict[(tuple[(int, int)], Type[L2AssociatedDataClassType])] = {
    (L2_AD_MAJOR_VERSION_2, L2_AD_MINOR_VERSION_0): L2AssociatedDataV20,
    (L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_2): L2AssociatedDataV12,
    (L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_1): L2AssociatedDataV11,
    (L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_0): L2AssociatedDataV10 }
L2_KEY_PAYLOAD_CLASSES: dict[(tuple[(int, int)], Type[L2KeyPayload | L2KeyPayloadECIESAD])] = {
    (EPS_MAJOR_VERSION_2, EPS_MINOR_VERSION_0): L2KeyPayloadECIESAD,
    (EPS_MAJOR_VERSION_1, EPS_MINOR_VERSION_0): L2KeyPayload }
L2_KEY_MAC_CLASSES: dict[(tuple[(int, int)], Type[L2KeyMAC | L2KeyMACECIES])] = {
    (EPS_MAJOR_VERSION_2, EPS_MINOR_VERSION_0): L2KeyMACECIES,
    (EPS_MAJOR_VERSION_1, EPS_MINOR_VERSION_0): L2KeyMAC }

class UIEEncryptionParameters(BaseParserGenerator):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the Encryption Parameter data of an ELF MBN image. '''
        self.info_header = None
        self.section_header = None
        self.l2_b0 = None
        self.l2_associated_data = None
        self.l2_key_payload = None
        self.l2_mac = None
        self.l3_b0 = None
        self.l3_associated_data = None
        self.l3_key_payload = None
        self.l3_mac = None
        self.base_iv = None
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, eps_major_version, l2_ad_major_version, l2_ad_minor_version, root_key_type, software_id, feature_id, encrypted_segment_indices, l1_key, l2_key, l2_wrapped_key, l3_key, l3_wrapped_key, **_):
        if eps_major_version not in (EPS_MAJOR_VERSION_1, EPS_MAJOR_VERSION_2):
            raise RuntimeError(f'''Creation of {self.class_type_string()} v{eps_major_version} Info Header is not supported.''')
        if (None, l2_ad_minor_version) not in ASSOCIATED_DATA_CLASSES:
            raise RuntimeError(f'''Creation of v{l2_ad_major_version}.{l2_ad_minor_version} L2 Associated Data is not supported.''')
        if (None, l2_ad_major_version, l2_ad_minor_version) not in ((EPS_MAJOR_VERSION_1, L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_0), (EPS_MAJOR_VERSION_1, L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_1), (EPS_MAJOR_VERSION_1, L2_AD_MAJOR_VERSION_2, L2_AD_MINOR_VERSION_0), (EPS_MAJOR_VERSION_2, L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_2)):
            raise RuntimeError(f'''Creation of {self.class_type_string()} v{eps_major_version} Info Header with v{l2_ad_major_version}.{l2_ad_minor_version} L2 Associated Data is not supported.''')
        if None not in ROOT_KEY_TYPE_DESCRIPTION:
            raise RuntimeError(f'''A Root Key Type of {root_key_type} is not supported.''')
        if None is not None and eps_major_version != EPS_MAJOR_VERSION_2:
            raise RuntimeError(f'''Feature ID cannot be provided when creating a v{eps_major_version} Encryption Parameter Section.''')
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        self.info_header = InfoHeader(data)
        offset = self.info_header.get_size()
        self.section_header = SECTION_HEADER_CLASSES[(self.info_header.eps1_major_version, self.info_header.eps1_minor_version)](data[offset:])
        offset += self.section_header.get_size()
        self.l2_b0 = BO_CLASSES[(self.info_header.eps1_major_version, self.info_header.eps1_minor_version)](data[offset:])
        offset += self.l2_b0.get_size()
        associated_data = L2AssociatedData(data[offset:])
        self.l2_associated_data = ASSOCIATED_DATA_CLASSES[(associated_data.major_version, associated_data.minor_version)](data[offset:])
        offset += self.l2_associated_data.get_size()
        self.l2_key_payload = L2_KEY_PAYLOAD_CLASSES[(self.info_header.eps1_major_version, self.info_header.eps1_minor_version)](data[offset:])
        offset += self.l2_key_payload.get_size()
        self.l2_mac = L2_KEY_MAC_CLASSES[(self.info_header.eps1_major_version, self.info_header.eps1_minor_version)](data[offset:])
        offset += self.l2_mac.get_size()
        self.l3_b0 = B0(data[offset:])
        offset += self.l3_b0.get_size()
        self.l3_associated_data = L3AssociatedData(data[offset:])
        offset += self.l3_associated_data.get_size()
        self.l3_key_payload = L3KeyPayload(data[offset:])
        offset += self.l3_key_payload.get_size()
        self.l3_mac = L3KeyMAC(data[offset:])
        offset += self.l3_mac.get_size()
        self.base_iv = BaseIV(data[offset:])

    
    def get_size(self = None):
        size = 0
        if self.info_header:
            size += self.info_header.get_size()
        if self.section_header:
            size += self.section_header.get_size()
        if self.l2_b0:
            size += self.l2_b0.get_size()
        if self.l2_associated_data:
            size += self.l2_associated_data.get_size()
        if self.l2_key_payload:
            size += self.l2_key_payload.get_size()
        if self.l2_mac:
            size += self.l2_mac.get_size()
        if self.l3_b0:
            size += self.l3_b0.get_size()
        if self.l3_associated_data:
            size += self.l3_associated_data.get_size()
        if self.l3_key_payload:
            size += self.l3_key_payload.get_size()
        if self.l3_mac:
            size += self.l3_mac.get_size()
        if self.base_iv:
            size += self.base_iv.get_size()
        return size

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        data = bytearray()
        if self.info_header:
            data += self.info_header.pack()
        if self.section_header:
            data += self.section_header.pack()
        if self.l2_b0:
            data += self.l2_b0.pack()
        if self.l2_associated_data:
            data += self.l2_associated_data.pack()
        if self.l2_key_payload:
            data += self.l2_key_payload.pack()
        if self.l2_mac:
            data += self.l2_mac.pack()
        if self.l3_b0:
            data += self.l3_b0.pack()
        if self.l3_associated_data:
            data += self.l3_associated_data.pack()
        if self.l3_key_payload:
            data += self.l3_key_payload.pack()
        if self.l3_mac:
            data += self.l3_mac.pack()
        if self.base_iv:
            data += self.base_iv.pack()
        return memoryview(data)

    
    def is_type(cls = None, data = None):
        return InfoHeader.is_type(data)

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        dump_files = { }
        for attr in ('info_header', 'section_header', 'l2_b0', 'l2_associated_data', 'l2_key_payload', 'l2_mac', 'l3_b0', 'l3_associated_data', 'l3_key_payload', 'l3_mac', 'base_iv'):
            if hasattr(self, attr):
                dump_files[f'''{directory}/{attr}.bin'''] = getattr(self, attr).pack()
        return dump_files

    
    def __repr__(self = None):
        string = ''
        if self.info_header:
            string += f'''{self.class_type_string()} Info Header:\n'''
            string += properties_repr(self.info_header.get_properties())
        if self.section_header:
            string += f'''\n\n{self.class_type_string()} Section Header:\n'''
            string += properties_repr(self.section_header.get_properties())
        if self.l2_b0:
            string += '\n\nWrapped L2 B0:\n'
            string += properties_repr(self.l2_b0.get_properties())
        if self.l2_associated_data:
            string += '\n\nWrapped L2 Associated Data:\n'
            string += properties_repr(self.l2_associated_data.get_properties())
        if self.l2_key_payload:
            string += '\n\nWrapped L2 Key Payload:\n'
            string += properties_repr(self.l2_key_payload.get_properties())
        if self.l2_mac:
            string += '\n\nWrapped L2 MAC:\n'
            string += properties_repr(self.l2_mac.get_properties())
        if self.l3_b0:
            string += '\n\nWrapped L3 B0:\n'
            string += properties_repr(self.l3_b0.get_properties())
        if self.l3_associated_data:
            string += '\n\nWrapped L3 Associated Data:\n'
            string += properties_repr(self.l3_associated_data.get_properties())
        if self.l3_key_payload:
            string += '\n\nWrapped L3 Key Payload:\n'
            string += properties_repr(self.l3_key_payload.get_properties())
        if self.l3_mac:
            string += '\n\nWrapped L3 MAC:\n'
            string += properties_repr(self.l3_mac.get_properties())
        if self.base_iv:
            string += '\n\nBase IV:\n'
            string += properties_repr(self.base_iv.get_properties())
        return string

    
    def get_encrypted_segment_indices(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_encryption_spec_size(eps_major_version = None, eps_minor_version = None, l2_ad_major_version = staticmethod, l2_ad_minor_version = ('eps_major_version', int, 'eps_minor_version', int, 'l2_ad_major_version', int, 'l2_ad_minor_version', int, 'return', int)):
        return sum((lambda .0: for cls in .0:
cls.get_size())(cast(list[Type[StructBase]], [
            InfoHeader,
            SECTION_HEADER_CLASSES[(eps_major_version, eps_minor_version)],
            BO_CLASSES[(eps_major_version, eps_minor_version)],
            ASSOCIATED_DATA_CLASSES[(l2_ad_major_version, l2_ad_minor_version)],
            L2_KEY_PAYLOAD_CLASSES[(eps_major_version, eps_minor_version)],
            L2_KEY_MAC_CLASSES[(eps_major_version, eps_minor_version)],
            B0,
            L3AssociatedData,
            L3KeyPayload,
            L3KeyMAC,
            BaseIV])))

    get_encryption_spec_size = None(get_encryption_spec_size)
    
    def is_segment_encrypted(self = None, idx = None, phdr = None, _ = ('idx', int, 'phdr', ProgramHeader32 | ProgramHeader64, '_', list[AbstractPositionalData], 'return', bool)):
        (all_segments_encrypted, encrypted_segment_indices) = self.get_encrypted_segment_indices()
        if not phdr.is_uie_encryptable and all_segments_encrypted:
            pass
        return idx in encrypted_segment_indices

    __classcell__ = None

