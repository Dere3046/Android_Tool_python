
from cmd_line_interface.base_defines import XMLInfo
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import INDEPENDENT, LOCAL, PLATFORM_BINDING, ROOT_CERTIFICATE_COUNT, ROOT_CERTIFICATE_INDEX, SECURITY_PROFILE, TEST, TRANSFER_ROOT
from cmd_line_interface.sectools.cmd_line_handler_interface import CMDLineHandlerInterface
from common.data.data import and_separated, numbered_string, plural_s
from profile.profile_core import SecurityProfile
from profile.schema import Profile

class CommonCMDLineHandler(CMDLineHandlerInterface):
    
    def show_available_variants(security_profile = None):
        CommonCMDLineHandler.show_values_from_profile(security_profile, 'Variants', 'get_variants')

    show_available_variants = None(show_available_variants)
    
    def show_available_signature_formats(security_profile = None):
        CommonCMDLineHandler.show_values_from_profile(security_profile, 'Signature Formats', 'get_signature_format_ids')

    show_available_signature_formats = None(show_available_signature_formats)
    
    def show_available_segment_hash_algorithms(security_profile = None):
        CommonCMDLineHandler.show_values_from_profile(security_profile, 'Segment Hash Algorithms', 'get_segment_hash_algorithms')

    show_available_segment_hash_algorithms = None(show_available_segment_hash_algorithms)
    
    def show_values_from_profile(security_profile = None, info_string = None, function_name = staticmethod):
        if not security_profile:
            raise RuntimeError(f'''{SECURITY_PROFILE} must be provided in order to show available {info_string}.''')
        if not None(security_profile, list):
            security_profile = [
                security_profile]
        available_ids_or_variants = getattr(SecurityProfile((lambda .0: [ profile.parsed_xml for profile in .0 ])(security_profile)), function_name)()
        if not available_ids_or_variants:
            print(f'''No {info_string} available that are supported by {SECURITY_PROFILE}.''')
            return None
        None(f'''Available {info_string}:\n{numbered_string(available_ids_or_variants)}''')

    show_values_from_profile = None(show_values_from_profile)
    
    def validate_cmd_line_args(cls = None, args = None):
        if args.signing_mode == LOCAL:
            if not args.root_certificate_index:
                pass
            if 0 >= len(args.root_certificate):
                raise RuntimeError(f'''Number of root certificates provided must be greater than {ROOT_CERTIFICATE_INDEX}.''')
            if None.transfer_root and len(args.root_certificate) == 1:
                raise RuntimeError(f'''{TRANSFER_ROOT} can only be provided when signing with multiple root certificates.''')
            if None.signing_mode == TEST:
                if not args.root_certificate_index:
                    pass
                if not args.root_certificate_count:
                    pass
                if 0 >= 1:
                    raise RuntimeError(f'''{ROOT_CERTIFICATE_COUNT} must be greater than {ROOT_CERTIFICATE_INDEX}.''')
                if None.transfer_root:
                    if not args.root_certificate_count:
                        pass
                    if 1 == 1:
                        raise RuntimeError(f'''{TRANSFER_ROOT} can only be provided when {ROOT_CERTIFICATE_COUNT} is greater than 1.''')
                    if None.get(PLATFORM_BINDING) or INDEPENDENT in args.get(PLATFORM_BINDING) or set(args.get(PLATFORM_BINDING))(restrictive_platform_bindings = set(args.get(PLATFORM_BINDING))) > 1:
                        restrictive_platform_bindings.remove(INDEPENDENT)
                        raise RuntimeError(f'''More restrictive platform binding{plural_s(restrictive_platform_bindings)}, {and_separated(restrictive_platform_bindings)}, cannot be provided along with {INDEPENDENT}.''')
                    return len
                return None
            return None

    validate_cmd_line_args = None(validate_cmd_line_args)

