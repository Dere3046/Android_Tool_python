
from argparse import ArgumentTypeError
from itertools import combinations
from cmd_line_interface.base_defines import AutoCloseFileType, HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP, KWARGS_ACTION, KWARGS_COUNT, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_NARGS, KWARGS_READ_BINARY, KWARGS_STORE_TRUE, KWARGS_TYPE, KWARGS_WRITE, KWARGS_WRITE_BINARY, OUTFILE_COMMON_HELP
from cmd_line_interface.basecmdline import AutoCloseDirType, CMDLineArgs, CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.auto_close_image_type import AutoCloseImageType
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_FORMAT_GROUP, IMAGE_INPUTS_GROUP, IMAGE_OUTPUTS_GROUP, OUTFILE, QTI_DPR, VERBOSE, VERBOSE_ABBREV, VERBOSE_HELP
from cmd_line_interface.sectools.metadata import DEPENDS_ON
from cmd_line_interface.sectools.secure_image.defines import PIL_SPLIT, PIL_SPLIT_OUTDIR
from common.parser.elf.bit32.elf_header import ELFHeader32
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.v7.hash_table_segment_header import HashTableSegmentHeaderV7
from common.parser.tme.dpr.dpr import DPR
from core.elf_consolidator.utils import get_loadable_phdrs
from core.tme_secure_debug.augmented_inspect import DESCRIBE_QTI_DPR
ELF_CONSOLIDATOR_NAME = 'elf-consolidator'
ELF_CONSOLIDATOR_DESCRIPTION = 'Tool for generating Consolidated ELF software images. A Consolidated ELF contains the contents of multiple subsystem images.'
IMAGES = '--images'
CONFIG = '--config'
IMAGES_HELP = 'Input ELF images to be added to the Consolidated ELF.'
CONFIG_HELP = 'The configuration file that describes the Consolidated ELF format of a Qualcomm chipset.'
OUTFILE_HELP = f'''{OUTFILE_COMMON_HELP} Consolidated ELF image.'''
DPR_HELP = 'Debug Policy Request (DPR) to be added to the Consolidated ELF.'
PIL_SPLIT_HELP = f'''PIL split {OUTFILE}. If not provided, {OUTFILE} will not be PIL split. The resulting PIL split files will be saved in the same directory as {OUTFILE} if {PIL_SPLIT_OUTDIR} is not provided. The name of the PIL split files will be prefixed with {OUTFILE}\'s file name.'''
PIL_SPLIT_OUTDIR_HELP = f'''Directory at which to store PIL split files. Must be used with {PIL_SPLIT}.'''

class AutoCloseELFWithHashTableSegmentType(AutoCloseImageType):
    
    def __init__(self = None):
        super().__init__((ELFWithHashTableSegment,))

    
    def __call__(self = None, path = None):
        elf = super().__call__(path)
    # WARNING: Decompyle incomplete

    __classcell__ = None


class AutoCloseDPRType(AutoCloseImageType):
    
    def __init__(self = None):
        super().__init__((DPR,))

    
    def __call__(self = None, path = None):
        dpr = super().__call__(path)
    # WARNING: Decompyle incomplete

    __classcell__ = None

COMMON_HELP: CMDLineGroup = [
    ([
        HELP_ABBREV,
        HELP], {
        KWARGS_HELP: HELP_HELP,
        KWARGS_ACTION: KWARGS_HELP }),
    ([
        VERBOSE_ABBREV,
        VERBOSE], {
        KWARGS_HELP: VERBOSE_HELP,
        KWARGS_DEFAULT: 0,
        KWARGS_ACTION: KWARGS_COUNT }, {
        DEPENDS_ON: [
            IMAGES] })]
IMAGE_INPUTS: CMDLineGroup = [
    ([
        IMAGES], {
        KWARGS_HELP: IMAGES_HELP,
        KWARGS_NARGS: '+',
        KWARGS_TYPE: AutoCloseELFWithHashTableSegmentType() }, {
        DEPENDS_ON: [
            CONFIG,
            OUTFILE] }),
    ([
        QTI_DPR], {
        KWARGS_HELP: DPR_HELP,
        KWARGS_TYPE: AutoCloseDPRType() }, {
        DEPENDS_ON: [
            IMAGES] }),
    ([
        CONFIG], {
        KWARGS_HELP: CONFIG_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY, True, **('return_path',)) }, {
        DEPENDS_ON: [
            OUTFILE,
            IMAGES] })]
IMAGE_OUTPUTS: CMDLineGroup = [
    ([
        OUTFILE], {
        KWARGS_HELP: OUTFILE_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY) }, {
        DEPENDS_ON: [
            CONFIG,
            IMAGES] })]
ELF_OPTIONS_INPUTS: CMDLineGroup = [
    ([
        PIL_SPLIT], {
        KWARGS_HELP: PIL_SPLIT_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        DEPENDS_ON: [
            IMAGES] }),
    ([
        PIL_SPLIT_OUTDIR], {
        KWARGS_HELP: PIL_SPLIT_OUTDIR_HELP,
        KWARGS_TYPE: AutoCloseDirType(KWARGS_WRITE) }, {
        DEPENDS_ON: [
            PIL_SPLIT] })]
ELF_CONSOLIDATOR: CMDLineArgs = {
    IMAGE_FORMAT_GROUP: ELF_OPTIONS_INPUTS,
    IMAGE_OUTPUTS_GROUP: IMAGE_OUTPUTS,
    IMAGE_INPUTS_GROUP: IMAGE_INPUTS,
    HELP_GROUP: COMMON_HELP }
