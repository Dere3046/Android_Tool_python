
import operator
from binascii import hexlify
from contextlib import suppress
from math import ceil
from typing import Any
import profile
from common.data.base_parser import DumpDict
from common.data.binary_struct import DetailsTuple, StructDynamic
from common.data.data import ceil_to_multiple, extract_data_or_fail, get_lsb, properties_repr
from common.data.defines import PAD_BYTE_1, SHA256_SIZE, SHA384_SIZE, SHA_DESCRIPTION_TO_SIZE
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS32, ELF_BLOCK_SIZE, PT_NULL, PT_ONE_SHOT_HASH, P_FLAGS_OS_NON_PAGED_SEGMENT, P_FLAGS_OS_SEGMENT_TYPE_MASK
from common.parser.elf.elf_header import ELFHeaderCommon
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.elf_with_hash_segment.defines import P_FLAGS_OS_SEGMENT_HASH
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import QBEC_VERSION_2
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec import QBECEncryptionParametersCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_block_encryption_parameters import QBECBlockEncryptionParameters
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_segment_encryption_parameters import QBECSegmentEncryptionParameters
from common.parser.elf_with_hash_segment.uie_encryption_parameters.uie_encryption_parameters import UIEEncryptionParameters
from common.parser.hash_segment.defines import HASH_SEGMENT_V3
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.parser.mbn.defines import HASH_TABLE_SEGMENT_HEADER_CLASSES
from common.parser.mdt.mdt import MDT
from profile.defines import ANY, START

class MDTWithHashTableSegment(HashTableSegmentCommon, MDT):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the data of an MDT With Hash Segment image. '''
        self.hash_table_hashes = []
        self.hash_table_segment_phdr = None
        self.hash_table_segment_idx = 0
        self.one_shot_hash_phdr = None
    # WARNING: Decompyle incomplete

    
    def hash_segment_type(cls = None):
        return 'Hash Table Segment'

    hash_segment_type = None(hash_segment_type)
    
    def image_type_string(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, elf_class, hash_table_segment_version, hash_table_segment_address, **_):
        MDT.create_default(self, elf_class, **('elf_class',))
        self.create_default_hash_table_segment(hash_table_segment_version, hash_table_segment_address, **('hash_table_segment_version', 'hash_table_segment_address'))

    
    def create_default_hash_table_segment(self = None, hash_table_segment_version = None, hash_table_segment_address = None, common_metadata_version = (None,)):
        HashTableSegmentCommon.create_default(self, hash_table_segment_version, common_metadata_version, **('hash_table_segment_version', 'common_metadata_version'))
    # WARNING: Decompyle incomplete

    
    def complete_default_hash_table(self = None, phdr = None, phdr_idx = None):
        self.phdrs.insert(phdr_idx, phdr)
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        super().unpack(data)
        for phdr in self.phdrs:
            if phdr.is_os_segment_hash():
                self.hash_table_segment_phdr = phdr
                self.hash_table_segment_idx = self.phdrs.index(phdr)
            if phdr.p_type == PT_ONE_SHOT_HASH:
                self.one_shot_hash_phdr = phdr
        HashTableSegmentCommon.unpack(self, self.get_hash_table_segment_data(data))

    
    def get_hash_table_segment_data(self = None, data = None):
        if not self.hash_table_segment_phdr:
            raise RuntimeError(f'''MDT does not contain a {self.hash_segment_type()}.''')
        return None(data, len(data) - self.get_size(), self.get_size())

    
    def is_type(cls = None, data = None):
        '''
        Ensure the data contains an ELF Header, a Hash Table Segment Program Header, and Hash Table Segment Data.
        '''
        match = False
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        subdir = f'''{directory}/{self.hash_segment_type().lower().replace(' ', '_')}'''
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        return memoryview(bytearray(super().pack()) + bytearray(self.pack_hash_table_segment_data()))

    
    def pack_hash_table_segment_data(self = None):
        hash_table_segment_data = HashTableSegmentCommon.pack(self)
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        return super().__repr__() + HashTableSegmentCommon.__repr__(self)

    
    def _get_phdr_properties(self = None):
        properties = super()._get_phdr_properties()
        properties[0].append('Encrypted')
        for idx, phdr in enumerate(self.phdrs):
            properties[idx + 1].append(self._is_segment_encrypted(idx, phdr))
        return properties

    
    def is_qbec_2_0_encrypted(self = None):
        if encryption_parameters = self.encryption_parameters and isinstance(encryption_parameters, QBECEncryptionParametersCommon) and encryption_parameters.header:
            pass
        return encryption_parameters.header.version == QBEC_VERSION_2

    
    def _is_segment_encrypted(self = None, idx = None, phdr = None):
        is_segment_encrypted = False
        if self.encryption_parameters:
            encryptable_entries = self.get_qbec_block_encryptable_entries() if isinstance(self.encryption_parameters, QBECBlockEncryptionParameters) else []
            is_segment_encrypted = self.encryption_parameters.is_segment_encrypted(idx, phdr, encryptable_entries)
        return is_segment_encrypted

    
    def get_qbec_block_encryptable_entries(self = None):
        non_empty_load_segment_phdrs = sorted((lambda .0: [ phdr for phdr in .0 if phdr.size ])(self.phdrs), operator.attrgetter('offset'), **('key',))
        start_address = non_empty_load_segment_phdrs[0].offset
        end_address = self.get_last_entry(non_empty_load_segment_phdrs).end
        entries_to_encrypt = []
    # WARNING: Decompyle incomplete

    
    def get_greatest_offset(self = None):
        return self.get_size()

    
    def get_number_of_pages(phdrs = None):
        number_of_hashable_pages = 0
        for phdr in phdrs:
            if phdr.p_flags_os_page_mode == P_FLAGS_OS_NON_PAGED_SEGMENT:
                number_of_hashable_pages += 1
                continue
            number_of_hashable_pages += ceil(phdr.p_filesz / ELF_BLOCK_SIZE)
        return number_of_hashable_pages

    get_number_of_pages = None(get_number_of_pages)
    
    def get_number_of_hashable_entries(self = None):
        number_of_segments = len(self.phdrs)
    # WARNING: Decompyle incomplete

    
    def unpack_header(self = None, data = None, version = None):
        self.header = HASH_TABLE_SEGMENT_HEADER_CLASSES[version](data)

    
    def unpack_encryption_parameters(self = None, remaining_data = None):
        pass
    # WARNING: Decompyle incomplete

    
    def contains_encrypted_data(self = None):
        if self.encryption_parameters:
            encryptable_entries = self.get_qbec_block_encryptable_entries() if isinstance(self.encryption_parameters, QBECBlockEncryptionParameters) else []
            for idx, phdr in enumerate(self.phdrs):
                if self.encryption_parameters.is_segment_encrypted(idx, phdr, encryptable_entries):
                    return True
                return False

    
    def unpack_hash_table_or_code(self = None, data = None):
        offset = 0
    # WARNING: Decompyle incomplete

    
    def pack_hash_table_or_code(self = None):
        if self.hash_table_hashes:
            return memoryview(b''.join(self.hash_table_hashes))
        return None(memoryview)

    
    def pack_encryption_parameters(self = None):
        if self.encryption_parameters:
            return self.encryption_parameters.pack()
        return None(b'')

    
    def get_details_hash_table_or_code(self = None, authority = None, details = None):
        (fields, format_str, details_dict) = details
        if self.hash_table_hashes:
            for idx, hash_table_hash in enumerate(self.hash_table_hashes):
                fields.append('hash_table_entry_' + str(idx))
                format_str = StructDynamic.concatenate_formats(format_str, f'''<{len(hash_table_hash)}s''')
        if self.include_qbec_encryption_parameters(authority):
            fields.append('qbec_encryption_parameters')
            format_str = StructDynamic.concatenate_formats(format_str, f'''<{self.encryption_parameters.header.total_size}s''')
        return (fields, format_str, details_dict)

    
    def repr_hash_table_hashes(self = None):
        string = ''
        if self.hash_table_hashes:
            hash_properties = [
                ('Index', 'Hash')]
            for idx, val in enumerate(self.hash_table_hashes):
                hash_properties.append((str(idx), '0x' + hexlify(val).decode()))
            string += '\n\nHash Table Entries:\n'
            string += properties_repr(hash_properties, [
                0], **('sep_rows',))
        return string

    
    def repr_encryption_parameters(self = None):
        if self.encryption_parameters:
            return f'''\n\n{self.encryption_parameters}'''

    
    def repr_hash_table_algorithm(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

