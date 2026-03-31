
from abc import abstractmethod
from typing import Any, Type, TypeAlias
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.data import properties_repr
from common.data.defines import PAD_BYTE_0
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.data_encryption_parameters_header_common import DataEncryptionParametersHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.gcm.data_encryption_parameters import DataEncryptionParametersGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.xts.data_encryption_parameters import DataEncryptionParametersXTS
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import DATA_ENCRYPTION_SCHEME_DESCRIPTION_TO_ID, DATA_ENCRYPTION_SCHEME_ID_AES_128_XTS, DATA_ENCRYPTION_SCHEME_ID_ELF_SEGMENT_AES_GCM, ENCRYPTED_THEN_SIGNED, KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_64_GCM, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_CMAC_GCM, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM_2, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_XTS, KEY_MANAGEMENT_SCHEME_ID_GCM_GCM, OEM, QBEC_VERSION_1, QBEC_VERSION_2, QTI
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm.key_management_parameters import KeyManagementParametersGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm2.key_management_parameters import KeyManagementParametersGCM2
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm_gcm.key_management_parameters import KeyManagementParametersGCMGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.key_management_parameters_header_common import KeyManagementParametersHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.siv_64_gcm.key_management_parameters import KeyManagementParametersSIV64GCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.siv_cmac_gcm.key_management_parameters import KeyManagementParametersSIVCMACGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.xts.key_management_parameters import KeyManagementParametersXTS
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_header import QBECHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.v1.qbec_header import QBECHeaderV1
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.v2.qbec_header import QBECHeaderV2
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
KeyManagementParameters: TypeAlias = KeyManagementParametersGCM | KeyManagementParametersXTS
DataEncryptionParameters: TypeAlias = DataEncryptionParametersGCM | DataEncryptionParametersXTS
ENCRYPTING_ENTITY_MAP = {
    AUTHORITY_OEM: OEM,
    AUTHORITY_QTI: QTI }
QBEC_HEADER_CLASSES: dict[(int, Type[QBECHeaderV1 | QBECHeaderV2])] = {
    QBEC_VERSION_2: QBECHeaderV2,
    QBEC_VERSION_1: QBECHeaderV1 }
KEY_MANAGEMENT_PARAMETER_GCM_CLASSES: dict[(int, Type[KeyManagementParametersGCM])] = {
    KEY_MANAGEMENT_SCHEME_ID_GCM_GCM: KeyManagementParametersGCMGCM,
    KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_CMAC_GCM: KeyManagementParametersSIVCMACGCM,
    KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_64_GCM: KeyManagementParametersSIV64GCM,
    KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM_2: KeyManagementParametersGCM2,
    KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM: KeyManagementParametersGCM }
KEY_MANAGEMENT_PARAMETER_CLASSES: dict[(int, Type[KeyManagementParameters])] = KEY_MANAGEMENT_PARAMETER_GCM_CLASSES | {
    KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_XTS: KeyManagementParametersXTS }
DATA_ENCRYPTION_PARAMETER_CLASSES: dict[(int, Type[DataEncryptionParameters])] = {
    DATA_ENCRYPTION_SCHEME_ID_AES_128_XTS: DataEncryptionParametersXTS,
    DATA_ENCRYPTION_SCHEME_ID_ELF_SEGMENT_AES_GCM: DataEncryptionParametersGCM }

class QBECEncryptionParametersCommon(BaseParserGenerator):
    
    def __init__(self = None, data = None, **kwargs):
        self.header = None
        self.key_management_parameters = None
        self.data_encryption_parameters = None
    # WARNING: Decompyle incomplete

    
    def create_default(self, version = None, encrypting_entity = None, encryption_order = None, km_size = (QBEC_VERSION_1, AUTHORITY_QTI, ENCRYPTED_THEN_SIGNED, 0, 0), de_size = ('version', int, 'encrypting_entity', str, 'encryption_order', int, 'km_size', int, 'de_size', int, 'return', None), **_):
        pass
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        data = memoryview(data)
        self.header = QBEC_HEADER_CLASSES[QBECHeaderCommon(data).version](data)
        offset = self.header.get_size()
        if self.header.key_management_parameters_size:
            end = offset + self.header.key_management_parameters_size
            key_management_scheme_id = KeyManagementParametersHeaderCommon(data[offset:]).key_management_scheme_id
            self.key_management_parameters = KEY_MANAGEMENT_PARAMETER_CLASSES[key_management_scheme_id](data[offset:end])
            offset = end
        if self.header.data_encryption_parameters_size:
            end = offset + self.header.data_encryption_parameters_size
            data_encryption_scheme_id = DataEncryptionParametersHeaderCommon(data[offset:]).data_encryption_scheme_id
            self.data_encryption_parameters = DATA_ENCRYPTION_PARAMETER_CLASSES[data_encryption_scheme_id](data[offset:end])
            return None

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def validate(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def validate_before_operation(self = None, **_):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        return QBECHeaderCommon.is_type(data)

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_size(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_encryption_spec_size(version, key_management_scheme = None, data_encryption_scheme = None, num_public_keys = staticmethod, phdrs = ('version', int, 'key_management_scheme', str, 'data_encryption_scheme', str, 'num_public_keys', int, 'phdrs', list[ProgramHeader32 | ProgramHeader64], 'return', int)):
        key_management_scheme_int = KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID[key_management_scheme]
        data_encryption_scheme_int = DATA_ENCRYPTION_SCHEME_DESCRIPTION_TO_ID[data_encryption_scheme]
        return QBEC_HEADER_CLASSES[version].get_size() + KEY_MANAGEMENT_PARAMETER_CLASSES[key_management_scheme_int].get_encryption_spec_size(num_public_keys) + DATA_ENCRYPTION_PARAMETER_CLASSES[data_encryption_scheme_int].get_encryption_spec_size(phdrs)

    get_encryption_spec_size = None(get_encryption_spec_size)
    
    def is_segment_encrypted(self = None, idx = None, phdr = abstractmethod, encryptable_entries = ('idx', int, 'phdr', ProgramHeader32 | ProgramHeader64, 'encryptable_entries', list[AbstractPositionalData], 'return', bool)):
        pass

    is_segment_encrypted = None(is_segment_encrypted)
    __classcell__ = None

