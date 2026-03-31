
from pathlib import Path
from typing import Type
import profile
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.base_defines import QTI
from cmd_line_interface.sectools.cmd_line_common.defines import GENERATE, HASH, INFILE, OEM_TEST_ROOT_CERTIFICATE_HASH, OUTFILE, SECURITY_PROFILE, SERIAL_NUMBER, SIGN, SIGNATURE_FORMAT
from cmd_line_interface.sectools.secure_debug import defines
from cmd_line_interface.sectools.secure_debug.defines import ALL_FLAGS, QTI_TEST_ROOT_CERTIFICATE_HASH, SECURE_DEBUG_NAME
from cmd_line_interface.sectools.secure_debug.dynamic_arguments import debug_option_id_to_argument
from common.logging.logger import log_debug, log_info, log_warning
from common.parser.debug_policy_elf.debug_policy_elf import DebugPolicyELF
from common.parser.elf.defines import INT_TO_ELFCLASS
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from common.parser.utils import get_parsed_image
from common.utils import write_cmdline_file
from core.core_interfaces.core_security_profile_validator_interface import CoreSecurityProfileValidatorInterface
from core.core_interfaces.core_specific_profile_consumer_interface import CoreSpecificProfileConsumerInterface
from core.core_interfaces.device_restrictions_consumer import DeviceRestrictions, DeviceRestrictionsConsumer
from core.hash_sign_core import HashSignCore, log_info_wrap
from core.secure_debug.secure_debug_device_restrictions import SecureDebugDeviceRestrictions
from profile.profile_core import SecurityProfile
from profile.schema.scale_profile import Profile

class SecureDebugCore(HashSignCore, CoreSecurityProfileValidatorInterface, CoreSpecificProfileConsumerInterface, DeviceRestrictionsConsumer):
    
    def run(self = None, parsed_args = None):
        log_debug(f'''Entering {SECURE_DEBUG_NAME} core''')
        super().run(parsed_args)
        if not self.parsed_image and isinstance(self.parsed_image, DebugPolicyELF):
            if parsed_args.get(HASH) or parsed_args.get(SIGN):
                raise RuntimeError(f'''{INFILE} is not a Debug Policy Image.''')
            None(f'''{INFILE} is not a Debug Policy Image.''')
    # WARNING: Decompyle incomplete

    
    def codependent_operations(self = None):
        return [
            HASH,
            SIGN]

    codependent_operations = None(codependent_operations)
    
    def device_restrictions_class(self = None):
        return SecureDebugDeviceRestrictions

    device_restrictions_class = None(device_restrictions_class)
    
    def validate_mandatory_security_profile_attributes(parsed_profiles = None, _ = None):
        for parsed_profile in parsed_profiles:
            if not parsed_profile.debugging and parsed_profile.debugging.legacy or parsed_profile.authentication:
                raise RuntimeError(f'''Security Profile does not support {SECURE_DEBUG_NAME} features.''')
            return None

    validate_mandatory_security_profile_attributes = None(validate_mandatory_security_profile_attributes)
    
    def set_core_specific_profile_attributes(cls = None, security_profile = None, parsed_args = classmethod):
        authority = AUTHORITY_QTI if parsed_args.get(QTI) else AUTHORITY_OEM
        security_profile.set_debugging_features(cls.get_image_ids(security_profile, parsed_args), authority)
        if security_profile.authenticators:
            security_profile.set_signing_features_and_signature_format(authority, parsed_args.get(SIGNATURE_FORMAT))
            return None

    set_core_specific_profile_attributes = None(set_core_specific_profile_attributes)
    
    def get_image_ids(security_profile = None, parsed_args = None):
        pass
    # WARNING: Decompyle incomplete

    get_image_ids = None(get_image_ids)
    
    def generate_operation(self, parsed_args):
        profile_debugging = profile.SECURITY_PROFILE.legacy_debugging_features
        debug_policy = DebugPolicyELF(profile_debugging.debug_policy_revisions.default_debug_policy_revision, int(profile_debugging.phy_addr, 0), INT_TO_ELFCLASS[profile_debugging.elf_class.default_elf_class], **('debug_policy_version', 'debug_policy_segment_address', 'elf_class'))
        if parsed_args.get(SERIAL_NUMBER):
            debug_policy.set_serial_numbers(parsed_args.get(SERIAL_NUMBER)[0])
        if parsed_args.get(OEM_TEST_ROOT_CERTIFICATE_HASH):
            debug_policy.set_oem_root_certificate_hashes(parsed_args.get(OEM_TEST_ROOT_CERTIFICATE_HASH))
        if parsed_args.get(QTI_TEST_ROOT_CERTIFICATE_HASH):
            debug_policy.set_qti_root_certificate_hashes(parsed_args.get(QTI_TEST_ROOT_CERTIFICATE_HASH))
        if parsed_args.get(ALL_FLAGS):
            debug_policy.set_all_flags()
        debug_options = (lambda .0 = None: [ debug_option for debug_option in .0 if parsed_args.get(debug_option_id_to_argument(debug_option.option_id)) ])(defines.security_profile_debug_options)
        debug_policy.set_flags(debug_options)
        self.parsed_image = debug_policy

    __classcell__ = None

