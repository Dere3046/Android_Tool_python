
from common.data.data import hex_val

class PermissiveFeatureIDHandler:
    key_management_feature_id: int = 'PermissiveFeatureIDHandler'
    
    def validate_key_management_feature_id():
        pass

    validate_key_management_feature_id = None(validate_key_management_feature_id)
    
    def get_properties_key_management_feature_id(self = None):
        return hex_val(self.key_management_feature_id, True, **('strip_leading_zeros',))


