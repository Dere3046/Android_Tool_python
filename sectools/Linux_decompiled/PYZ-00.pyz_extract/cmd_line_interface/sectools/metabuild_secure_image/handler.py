
from argparse import SUPPRESS
from json import dumps
from textwrap import indent
from typing import cast
from cmd_line_interface.auto_close_security_profile_type import auto_close_security_profile_type
from cmd_line_interface.base_defines import AutoCloseFileType, XMLInfo
from cmd_line_interface.basecmdline import BaseCMDLine, NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_ID, OUTFILE
from cmd_line_interface.sectools.cmd_line_common.handler import CommonCMDLineHandler
from cmd_line_interface.sectools.cmd_line_handler_interface import CMDLineHandlerInterface
from cmd_line_interface.sectools.metabuild_secure_image.defines import CHIPSET, FLAVOR, SECURE_IMAGE_OPTIONS, STORAGE
from cmd_line_interface.sectools.metabuild_secure_image.utils import get_image_finder_data, get_image_finder_script
from cmd_line_interface.sectools.secure_image.defines import COMPRESS, VOUCH_FOR
from common.data.data import and_separated, numbered_string
from common.logging.logger import log_warning
from common.subprocess.subprocess import get_function_from_script
from core.metabuild_secure_image.defines import SECURITY_PROFILE_FINDER_FUNCTION_NAME, SECURITY_PROFILE_FINDER_FUNCTION_SIGNATURE
from profile.profile_core import SecurityProfile

class SecureImageOptionsCMDLine(BaseCMDLine):
    
    def __init__(self = None):
        super().__init__(SECURE_IMAGE_OPTIONS, SUPPRESS, **('usage',))

    __classcell__ = None


class MetabuildSecureImageCMDLineHandler(CMDLineHandlerInterface):
    
    def show_secure_image_options_help():
        SecureImageOptionsCMDLine().print_help()

    show_secure_image_options_help = None(show_secure_image_options_help)
    
    def show_available_filters(image_finder = None):
        print('Available Filters:')
        image_finder_data = get_image_finder_data(image_finder)
        for chipset in sorted(image_finder_data.keys()):
            print(f'''{CHIPSET}''', chipset)
            for storage in sorted(image_finder_data[chipset].keys()):
                if storage:
                    print(indent(f'''{STORAGE} {storage}''', '  '))
                for flavor in sorted(image_finder_data[chipset][storage].keys()):
                    if flavor:
                        print(indent(f'''{FLAVOR} {flavor}''', '    '))
                    for image_id in sorted(image_finder_data[chipset][storage][flavor].keys()):
                        print(indent(f'''{IMAGE_ID} {image_id}''', '      '))

    show_available_filters = None(show_available_filters)
    
    def show_available_image_ids(image_finder = None, chipset = None, storage = staticmethod, flavor = (None, None, None, None, False), json_info = ('image_finder', AutoCloseFileType.FileInfo | None, 'chipset', str | None, 'storage', str | None, 'flavor', str | None, 'json_info', bool, 'return', None)):
        available_image_ids = set()
        image_finder_data = get_image_finder_data(image_finder)
        available_chipsets = []
        if chipset:
            if chipset in image_finder_data:
                available_chipsets = [
                    chipset]
            else:
                available_chipsets = sorted(image_finder_data.keys())
        for available_chipset in available_chipsets:
            if storage and storage not in image_finder_data[available_chipset]:
                continue
            available_storages = [
                storage] if storage else sorted(image_finder_data[available_chipset].keys())
            for available_storage in available_storages:
                if flavor and flavor not in image_finder_data[available_chipset][available_storage]:
                    continue
                available_flavors = [
                    flavor] if flavor else sorted(image_finder_data[available_chipset][available_storage].keys())
                for available_flavor in available_flavors:
                    for image_id in sorted(image_finder_data[available_chipset][available_storage][available_flavor].keys()):
                        available_image_ids.add(image_id)
        if not available_image_ids:
            requested_filters = (lambda .0: [ arg_name for requested_filter, arg_name in .0 if requested_filter ])({
                flavor: FLAVOR,
                storage: STORAGE,
                chipset: CHIPSET }.items())
            requested_filters_string = f''' for the requested {and_separated(requested_filters)}'''
            print(f'''No Image IDs available{requested_filters_string if requested_filters else ''}.''')
            return None
        if None:
            log_warning(f'''supported_operations currently only reflects whether the {COMPRESS} operation is supported for a given {IMAGE_ID}. It will be updated to give additional information in a future release.''')
            security_profiles = MetabuildSecureImageCMDLineHandler.get_security_profiles_from_script(image_finder, chipset)
            security_profile = SecurityProfile((lambda .0: [ profile.parsed_xml for profile in .0 ])(security_profiles))
            print(f'''{dumps(security_profile.get_image_id_record(available_image_ids), 4, **('indent',))}''')
            return None
        None(f'''Available Image IDs:\n{numbered_string(available_image_ids)}''')

    show_available_image_ids = None(show_available_image_ids)
    
    def get_security_profiles_from_script(image_finder = None, chipset = None):
        get_security_profiles_function = get_function_from_script(get_image_finder_script(image_finder), SECURITY_PROFILE_FINDER_FUNCTION_SIGNATURE, SECURITY_PROFILE_FINDER_FUNCTION_NAME)
        security_profiles = cast(list[XMLInfo], (lambda .0: [ auto_close_security_profile_type(security_profile) for security_profile in .0 ])(set(get_security_profiles_function(chipset).values())))
        return security_profiles

    get_security_profiles_from_script = None(get_security_profiles_from_script)
    
    def show_available_variants(image_finder = None, chipset = None):
        security_profiles = MetabuildSecureImageCMDLineHandler.get_security_profiles_from_script(image_finder, chipset)
        CommonCMDLineHandler.show_values_from_profile(security_profiles, 'Variants', 'get_variants')

    show_available_variants = None(show_available_variants)
    
    def show_available_signature_formats(image_finder = None, chipset = None):
        security_profiles = MetabuildSecureImageCMDLineHandler.get_security_profiles_from_script(image_finder, chipset)
        CommonCMDLineHandler.show_values_from_profile(security_profiles, 'Signature Formats', 'get_signature_format_ids')

    show_available_signature_formats = None(show_available_signature_formats)
    
    def show_available_segment_hash_algorithms(image_finder = None, chipset = None):
        security_profiles = MetabuildSecureImageCMDLineHandler.get_security_profiles_from_script(image_finder, chipset)
        CommonCMDLineHandler.show_values_from_profile(security_profiles, 'Segment Hash Algorithms', 'get_segment_hash_algorithms')

    show_available_segment_hash_algorithms = None(show_available_segment_hash_algorithms)
    
    def show_available_encryption_formats(image_finder = None, chipset = None):
        security_profiles = MetabuildSecureImageCMDLineHandler.get_security_profiles_from_script(image_finder, chipset)
        CommonCMDLineHandler.show_values_from_profile(security_profiles, 'Encryption Formats', 'get_encryption_format_ids')

    show_available_encryption_formats = None(show_available_encryption_formats)
    
    def validate_cmd_line_args(cls = None, args = None):
        if args.get(OUTFILE):
            if not args.get(IMAGE_ID) and args.get(VOUCH_FOR):
                raise RuntimeError(f'''{IMAGE_ID} must be provided with {OUTFILE} when not performing {VOUCH_FOR}.''')
            if not None.get(IMAGE_ID) or len(args.get(IMAGE_ID)) > 1 or args.get(VOUCH_FOR):
                raise RuntimeError(f'''Only one {IMAGE_ID} must be provided when providing {OUTFILE}.''')
            return None
        return None
        return None

    validate_cmd_line_args = None(validate_cmd_line_args)

