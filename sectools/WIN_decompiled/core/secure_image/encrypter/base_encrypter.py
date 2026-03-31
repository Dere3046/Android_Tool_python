
from abc import ABC, abstractmethod
from itertools import combinations
from typing import Any
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_block_encryption_parameters import QBECBlockEncryptionParameters
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_segment_encryption_parameters import QBECSegmentEncryptionParameters
from common.parser.elf_with_hash_segment.uie_encryption_parameters.uie_encryption_parameters import UIEEncryptionParameters

class BaseEncrypter(ABC):
    
    def __init__(self = None, parsed_image = None, **_):
        self.image = parsed_image

    
    def overlap_is_fatal(self = None):
        return True

    overlap_is_fatal = None(overlap_is_fatal)
    
    def _validate_image_before_encrypt(self = None, entries_to_encrypt = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_indices_phdrs_of_segments_to_encrypt(self = None):
        pass

    get_indices_phdrs_of_segments_to_encrypt = None(get_indices_phdrs_of_segments_to_encrypt)
    
    def _encrypt(self, authority = None, indices_to_encrypt = None, entries_to_encrypt = abstractmethod, encryption_order = ('authority', str, 'indices_to_encrypt', list[int], 'entries_to_encrypt', list[AbstractPositionalData], 'encryption_order', int, 'return', UIEEncryptionParameters | QBECSegmentEncryptionParameters | QBECBlockEncryptionParameters)):
        pass

    _encrypt = None(_encrypt)
    
    def encrypt(self = None, authority = None, encryption_order = None):
        (indices_to_encrypt, entries_to_encrypt) = self.get_indices_phdrs_of_segments_to_encrypt()
        self._validate_image_before_encrypt(entries_to_encrypt)
        return self._encrypt(authority, indices_to_encrypt, entries_to_encrypt, encryption_order)


