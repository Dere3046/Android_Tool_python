
from copy import deepcopy
from cmd_line_interface.base_defines import AutoCloseFileType, HELP_GROUP, KWARGS_ACTION, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_NARGS, KWARGS_STORE_TRUE, KWARGS_TYPE, KWARGS_WRITE, KWARGS_WRITE_BINARY, MUTUALLY_EXCLUSIVE, OPTIONAL
from cmd_line_interface.basecmdline import AutoCloseDirType, BaseCMDLine, CMDLineArgs, CMDLineGroup, update_cmdline_arg
from cmd_line_interface.sectools.cmd_line_common.auto_close_image_type import AutoCloseImageType
from cmd_line_interface.sectools.cmd_line_common.base_defines import AVAILABLE_SIGNATURE_FORMATS, ENCRYPTION_MODE, QTI, SECURITY_PROFILE, SIGN, SIGNING_MODE
from cmd_line_interface.sectools.cmd_line_common.defines import AVAILABLE_SEGMENT_HASH_ALGORITHMS, AVAILABLE_SIGNATURE_FORMATS_HELP, AVAILABLE_VARIANTS, AVAILABLE_VARIANTS_HELP, COMMON, FUSE_BLOWER_IMAGES, FUSE_BLOWER_IMAGES_HELP, HASH, IMAGE_ID, IMAGE_INPUTS_GROUP, IMAGE_OPERATIONS_GROUP, IMAGE_OUTPUTS_GROUP, INFILE, INSPECT, INSPECT_HELP, OPTIONAL_ARGUMENTS, OUTFILE, OUTFILE_HELP as COMMON_OUTFILE_HELP, SECURITY_PROFILE_GROUP, VALIDATE, VERBOSE, VERIFY_ROOT, VERIFY_ROOT_HELP, sha256_sha384_hash
from cmd_line_interface.sectools.defines import SECTOOLS_DESCRIPTION
from cmd_line_interface.sectools.metadata import DEPENDS_ON, DEPENDS_ON_ANY_OF, INCOMPATIBLE_WITH, INCOMPATIBLE_WITH_ALL_BUT
from cmd_line_interface.sectools.secure_image.cmdline_dict import SECURE_IMAGE
from cmd_line_interface.sectools.secure_image.defines import AVAILABLE_ENCRYPTION_FORMATS, AVAILABLE_ENCRYPTION_FORMATS_HELP, AVAILABLE_IMAGE_IDS, AVAILABLE_IMAGE_IDS_HELP, AVAILABLE_SEGMENT_HASH_ALGORITHMS_HELP, ENCRYPT, ENCRYPT_HELP, JSON_INFO, JSON_INFO_HELP, PIL_SPLIT, PIL_SPLIT_HELP, PIL_SPLIT_OUTDIR, SECURE_IMAGE_HASH_HELP, SECURE_IMAGE_NAME, SECURE_IMAGE_SIGN_HELP, VOUCH_FOR
from common.data.data import tuple_to_version_string
from common.parser.multi_image.defines import MULTI_IMAGE
from common.parser.sec_dat.sec_dat import SecDat
from common.parser.sec_elf.sec_elf import SecELF
METABUILD_SECURE_IMAGE_NAME = 'metabuild-secure-image'
METABUILD_SECURE_IMAGE_VERSION = (1, 0)
METABUILD_SECURE_IMAGE_DESCRIPTION = f'''Metabuild Secure Image v{tuple_to_version_string(METABUILD_SECURE_IMAGE_VERSION)}. Based on {SECTOOLS_DESCRIPTION}. Tool for performing {SECURE_IMAGE_NAME} operations on a Metabuild\'s software images.'''
OUTDIR = '--outdir'
IMAGE_FINDER = '--image-finder'
CHIPSET = '--chipset'
FLAVOR = '--flavor'
STORAGE = '--storage'
SECURE_IMAGE_HELP = '--secure-image-help'
AVAILABLE_FILTERS = '--available-filters'
EXTENDED_AVAILABLE_IMAGE_IDS_HELP = f'''{AVAILABLE_IMAGE_IDS_HELP} Provide along with {CHIPSET}, {STORAGE}, and/or {FLAVOR} to show Image IDs of a specific chipset, storage, and/or flavor.'''
CHIPSET_HELP_STRING = f'''Provide along with {CHIPSET} ''' + 'to show {0} of a specific chipset.'
EXTENDED_AVAILABLE_VARIANTS_HELP = f'''{AVAILABLE_VARIANTS_HELP} {CHIPSET_HELP_STRING.format('variants')}'''
EXTENDED_AVAILABLE_SIGNATURE_FORMATS = f'''{AVAILABLE_SIGNATURE_FORMATS_HELP} {CHIPSET_HELP_STRING.format('signature formats')}'''
EXTENDED_AVAILABLE_ENCRYPTION_FORMATS = f'''{AVAILABLE_ENCRYPTION_FORMATS_HELP} {CHIPSET_HELP_STRING.format('encryption formats')}'''
EXTENDED_AVAILABLE_SEGMENT_HASH_ALGORITHMS = f'''{AVAILABLE_SEGMENT_HASH_ALGORITHMS_HELP} {CHIPSET_HELP_STRING.format('segment hash algorithms')}'''
OUTFILE_HELP = f'''{COMMON_OUTFILE_HELP} Can be provided when one {IMAGE_ID} value or {VOUCH_FOR} is provided.'''
OUTDIR_HELP = f'''Directory at which to store output software images. Can be provided when zero or multiple Image IDs are provided. Cannot be provided with {VOUCH_FOR}.'''
IMAGE_ID_HELP = f'''IDs of the images on which to operate. IDs of images to add as entries to {MULTI_IMAGE} when performing {VOUCH_FOR} operation. If not provided, all images in the Metabuild identified by {CHIPSET}, {FLAVOR}, and {STORAGE} will be operated on.'''
IMAGE_FINDER_HELP = 'File path of Python script which implements image discovery interface. The script provides the file paths of software images and Security Profiles contained within the Metabuild. If not provided, a script within the Metabuild implementing the image discovery interface will be auto-discovered.'
CHIPSET_HELP = 'Chipset whose images on which to operate. If not provided, images of all chipsets in the Metabuild will be operated on.'
FLAVOR_HELP = 'Chipset flavor whose images on which to operate. If not provided, images of all chipset flavors in the Metabuild will be operated on.'
STORAGE_HELP = 'Chipset storage type whose images on which to operate. If not provided, images of all chipset storage types in the Metabuild will be operated on.'
VOUCH_FOR_HELP = f'''Defaults to false. If provided, {OUTFILE} will be a {MULTI_IMAGE} and will contain the hashes of images identified by {IMAGE_ID}, {CHIPSET}, {FLAVOR}, and {STORAGE}.'''
SECURE_IMAGE_HELP_HELP = 'Show secure-image options and exit.'
AVAILABLE_FILTERS_HELP = f'''Show available values for {CHIPSET}, {FLAVOR}, {STORAGE}, {IMAGE_ID} and exit.'''
IMAGE_OUTPUTS_GROUP_DESCRIPTION = f'''{OUTFILE} and {OUTDIR} are mutually exclusive.'''
METABUILD_SECURE_IMAGE_EPILOG = f'''For {SECURE_IMAGE_NAME} options: {BaseCMDLine.TOOL_NAME} {METABUILD_SECURE_IMAGE_NAME} {SECURE_IMAGE_HELP}'''
INFILE_REPLACEMENT = 'input software image(s)'
SECURITY_PROFILE_REPLACEMENT = 'Security Profile'
OUTFILE_REPLACEMENT = 'output software image(s)'
METABUILD_SECURE_IMAGE_VALIDATE_HELP = f'''If provided along with {OUTFILE} or {OUTDIR}, validates output software images against the {SECURITY_PROFILE_REPLACEMENT} and any provided {FUSE_BLOWER_IMAGES}. If neither {OUTFILE} nor {OUTDIR} is provided, validates that {INFILE_REPLACEMENT} are compatible with the {SECURITY_PROFILE_REPLACEMENT} and any provided {FUSE_BLOWER_IMAGES}.'''
METABUILD_SECURE_IMAGE_HELP_GROUP: CMDLineGroup = COMMON[HELP_GROUP][:2]
METABUILD_SECURE_IMAGE_HELP_GROUP += [
    ([
        SECURE_IMAGE_HELP], {
        KWARGS_HELP: SECURE_IMAGE_HELP_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        AVAILABLE_FILTERS], {
        KWARGS_HELP: AVAILABLE_FILTERS_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        AVAILABLE_IMAGE_IDS], {
        KWARGS_HELP: EXTENDED_AVAILABLE_IMAGE_IDS_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        JSON_INFO], {
        KWARGS_HELP: JSON_INFO_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        DEPENDS_ON: [
            AVAILABLE_IMAGE_IDS] }),
    ([
        AVAILABLE_VARIANTS], {
        KWARGS_HELP: EXTENDED_AVAILABLE_VARIANTS_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        AVAILABLE_SIGNATURE_FORMATS], {
        KWARGS_HELP: EXTENDED_AVAILABLE_SIGNATURE_FORMATS,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        AVAILABLE_ENCRYPTION_FORMATS], {
        KWARGS_HELP: EXTENDED_AVAILABLE_ENCRYPTION_FORMATS,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        AVAILABLE_SEGMENT_HASH_ALGORITHMS], {
        KWARGS_HELP: EXTENDED_AVAILABLE_SEGMENT_HASH_ALGORITHMS,
        KWARGS_ACTION: KWARGS_STORE_TRUE })]
METABUILD_SECURE_IMAGE: CMDLineArgs = {
    OPTIONAL_ARGUMENTS: [
        ([
            IMAGE_FINDER], {
            KWARGS_HELP: IMAGE_FINDER_HELP,
            KWARGS_TYPE: AutoCloseFileType(True, 'utf-8', **('return_path', 'encoding')) }, {
            DEPENDS_ON_ANY_OF: [
                INSPECT,
                VERIFY_ROOT,
                HASH,
                SIGN,
                ENCRYPT,
                VALIDATE] }),
        ([
            IMAGE_ID], {
            KWARGS_HELP: IMAGE_ID_HELP,
            KWARGS_NARGS: '+' }, {
            DEPENDS_ON_ANY_OF: [
                INSPECT,
                VERIFY_ROOT,
                HASH,
                SIGN,
                ENCRYPT,
                VALIDATE] }),
        ([
            CHIPSET], {
            KWARGS_HELP: CHIPSET_HELP }, {
            DEPENDS_ON_ANY_OF: [
                INSPECT,
                VERIFY_ROOT,
                HASH,
                SIGN,
                ENCRYPT,
                VALIDATE] }),
        ([
            FLAVOR], {
            KWARGS_HELP: FLAVOR_HELP }, {
            DEPENDS_ON_ANY_OF: [
                INSPECT,
                VERIFY_ROOT,
                HASH,
                SIGN,
                ENCRYPT,
                VALIDATE] }),
        ([
            STORAGE], {
            KWARGS_HELP: STORAGE_HELP }, {
            DEPENDS_ON_ANY_OF: [
                INSPECT,
                VERIFY_ROOT,
                HASH,
                SIGN,
                ENCRYPT,
                VALIDATE] }),
        ([
            VOUCH_FOR], {
            KWARGS_HELP: VOUCH_FOR_HELP,
            KWARGS_DEFAULT: False,
            KWARGS_ACTION: KWARGS_STORE_TRUE }, {
            INCOMPATIBLE_WITH: [
                OUTDIR],
            DEPENDS_ON: [
                OUTFILE],
            DEPENDS_ON_ANY_OF: [
                HASH,
                SIGN,
                ENCRYPT] })],
    (IMAGE_OUTPUTS_GROUP, IMAGE_OUTPUTS_GROUP_DESCRIPTION, MUTUALLY_EXCLUSIVE, OPTIONAL): [
        ([
            OUTFILE], {
            KWARGS_HELP: OUTFILE_HELP,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY) }, {
            DEPENDS_ON_ANY_OF: [
                HASH,
                SIGN,
                ENCRYPT] }),
        ([
            OUTDIR], {
            KWARGS_HELP: OUTDIR_HELP,
            KWARGS_TYPE: AutoCloseDirType(KWARGS_WRITE) }, {
            DEPENDS_ON_ANY_OF: [
                HASH,
                SIGN,
                ENCRYPT] })],
    HELP_GROUP: METABUILD_SECURE_IMAGE_HELP_GROUP }
SECURE_IMAGE_OPTIONS: CMDLineArgs = deepcopy(SECURE_IMAGE)
del SECURE_IMAGE_OPTIONS[HELP_GROUP]
del SECURE_IMAGE_OPTIONS[SECURITY_PROFILE_GROUP]
del SECURE_IMAGE_OPTIONS[IMAGE_OUTPUTS_GROUP]
SECURE_IMAGE_OPTIONS[IMAGE_INPUTS_GROUP] = [
    ([
        FUSE_BLOWER_IMAGES], {
        KWARGS_HELP: FUSE_BLOWER_IMAGES_HELP,
        KWARGS_NARGS: '+',
        KWARGS_TYPE: AutoCloseImageType((SecELF, SecDat), True, **('return_path',)) }, {
        DEPENDS_ON: [
            VALIDATE] })]
SECURE_IMAGE_OPTIONS[IMAGE_OPERATIONS_GROUP] = [
    ([
        INSPECT], {
        KWARGS_HELP: INSPECT_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        INCOMPATIBLE_WITH_ALL_BUT: [
            VERBOSE,
            IMAGE_FINDER,
            IMAGE_ID,
            CHIPSET,
            FLAVOR,
            STORAGE] }),
    ([
        VERIFY_ROOT], {
        KWARGS_HELP: VERIFY_ROOT_HELP,
        KWARGS_TYPE: sha256_sha384_hash }, {
        INCOMPATIBLE_WITH_ALL_BUT: [
            VERBOSE,
            IMAGE_FINDER,
            IMAGE_ID,
            CHIPSET,
            FLAVOR,
            STORAGE,
            QTI] }),
    ([
        VALIDATE], {
        KWARGS_HELP: METABUILD_SECURE_IMAGE_VALIDATE_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        INCOMPATIBLE_WITH: [
            INSPECT,
            VERIFY_ROOT] }),
    ([
        SIGN], {
        KWARGS_HELP: SECURE_IMAGE_SIGN_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        INCOMPATIBLE_WITH: [
            INSPECT,
            VERIFY_ROOT],
        DEPENDS_ON: [
            SIGNING_MODE],
        DEPENDS_ON_ANY_OF: [
            OUTFILE,
            OUTDIR] }),
    ([
        HASH], {
        KWARGS_HELP: SECURE_IMAGE_HASH_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        INCOMPATIBLE_WITH: [
            INSPECT,
            VERIFY_ROOT],
        DEPENDS_ON_ANY_OF: [
            OUTFILE,
            OUTDIR] }),
    ([
        ENCRYPT], {
        KWARGS_HELP: ENCRYPT_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        INCOMPATIBLE_WITH: [
            INSPECT,
            VERIFY_ROOT],
        DEPENDS_ON: [
            ENCRYPTION_MODE],
        DEPENDS_ON_ANY_OF: [
            OUTFILE,
            OUTDIR] })]
METABUILD_SECURE_IMAGE.update(SECURE_IMAGE_OPTIONS)
update_cmdline_arg(METABUILD_SECURE_IMAGE, VERBOSE, {
    DEPENDS_ON_ANY_OF: [
        INSPECT,
        VERIFY_ROOT,
        SIGN,
        HASH,
        ENCRYPT,
        VALIDATE] }, **('metadata_kwargs',))
update_cmdline_arg(METABUILD_SECURE_IMAGE, PIL_SPLIT, PIL_SPLIT_HELP.replace(f''' if {PIL_SPLIT_OUTDIR} is not provided''', ''), **('cmd_help',))
for arg_list in METABUILD_SECURE_IMAGE.values():
    for idx, arg_tuple in enumerate(arg_list):
        arg_tuple[1][KWARGS_HELP] = arg_tuple[1][KWARGS_HELP].replace(INFILE, INFILE_REPLACEMENT).replace(SECURITY_PROFILE, SECURITY_PROFILE_REPLACEMENT)
        if OUTDIR not in arg_tuple[1][KWARGS_HELP] and VOUCH_FOR not in arg_tuple[0]:
            arg_tuple[1][KWARGS_HELP] = arg_tuple[1][KWARGS_HELP].replace(OUTFILE, OUTFILE_REPLACEMENT)
