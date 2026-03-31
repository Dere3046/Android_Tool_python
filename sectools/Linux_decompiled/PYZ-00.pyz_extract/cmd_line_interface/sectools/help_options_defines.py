
from os import walk
from os.path import join
from pathlib import Path
from cmd_line_interface.base_defines import HELP, get_cmd_member
from cmd_line_interface.profile_validator.defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.base_defines import AVAILABLE_SIGNATURE_FORMATS
from cmd_line_interface.sectools.cmd_line_common.defines import AVAILABLE_DEVICE_RESTRICTIONS, AVAILABLE_SEGMENT_HASH_ALGORITHMS, AVAILABLE_VARIANTS, OPEN_SOURCE_LICENSES, SIGNING_HELP
from cmd_line_interface.sectools.elf_tool.generate.defines import AVAILABLE_ELF_MACHINE_TYPES
from cmd_line_interface.sectools.fuseblower.defines import AVAILABLE_FUSE_GROUPS, SHOW_OEM_CHOICE_FUSES, SHOW_RECOMMENDED_FUSES
from cmd_line_interface.sectools.metabuild_secure_image.defines import AVAILABLE_FILTERS, CHIPSET, FLAVOR, IMAGE_FINDER, SECURE_IMAGE_HELP, STORAGE
from cmd_line_interface.sectools.secure_image.defines import AVAILABLE_ENCRYPTION_FORMATS, AVAILABLE_IMAGE_IDS, ENCRYPTION_HELP, JSON_INFO
from common.utils import SECTOOLS_PATH

def get_open_source_licenses(public_sectools_build = None):
    ignored_directories = [
        'venv',
        '__pycache__']
    if public_sectools_build:
        nonpublic_ignored_directories = nonpublic_ignored_directories
        import cmd_line_interface.sectools.nonpublic.nonpublic_defines
        ignored_directories = nonpublic_ignored_directories
    return (lambda .0 = None: [ join(dir_path, file_name) for dir_path, _, file_names in .0 for file_name in file_names if file_name in ('LICENSE', 'LICENSE.txt', 'LICENSE.rst', 'LICENSE1.txt', 'LICENSE.md', 'LICENCE.rst', 'COPYING') ])(walk(SECTOOLS_PATH))


def show_open_source_licenses():
    print('\n\n'.join((lambda .0: pass# WARNING: Decompyle incomplete
)(get_open_source_licenses())))


def conditional_new_line(arguments, current_argument):
    for cluster in arguments.cluster_args:
        for idx, help_argument in enumerate(HELP_ARGUMENTS):
            if getattr(cluster, get_cmd_member(help_argument), False) and idx < HELP_ARGUMENTS.index(current_argument):
                print()
            
            return None

HELP_ARGUMENTS = [
    HELP,
    AVAILABLE_DEVICE_RESTRICTIONS,
    SIGNING_HELP,
    ENCRYPTION_HELP,
    SECURE_IMAGE_HELP,
    AVAILABLE_IMAGE_IDS,
    AVAILABLE_VARIANTS,
    AVAILABLE_FILTERS,
    AVAILABLE_SIGNATURE_FORMATS,
    AVAILABLE_ENCRYPTION_FORMATS,
    AVAILABLE_SEGMENT_HASH_ALGORITHMS,
    AVAILABLE_ELF_MACHINE_TYPES,
    AVAILABLE_FUSE_GROUPS,
    SHOW_RECOMMENDED_FUSES,
    SHOW_OEM_CHOICE_FUSES,
    OPEN_SOURCE_LICENSES]
PARSER_HELP_ARGUMENTS_FUNCTIONS = {
    HELP: 'print_help' }
HANDLER_HELP_ARGUMENTS_FUNCTIONS = {
    SHOW_OEM_CHOICE_FUSES: ('show_oem_choice_fuses', None),
    SHOW_RECOMMENDED_FUSES: ('show_recommended_fuses', None),
    AVAILABLE_FUSE_GROUPS: ('show_available_fuse_groups', None),
    AVAILABLE_ELF_MACHINE_TYPES: ('show_available_elf_machine_types', None),
    AVAILABLE_SEGMENT_HASH_ALGORITHMS: ('show_available_segment_hash_algorithms', (SECURITY_PROFILE, IMAGE_FINDER, CHIPSET)),
    AVAILABLE_ENCRYPTION_FORMATS: ('show_available_encryption_formats', (SECURITY_PROFILE, IMAGE_FINDER, CHIPSET)),
    AVAILABLE_SIGNATURE_FORMATS: ('show_available_signature_formats', (SECURITY_PROFILE, IMAGE_FINDER, CHIPSET)),
    AVAILABLE_FILTERS: ('show_available_filters', (IMAGE_FINDER,)),
    AVAILABLE_VARIANTS: ('show_available_variants', (SECURITY_PROFILE, IMAGE_FINDER, CHIPSET)),
    AVAILABLE_IMAGE_IDS: ('show_available_image_ids', (SECURITY_PROFILE, IMAGE_FINDER, CHIPSET, STORAGE, FLAVOR, JSON_INFO)),
    SECURE_IMAGE_HELP: ('show_secure_image_options_help', None),
    ENCRYPTION_HELP: ('show_encryption_options_help', None),
    SIGNING_HELP: ('show_signing_options_help', None),
    AVAILABLE_DEVICE_RESTRICTIONS: ('show_available_device_restrictions', None) }
GLOBAL_HELP_ARGUMENTS_FUNCTION = {
    OPEN_SOURCE_LICENSES: show_open_source_licenses }
help_arguments = list(PARSER_HELP_ARGUMENTS_FUNCTIONS.keys()) + list(HANDLER_HELP_ARGUMENTS_FUNCTIONS.keys()) + list(GLOBAL_HELP_ARGUMENTS_FUNCTION.keys())
# WARNING: Decompyle incomplete
