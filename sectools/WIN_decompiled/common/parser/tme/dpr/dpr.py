
from functools import partial
from pathlib import Path
from typing import Tuple, Union
from cmd_line_interface.sectools.tme_secure_debug.defines import defines
from common.data.data import tuple_to_version_string, version_string_to_tuple
from common.data.defines import PAD_BYTE_0, SHA_DESCRIPTION_TO_FUNCTION
from common.parser.parser_security_profile_validator_interface import ParserSecurityProfileValidatorInterface
from common.parser.tme.base_tme import BaseTME
from common.parser.tme.dpr.validations import DPRValidationOptions, validate_dpr
from common.parser.tme.tme_parser.defines import SIGNATURE_PATH
from common.parser.tme.tme_parser.tme import TME
from common.parser.tme.tme_signable_interface import TMESignableInterface
from core.tme_secure_debug.tme_signing_algorithm_details import SigningAlgorithm, tme_signing_algorithm_details
from profile.profile_core import SecurityProfile
from public.tme_signable import TMESignable
FORMAT_TME = 'TME'

class DPR(ParserSecurityProfileValidatorInterface, TMESignableInterface):
    '''TME Debug Policy Request parser.'''
    SIGNATURE_JSON_POINTER: str = SIGNATURE_PATH
    SIGNATURE_ID_JSON_POINTER: str = 'SvcDebugPolicy/CmdSigningAlgorithmId'
    
    def __init__(self = None, data = None, dpr_validation_options = None):
        if 'oem_debug_policy_format' in defines.security_profile_data:
            pass
        is_oem_tme_format = defines.security_profile_data['oem_debug_policy_format'] == FORMAT_TME
        self.dpr_validation_options = dpr_validation_options._replace(is_oem_tme_format, **('allow_delegate_key_in_oem_dpr',))
        super().__init__(data)

    
    def class_type_string(cls = None):
        return 'DPR'

    class_type_string = None(class_type_string)
    
    def validate(self = None):
        '''Verifies that the DPR object is correct and follows the Security Profile.'''
        super().validate()
    # WARNING: Decompyle incomplete

    
    def validate_against_security_profile(self = None, security_profile = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_signable_data(self = None, algorithm_id = None):
        '''
        Returns the binary data to sign. The signature is computed over a subset of the TME object\'s binary data rather
        than all of its data, hence the existence of this method. Requires the algorithm that will be used for signing
        as an argument (as the data generated will contain the algorithm id in it).

        Note: The method will make sure that the algorithm id is a valid algorithm identifier. However, the method will
        not verify it against the Security Profile. Therefore, the desired algorithm id should always be selected from
        the algorithm ids provided by the plugin signer "sign" function\'s "allowed_algorithm_ids" parameter.
        '''
        return self._get_signable_data(algorithm_id)[1]

    
    def get_signable_hash(self = None, algorithm_id = None):
        '''
        Returns the hash computed over the binary data to sign. Requires the algorithm that will be used for signing as
        an argument (as the data generated will contain the algorithm id in it, and the corresponding hash function
        will be used).

        Note: The method will make sure that the algorithm id is a valid algorithm identifier. However, the method will
        not verify it against the Security Profile. Therefore, the desired algorithm id should always be selected from
        the algorithm ids provided by the plugin signer "sign" function\'s "allowed_algorithm_ids" parameter.
        '''
        (algorithm_record, data_to_sign) = self._get_signable_data(algorithm_id)
        hash_to_sign = SHA_DESCRIPTION_TO_FUNCTION[algorithm_record.hash_id](data_to_sign).digest()
        return hash_to_sign

    
    def _get_signable_data(self = None, algorithm_id = None):
        pass
    # WARNING: Decompyle incomplete

    
    def from_unsigned(cls = None, tme = None):
        pass
    # WARNING: Decompyle incomplete

    from_unsigned = None(from_unsigned)
    __classcell__ = None

