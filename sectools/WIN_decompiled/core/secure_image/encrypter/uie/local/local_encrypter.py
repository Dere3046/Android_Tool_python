
from os import urandom
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.defines import EPS_MAJOR_VERSION_1, EPS_MAJOR_VERSION_2
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.defines import ECIES_KEY_PAYLOAD_SIZE, KEY_PAYLOAD_SIZE
from common.parser.elf_with_hash_segment.uie_encryption_parameters.uie_encryption_parameters import UIEEncryptionParameters
from core.secure_image.encrypter.uie.uie_encrypter import UIEEncrypter, extract_encryption_spec_versions
from profile.profile_core import SecurityProfile
from profile.schema import EncryptionFormat

class LocalEncrypter(UIEEncrypter):
    
    def __init__(self = None, parsed_image = None, security_profile = None, encryption_format = None, l1_key = None, l2_key = None, l3_key = None, feature_id = None, root_key_type = None):
        super().__init__(parsed_image, security_profile, encryption_format, feature_id, root_key_type, **('root_key_type',))
        self.l1_key = l1_key
        if not l2_key:
            pass
        self.l2_key = urandom(KEY_PAYLOAD_SIZE)
        if not l3_key:
            pass
        self.l3_key = urandom(KEY_PAYLOAD_SIZE)

    
    def get_encryption_parameters(self = None, authority = None):
        if self.eps_major_version == EPS_MAJOR_VERSION_1 and len(self.l1_key) != KEY_PAYLOAD_SIZE:
            raise RuntimeError(f'''The L1 key must be {KEY_PAYLOAD_SIZE} bytes.''')
        if None.eps_major_version == EPS_MAJOR_VERSION_2 and len(self.l1_key) != ECIES_KEY_PAYLOAD_SIZE:
            raise RuntimeError('The L1 key must be 64 bytes.')
        if None.l2_key and len(self.l2_key) != KEY_PAYLOAD_SIZE:
            raise RuntimeError(f'''The L2 key must be {KEY_PAYLOAD_SIZE} bytes.''')
        if None.l3_key and len(self.l3_key) != KEY_PAYLOAD_SIZE:
            raise RuntimeError(f'''The L3 key must be {KEY_PAYLOAD_SIZE} bytes.''')
        return None.create_encryption_parameters(self.l1_key, self.l2_key, self.l3_key, **('l1_key', 'l2_key', 'l3_key'))

    
    def get_encryption_spec_versions(self = None):
        encryption_spec = self.supported_encryption_features.encryption_specs.default_encryption_spec
        return extract_encryption_spec_versions(encryption_spec)

    __classcell__ = None

