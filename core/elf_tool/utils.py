"""ELF tool utilities."""

from pathlib import Path
from typing import Union

from common.parser.elf.elf import ELF
from common.logging.logger import log_info


def validate_args_for_elf_class(args: dict) -> None:
    """Validate ELF class arguments.
    
    Args:
        args: Command line arguments dictionary
        
    Raises:
        ValueError: If arguments are invalid
    """
    elf_class = args.get('elf_class')
    if elf_class is not None:
        if elf_class not in (1, 2):
            raise ValueError(f"Invalid ELF class: {elf_class}")
    
    machine_type = args.get('elf_machine_type')
    if machine_type is not None and isinstance(machine_type, str):
        from common.parser.elf.defines import EM_STRING_TO_INT
        if machine_type not in EM_STRING_TO_INT:
            raise ValueError(f"Invalid ELF machine type: {machine_type}")


def write_elf_outfile(elf: ELF, outfile_path: Union[str, Path]) -> None:
    """Write ELF output file.
    
    Args:
        elf: ELF object
        outfile_path: Output file path
    """
    outfile_path = Path(outfile_path)
    outfile_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = elf.pack()
    
    with open(outfile_path, 'wb') as f:
        f.write(bytes(data))
    
    log_info(f"Written ELF image to {outfile_path}")
