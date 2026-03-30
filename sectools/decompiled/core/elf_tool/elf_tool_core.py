
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.auto_close_image_type import ImageWithPath
from cmd_line_interface.sectools.cmd_line_common.defines import GENERATE_OP, INFILE, SUBFEATURE
from cmd_line_interface.sectools.elf_tool.combine.defines import COMBINE
from cmd_line_interface.sectools.elf_tool.common.defines import ALIGN, DATA, ELF_ENTRY, FLAGS, MEMSZ, OFFSET, PADDR, TYPE, VADDR
from cmd_line_interface.sectools.elf_tool.generate.defines import ELF_CLASS, ELF_MACHINE_TYPE
from cmd_line_interface.sectools.elf_tool.insert.defines import INSERT
from cmd_line_interface.sectools.elf_tool.remove_sections.defines import REMOVE_SECTIONS
from common.logging.logger import log_debug, log_warning
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS_TO_INT, EM_STRING_TO_INT, INT_TO_ELFCLASS, PT_DESCRIPTION
from common.parser.elf.elf import ELF
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from core.core_interface import CoreInterface
from core.elf_tool.utils import validate_args_for_elf_class, write_elf_outfile
from core.hash_sign_core import log_info_wrap

class ELFToolCore(CoreInterface):
    
    def run(self = None, parsed_args = None):
        pass
    # WARNING: Decompyle incomplete

    
    def insert_operation(self = None, parsed_args = None):
        infile = parsed_args.get(INFILE)
        self.validate_infile(infile)
        elf = infile.image
    # WARNING: Decompyle incomplete

    
    def generate_operation(self = None, parsed_args = None):
        log_debug('Constructing ELF.')
        validate_args_for_elf_class(parsed_args, (OFFSET, VADDR, PADDR, MEMSZ, ALIGN, ELF_ENTRY), parsed_args.get(ELF_CLASS))
        elf = ELF(INT_TO_ELFCLASS[parsed_args.get(ELF_CLASS)], int(parsed_args.get(ELF_ENTRY), 0), EM_STRING_TO_INT[parsed_args.get(ELF_MACHINE_TYPE)], **('elf_class', 'e_entry', 'e_machine'))
        self.add_segment(parsed_args, elf)
        write_elf_outfile(parsed_args, elf)

    
    def combine_operation(self = None, parsed_args = None):
        elf_entry = int(parsed_args.get(ELF_ENTRY), 0) if parsed_args.get(ELF_ENTRY) else parsed_args.get(INFILE)[0].image.elf_header.e_entry
        log_debug(f'''ELF entry point address set to {hex(elf_entry)}.''')
        combined_elf = ELF(parsed_args.get(INFILE)[0].image.elf_header.e_ident_class, elf_entry, **('elf_class', 'e_entry'))
    # WARNING: Decompyle incomplete

    
    def remove_sections_operation(self = None, parsed_args = None):
        infile = parsed_args.get(INFILE)
        self.validate_infile(infile)
        elf = infile.image
        if not elf.shdrs:
            log_warning(f'''{infile.path} does not contain any sections.''')
        else:
            elf.remove_sections()
        write_elf_outfile(parsed_args, elf)

    
    def add_segment(self = None, parsed_args = None, elf = None):
        data = memoryview(parsed_args.get(DATA))
        log_debug("Constructing new segment's Program Header.")
    # WARNING: Decompyle incomplete

    
    def get_phdr_for_segment(parsed_args = None, elf_bits = None, data_size = staticmethod):
        log_debug(f'''Creating new Program Header for a {elf_bits} bit ELF.''')
        log_debug(f'''Setting filesz to {hex(data_size)}.''')
        phdr = PROGRAM_HEADER_CLASSES[INT_TO_ELFCLASS[elf_bits]].from_fields((lambda .0: pass# WARNING: Decompyle incomplete
)(PT_DESCRIPTION.items())[parsed_args.get(TYPE)], int(parsed_args.get(OFFSET), 0), int(parsed_args.get(VADDR), 0), int(parsed_args.get(PADDR), 0), data_size, int(parsed_args.get(MEMSZ), 0) if parsed_args.get(MEMSZ) else data_size, int(parsed_args.get(FLAGS), 0), int(parsed_args.get(ALIGN), 0), **('p_type', 'p_offset', 'p_vaddr', 'p_paddr', 'p_filesz', 'p_memsz', 'p_flags', 'p_align'))
        log_debug(f'''Validating provided memsz is large enough to hold {DATA}.''')
        if phdr.p_filesz > phdr.p_memsz:
            raise RuntimeError(f'''{DATA} is {hex(phdr.p_filesz)} bytes in size which is larger than {MEMSZ}.''')
        None.validate_before_operation()
        return phdr

    get_phdr_for_segment = None(get_phdr_for_segment)
    
    def validate_infile(infile = None):
        log_debug(f'''Validating {INFILE}: {infile.path}.''')
        infile.image.validate_before_operation()
        if isinstance(infile.image, ELFWithHashTableSegment):
            raise RuntimeError(f'''{infile.path} was detected as an {ELFWithHashTableSegment.class_type_string()} image, however only {ELF.class_type_string()} images are supported.''')

    validate_infile = None(validate_infile)

