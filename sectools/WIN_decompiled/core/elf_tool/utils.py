
from argparse import ArgumentTypeError
from pathlib import Path
from typing import cast
from cmd_line_interface.base_defines import get_cmd_member
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import OUTFILE, sanitize_hex
from common.logging.logger import log_debug, log_info
from common.parser.elf.elf import ELF
from common.utils import write_cmdline_file

def write_elf_outfile(parsed_args = None, elf = None):
    log_debug('Packing generated image.')
    elf_data = elf.pack()
    log_info(f'''Writing image to: {Path(parsed_args.get(OUTFILE))}.''')
    write_cmdline_file(Path(parsed_args.get(OUTFILE)), elf_data, OUTFILE)


def validate_args_for_elf_class(parsed_args = None, args_to_validate = None, elf_bits = None):
    log_debug(f'''Validating Program Header values to be compatible with a {elf_bits} bit ELF.''')
# WARNING: Decompyle incomplete

