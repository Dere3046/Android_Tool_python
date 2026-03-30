
from common.parser.elf_with_hash_segment.hash_table_segment_header_getters_interface import HashTableSegmentHeaderGettersInterface
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from common.parser.hash_segment.hash_segment_utils import get_ou_fields
from core.secure_image.signer.defines import OU_ACTIVATION_ENABLEMENT, OU_APP_ID, OU_HW_ID, OU_IN_USE_SOC_HW_VERSION, OU_MODEL_ID, OU_OEM_ID, OU_OEM_ID_INDEPENDENT, OU_REVOCATION_ENABLEMENT, OU_ROOT_CERT_SEL, OU_ROOT_REVOKE_ACTIVATE_ENABLE, OU_SOC_VERS, OU_SW_ID

class BindingImplementationOUFields(HashTableSegmentHeaderGettersInterface):
    
    def __init__(self):
        self._ou_fields_dict = {
            AUTHORITY_OEM: { },
            AUTHORITY_QTI: { } }

    
    def set_ou_data(self = None, qti_attest_cert = None, oem_attest_cert = None):
        if qti_attest_cert:
            self._ou_fields_dict[AUTHORITY_QTI] = get_ou_fields(qti_attest_cert)
        if oem_attest_cert:
            self._ou_fields_dict[AUTHORITY_OEM] = get_ou_fields(oem_attest_cert)
            return None

    
    def refresh_ou_data(self = None, authority = None, attestation_certificate = None):
        (qti_attest, oem_attest) = (None, None)
        if authority == AUTHORITY_QTI:
            qti_attest = attestation_certificate
        else:
            oem_attest = attestation_certificate
        self.set_ou_data(qti_attest, oem_attest)

    
    def get_software_id(self = None, authority = None):
        '''Returns the Software ID from OU fields. Returns None if the field does not exist.'''
        pass
    # WARNING: Decompyle incomplete

    
    def get_secondary_software_id(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_mrc_index(self = None, authority = None, _ = None):
        '''Returns the MRC Index from OU fields. Returns None if the field does not exist.'''
        pass
    # WARNING: Decompyle incomplete

    
    def get_root_revoke_activate_enable(self = None, authority = None):
        '''Returns Root Revoke Activate Enable value from OU fields. Returns False if the field does not exist.'''
        root_revoke_activate_enable = False
        for ou_name in (OU_ROOT_REVOKE_ACTIVATE_ENABLE, OU_REVOCATION_ENABLEMENT, OU_ACTIVATION_ENABLEMENT):
            if ou_val = self._get_ou_field_value(authority, ou_name):
                root_revoke_activate_enable = bool(int(ou_val, 0))
        return root_revoke_activate_enable

    
    def get_hash_table_algorithm(self = None):
        pass

    
    def get_oem_id(self = None, authority = None):
        '''Returns the OEM ID from OU fields. Returns None if the field does not exist.'''
        return self._get_conditional_ou_value(authority, OU_OEM_ID_INDEPENDENT, OU_OEM_ID)

    
    def get_oem_product_id(self = None, authority = None):
        '''Returns the OEM Product ID from OU fields. Returns None if the field does not exist.'''
        return self._get_conditional_ou_value(authority, OU_OEM_ID_INDEPENDENT, OU_MODEL_ID)

    
    def get_soc_hw_versions(self = None, authority = None):
        '''Returns the SoC HW Versions from OU fields. Returns None if the field does not exist.'''
        soc_hw_vers_strs = self._get_ou_field_value(authority, OU_SOC_VERS)
        soc_hw_vers = (lambda .0: pass# WARNING: Decompyle incomplete
)(soc_hw_vers_strs) - {
            0} if soc_hw_vers_strs else set()
        in_use_soc_hw_vers = self._get_ou_field_value(authority, OU_IN_USE_SOC_HW_VERSION)
    # WARNING: Decompyle incomplete

    
    def _get_ou_field_value(self = None, authority = None, ou_field_name = None):
        return self._ou_fields_dict[authority].get(ou_field_name)

    
    def _get_conditional_ou_value(self = None, authority = None, depends_on = None, ou_name = ('authority', str, 'depends_on', str, 'ou_name', str, 'return', int | None)):
        ou_value = None
        not_bound_to_value = self._get_ou_field_value(authority, depends_on)
    # WARNING: Decompyle incomplete


