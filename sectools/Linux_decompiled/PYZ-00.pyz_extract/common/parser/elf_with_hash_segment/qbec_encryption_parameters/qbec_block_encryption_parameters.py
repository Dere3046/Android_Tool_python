
from contextlib import suppress
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.xts.data_encryption_parameters import DataEncryptionParametersXTS
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.xts.data_encryption_parameters_header import DataEncryptionParametersHeaderXTS
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import ENCRYPTED_THEN_SIGNED, QBEC_VERSION_1, XTS_ENCRYPTION_LABEL
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.xts.key_management_parameters import KeyManagementParametersXTS
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.xts.key_management_parameters_header import KeyManagementParametersHeaderXTS
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec import QBECEncryptionParametersCommon, QBEC_HEADER_CLASSES
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_header import QBECHeaderCommon
from common.parser.hash_segment.defines import AUTHORITY_QTI

class QBECBlockEncryptionParameters(QBECEncryptionParametersCommon):
    
    def create_default(self = None, version = None, encrypting_entity = None, encryption_order = None, label = None, nonce = None, public_key_x = None, public_key_y = None, wrapped_keys = None, seed = None, **_):
        self.key_management_parameters = KeyManagementParametersXTS(label, nonce, public_key_x, public_key_y, wrapped_keys, **('label', 'nonce', 'public_key_x', 'public_key_y', 'wrapped_keys'))
    # WARNING: Decompyle incomplete

    
    def is_segment_encrypted(self = None, _ = None, phdr = None, encryptable_entries = ('_', int, 'phdr', ProgramHeader32 | ProgramHeader64, 'encryptable_entries', list[AbstractPositionalData], 'return', bool)):
        if phdr.is_qbec_encryptable:
            pass
        return phdr in encryptable_entries

    
    def is_type(cls = None, data = None):
        '''
        Detect whether the data is of QBEC Encryption Parameters containing a KeyManagementParametersHeaderXTS and
        DataEncryptionParametersHeaderXTS.
        '''
        match = False
        if super().is_type(data):
            with suppress(Exception):
                header = QBEC_HEADER_CLASSES[QBECHeaderCommon(data).version](data)
                qbec_header_size = header.get_size()
                if KeyManagementParametersHeaderXTS.is_type(data[qbec_header_size:]):
                    pass
            match = DataEncryptionParametersHeaderXTS.is_type(data[qbec_header_size + header.key_management_parameters_size:])
        None(None, None, None)
        return match
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    __classcell__ = None

