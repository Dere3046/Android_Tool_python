
from os import urandom
from typing import Any
from Cryptodome.Cipher import AES
from Cryptodome.Cipher._mode_gcm import GcmMode
from common.data.data import and_separated, are_or_is, plural_noun
from common.logging.logger import log_info
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_segment_encryption_parameters import QBECSegmentEncryptionParameters
from core.secure_image.encrypter.qbec.defines import DATA_ENCRYPTION_KEY_SIZE, SEGMENT_ENCRYPTION_NONCE_SIZE
from core.secure_image.encrypter.qbec.local.qbec_encrypter import QBECEncrypter
from common.utils import generate_symmetric_key
from profile.profile_core import SecurityProfile

class SegmentEncrypter(QBECEncrypter):
    
    def __init__(self = None, parsed_image = None, security_profile = None, encrypting_entity = None, key_management_feature_id = None, device_public_keys = None, device_nonce = None, encrypted_segment_index = None, retain_encrypted_segment_indices = None, device_private_key = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def get_indices_phdrs_of_segments_to_encrypt(self = None):
        phdrs = self.image.phdrs
        if self.cmdline_encrypted_segment_indices:
            indices_of_segments_to_encrypt = self.cmdline_encrypted_segment_indices
            if not self.retain_encrypted_segment_indices:
                for idx, phdr in enumerate(phdrs):
                    if phdr.is_os_segment_phdr() or phdr.is_os_segment_hash():
                        indices_of_segments_to_encrypt = (lambda .0 = None: for index in .0:
passcontinueindex + 1[index])(indices_of_segments_to_encrypt)
            non_encryptable_indices = []
            for updated_index, original_index in zip(indices_of_segments_to_encrypt, self.cmdline_encrypted_segment_indices):
                if updated_index >= len(phdrs):
                    raise RuntimeError(f'''There is no segment at index {original_index}.''')
                if not None[updated_index].is_qbec_encryptable:
                    non_encryptable_indices.append(original_index)
            if count = len(non_encryptable_indices):
                raise RuntimeError(f'''{plural_noun('Segment', count)} at {plural_noun('index', count)} {and_separated(non_encryptable_indices)} {are_or_is(count)} not encryptable.''')
        indices_of_segments_to_encrypt = (lambda .0: [ idx for idx, phdr in .0 if phdr.is_qbec_encryptable ])(enumerate(phdrs))
        return (None, (lambda .0 = None: [ phdrs[idx] for idx in .0 ])(indices_of_segments_to_encrypt))

    
    def _encrypt(self, authority = None, indices_to_encrypt = None, entries_to_encrypt = None, encryption_order = ('authority', str, 'indices_to_encrypt', list[int], 'entries_to_encrypt', list[AbstractPositionalData], 'encryption_order', int, 'return', QBECSegmentEncryptionParameters)):
        self.set_key_management_wrapped_keys()
        iv_auth_tags = []
    # WARNING: Decompyle incomplete

    
    def _encrypt_segment(self = None, segment_data = None):
        cipher = AES.new(self.data_encryption_key, AES.MODE_GCM, urandom(SEGMENT_ENCRYPTION_NONCE_SIZE), **('nonce',))
    # WARNING: Decompyle incomplete

    __classcell__ = None

