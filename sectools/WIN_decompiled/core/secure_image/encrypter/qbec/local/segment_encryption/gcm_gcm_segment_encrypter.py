
from binascii import unhexlify
from core.secure_image.encrypter.qbec.local.segment_encryption.segment_encrypter import SegmentEncrypter

class GCMGCMSegmentEncrypter(SegmentEncrypter):
    
    def _get_gcm_wrapped_data_encryption_keys(self = None):
        policy = self.key_management_parameter_class.get_key_policy(None)
    # WARNING: Decompyle incomplete

    
    def set_key_management_wrapped_keys(self = None):
        (self.wrapped_keys, self.wrapped_keys_ivs, self.wrapped_keys_auth_tags, self.wrapped_keys_policies) = self._get_gcm_wrapped_data_encryption_keys()
        self.data_encryption_key = self.key_management_parameter_class.process_data_encryption_key(self.data_encryption_key)


