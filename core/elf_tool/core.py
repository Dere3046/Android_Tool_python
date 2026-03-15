"""ELF tool core implementation."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from common.logging.logger import log_debug, log_info, log_warning
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import (
    PT_LOAD, PT_DESCRIPTION,
    ELFCLASS32, ELFCLASS64,
    EM_ARM, EM_STRING_TO_INT, EM_INT_TO_STRING,
    ELF32_PHDR_SIZE, ELF64_PHDR_SIZE
)
from common.parser.elf.elf import ELF
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.parser_image_info_interface import CoreInterface
from common.utils import write_cmdline_file


def validate_args_for_elf_class(args: Dict[str, Any]) -> None:
    """Validate ELF class arguments."""
    elf_class = args.get('elf_class', ELFCLASS64)
    if elf_class not in (ELFCLASS32, ELFCLASS64):
        raise ValueError(f"Invalid ELF class: {elf_class}")
    
    machine_type = args.get('elf_machine_type', 'ARM')
    if isinstance(machine_type, str):
        if machine_type not in EM_STRING_TO_INT:
            raise ValueError(f"Invalid ELF machine type: {machine_type}")


def write_elf_outfile(elf: ELF, outfile_path: Union[str, Path]) -> None:
    """Write ELF output file."""
    outfile_path = Path(outfile_path)
    outfile_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = elf.pack()
    
    with open(outfile_path, 'wb') as f:
        f.write(bytes(data))
    
    log_info(f"Written ELF image to {outfile_path}")


def log_info_wrap(operation: str):
    """Log info context manager."""
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


class ELFToolCore(CoreInterface):
    """ELF tool core class."""
    
    def __init__(self):
        """Initialize ELF tool core."""
        pass
    
    def run(self, parsed_args: Dict[str, Any]) -> None:
        """Run ELF tool."""
        subfeature = parsed_args.get('subfeature')
        
        if subfeature == 'insert':
            with log_info_wrap('insert'):
                self.insert_operation(parsed_args)
        elif subfeature == 'generate':
            with log_info_wrap('generate'):
                self.generate_operation(parsed_args)
        elif subfeature == 'combine':
            with log_info_wrap('combine'):
                self.combine_operation(parsed_args)
        elif subfeature == 'remove-sections':
            with log_info_wrap('remove-sections'):
                self.remove_sections_operation(parsed_args)
        else:
            raise RuntimeError(f"Subfeature '{subfeature}' is unsupported.")
    
    def generate_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Generate new ELF image."""
        validate_args_for_elf_class(parsed_args)
        
        elf_class = parsed_args.get('elf_class', ELFCLASS64)
        elf_machine_type = parsed_args.get('elf_machine_type', 'ARM')
        elf_entry = parsed_args.get('elf_entry', 0)
        data_file = parsed_args.get('data')
        outfile = parsed_args.get('outfile')
        
        seg_type = parsed_args.get('type', PT_DESCRIPTION.get(PT_LOAD, 'LOAD'))
        seg_offset = parsed_args.get('offset', 0)
        seg_vaddr = parsed_args.get('vaddr', 0)
        seg_paddr = parsed_args.get('paddr', 0)
        seg_memsz = parsed_args.get('memsz')
        seg_flags = parsed_args.get('flags', 0)
        seg_align = parsed_args.get('align', 0x1000)
        
        if data_file:
            with open(data_file, 'rb') as f:
                data = memoryview(f.read())
        else:
            data = memoryview(b'')
        
        if seg_memsz is None:
            seg_memsz = len(data)
        
        elf = ELF()
        
        if elf_class == ELFCLASS64:
            from common.parser.elf.bit64.elf_header import ELFHeader64
            elf.elf_header = ELFHeader64()
            phdr_class = ProgramHeader64
            phdr_size = ELF64_PHDR_SIZE
        else:
            from common.parser.elf.bit32.elf_header import ELFHeader32
            elf.elf_header = ELFHeader32()
            phdr_class = ProgramHeader32
            phdr_size = ELF32_PHDR_SIZE
        
        elf.elf_header.e_type = 2
        elf.elf_header.e_machine = EM_STRING_TO_INT.get(elf_machine_type, EM_ARM)
        elf.elf_header.e_version = 1
        elf.elf_header.e_entry = elf_entry
        elf.elf_header.e_phoff = 64 if elf_class == ELFCLASS64 else 52
        elf.elf_header.e_shoff = 0
        elf.elf_header.e_flags = 0
        elf.elf_header.e_ehsize = 64 if elf_class == ELFCLASS64 else 52
        elf.elf_header.e_phentsize = phdr_size
        elf.elf_header.e_phnum = 0
        elf.elf_header.e_shentsize = 64 if elf_class == ELFCLASS64 else 40
        elf.elf_header.e_shnum = 0
        elf.elf_header.e_shstrndx = 0
        
        elf.elf_header.e_ident = bytearray([
            0x7f, ord('E'), ord('L'), ord('F'),
            elf_class, 1, 1, 0,
        ]) + b'\x00' * 8
        
        phdr = phdr_class()
        phdr.p_type = PT_LOAD
        phdr.p_flags = seg_flags
        phdr.p_offset = seg_offset if seg_offset else 0
        phdr.p_vaddr = seg_vaddr
        phdr.p_paddr = seg_paddr
        phdr.p_filesz = len(data)
        phdr.p_memsz = seg_memsz
        phdr.p_align = seg_align if seg_align else 0x1000
        
        elf.add_segment(phdr, data)
        
        elf.elf_header.e_phnum = len(elf.phdrs)
        
        write_elf_outfile(elf, outfile)
        
        log_info(f"Generated ELF image: {outfile}")
    
    def insert_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Insert segment into existing ELF."""
        infile = parsed_args.get('infile')
        outfile = parsed_args.get('outfile')
        data_file = parsed_args.get('data')
        
        seg_type = parsed_args.get('type', PT_DESCRIPTION.get(PT_LOAD, 'LOAD'))
        seg_offset = parsed_args.get('offset')
        seg_vaddr = parsed_args.get('vaddr', 0)
        seg_paddr = parsed_args.get('paddr', 0)
        seg_memsz = parsed_args.get('memsz')
        seg_flags = parsed_args.get('flags', 0)
        seg_align = parsed_args.get('align', 0x1000)
        
        with open(infile, 'rb') as f:
            data = memoryview(f.read())
        
        elf = ELF(data)
        elf.unpack(data)
        
        if data_file:
            with open(data_file, 'rb') as f:
                segment_data = memoryview(f.read())
        else:
            segment_data = memoryview(b'')
        
        if seg_memsz is None:
            seg_memsz = len(segment_data)
        
        elf_class = elf.elf_header.e_ident_class
        if elf_class == ELFCLASS64:
            phdr_class = ProgramHeader64
        else:
            phdr_class = ProgramHeader32
        
        phdr = phdr_class()
        
        for type_val, type_desc in PT_DESCRIPTION.items():
            if type_desc == seg_type:
                phdr.p_type = type_val
                break
        else:
            phdr.p_type = PT_LOAD
        
        phdr.p_flags = seg_flags
        phdr.p_vaddr = seg_vaddr
        phdr.p_paddr = seg_paddr
        phdr.p_memsz = seg_memsz
        phdr.p_align = seg_align if seg_align else 0x1000
        
        if seg_offset is not None:
            phdr.p_offset = seg_offset
        else:
            greatest_offset = elf.get_greatest_offset()
            phdr.p_offset = greatest_offset
        
        phdr.p_filesz = len(segment_data)
        
        elf.add_segment(phdr, segment_data)
        
        elf.elf_header.e_phnum = len(elf.phdrs)
        
        write_elf_outfile(elf, outfile)
        
        log_info(f"Inserted segment into ELF image: {outfile}")
    
    def combine_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Combine multiple ELF files."""
        infiles = parsed_args.get('infile', [])
        outfile = parsed_args.get('outfile')
        elf_entry = parsed_args.get('elf_entry')
        
        if len(infiles) < 2:
            raise ValueError("combine requires at least 2 input ELF files")
        
        with open(infiles[0], 'rb') as f:
            data = memoryview(f.read())
        
        combined_elf = ELF(data)
        combined_elf.unpack(data)
        
        if elf_entry is not None:
            combined_elf.elf_header.e_entry = elf_entry
        
        for infile in infiles[1:]:
            with open(infile, 'rb') as f:
                data = memoryview(f.read())
            
            other_elf = ELF()
            other_elf.unpack(data)
            
            greatest_offset = combined_elf.get_greatest_offset()
            
            for phdr in other_elf.phdrs:
                if phdr.p_type == PT_LOAD and phdr.p_filesz > 0:
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
                    
                    segment_data = other_elf.segments.get(phdr, memoryview(b''))
                    
                    combined_elf.add_segment(new_phdr, segment_data)
                    
                    greatest_offset += len(segment_data)
        
        combined_elf.elf_header.e_phnum = len(combined_elf.phdrs)
        
        write_elf_outfile(combined_elf, outfile)
        
        log_info(f"Combined {len(infiles)} ELF images into: {outfile}")
    
    def remove_sections_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Remove sections from ELF."""
        infile = parsed_args.get('infile')
        outfile = parsed_args.get('outfile')
        
        with open(infile, 'rb') as f:
            data = memoryview(f.read())
        
        elf = ELF(data)
        elf.unpack(data)
        
        sections_to_remove = list(elf.shdrs)
        elf.remove_sections(sections_to_remove)
        
        elf.elf_header.e_shnum = len(elf.shdrs)
        elf.elf_header.e_shoff = 0
        
        write_elf_outfile(elf, outfile)
        
        log_info(f"Removed sections from ELF image: {outfile}")
