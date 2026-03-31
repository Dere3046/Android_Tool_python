
import sys
from collections import Counter
from os import makedirs, sep
from pathlib import Path
from pprint import pformat
from shutil import copyfile
from textwrap import indent
from typing import Callable, cast
from cmd_line_interface.auto_close_security_profile_type import auto_close_security_profile_type
from cmd_line_interface.base_defines import get_cmd_member
from cmd_line_interface.basecmdline import CORE_ERROR, NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_ID, INSPECT, QTI, SECURITY_PROFILE, VERIFY_ROOT
from cmd_line_interface.sectools.cmdline import SectoolsCMDLine
from cmd_line_interface.sectools.metabuild_secure_image import defines
from cmd_line_interface.sectools.metabuild_secure_image.defines import AVAILABLE_FILTERS, CHIPSET, FLAVOR, IMAGE_FINDER, OUTDIR, OUTFILE, SECURE_IMAGE_OPTIONS, STORAGE
from cmd_line_interface.sectools.metabuild_secure_image.utils import get_image_finder_script
from cmd_line_interface.sectools.secure_image.defines import SECURE_IMAGE_NAME, VOUCH_FOR
from common.data.data import a_or_an, and_separated, plural_s, plural_verb
from common.logging.logger import QuietError, log_debug, log_error, log_info, log_warning
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from common.parser.multi_image.multi_image import MultiImage
from common.subprocess.subprocess import get_function_from_script
from core.core_interface import CoreInterfaceNoNamespace
from core.hash_sign_core import log_info_wrap
from core.metabuild_secure_image.defines import IMAGE_FINDER_FUNCTION_SIGNATURE, OEM_IMAGE_FINDER_FUNCTION_NAME, QTI_IMAGE_FINDER_FUNCTION_NAME, SECURITY_PROFILE_FINDER_FUNCTION_NAME, SECURITY_PROFILE_FINDER_FUNCTION_SIGNATURE
from profile.profile_core import SecurityProfile
from profile.schema import Image, SigningFeatures

class MetabuildSecureImageCore(CoreInterfaceNoNamespace):
    
    def __init__(self = None):
        self.image_finder_data = { }
        self.chipset = []
        self.flavor = []
        self.storage = []
        self.image_id = []
        self.security_profiles = { }

    
    def run(self = None, args = None):
        log_debug('Retaining metabuild-secure-image specific command line arguments.')
        original_state = defines.METABUILD_SECURE_IMAGE
        defines.METABUILD_SECURE_IMAGE = (lambda .0: pass# WARNING: Decompyle incomplete
)(defines.METABUILD_SECURE_IMAGE.items())
        (parsed_args_namespace, secure_image_args) = SectoolsCMDLine().parse_known_args(args)
        parsed_args = NamespaceWithGet(parsed_args_namespace)
        defines.METABUILD_SECURE_IMAGE = original_state
        image_finder_script = get_image_finder_script(parsed_args.get(IMAGE_FINDER))
        log_debug('Fetching paths of infiles from image finder script.')
        get_infiles_function = get_function_from_script(image_finder_script, IMAGE_FINDER_FUNCTION_SIGNATURE, QTI_IMAGE_FINDER_FUNCTION_NAME if QTI in secure_image_args else OEM_IMAGE_FINDER_FUNCTION_NAME)
        self.image_finder_data = get_infiles_function(parsed_args.get(IMAGE_ID), parsed_args.get(CHIPSET), parsed_args.get(STORAGE), parsed_args.get(FLAVOR))
        log_debug(f'''Infiles returned from image finder script:\n{pformat(self.image_finder_data)}''')
        get_security_profiles_function = get_function_from_script(image_finder_script, SECURITY_PROFILE_FINDER_FUNCTION_SIGNATURE, SECURITY_PROFILE_FINDER_FUNCTION_NAME)
        self.security_profiles = get_security_profiles_function(parsed_args.get(CHIPSET))
        log_debug(f'''Security Profiles returned from image finder script:\n{self.security_profiles}''')
        self.validate_image_finder_values(parsed_args)
    # WARNING: Decompyle incomplete

    
    def set_filter_values(self = None, parsed_args = None, argument = None, image_finder_values = ('parsed_args', NamespaceWithGet, 'argument', str, 'image_finder_values', set[str], 'return', None)):
        log_debug(f'''Validating {argument} returned from image finder script.''')
        argument_value = getattr(parsed_args, argument)
        value = None
        if argument_value:
            if argument == get_cmd_member(IMAGE_ID):
                missing_image_ids = set(argument_value) - image_finder_values
                additional_filter_values = list(image_finder_values - set(argument_value))
                if missing_image_ids:
                    raise RuntimeError(f'''No infiles returned for requested Image ID{plural_s(missing_image_ids)} {and_separated(missing_image_ids)}''')
                value = None
            elif argument_value not in image_finder_values:
                raise RuntimeError(f'''{argument} returned from the image finder script does not match the provided --{argument}. Use {AVAILABLE_FILTERS} to show available {argument}s.''')
            additional_filter_values = list(image_finder_values - {
                argument_value})
            value = [
                argument_value]
            if additional_filter_values:
                log_warning(f'''Infiles for additional argument{plural_s(additional_filter_values)} {and_separated(additional_filter_values)} provided.''')
        if argument_value:
            setattr(self, argument, value)
            return None
        None(setattr, self, argument(image_finder_values))

    
    def validate_image_finder_values(self = None, parsed_args = None):
        chipsets = []
        flavors = []
        storages = []
        image_ids = []
        for chipset in self.image_finder_data.keys():
            chipsets.append(chipset)
            for storage in self.image_finder_data[chipset].keys():
                storages.append(storage)
                for flavor in self.image_finder_data[chipset][storage].keys():
                    flavors.append(flavor)
                    for image_id in self.image_finder_data[chipset][storage][flavor].keys():
                        image_ids.append(image_id)
        for argument_name, image_finder_values in ((CHIPSET, chipsets), (FLAVOR, flavors), (STORAGE, storages), (IMAGE_ID, image_ids)):
            self.set_filter_values(parsed_args, get_cmd_member(argument_name), set(image_finder_values))
        log_debug('Computing number of images to operate on.')
        infile_count = 0
        for chipset in self.chipset:
            for storage in self.storage:
                if self.image_finder_data[chipset].get(storage, []):
                    for flavor in self.flavor:
                        if self.image_finder_data[chipset][storage].get(flavor, []):
                            for image_id in self.image_id:
                                if self.image_finder_data[chipset][storage][flavor].get(image_id, []):
                                    infile_count += len(self.image_finder_data[chipset][storage][flavor][image_id])
        log_debug(f'''Validating {OUTFILE} is only provided when operating on a single image.''')
        if not infile_count > 1 or parsed_args.get(OUTFILE) or parsed_args.get(VOUCH_FOR):
            raise RuntimeError(f'''{OUTDIR} must be provided when operating on multiple images.''')
        return None
        return None

    
    def image_can_be_added_to_multi_image(authority = None, image_entry = None, signing_features = staticmethod):
        if not authority == AUTHORITY_QTI and image_entry.authenticator_qti or not (image_entry.qti_vouch_for_disallowed):
            if authority == AUTHORITY_OEM and image_entry.authenticator_oem and not (image_entry.oem_vouch_for_disallowed) and signing_features:
                pass
        return signing_features.supports_vouch_for

    image_can_be_added_to_multi_image = None(image_can_be_added_to_multi_image)
    
    def get_image_ids_for_vouch_for(self = None, parsed_args = None, secure_image_args = None):
        parsed_xml = auto_close_security_profile_type(Path(self.security_profiles[self.chipset[0]])).parsed_xml
        (security_profile,) = SecurityProfile.process_profiles([
            parsed_xml])
        authority = AUTHORITY_QTI if QTI in secure_image_args else AUTHORITY_OEM
        authority_member = authority.lower()
        authenticator_signing_features = { }
        image_signing_features = { }
        for authenticator in security_profile.authentication.authenticators.authenticator:
            authenticator_signing_features[authenticator.id] = getattr(authenticator, f'''supported_{authority_member}_signing_features''')
        for image in security_profile.authentication.image_list.image:
            authenticator_id = getattr(image, f'''authenticator_{authority_member}''')
            image_signing_features[image.id] = (image, authenticator_signing_features.get(authenticator_id, None))
        error = f'''not support being added to {a_or_an(authority.upper())} {MultiImage.class_type_string()}.'''
        if image_ids = parsed_args.get(IMAGE_ID):
            log_debug(f'''Setting images that can be added to the Multi Image based on user provided {IMAGE_ID} values.''')
            blacklisted_image_ids = []
            for image_id in image_ids:
                (image_entry, signing_features) = image_signing_features[image_id]
                if not self.image_can_be_added_to_multi_image(authority, image_entry, signing_features):
                    blacklisted_image_ids.append(image_id)
            if count = len(blacklisted_image_ids):
                raise RuntimeError(f'''{and_separated(blacklisted_image_ids)} {plural_verb('does', count)} {error}''')
            vouch_for_image_ids = len(blacklisted_image_ids)
            return vouch_for_image_ids
        parsed_args.get(IMAGE_ID)(f'''Auto-detecting images that can be added to the Multi Image from the {IMAGE_FINDER} data.''')
        vouch_for_image_ids = []
        for image_id in self.image_finder_data[self.chipset[0]][self.storage[0]][self.flavor[0]]:
            (image_entry, signing_features) = image_signing_features[image_id]
            if self.image_can_be_added_to_multi_image(authority, image_entry, signing_features):
                vouch_for_image_ids.append(image_id)
                continue
            log_debug(f'''Skipping {image_id} as it does {error}''')
        return vouch_for_image_ids

    
    def perform_vouch_for_operation(self = None, parsed_args = None, secure_image_args = None):
