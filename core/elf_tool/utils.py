"""ELF tool utilities based on decompiled analysis."""

from pathlib import Path
from typing import Dict, Tuple, Union

from common.parser.elf.elf import ELF
from common.logging.logger import log_info


def validate_args_for_elf_class(
    args: Dict,
    check_fields: Tuple[str, ...],
    elf_class: int
) -> None:
    """Validate arguments for ELF class.

    Args:
        args: Command line arguments
        check_fields: Fields to validate
        elf_class: ELF class (32 or 64)
    """
    # Validate each field can be converted to hex
    for field in check_fields:
        value = args.get(field)
        if value is not None:
            if isinstance(value, str):
                try:
                    int(value, 16) if value.startswith('0x') else int(value)
                except ValueError:
                    raise ValueError(f"Invalid {field}: {value}")


def write_elf_outfile(args: Dict, elf: ELF) -> None:
    """Write ELF output file.

    Args:
        args: Command line arguments
        elf: ELF object
    """
    outfile_path = args.get('outfile')
    if outfile_path is None:
        raise ValueError("outfile must be provided")

    outfile_path = Path(outfile_path)
    outfile_path.parent.mkdir(parents=True, exist_ok=True)

    data = elf.pack()

    with open(outfile_path, 'wb') as f:
        f.write(bytes(data))

    log_info(f"Written ELF image to {outfile_path}")
