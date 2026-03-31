
from contextlib import suppress
from typing import Type
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.gcm.data_encryption_parameters import DataEncryptionParametersGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.gcm.data_encryption_parameters_header import DataEncryptionParametersHeaderGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import ENCRYPTED_THEN_SIGNED, KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM, QBEC_VERSION_1
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm.key_management_parameters_header import KeyManagementParametersHeaderGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm2.key_management_parameters_header import KeyManagementParametersHeaderGCM2
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm_gcm.key_management_parameters_header import KeyManagementParametersHeaderGCMGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.siv_64_gcm.key_management_parameters_header import KeyManagementParametersHeaderSIV64GCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.siv_cmac_gcm.key_management_parameters_header import KeyManagementParametersHeaderSIVCMACGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec import KEY_MANAGEMENT_PARAMETER_GCM_CLASSES, QBECEncryptionParametersCommon, QBEC_HEADER_CLASSES
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_header import QBECHeaderCommon
from common.parser.hash_segment.defines import AUTHORITY_QTI

class QBECSegmentEncryptionParameters(QBECEncryptionParametersCommon):
    KEY_MANAGEMENT_HEADER_GCM_CLASSES: list[Type[KeyManagementParametersHeaderGCM]] = [
        KeyManagementParametersHeaderGCM,
        KeyManagementParametersHeaderGCM2,
        KeyManagementParametersHeaderSIV64GCM,
        KeyManagementParametersHeaderSIVCMACGCM,
        KeyManagementParametersHeaderGCMGCM]
    
    def create_default(self, version, encrypting_entity = None, encryption_order = None, key_management_scheme_id = None, key_management_feature_id = None, key_management_nonce = None, public_key_x = None, public_key_y = None, wrapped_keys = None, wrapped_keys_ivs = None, wrapped_keys_auth_tags = None, wrapped_keys_policies = None, segment_indices = (QBEC_VERSION_1, AUTHORITY_QTI, ENCRYPTED_THEN_SIGNED, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM, KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE, b'', b'', b'', (b'',), (b'',), (b'',), (b'',), None, None), iv_auth_tags = (('version', int, 'encrypting_entity', str, 'encryption_order', int, 'key_management_scheme_id', int, 'key_management_feature_id', int, 'key_management_nonce', bytes, 'public_key_x', bytes, 'public_key_y', bytes, 'wrapped_keys', tuple[(bytes, ...)], 'wrapped_keys_ivs', tuple[(bytes, ...)], 'wrapped_keys_auth_tags', tuple[(bytes, ...)], 'wrapped_keys_policies', tuple[(bytes, ...)], 'segment_indices', list[int] | None, 'iv_auth_tags', list[tuple[(bytes, bytes)]] | None, 'return', None),), **_):
        key_management_parameter_class = KEY_MANAGEMENT_PARAMETER_GCM_CLASSES[key_management_scheme_id]
        self.key_management_parameters = key_management_parameter_class(key_management_feature_id, key_management_nonce, public_key_x, public_key_y, wrapped_keys, wrapped_keys_ivs, wrapped_keys_auth_tags, wrapped_keys_policies, **('key_management_feature_id', 'nonce', 'public_key_x', 'public_key_y', 'wrapped_keys', 'wrapped_keys_ivs', 'wrapped_keys_auth_tags', 'wrapped_keys_policies'))
        if not segment_indices:
            pass
        if not iv_auth_tags:
            pass
    # WARNING: Decompyle incomplete

    
    def is_segment_encrypted(self = None, idx = None, phdr = None, _ = ('idx', int, 'phdr', ProgramHeader32 | ProgramHeader64, '_', list[AbstractPositionalData], 'return', bool)):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        '''
        Detect whether the data is of QBEC Encryption Parameters containing a GCM KeyManagementParametersHeader and
        DataEncryptionParametersHeaderGCM.
        '''
        match = False
        if super().is_type(data):
            with suppress(Exception):
                header = QBEC_HEADER_CLASSES[QBECHeaderCommon(data).version](data)
                qbec_header_size = header.get_size()
                for key_management_parameter_header_class in cls.KEY_MANAGEMENT_HEADER_GCM_CLASSES:
                    if not match:
                        pass
                    match = key_management_parameter_header_class.is_type(data[qbec_header_size:])
                if match:
                    pass
            match = DataEncryptionParametersHeaderGCM.is_type(data[qbec_header_size + header.key_management_parameters_size:])
        None(None, None, None)
        return match
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    __classcell__ = None

