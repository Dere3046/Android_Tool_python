
from binascii import hexlify
from typing import Any, List, Optional, Tuple, Type, Union
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.data import and_separated, ceil_to_multiple, get_enabled_bit_indices_from_byte, properties_repr
from common.data.defines import LITTLE_ENDIAN
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.data_encryption_parameters_common import DataEncryptionParametersCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.gcm.data_encryption_parameters_header import DataEncryptionParametersHeaderGCM

class DataEncryptionParametersGCM(DataEncryptionParametersCommon, BaseParserGenerator):
    HEADER_CLASS: Type[DataEncryptionParametersHeaderGCM] = DataEncryptionParametersHeaderGCM
    IV_SIZE = 12
    AUTH_TAG_SIZE = 16
    
    def __init__(self = None, data = None, **kwargs):
        self.encrypted_segment_indices = []
        self.iv_auth_tags = []
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, segment_indices = None, iv_auth_tags = None, **_):
        segment_bitmask_size = self.get_segment_bitmask_size(max(segment_indices) if segment_indices else 0)
        if not segment_indices:
            pass
        self.encrypted_segment_indices = []
        self.header = self.HEADER_CLASS.from_fields(segment_bitmask_size, len(iv_auth_tags) if iv_auth_tags else 0, **('segment_bitmask_size', 'num_iv_auth_tags'))
        if not iv_auth_tags:
            pass
        self.iv_auth_tags = self.iv_auth_tags

    
    def unpack(self = None, data = None):
        super().unpack(data)
    # WARNING: Decompyle incomplete

    
    def _pack_encrypted_segment_indices(self = None):
        segment_bitmask = 0
        for encrypted_segment_index in self.encrypted_segment_indices:
            segment_bitmask |= 1 << encrypted_segment_index
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        data = bytes(super().pack())
        segment_bitmask = 0
        for encrypted_segment_index in self.encrypted_segment_indices:
            segment_bitmask |= 1 << encrypted_segment_index
        data += self._pack_encrypted_segment_indices()
        for iv, tag in self.iv_auth_tags:
            data = data + iv + tag
        return memoryview(data)

    
    def validate_before_operation(self = None, **_):
        super().validate_before_operation()
    # WARNING: Decompyle incomplete

    
    def get_size(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_iv_auth_tag_size(cls = None, num_iv_auth_tags = None):
        return (cls.IV_SIZE + cls.AUTH_TAG_SIZE) * num_iv_auth_tags

    get_iv_auth_tag_size = None(get_iv_auth_tag_size)
    
    def get_dump_files(self = None, directory = None):
        dump_files = super().get_dump_files(directory)
        if self.encrypted_segment_indices:
            dump_files[f'''{directory}/segment_bitmask.bin'''] = self._pack_encrypted_segment_indices()
        if self.iv_auth_tags:
            for iv, auth_tag in enumerate(self.iv_auth_tags):
                dump_files[f'''{directory}/iv_auth_tags/iv_{i}.bin'''] = iv
                dump_files[f'''{directory}/iv_auth_tags/auth_tag_{i}.bin'''] = auth_tag
        return dump_files

    
    def __repr__(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_segment_bitmask_size(highest_encryptable_segment_idx = None):
        return ceil_to_multiple(ceil_to_multiple(highest_encryptable_segment_idx + 1, 8) // 8, 4)

    get_segment_bitmask_size = None(get_segment_bitmask_size)
    
    def get_encryption_spec_size(cls = None, phdrs = None):
        indices_to_encrypt = (lambda .0: [ idx for idx, phdr in .0 if phdr.is_qbec_encryptable ])(enumerate(phdrs))
        encryption_spec_size = super().get_encryption_spec_size(phdrs)
        if indices_to_encrypt:
            encryption_spec_size += DataEncryptionParametersGCM.get_segment_bitmask_size(max(indices_to_encrypt)) + DataEncryptionParametersGCM.get_iv_auth_tag_size(len(indices_to_encrypt))
        return encryption_spec_size

    get_encryption_spec_size = None(get_encryption_spec_size)
    __classcell__ = None

