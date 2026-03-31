
from copy import deepcopy
from common.data.binary_struct import StructDynamic
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.uie_encryption_parameters.uie_encryption_parameters import UIEEncryptionParameters
from common.subprocess.subprocess import get_function_from_script, get_function_from_script2
from core.secure_image.encrypter.uie.uie_encrypter import UIEEncrypter
from profile.profile_core import SecurityProfile
from profile.schema import EncryptionFormat
WRAPPED_L2_WRAPPED_L3_CLEAR_L3_FUNCTION_SIGNATURE = '(image_inspectable_data, root_key_type, encrypted_segment_indices, security_profile, plugin_encrypter_args, **kwargs) -> Tuple[bytes, bytes, bytes]'
WRAPPED_L2_WRAPPED_L3_CLEAR_L3_FUNCTION_SIGNATURE_2 = '(image_inspectable_data: Any, root_key_type: int, encrypted_segment_indices: List[int], security_profile: Any, plugin_encrypter_args: str, **kwargs: Any) -> Tuple[bytes, bytes, bytes]'
WRAPPED_L2_WRAPPED_L3_CLEAR_L3_FUNCTION_NAME = 'get_wrapped_l2_wrapped_l3_clear_l3'
ENCRYPTION_SPEC_VERSION_FUNCTION_SIGNATURE = '() -> Tuple[int, int, int]'
ENCRYPTION_SPEC_VERSION_FUNCTION_NAME = 'get_encryption_spec_versions'

class UIEPluginEncrypter(UIEEncrypter):
    
    def __init__(self = None, parsed_image = None, security_profile = None, encryption_format = None, plugin_encrypter = None, plugin_encrypter_args = None, feature_id = None, root_key_type = None):
        self.plugin_encrypter = plugin_encrypter
        self.plugin_encrypter_args = plugin_encrypter_args
        super().__init__(parsed_image, security_profile, encryption_format, feature_id, root_key_type, **('root_key_type',))

    
    def get_encryption_parameters(self = None, authority = None):
        image_details = self.image.get_details(authority)
    # WARNING: Decompyle incomplete

    
    def get_encryption_spec_versions(self = None):
        return get_function_from_script(self.plugin_encrypter, ENCRYPTION_SPEC_VERSION_FUNCTION_SIGNATURE, ENCRYPTION_SPEC_VERSION_FUNCTION_NAME)()

    __classcell__ = None

