
from dataclasses import dataclass, field
from itertools import chain
from operator import attrgetter, methodcaller
from typing import Iterable
from cmd_line_interface.sectools.elf_consolidator.defines import IMAGES
from common.data.data import and_separated
from common.logging.logger import log_debug, log_warning
from common.parser.elf.bit32.elf_header import ELFHeader32
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.defines import PT_LOAD
from common.parser.elf.elf import ELF
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from common.parser.multi_image.defines import MULTI_IMAGE
from common.parser.multi_image.multi_image import MultiImage
from common.parser.tme.dpr.dpr import DPR
from core.elf_consolidator.config.config import Config
from core.elf_consolidator.utils import get_loadable_phdrs
P_FLAGS_RELOCATABLE = 134217728
SortedMISCAndImages = dataclass(<NODE:12>)

def generate_consolidated_elf(parsed_images = None, config = None, qti_dpr = None):
    pass
# WARNING: Decompyle incomplete


def validate_and_split_images(parsed_images = None):
    '''Note, all the ELFs are validated with validate_before_operation() called in the handler.'''
    miscs = []
    elfs = []
    software_ids = []
# WARNING: Decompyle incomplete


def sort_images(miscs = None, elfs = None):
    elfs_mapping = (lambda .0: pass# WARNING: Decompyle incomplete
)(elfs)
# WARNING: Decompyle incomplete


def package_input_segments(parsed_images = None, concatenated_mdt_data = None, config = None, qti_dpr = ('parsed_images', list[ELFWithHashTableSegment], 'concatenated_mdt_data', bytes, 'config', Config, 'qti_dpr', DPR | None, 'return', ELF)):
    '''
    Create an ELF and add all the loadable segments of all input ELFs.
    Address translations defined in the config file will be applied here.
    Exclusions:
    - Only PT_LOAD segments are packaged.
    - Only non-empty segments are packaged.

    Note: Entry point of the output ELF will match the entry point of image provided in the config if present.
    It will be zero otherwise.
    '''
    consolidated_elf = ELF()
# WARNING: Decompyle incomplete

