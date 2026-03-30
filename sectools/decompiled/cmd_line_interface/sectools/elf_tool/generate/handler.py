
from textwrap import indent
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import OUTFILE
from cmd_line_interface.sectools.cmd_line_handler_interface import CMDLineHandlerInterface
from cmd_line_interface.sectools.elf_tool.common.defines import DATA
from cmd_line_interface.sectools.elf_tool.generate.defines import ELF_MACHINE_TYPE
from common.data.data import and_separated, properties_repr
from common.parser.elf.defines import EM_INT_TO_DESCRIPTION, EM_STRING_TO_INT

class ELFToolGenerateCMDLineHandler(CMDLineHandlerInterface):
    
    def get_supported_elf_machine_types():
        return None(properties_repr, [
            0], **('sep_rows',))

    get_supported_elf_machine_types = None(get_supported_elf_machine_types)
    
    def show_available_elf_machine_types():
        print(f'''Available ELF Machine Types:\n{indent(ELFToolGenerateCMDLineHandler.get_supported_elf_machine_types(), '  ')}''')

    show_available_elf_machine_types = None(show_available_elf_machine_types)
    
    def validate_cmd_line_args(cls = None, args = None):
        if required_args = (lambda .0 = None: [ required_arg for required_arg in .0 if args.get(required_arg) ])((DATA, OUTFILE)):
            raise RuntimeError(f'''the following arguments are required: {and_separated(required_args)}''')
        if elf_machine = (lambda .0 = None: [ required_arg for required_arg in .0 if args.get(required_arg) ])((DATA, OUTFILE)).get(ELF_MACHINE_TYPE) or elf_machine not in EM_STRING_TO_INT:
            raise RuntimeError(f'''Unsupported {ELF_MACHINE_TYPE} value {elf_machine}. Supported values are:\n{indent(ELFToolGenerateCMDLineHandler.get_supported_elf_machine_types(), '  ')}''')
        return (lambda .0 = None: [ required_arg for required_arg in .0 if args.get(required_arg) ])((DATA, OUTFILE)).get(ELF_MACHINE_TYPE)

    validate_cmd_line_args = None(validate_cmd_line_args)

