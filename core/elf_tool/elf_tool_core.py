"""ELF tool core implementation based on decompiled analysis."""

from pathlib import Path
from typing import Any, Dict, List, Union

from common.logging.logger import log_debug, log_info, log_warning
from common.parser.elf.elf import ELF
from common.parser.elf.defines import (
    ELFCLASS_TO_INT, EM_STRING_TO_INT, INT_TO_ELFCLASS, PT_DESCRIPTION,
    PT_LOAD, PT_NOTE, PT_NULL
)
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from core.core_interface import CoreInterface
from core.elf_tool.utils import validate_args_for_elf_class, write_elf_outfile


def log_info_wrap(operation: str):
    """Log info context manager."""
    from common.logging.logger import log_info, log_warning
    
    class LogInfoContext:
        def __enter__(self):
            log_info(f"Starting {operation} operation...")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                log_info(f"Completed {operation} operation successfully.")
            else:
                log_warning(f"{operation} operation failed: {exc_val}")
            return False
    
    return LogInfoContext()


GENERATE_OP = 'generate'
INSERT = 'insert'
COMBINE = 'combine'
REMOVE_SECTIONS = 'remove-sections'
SUBFEATURE = 'subfeature'
INFILE = 'infile'
OFFSET = 'offset'
VADDR = 'vaddr'
PADDR = 'paddr'
MEMSZ = 'memsz'
ALIGN = 'align'
ELF_ENTRY = 'elf-entry'
ELF_CLASS = 'elf-class'
ELF_MACHINE_TYPE = 'elf-machine-type'
DATA = 'data'
TYPE = 'type'
FLAGS = 'flags'


class ELFToolCore(CoreInterface):
    """ELF tool core class."""

    def run(self, parsed_args: Dict[str, Any]) -> None:
        """Run ELF tool operations."""
        subfeature = parsed_args.get(SUBFEATURE)

        if subfeature == INSERT:
            with log_info_wrap(INSERT):
                self.insert_operation(parsed_args)
        elif subfeature == GENERATE_OP:
            with log_info_wrap(GENERATE_OP):
                self.generate_operation(parsed_args)
        elif subfeature == COMBINE:
            with log_info_wrap(COMBINE):
                self.combine_operation(parsed_args)
        elif subfeature == REMOVE_SECTIONS:
            with log_info_wrap(REMOVE_SECTIONS):
                self.remove_sections_operation(parsed_args)
        else:
            raise RuntimeError(f"{subfeature} operation is unsupported.")

    def insert_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Insert segment into existing ELF."""
        infile = parsed_args.get(INFILE)
        elf = self.validate_infile(infile)

        if elf.elf_header is None:
            raise AssertionError("ELF header not loaded")

        validate_args_for_elf_class(parsed_args, (OFFSET, VADDR, PADDR, MEMSZ, ALIGN),
                                    ELFCLASS_TO_INT[elf.elf_header.e_ident_class])
        self.add_segment(parsed_args, elf)
        write_elf_outfile(parsed_args, elf)

    def generate_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Generate new ELF image."""
        log_debug("Constructing ELF.")

        validate_args_for_elf_class(
            parsed_args,
            (OFFSET, VADDR, PADDR, MEMSZ, ALIGN, ELF_ENTRY),
            parsed_args.get(ELF_CLASS, ELFCLASS_TO_INT['ELF64'])
        )

        elf_class = parsed_args.get(ELF_CLASS, ELFCLASS_TO_INT['ELF64'])
        elf_machine_type = parsed_args.get(ELF_MACHINE_TYPE, 'ARM')

        if elf_class == ELFCLASS_TO_INT['ELF64']:
            elf = ELFWithHashTableSegment()
            elf.elf_header = elf.elf_header.__class__()
        else:
            elf = ELFWithHashTableSegment()
            elf.elf_header = elf.elf_header.__class__()

        elf.elf_header.e_machine = EM_STRING_TO_INT.get(elf_machine_type, 40)

        if parsed_args.get(ELF_ENTRY):
            entry_val = int(parsed_args[ELF_ENTRY], 16) if isinstance(parsed_args[ELF_ENTRY], str) else parsed_args[ELF_ENTRY]
            elf.elf_header.e_entry = entry_val

        self.add_segment(parsed_args, elf)
        write_elf_outfile(parsed_args, elf)

    def combine_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Combine multiple ELF files into one."""
        infiles = parsed_args.get(INFILE, [])
        if len(infiles) < 2:
            raise ValueError(f"combine requires at least 2 input files, got {len(infiles)}")

        # Parse first ELF as base
        base_elf = self.validate_infile(infiles[0])
        
        # Get entry point from args or use first ELF's entry
        if parsed_args.get(ELF_ENTRY):
            entry_val = int(parsed_args[ELF_ENTRY], 16) if isinstance(parsed_args[ELF_ENTRY], str) else parsed_args[ELF_ENTRY]
            base_elf.elf_header.e_entry = entry_val

        # Combine remaining ELFs
        for infile in infiles[1:]:
            other_elf = self.validate_infile(infile)
            
            # Find greatest offset in base ELF
            greatest_offset = base_elf.get_greatest_offset()
            
            # Add segments from other ELF
            for phdr in other_elf.phdrs:
                if phdr.p_type == PT_LOAD and phdr.p_filesz > 0:
                    # Create new program header
                    if isinstance(phdr, ProgramHeader64):
                        new_phdr = ProgramHeader64()
                    else:
                        new_phdr = ProgramHeader32()
                    
                    new_phdr.p_type = phdr.p_type
                    new_phdr.p_flags = phdr.p_flags
                    new_phdr.p_offset = greatest_offset
                    new_phdr.p_vaddr = phdr.p_vaddr
                    new_phdr.p_paddr = phdr.p_paddr
                    new_phdr.p_filesz = phdr.p_filesz
                    new_phdr.p_memsz = phdr.p_memsz
                    new_phdr.p_align = phdr.p_align
                    
                    # Get segment data
                    segment_data = other_elf.segments.get(phdr, memoryview(b''))
                    
                    # Add to base ELF
                    base_elf.segments[new_phdr] = segment_data
                    base_elf.phdrs.append(new_phdr)
                    
                    # Update offset for next segment
                    greatest_offset += len(segment_data)

        # Update program header count
        if base_elf.elf_header:
            base_elf.elf_header.e_phnum = len(base_elf.phdrs)

        write_elf_outfile(parsed_args, base_elf)

    def remove_sections_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Remove sections from ELF."""
        infile = parsed_args.get(INFILE)
        elf = self.validate_infile(infile)
        
        # Remove all sections (simplified - sectools.exe may have more options)
        elf.shdrs.clear()
        elf.sections.clear()
        
        if elf.elf_header:
            elf.elf_header.e_shnum = 0
            elf.elf_header.e_shoff = 0

        write_elf_outfile(parsed_args, elf)

    def validate_infile(self, infile: Union[str, Path]) -> ELFWithHashTableSegment:
        """Validate input ELF file."""
        if infile is None:
            raise ValueError(f"{INFILE} must be provided")

        infile_path = Path(infile)
        if not infile_path.exists():
            raise FileNotFoundError(f"{INFILE} not found: {infile}")

        with open(infile_path, 'rb') as f:
            data = memoryview(f.read())

        elf = ELFWithHashTableSegment()
        elf.unpack(data)

        if elf.elf_header is None:
            raise AssertionError(f"Failed to parse ELF header from {infile}")

        return elf

    def add_segment(self, parsed_args: Dict[str, Any], elf: ELFWithHashTableSegment) -> None:
        """Add segment to ELF."""
        data_file = parsed_args.get(DATA)
        if data_file is None:
            raise ValueError(f"{DATA} must be provided")

        data_path = Path(data_file)
        if not data_path.exists():
            raise FileNotFoundError(f"{DATA} not found: {data_file}")

        with open(data_path, 'rb') as f:
            segment_data = memoryview(f.read())

        # Get segment parameters
        seg_type_str = parsed_args.get(TYPE, PT_DESCRIPTION[PT_LOAD])
        seg_offset = parsed_args.get(OFFSET)
        seg_vaddr = parsed_args.get(VADDR, 0)
        seg_paddr = parsed_args.get(PADDR, 0)
        seg_memsz = parsed_args.get(MEMSZ)
        seg_flags = parsed_args.get(FLAGS, 0)
        seg_align = parsed_args.get(ALIGN, 0x1000)

        # Convert type string to value
        type_map = {v: k for k, v in PT_DESCRIPTION.items()}
        seg_type = type_map.get(seg_type_str, PT_LOAD)

        # Determine ELF class and program header type
        elf_class = elf.elf_header.e_ident_class if elf.elf_header else ELFCLASS_TO_INT['ELF64']
        phdr_class = PROGRAM_HEADER_CLASSES.get(elf_class, ProgramHeader64)

        # Create program header
        phdr = phdr_class()
        phdr.p_type = seg_type
        phdr.p_flags = seg_flags if isinstance(seg_flags, int) else int(seg_flags, 16) if isinstance(seg_flags, str) else 0
        phdr.p_vaddr = seg_vaddr if isinstance(seg_vaddr, int) else int(seg_vaddr, 16) if isinstance(seg_vaddr, str) else 0
        phdr.p_paddr = seg_paddr if isinstance(seg_paddr, int) else int(seg_paddr, 16) if isinstance(seg_paddr, str) else 0
        phdr.p_memsz = seg_memsz if seg_memsz else len(segment_data)
        phdr.p_filesz = len(segment_data)
        phdr.p_align = seg_align if isinstance(seg_align, int) else int(seg_align, 16) if isinstance(seg_align, str) else 0x1000

        # Calculate offset if not provided
        if seg_offset:
            phdr.p_offset = seg_offset if isinstance(seg_offset, int) else int(seg_offset, 16) if isinstance(seg_offset, str) else 0
        else:
            # Find lowest available offset
            greatest_offset = elf.get_greatest_offset() if hasattr(elf, 'get_greatest_offset') else 0
            phdr.p_offset = greatest_offset

        # Add segment to ELF
        elf.segments[phdr] = segment_data
        elf.phdrs.append(phdr)

        if elf.elf_header:
            elf.elf_header.e_phnum = len(elf.phdrs)
