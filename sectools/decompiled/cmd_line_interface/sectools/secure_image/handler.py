
from argparse import SUPPRESS
from json import dumps
from cmd_line_interface.base_defines import XMLInfo
from cmd_line_interface.basecmdline import BaseCMDLine, NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_ID, OUTFILE
from cmd_line_interface.sectools.cmd_line_common.handler import CommonCMDLineHandler
from cmd_line_interface.sectools.secure_image.cmdline_dict import SECURE_IMAGE_DEVICE_RESTRICTIONS, SECURE_IMAGE_ENCRYPTION, SECURE_IMAGE_SIGNING
from cmd_line_interface.sectools.secure_image.defines import COMPRESS, COMPRESSED_OUTFILE, VOUCH_FOR
from common.logging.logger import log_warning
from profile.profile_core import SecurityProfile
from profile.schema import Profile

class SecureImageEncryptionOptionsCMDLine(BaseCMDLine):
    
    def __init__(self = None):
        super().__init__(SECURE_IMAGE_ENCRYPTION, SUPPRESS, **('usage',))

    __classcell__ = None


class SecureImageSigningOptionsCMDLine(BaseCMDLine):
    
    def __init__(self = None):
        super().__init__(SECURE_IMAGE_SIGNING, SUPPRESS, **('usage',))

    __classcell__ = None


class SecureImageDeviceRestrictionsCMDLine(BaseCMDLine):
    
    def __init__(self = None):
        super().__init__(SECURE_IMAGE_DEVICE_RESTRICTIONS, SUPPRESS, **('usage',))

    __classcell__ = None


class SecureImageCMDLineHandler(CommonCMDLineHandler):
    
    def show_signing_options_help():
        SecureImageSigningOptionsCMDLine().print_help()

    show_signing_options_help = None(show_signing_options_help)
    
    def show_encryption_options_help():
        SecureImageEncryptionOptionsCMDLine().print_help()

    show_encryption_options_help = None(show_encryption_options_help)
    
    def show_available_device_restrictions():
        SecureImageDeviceRestrictionsCMDLine().print_help()

    show_available_device_restrictions = None(show_available_device_restrictions)
    
    def show_available_image_ids(security_profile = None, json_info = None):
        if json_info:
            if not security_profile:
                raise RuntimeError(f'''{SECURITY_PROFILE} must be provided in order to show available Image IDs.''')
            None(f'''supported_operations currently only reflects whether the {COMPRESS} operation is supported for a given {IMAGE_ID}. It will be updated to give additional information in a future release.''')
            image_id_record_data = SecurityProfile((lambda .0: [ profile.parsed_xml for profile in .0 ])(security_profile)).get_image_id_record()
            print(f'''{dumps(image_id_record_data, 4, **('indent',))}''')
            return None
        None.show_values_from_profile(security_profile, 'Image IDs', 'get_image_ids')

    show_available_image_ids = None(show_available_image_ids)
    
    def show_available_encryption_formats(security_profile = None):
        CommonCMDLineHandler.show_values_from_profile(security_profile, 'Encryption Formats', 'get_encryption_format_ids')

    show_available_encryption_formats = None(show_available_encryption_formats)
    
    def validate_cmd_line_args(cls = None, args = None):
        super().validate_cmd_line_args(args)
        if args.get(IMAGE_ID):
            if not len(args.get(IMAGE_ID)) > 1 and args.get(VOUCH_FOR):
                raise RuntimeError(f'''{VOUCH_FOR} must be provided when providing more than one {IMAGE_ID}.''')
            if None.get(VOUCH_FOR) and len(args.get(IMAGE_ID)) != len(args.get(VOUCH_FOR)):
                raise RuntimeError(f'''Number of {IMAGE_ID} values provided must equal the number of {VOUCH_FOR} images provided.''')
            if None.get(COMPRESSED_OUTFILE) or args.get(OUTFILE) or args.get(COMPRESSED_OUTFILE) == args.get(OUTFILE):
                raise RuntimeError(f'''{OUTFILE} and {COMPRESSED_OUTFILE} must be different file paths.''')
            return None
        return None

    validate_cmd_line_args = None(validate_cmd_line_args)
    __classcell__ = None

