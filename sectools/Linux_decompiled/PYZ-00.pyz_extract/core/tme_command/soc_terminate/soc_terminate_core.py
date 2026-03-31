
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import GENERATE_OP, OPERATION
from cmd_line_interface.sectools.elf_tool.common.defines import ALIGN, FLAGS
from cmd_line_interface.sectools.elf_tool.generate.defines import ELF_CLASS
from cmd_line_interface.sectools.tme_command.soc_terminate.defines import COMMAND_ENTITLEMENT_CERTIFICATE, PADDR
from common.data.data import and_separated
from common.logging.logger import log_debug
from common.parser.elf.defines import INT_TO_ELFCLASS, PT_LOAD
from common.parser.elf.elf import ELF
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.tme.tme_parser.defines import COMMAND_ENTITLEMENT_CHIP_CONSTRAINTS_PATH, COMMAND_ENTITLEMENT_CHIP_UNIQUE_IDENTIFIER_PATH, COMMAND_ENTITLEMENT_INSTANTIATION_CONSTRAINTS_PATH, COMMAND_ENTITLEMENT_PATH, COMMAND_ENTITLEMENT_PUBLIC_KEY_PATH, COMMAND_ENTITLEMENT_SERIAL_NUMBER_PATH, IS_CHIP_UNIQUE_ID_BOUND
from common.parser.tme.tme_parser.tme import TME
from core.core_interface import CoreInterface
from core.elf_tool.utils import validate_args_for_elf_class, write_elf_outfile
from core.hash_sign_core import log_info_wrap
from core.tme_command.common.command_entitlement_validator_interface import CommandEntitlementValidatorInterface
from core.tme_command.common.utils import validate_path_in_entitlement

class SocTerminateCore(CommandEntitlementValidatorInterface, CoreInterface):
    
    def run(self = None, parsed_args = None):
        pass
    # WARNING: Decompyle incomplete

    
    def generate_soc_terminate_request(self = None, parsed_args = None):
        log_debug(f'''Parsing {COMMAND_ENTITLEMENT_CERTIFICATE}.''')
    # WARNING: Decompyle incomplete

    
    def validate_command_entitlement(command_entitlement = None):
        log_debug(f'''Validating {COMMAND_ENTITLEMENT_CERTIFICATE}.''')
    # WARNING: Decompyle incomplete

    validate_command_entitlement = None(validate_command_entitlement)
    
    def create_elf(parsed_args = None, tme_data = None):
        elf_class = parsed_args.get(ELF_CLASS)
        tme_data_size = len(tme_data)
        validate_args_for_elf_class(parsed_args, (PADDR, ALIGN), elf_class)
        log_debug('Constructing ELF.')
        elf = ELF(INT_TO_ELFCLASS[elf_class], int(parsed_args.get(PADDR), 0), **('elf_class', 'e_entry'))
    # WARNING: Decompyle incomplete

    create_elf = None(create_elf)

