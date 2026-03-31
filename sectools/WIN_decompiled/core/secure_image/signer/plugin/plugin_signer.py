
from common.crypto.openssl.defines import SignatureDescription
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.subprocess.subprocess import FunctionSignatureException, get_function_from_script
from core.base_device_restrictions import BaseDeviceRestrictions
from core.secure_image.signer.base_signer import BaseSigner
from profile.profile_core import SecurityProfile
SIGN_FUNCTION_SIGNATURE = '(hash_to_sign, image_inspectable_data, subject, security_profile, plugin_signer_args, **kwargs)'
SIGN_FUNCTION_NAME = 'sign'
NUMBER_OF_CERTIFICATES_FUNCTION_SIGNATURE = '()'
NUMBER_OF_CERTIFICATES_FUNCTION_NAME = 'get_number_of_certificates'
SIGNATURE_ALGORITHM_FUNCTION_SIGNATURE = '()'
SIGNATURE_ALGORITHM_FUNCTION_NAME = 'get_signature_algorithm'
NUMBER_OF_ROOT_CERTIFICATES_FUNCTION_SIGNATURE = '()'
NUMBER_OF_ROOT_CERTIFICATES_FUNCTION_NAME = 'get_number_of_root_certificates'

class PluginSigner(BaseSigner):
    
    def __init__(self = None, image = None, security_profile = None, device_restrictions = None, authority = None, outfile = None, plugin_signer = None, plugin_signer_args = None, subject = None):
        super().__init__(image, security_profile, device_restrictions, authority, outfile, subject)
        self.plugin_signer = plugin_signer
        self.plugin_signer_args = plugin_signer_args
        self.subject = subject

    
    def sign(self = None):
        (hash_to_sign, image_inspectable_data, subject) = self.get_image_assets()
        sign_function = get_function_from_script(self.plugin_signer, SIGN_FUNCTION_SIGNATURE, SIGN_FUNCTION_NAME)
        return sign_function(hash_to_sign, image_inspectable_data, subject, self.security_profile, self.plugin_signer_args)

    
    def get_number_of_certificates(self = None):
        return get_function_from_script(self.plugin_signer, NUMBER_OF_CERTIFICATES_FUNCTION_SIGNATURE, NUMBER_OF_CERTIFICATES_FUNCTION_NAME)()

    
    def get_signature_algorithm(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_number_of_root_certificates(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

