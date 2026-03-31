
from pathlib import Path
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.defines import EPS_MAJOR_VERSION_2
from common.parser.elf_with_hash_segment.uie_encryption_parameters.uie_encryption_parameters import UIEEncryptionParameters
from common.utils import SECTOOLS_PATH
from core.secure_image.encrypter.uie.local.local_encrypter import LocalEncrypter

class TestEncrypter(LocalEncrypter):
    
    def get_encryption_parameters(self = None, authority = None):
        encryption_assets_dir = Path(SECTOOLS_PATH) / 'core/secure_image/encrypter/uie/test/encryption_assets'
        encryption_assets_dir = encryption_assets_dir / 'ecies' if self.eps_major_version == EPS_MAJOR_VERSION_2 else encryption_assets_dir / 'aes'
        self.l1_key = Path(encryption_assets_dir / 'l1.key').read_bytes()
        self.l2_key = Path(encryption_assets_dir / 'l2.key').read_bytes()
        self.l3_key = Path(encryption_assets_dir / 'l3.key').read_bytes()
        return self.create_encryption_parameters(self.l1_key, self.l2_key, self.l3_key, **('l1_key', 'l2_key', 'l3_key'))


