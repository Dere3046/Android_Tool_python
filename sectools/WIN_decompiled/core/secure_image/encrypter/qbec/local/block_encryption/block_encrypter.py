
from os import urandom
from typing import Any
from Cryptodome.Cipher import AES
from common.data.defines import LITTLE_ENDIAN
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import PADDING, SEGMENT
from common.parser.elf.positional_data import AbstractPositionalData, PositionalData
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import XTS_BLOCK_SIZE
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_block_encryption_parameters import QBECBlockEncryptionParameters
from core.secure_image.encrypter.qbec.defines import BLOCK_ENCRYPTION_NONCE_SIE, DATA_ENCRYPTION_KEY_SIZE, SEED_SIZE
from core.secure_image.encrypter.qbec.local.qbec_encrypter import QBECEncrypter
from profile.profile_core import SecurityProfile

class BlockEncrypter(QBECEncrypter):
    
    def __init__(self = None, parsed_image = None, security_profile = None, encrypting_entity = None, key_management_feature_id = None, device_public_keys = None, data_encryption_key = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def overlap_is_fatal(self = None):
        return False

    overlap_is_fatal = None(overlap_is_fatal)
    
    def _validate_image_before_encrypt(self = None, entries_to_encrypt = None):
        super()._validate_image_before_encrypt(entries_to_encrypt)
        first_entry = entries_to_encrypt[0]
        last_entry = self.image.get_last_entry(entries_to_encrypt)
        for positional_entry in self.image.get_positional_entries():
            if positional_entry.size:
                if not positional_entry.offset <= positional_entry.offset or positional_entry.offset <= last_entry.end:
                    pass
                else:
                    first_entry.offset
                if positional_entry.end <= positional_entry.end or positional_entry.end <= last_entry.end:
                    pass
                else:
                    first_entry.offset
                if positional_entry not in entries_to_encrypt or positional_entry.data_name not in (SEGMENT, PADDING):
                    raise RuntimeError(f'''Cannot encrypt an ELF containing encryptable data interspersed or overlapping with non-encryptable data. {positional_entry} cannot be encrypted.''')
                return None

    
    def get_indices_phdrs_of_segments_to_encrypt(self = None):
        return ([], self.image.get_qbec_block_encryptable_entries())

    
    def _encrypt(self, authority = None, _ = None, entries_to_encrypt = None, encryption_order = ('authority', str, '_', list[int], 'entries_to_encrypt', list[AbstractPositionalData], 'encryption_order', int, 'return', QBECBlockEncryptionParameters)):
        self.set_key_management_wrapped_keys()
        data = self.image.get_data_from_entries(entries_to_encrypt)
        seed = ((int.from_bytes(urandom(SEED_SIZE), LITTLE_ENDIAN) >> 28) << 28).to_bytes(SEED_SIZE, LITTLE_ENDIAN)
        encrypted_data = self._encrypt_block(data, seed)
        base_offset = entries_to_encrypt[0].offset
    # WARNING: Decompyle incomplete

    
    def _encrypt_block(self = None, data = None, seed = None):
        flash_section_byte_address = 0
        offset = 0
        key1 = self.data_encryption_key[:16]
        key2 = self.data_encryption_key[16:]
        cipher1 = AES.new(key1, AES.MODE_ECB)
        cipher2 = AES.new(key2, AES.MODE_ECB)
        encrypted_data = bytearray()
        if offset < len(data):
            block = data[offset:offset + XTS_BLOCK_SIZE]
            i = (int.from_bytes(seed, LITTLE_ENDIAN) + (flash_section_byte_address >> 4)).to_bytes(XTS_BLOCK_SIZE, LITTLE_ENDIAN)
            offset += XTS_BLOCK_SIZE
            flash_section_byte_address += XTS_BLOCK_SIZE
            encrypted_i = cipher2.encrypt(i)
            xored_block = (int.from_bytes(block, LITTLE_ENDIAN) ^ int.from_bytes(encrypted_i, LITTLE_ENDIAN)).to_bytes(XTS_BLOCK_SIZE, LITTLE_ENDIAN)
            encrypted_xored_block = cipher1.encrypt(xored_block)
            encrypted_data += (int.from_bytes(encrypted_xored_block, LITTLE_ENDIAN) ^ int.from_bytes(encrypted_i, LITTLE_ENDIAN)).to_bytes(XTS_BLOCK_SIZE, LITTLE_ENDIAN)
            if not offset < len(data):
                return encrypted_data

    __classcell__ = None

